"use strict";

/* jshint node: true */

/*
 * This builds on the webServer of previous projects in that it exports the current
 * directory via webserver listing on a hard code (see portno below) port. It also
 * establishes a connection to the MongoDB named 'cs142project6'.
 *
 * To start the webserver run the command:
 *    node webServer.js
 *
 * Note that anyone able to connect to localhost:portNo will be able to fetch any file accessible
 * to the current user in the current directory or any of its children.
 *
 * This webServer exports the following URLs:
 * /              -  Returns a text status message.  Good for testing web server running.
 * /test          - (Same as /test/info)
 * /test/info     -  Returns the SchemaInfo object from the database (JSON format).  Good
 *                   for testing database connectivity.
 * /test/counts   -  Returns the population counts of the cs142 collections in the database.
 *                   Format is a JSON object with properties being the collection name and
 *                   the values being the counts.
 *
 * The following URLs need to be implemented:
 * /user/list     -  Returns an array containing all the User objects from the database.
 *                   (JSON format)
 * /user/:id      -  Returns the User object with the _id of id. (JSON format).
 * /photosOfUser/:id' - Returns an array with all the photos of the User (id). Each photo
 *                      should have all the Comments on the Photo (JSON format)
 *
 */

var mongoose = require('mongoose');
var async = require('async');


// Load the Mongoose schema for User, Photo, and SchemaInfo
var User = require('./schema/user.js');
var Photo = require('./schema/photo.js');
var SchemaInfo = require('./schema/schemaInfo.js');
var fs = require("fs"); //new

var express = require('express');
var app = express();
//new:
var session = require('express-session');
var bodyParser = require('body-parser');
var multer = require('multer');
var processFormBody = multer({storage: multer.memoryStorage()}).single('uploadedphoto');

//added for communication w/ django
var http = require('http');
var querystring = require('querystring');

mongoose.connect('mongodb://localhost/cs142project6');

// We have the express static module (http://expressjs.com/en/starter/static-files.html) do all
// the work for us.
app.use(express.static(__dirname));
//new:
app.use(session({secret: 'secretKey', resave: false, saveUninitialized: false})); //this has the key crypto
app.use(bodyParser.json());


app.get('/', function (request, response) {
    response.send('Simple web server of files from ' + __dirname);
});



/*
 * Use express to handle argument passing in the URL.  This .get will cause express
 * To accept URLs with /test/<something> and return the something in request.params.p1
 * If implement the get as follows:
 * /test or /test/info - Return the SchemaInfo object of the database in JSON format. This
 *                       is good for testing connectivity with  MongoDB.
 * /test/counts - Return an object with the counts of the different collections in JSON format
 */
app.get('/test/:p1', function (request, response) {
    // Express parses the ":p1" from the URL and returns it in the request.params objects.
    // console.log('/test called with param1 = ', request.params.p1);

    var param = request.params.p1 || 'info';

    if (param === 'info') {
        // Fetch the SchemaInfo. There should only one of them. The query of {} will match it.
        SchemaInfo.find({}, function (err, info) {
            if (err) {
                // Query returned an error.  We pass it back to the browser with an Internal Service
                // Error (500) error code.
                console.error('Doing /user/info error:', err);
                response.status(500).send(JSON.stringify(err));
                return;
            }
            if (info.length === 0) {
                // Query didn't return an error but didn't find the SchemaInfo object - This
                // is also an internal error return.
                response.status(500).send('Missing SchemaInfo');
                return;
            }

            // We got the object - return it in JSON format.
            console.log('SchemaInfo1', info[0]);
            response.end(JSON.stringify(info[0]));
        });
    } else if (param === 'counts') {
        // In order to return the counts of all the collections we need to do an async
        // call to each collections. That is tricky to do so we use the async package
        // do the work.  We put the collections into array and use async.each to
        // do each .count() query.
        var collections = [
            {name: 'user', collection: User},
            {name: 'photo', collection: Photo},
            {name: 'schemaInfo', collection: SchemaInfo}
        ];
        async.each(collections, function (col, done_callback) {
            col.collection.count({}, function (err, count) {
                col.count = count;
                done_callback(err);
            });
        }, function (err) {
            if (err) {
                response.status(500).send(JSON.stringify(err));
            } else {
                var obj = {};
                for (var i = 0; i < collections.length; i++) {
                    obj[collections[i].name] = collections[i].count;
                }
                response.end(JSON.stringify(obj));

            }
        });
    } else {
        // If we know understand the parameter we return a (Bad Parameter) (400) status.
        response.status(400).send('Bad param ' + param);
    }
});

/*
 * URL /user/list - Return all the User object.
 */
app.get('/user/list', function (request, response) {
    // response.status(501).send("Not Implemented");
    // console.log("request : " + request);
    if (!request.session.logged_user) {
        response.status(401).send("Please log in");
        return;
    }
    
    User.find(function (err, info) {

        // console.log("my info for /user/list is : "+info);

        if (err) {
            // Query returned an error.  We pass it back to the browser with an Internal Service
            // Error (500) error code.
            console.error('Doing /user/info error:', err);
            response.status(500).send(JSON.stringify(err));
            return;
        }
        if (info.length === 0) {
            // Query didn't return an error but didn't find the SchemaInfo object - This
            // is also an internal error return.
            response.status(500).send('Missing SchemaInfo');
            return;
        }


        var userlist = [];
        for (var i = 0; i < info.length; i++) {
            var temp_user = {};
            temp_user.id = info[i].id;
            temp_user.first_name = info[i].first_name;
            temp_user.last_name = info[i].last_name;
            temp_user._id = info[i]._id;
            userlist.push(temp_user);
        }
        // console.log("my parsed_users for /user/list is : "+JSON.stringify(userlist));
        response.send(JSON.stringify(userlist));

    });

});

/*
 * URL /user/:id - Return the information for User (id)
 */
app.get('/user/:id', function (request, response) {
    // response.status(501).send("Not Implemented");
    if (!request.session.logged_user) {
        response.status(401).send("Please log in");
        return;
    }


    var user_id = request.params.id || 'info';
 
    User.find({_id: user_id}, function (err, info) {
        
        if(info===undefined){
            response.status(400).send('Bad param ' + user_id);
            return;
        } else if (err) {
            // Query returned an error.  We pass it back to the browser with an Internal Service
            // Error (500) error code.
            console.error('Doing /user/info error:', err);
            response.status(500).send(JSON.stringify(err));
            return;
        } else if (info.length === 0) {
            // Query didn't return an error but didn't find the SchemaInfo object - This
            // is also an internal error return.
            response.status(500).send('Missing SchemaInfo');
            return;
        }

        // We got the object - return it in JSON format.
        // console.log('success'); //test

        var newUser = {};
        newUser.occupation = info[0].occupation;
        newUser.description = info[0].description;
        newUser.location = info[0].location;
        newUser.id = info[0].id;
        newUser.last_name = info[0].last_name;
        newUser.first_name = info[0].first_name;
        // response.send(new_user);
        response.status(200).send(JSON.stringify(newUser));
        //response.status(200).send(JSON.stringify(info[0])); //used to be info[0]

    });

});

/*
 * URL /photosOfUser/:id - Return the Photos for User (id)
 */
app.get('/photosOfUser/:id', function (request, response) {
    // response.status(501).send("Not Implemented");
    if (!request.session.logged_user) {
        response.status(401).send("Please log in");
        return;
    }

    var user_id = request.params.id;
    Photo.find({user_id: user_id}, function (err, photosz) {
        // console.log("photos: ", photosz);
        if(photosz===undefined){
                response.status(400).send('Bad param ' + user_id);
                return;
        } else if (err) {
            // Query returned an error.  We pass it back to the browser with an Internal Service
            // Error (500) error code.
            console.error('Doing /user/info error:', err);
            response.status(500).send(JSON.stringify(err));
            return;
        } else if (photosz.length === 0) {
            // Query didn't return an error but didn't find the SchemaInfo object - This
            // is also an internal error return.
            response.status(400).send('Missing SchemaInfo');
            return;
        }

        var photos = JSON.parse(JSON.stringify(photosz));
        // We got the object - return it in JSON format.
        // console.log("#######1");
        // console.log(photos[0]); //test
        //process photos to photo list: //item is one photo
        async.each(photos, function(item, photodonecallback){
            var comments = item.comments;

            async.each(comments, function(comment, commentdonecallback){
                User.findOne({_id: comment.user_id}, function (err2, user) {
                    if (err2) {
                        response.status(500).send(JSON.stringify(err));
                        return;
                    }
                    if (user.length === 0) {
                        response.status(500).send('Missing SchemaInfo');
                        return;
                    }
                    var f_name = user.first_name;
                    var l_name = user.last_name;
                    // comment.user = f_name+ " " +l_name;
                    // console.log("my first name is:" +  f_name);
                    // console.log("my last name is:" +  l_name);
                    comment.user = user;
                    // console.log("#######2");
                    // console.log("comment and user: " + comment.user);
                    // console.log(comments);
                    commentdonecallback(err2);
                });
            }, function(err2){
                photodonecallback(err);
            });
            
        }, function(err){
            // console.log("#######3");
            // console.log("information: " +photos);
            response.status(200).send(JSON.stringify(photos));
        });

        
    });
});

app.post('/admin/login', function (request, response) {
    // console.log("my request is" + JSON.stringify(request) );
    // console.log("request details body:", request.body);
    // console.log("request details params:", request.params);
    var login_name = request.body.login_name;
    var passWord = request.body.password;
    console.log("login_name passed in body is:" , login_name);
    console.log("password passed in body is:" , passWord);
    // console.log("my login_name is:"+ login_name);
    // console.log("my params are: "+ request.params);
    console.log('/admin/login request.session info'+ JSON.stringify(request.session));

    User.findOne({login_name: login_name}, function (err, data) {
        // console.log("my data is: "+ data);
        if(err){ //verify
                response.status(500).send('login_name or password is not a valid account ');
                return;
        } 
        if(!data) { //verify
                response.status(400).send('User name could not be found!');
                return;
        } 
        if (passWord !== data.password){
            response.status(400).send('Incorrect password. Please try again.');
            return;
        } 
        request.session.logged_user = data;
        response.end(JSON.stringify(data));
        // response.status(200).send(); //send response
    });

});

app.post('/admin/logout', function (request, response) {

    // var login_name = request.params.login_name;
    // var user_id  = request.session.user_id; 
    var login_name = request.session.logged_user.login_name;
    console.log("login_name: " + login_name);

    // console.log('/admin/logout request.session info'+ JSON.stringify(request));

    User.findOne({login_name: login_name}, function (err, data) {
        if(err){ //verify
                response.status(500).send('login_name is not valid');
                return;
        } if(!data){ //verify
                response.status(400).send('Missing SchemaInfo');
                return;
        }
        console.log("reached destroy!!!");
        request.session.destroy(
            function(err2){
                if (err2){ //verify
                    response.status(500).send('login_name is not a valid account');
                    return;
                }
                response.status(200).send();
            }
        );
    }); 
});

app.post('/commentsOfPhoto/:photo_id', function (request, response) {

    var photoId = request.params.photo_id; //what should that be?
    var newComment = request.body.comment;
    var userId = request.session.logged_user.id;
    //get something for the user Id to
    Photo.findOne({id: photoId}, function (err, photoData) { //what should that be?
        //update
        if(err){ //verify
                response.status(500).send('login_name is not a valid account');
                return;
        } if(!photoData){ //verify
                response.status(400).send('Missing SchemaInfo');
                return;
        }
        var date = new Date();
        var fullComment = {comment: newComment, date_time: date, user_id: userId};
        console.log("created comment is: ", newComment);
        photoData.comments.push(fullComment);
        photoData.save();
        response.status(200).send();
    });

});

app.post('/photos/new', function (request, response) {
    var userId = request.session.logged_user.id;

    if (!request.session.logged_user) {
        response.status(400).send("Please Log In");
        return;
    }

    processFormBody(request, response, function (err) {
        if (err || !request.file) {
            // XXX -  Insert error handling code here.
            response.status(400).send("error");
            return;
        }
        // request.file has the following properties of interest
        //      fieldname      - Should be 'uploadedphoto' since that is what we sent
        //      originalname:  - The name of the file the user uploaded
        //      mimetype:      - The mimetype of the image (e.g. 'image/jpeg',  'image/png')
        //      buffer:        - A node Buffer containing the contents of the file
        //      size:          - The size of the file in bytes

        // XXX - Do some validation here.
        // We need to create the file in the directory "images" under an unique name. We make
        // the original file name unique by adding a unique prefix with a timestamp.
        var timestamp = new Date().valueOf();
        var filename = 'U' +  String(timestamp) + request.file.originalname;

        fs.writeFile("./images/" + filename, request.file.buffer, function (err) {
          // XXX - Once you have the file written into your images directory under the name
          // filename you can create the Photo object in the database
          var date = new Date();
          var comments_arr = [];
          var newPhoto = {file_name: filename, date_time: date, comments: comments_arr, user_id: userId};
          Photo.create(newPhoto, function(err, photoData){
                if (!photoData ||err) {
                    response.status(400).send("An error occured");
                    return;
                }
                photoData.id = photoData._id;
                photoData.save();

                console.log("Photo data of newly created photo is: " , photoData);
                response.status(200).send("Photo successfully uploaded");
          });
        });
    });


});

app.post('/user', function (request, response) {

    var firstName = request.body.first_name;
    var lastName = request.body.last_name;
    var location = request.body.location;
    var description = request.body.description;
    var occupation = request.body.occupation;
    var passWord = request.body.password;
    var loginName = request.body.login_name;

    User.findOne({login_name: loginName}, function (err, data) {
        if(err){ //verify
            response.status(500).send('Error occured: ' + err);
            return;
        } else if (!data){ //no user we can go a head and create new user
            // response.status(400).send('Missing SchemaInfo');
            // return;

            var newObj = {first_name:firstName , last_name:lastName , location:location , description:description , occupation:occupation , password:passWord, login_name:loginName};

            User.create(newObj, function(err, userObj){
                if (!userObj ||err) {
                    response.status(400).send("An error occured");
                    return;
                }
                userObj.id = userObj._id;
                userObj.save();
                response.status(200).send();
            });
            return;
        } else {
            response.status(400).send("Login Name already exists please choose a different login name.");
            return;
        }
    });

});

//new functions:

var postDjango = function(request, response, path, cb) {
    var post_data = querystring.stringify({
      'compilation_level' : 'ADVANCED_OPTIMIZATIONS',
      'output_format': 'json',
      'output_info': 'compiled_code',
      'warning_level' : 'QUIET',
      'js_resp' : JSON.stringify(request.body)
    });
    var post_options = {
      host: '127.0.0.1',
      port: '8000',
      path: '/' + path + '/',
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Content-Length': Buffer.byteLength(post_data)
      }
    };
    var post_req = http.request(post_options, function(res) {
      res.setEncoding('utf8');
      res.on('data', function (chunk) {
            cb(chunk);
      }).on('error', function(err) {
        console.log(err);
      });
    });

    post_req.write(post_data);
    post_req.end();
}

app.post('/newGame', function (request, response) {
    console.log("hello")
    postDjango(request, response, 'initialize', function(chunk) {
        console.log("INITIAL CHUNK:")
        console.log(chunk);
        response.status(200).send(chunk);
    });
});

app.post('/gameState', function (request, response) {
    postDjango(request, response, 'djangotest', function(chunk) {
        console.log(chunk);
        console.log("sending chunk!")
        response.status(200).send(chunk);
    });
});

//****************************************************
//Functions to respond to user game actions:
//****************************************************
app.post('/endOfTurn', function (request, response) {
    console.log("endOfTurn pressed")
    response.status(200).send();
});


app.post('/rollADie', function (request, response) {
    console.log("rollDieButton Pressed")
    //TODO: send an updated game state with roll result
    response.status(200).send();
});

app.post('/buildRoad', function (request, response) {
    var roadLocation = request.body.suggestedLocation
    console.log("buildRoad Pressed, location: "+ roadLocation)
    response.status(200).send();
});

app.post('/buildSettlement', function (request, response) {
    var settlementLocation = request.body.suggestedLocation
    console.log("buildSettlement Pressed, location: "+ settlementLocation)
    response.status(200).send();
});

app.post('/buildCity', function (request, response) {
    var cityLocation = request.body.suggestedLocation
    console.log("buildCity Pressed, location: "+ cityLocation)
    response.status(200).send();
});

app.post('/buyCard', function (request, response) {
    var devCardType = request.body.devCardType
    console.log("buyCard Pressed, Type: "+ devCardType)
    response.status(200).send();
});

app.post('/playDevCard', function (request, response) {
    var devCardType = request.body.devCardType
    console.log("playDevCard Pressed, Type: "+ devCardType)
    response.status(200).send();
});

app.post('/setRobberPosition', function (request, response) {
    var tilePosition = request.body.tilePosition
    console.log("setRobberPosition Pressed, new position: "+ tilePosition)
    response.status(200).send();
});






var server = app.listen(3000, function () {
    var port = server.address().port;
    console.log('Listening at http://localhost:' + port + ' exporting the directory ' + __dirname);
});
