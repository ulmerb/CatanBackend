'use strict';

var cs142App = angular.module('cs142App', ['ngRoute', 'ngMaterial', 'ngResource']); //consider adding ngResource



cs142App.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/users', {
                templateUrl: 'components/user-list/user-listTemplate.html',
                controller: 'UserListController'
            }).
            when('/login-register', {
                templateUrl: 'components/login-register/login-registerTemplate.html',
                controller: 'LoginRegisterController'
            }).
            otherwise({
                redirectTo: '/users'
            });
    }]);


cs142App.config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
            .primaryPalette('light-blue')
            .accentPalette('orange');
});



cs142App.controller('MainController', ['$scope','$rootScope', '$location', '$resource', '$http',
    function ($scope, $rootScope, $location, $resource, $http) {
        $scope.main = {};
        $scope.main.title = {title: 'Users'};
        $scope.main.titleText = "main page";
        $scope.main.version = "0"; //added this version
        $scope.main.map = ["                         /~~~~~~\\~~port3~~/~~~~~~~\\\n", "                        /~~~~~~~~\\*~~~~~*/~~~~~~~~~\\\n", "                 >-----<~~~~~~~~~01V-01R-02V~~~~~~~~>-----<\n", "                /~~~~~~~\\~~~~~~~~/       \\~~~~~~~~~~/~~~~~~\\\n", "               /~~~~~~~~\\~~~~~~~02R      03R~~~~~~~~/~~~~~~~\\\n", "              /~~~~~~~~~\\~~~~~~~/   01T    \\~~~~~~~/~~~~~~~~\\\n", "       >-----<~~port2~*03V-04R-04V        05V-05R-06V*~port4~>-----<\n", "      /~~~~~~~\\~~~~~~~~~/       \\         /       \\~~~~~~~~~~/~~~~~~\\\n", "      /~~~~~~~\\~~~~~~~~06R       07R      08R      09R~~~~~~~/~~~~~~~\\\n", "     /~~~~~~~~~\\~~~~~~*/  02T    \\       /   03T    \\*~~~~~~/~~~~~~~~\\\n", "    <~~~~~~~~~07V-10R-08V        09V-11R-10V       11V-12R-12V~~~~~~~~>\n", "     \\~~~~~~~~~/       \\         /       \\         /       \\~~~~~~~~~/\n", "     \\~~~~~~~13R      14R      15R      16R      17R      18R~~~~~~~~/\n", "      \\~~~~~~~/  04T    \\       /   05T   \\       /   06T   \\~~~~~~~/\n", "       >---- 13V       14V-19R-15V       15V-20R-16V        17V----<\n", "      /~~~~~~~\\         /       \\         /       \\         /~~~~~~\\\n", "     /~~~~~~~~21R      22R      23R      24R      25R     26R~~~~~~~\\\n", "     /~~~~~~~~~\\       /    07T  \\       /   08T   \\       /~~~~~~~~~\\\n", "   <~~~port1~~*18V-27R-19V      20V-28R-21V       22V-29R-23V*~port5~~>\n", "     \\~~~~~~~~~/       \\         /       \\         /       \\~~~~~~~~~~/\n", "     \\~~~~~~~30R      31R      32R      33R      34R      35R~~~~~~~~/ \n", "      \\~~~~~~*/   09T   \\       /   10T   \\       /   11T   \\*~~~~~~~/\n", "       >----24V        25V-36R-26V       27V-37R-28V        29V-----<\n", "      /~~~~~~~\\         /       \\         /       \\         /~~~~~~~\\\n", "     /~~~~~~~38R      39R     40R       41R      42R      43R~~~~~~~~\\\n", "     /~~~~~~~~~\\       /   12T   \\       /   13T   \\       /~~~~~~~~~\\\n", "    <~~~~~~~~~30V-44R-31V       32V-45R-33V       34V-46R-35V~~~~~~~~~>\n", "     \\~~~~~~~~~/       \\         /       \\         /       \\~~~~~~~~/\n", "     \\~~~~~~~~47R     48R       49R      50R     51R      52R~~~~~~~/\n", "      \\~~~~~~~/   14T   \\       /   15T   \\       /   16T   \\~~~~~~~~/\n", "       >-----36V       37V-53R-38V       39V-54R-40V       41V------< \n", "      /~~~~~~*\\         /       \\         /       \\         /*~~~~~~\\\n", "     /~~~~~~~~55R      56R     57R       58R     59R       60R~~~~~~\\\n", "     /~~~~~~~~~\\       /   17T   \\       /   18T   \\       /~~~~~~~~~\\\n", "    <~~port9~~*42V-61R-43V      44V-62R-45V       46V-63R-47V*~port6~~>\n", "     \\~~~~~~~~~/~~~~~~~\\         /       \\         /~~~~~~~\\~~~~~~~~~/\n", "     \\~~~~~~~~/~~~~~~~~63R      64R      65R     66R~~~~~~~\\~~~~~~~~~/\n", "      \\~~~~~~~/~~~~~~~~~\\       /   19T   \\       /~~~~~~~~~\\~~~~~~~/\n", "       >-----< ~~~~~~~~48V-67R-49V       50V-68R-51V~~~~~~~~~>------<\n", "              \\~~~~~~~~~/*~~~~~*\\         /*~~~~~*\\~~~~~~~~~/\n", "              \\~~~~~~~~/~~~~~~~~69R     70R~~~~~~~\\~~~~~~~~/\n", "               \\~~~~~~~/~~~~~~~~~\\       /~~~~~~~~~\\~~~~~~~/\n", "                >-----<~~~port8~~52V-71R-53V~~port7~>-----<\n", "                       \\~~~~~~~~~/~~~~~~~\\~~~~~~~~~/\n", "                        \\~~~~~~~/~~~~~~~~~\\~~~~~~~/\n"];
        $scope.main.temp = ["1","2","2"]

        $scope.main.message_to_user = ""
        // trading vars:
        $scope.main.give_ore = 0
        $scope.main.give_wood = 0
        $scope.main.give_brick = 0
        $scope.main.give_grain = 0
        $scope.main.give_sheep = 0
        $scope.main.get_ore = 0
        $scope.main.get_wood = 0
        $scope.main.get_brick = 0
        $scope.main.get_grain = 0
        $scope.main.get_sheep = 0

        $scope.main.currentPlayer = 1
        //temp
        $scope.main.numPlayers = 2
        $scope.main.devCards = []
        $scope.main.players = []
        $scope.main.hasLongestRoad = false
        $scope.main.hasLargestArmy = false
        $scope.main.victoryPointCardsPlayed = 0
        $scope.main.portsControlled = 0
        
        $scope.main.isUserLoggedIn = false
        $scope.main.userAlreadyRolledDieThisTurn = false
        $scope.main.lastDieRollValue = 0
        /*send this to the backend when filled*/
        $scope.main.buildRoadLocation = ""
        $scope.main.buildSettlementLocation = ""
        $scope.main.buildCityLocation = ""
        $scope.main.robberLocation = ""

        /*
        * FetchModel - Fetch a model from the web server.
          *   url - string - The URL to issue the GET request.
          *   doneCallback - function - called with argument (model) when the
          *                  the GET request is done. The argument model is the object
          *                  containing the model. model is undefined in the error case.
          */
        $scope.FetchModel = function(url, doneCallback) {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function xhrHandler() {
                //Don’t do anything if not final state
                if (this.readyState !== 4){ 
                    return; 
                }
                //Final State but status not OK
                if (this.status !== 200) {
                    return;
                }
                var model = this.responseText;
                doneCallback(model);
            };
            xhr.open("GET", url);
            console.log("my url is: ", url);
            xhr.send();
         };

        // Call fetch model to display the version.
        $scope.FetchModel("http://localhost:3000/test/info", function(model) {
          $scope.$apply(function () {
            $scope.main.version = JSON.parse(model).version;
            console.log($scope.main.version); 
          });
        });


        $rootScope.$on( "$routeChangeStart", function(event, next, current) {
          if (!$scope.main.isUserLoggedIn) {
             // no logged user, redirect to /login-register unless already there
            if (next.templateUrl !== "components/login-register/login-registerTemplate.html") {
                $location.path("/login-register");
            }
          }
        });


        $scope.main.logout = function($event) {
            var logout = $resource("/admin/logout");
            logout.save({},function(){
                $scope.main.isUserLoggedIn = false;
                $scope.main.titleText = "Please Login";
                $rootScope.$broadcast("loggedOut");
                $location.path("/login-register");
            },function errorHandling(err){
                //errors
            });
        };

        //Uploading the photos:

        var selectedPhotoFile;   // Holds the last file selected by the user

        // Called on file selection - we simply save a reference to the file in selectedPhotoFile
        $scope.inputFileNameChanged = function (element) {
            selectedPhotoFile = element.files[0];
        };

        // Has the user selected a file?
        $scope.inputFileNameSelected = function () {
            return !!selectedPhotoFile;
        };

        // Upload the photo file selected by the user using a post request to the URL /photos/new
        $scope.uploadPhoto = function () {
            console.log("uploadPhoto button clicked");
            if (!$scope.inputFileNameSelected()) {
                console.error("uploadPhoto called will no selected file");
                return;
            }
            console.log('fileSubmitted', selectedPhotoFile);

            // Create a DOM form and add the file to it under the name uploadedphoto
            var domForm = new FormData();
            domForm.append('uploadedphoto', selectedPhotoFile);

            // Using $http to POST the form
            $http.post('/photos/new', domForm, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            }).success(function(newPhoto){
                // The photo was successfully uploaded. XXX - Do whatever you want on success.
                console.log("photo was successfully uploaded");
                //do a broad cast;
            }).error(function(err){
                // Couldn't upload the photo. XXX  - Do whatever you want on failure.
                console.error('ERROR uploading photo', err);
            });

        };

        $scope.readTextFile = function(file)
        {
            var rawFile = new XMLHttpRequest();
            rawFile.open("GET", file, false);
            rawFile.onreadystatechange = function ()
            {
                if(rawFile.readyState === 4)
                {
                    if(rawFile.status === 200 || rawFile.status == 0)
                    {
                        var allText = rawFile.responseText;
                        alert(allText);
                    }
                }
            }
            rawFile.send(null);
        }

        $scope.sendTradeMessageToUserMessage = function(){
            $scope.main.message_to_user = "This is your offer: Ore:"+$scope.main.give_ore+", Brick:"+ $scope.main.give_brick
                 + ",Grain:" + $scope.main.give_grain + ", Wood: " + $scope.main.give_wood + ", Sheep:" +$scope.main.give_sheep+". "
                 + "This is what you want: Ore:" + $scope.main.get_ore + ", Brick:" + $scope.main.get_brick 
                 + ",Grain:" + $scope.main.get_grain + ", Wood: " + $scope.main.get_wood+ ", Sheep:" + $scope.main.get_sheep 
        }

        //New functions:

        $scope.rollDieButtonPressed = function() {
            $scope.main.userAlreadyRolledDieThisTurn = true
            $scope.main.lastDieRollValue = 7 //remove later
        }

        $scope.getGameState = function() {
            var userRes = $resource("/gameState");
            userRes.save({'action':'build'},  
                function (model){
                    $scope.main.message_to_user = "data passed successfully!";
                    console.log("model:");
                    // console.log(model);
                    //update all variables on UI
                    $scope.updateBoardBasedOnRecievedGameState(model)
                }, function errorHandling(err) {
                    $scope.login_name = "";
                    $scope.password = "";
                    $scope.error_text = "Error: "+ err.data;
                    $scope.main.message_to_user = "Error: "+ err.data;
                }
            )
        }

        $scope.updateBoardBasedOnRecievedGameState = function(model) {
            console.log("JSON data is: ");
            console.log(model);
            console.log(model.message);
            console.log(model.numPlayers);
        }


    }]);

    


 






