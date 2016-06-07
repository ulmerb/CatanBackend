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

        $scope.main.currentPlayer = 0
        //temp
        $scope.main.numPlayers = 0
        $scope.main.devCards = []
        $scope.main.players = []
        $scope.main.hasLongestRoad = false
        $scope.main.hasLargestArmy = false
        $scope.main.victoryPoints = 0
        $scope.main.victoryPointCardsPlayed = 0
        $scope.main.lengthOfLongestRoad = 0
        $scope.main.knightsPlayed = 0
        $scope.main.portsControlled = 0
        $scope.main.resources = []
        $scope.main.cities = []
        $scope.main.ports = []
        $scope.main.settlements = []
        $scope.main.roads = []
        
        $scope.main.isUserLoggedIn = false
        $scope.main.userAlreadyRolledDieThisTurn = false
        $scope.main.lastDieRollValue = 0
        
        /*send this to the backend when filled*/
        $scope.main.buildRoadLocation = ""
        $scope.main.buildSettlementLocation = ""
        $scope.main.buildCityLocation = ""
        $scope.main.robberLocation = ""
        $scope.main.buyDevCard = "" 
        $scope.main.playDevCard = ""
        
        //Dev cards booleans:
        $scope.main.devCardMonopolyYOP = false
        $scope.main.devCardKnight = false
        $scope.main.devCardRoadBuilding = false

        $scope.main.robberPlayerToStealFrom = 0
        
        //play dev cards:
        $scope.main.devCardBrick = false
        $scope.main.devCardWood = false
        $scope.main.devCardSheep = false
        $scope.main.devCardGrain = false
        $scope.main.devCardOre = false
        $scope.main.devCardRoadLocation1 = 0
        $scope.main.devCardRoadLocation2 = 0

        //trading:
        $scope.main.offer = {}
        $scope.main.take = {}
        $scope.main.isTrading = false
        $scope.main.proposer = 0

        $scope.testPlayDevCard = function(str){
            console.log("brick " + $scope.main.devCardBrick)
            console.log(str)
        }

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

        //New functions:
        $scope.getGameState = function() {
            var userRes = $resource("/gameState");
            console.log("calling: getGameState");
            userRes.save({'action':'build'},  
                function (model){
                    $scope.main.message_to_user = "data passed successfully!";
                    console.log("model: success");
                    // console.log(model);
                    //update all variables on UI
                    $scope.updateBoardBasedOnRecievedGameState(model)
                }, function errorHandling(err) {
                    $scope.login_name = "";
                    $scope.password = "";
                    $scope.error_text = "Error: "+ err;
                    $scope.main.message_to_user = "Error: "+ err.data;
                }
            )
        }

        $scope.newGame = function() {
            var userRes = $resource("/newGame");
            userRes.save({'newgame':'newgame', 'numPlayers': 2, 'AI':false},
                function (model){
                    console.log('new game model');
                    $scope.updateBoardBasedOnRecievedGameState(model);
                    $scope.initialPlacement(model);
                    //update all variables on UI
                    //$scope.updateBoardBasedOnRecievedGameState(model)
                }, function errorHandling(err) {
                    $scope.login_name = "";
                    $scope.password = "";
                    $scope.error_text = "Error: "+ err.data;
                    $scope.main.message_to_user = "Error: "+ err.data;
                }
            )
        }

        $scope.initialPlacement = function(model) {
            for(var i =0; i < $scope.main.numPlayers; i++) {
                
            }
        }

        $scope.updateBoardBasedOnRecievedGameState = function(model) {
            console.log("JSON data is: ");
            console.log(model);
            
            //update variables:
            $scope.main.currentPlayer = model.currentPlayer
            $scope.main.numPlayers = model.numPlayers
            $scope.main.message_to_user = model.message
            $scope.main.players = model.players
            if(model.currentDiceRoll) {
                $scope.main.lastDieRollValue = model.currentDiceRoll
            }
            $scope.main.devCards = model.players[$scope.main.currentPlayer].devCards
            $scope.main.resources = model.players[$scope.main.currentPlayer].resources
            $scope.main.hasLongestRoad = model.players[$scope.main.currentPlayer].hasLongestRoad
            $scope.main.hasLargestArmy = model.players[$scope.main.currentPlayer].hasLargestArmy
            $scope.main.victoryPoints = model.players[$scope.main.currentPlayer].victoryPoints
            $scope.main.cities = model.players[$scope.main.currentPlayer].cities
            $scope.main.ports = model.players[$scope.main.currentPlayer].ports
            $scope.main.settlements = model.players[$scope.main.currentPlayer].settlements
            $scope.main.roads = model.players[$scope.main.currentPlayer].roads
            $scope.main.victoryPointCardsPlayed = model.players[$scope.main.currentPlayer].victoryPointCardsPlayed
            $scope.main.lengthOfLongestRoad = model.players[$scope.main.currentPlayer].lengthOfLongestRoad
            //$scope.main.knightsPlayed = model.players[$scope.main.currentPlayer].devCardsPlayed.knight
            
            var arr = model.boardString.split("\n");
            var newArr = [];
            for(var i = 0; i < arr.length; i++) {
                if(arr[i] !== "") {
                    var z = arr[i] + '\n';
                    newArr.push(z);
                }
            }
            $scope.main.map = newArr;
        
            if ($scope.main.lastDieRollValue == 0) {
                $scope.main.userAlreadyRolledDieThisTurn = false
            } else {
                $scope.main.userAlreadyRolledDieThisTurn = true
            }

        }
        //***************************
        //Functions for Game actions:
        //***************************
        $scope.endTurnPressed = function () {  
            if($scope.main.currentPlayer) {}
            var userRes = $resource("/endOfTurn");
            console.log('currentPlayer before' + $scope.main.currentPlayer);
            userRes.save({'currentPlayer': $scope.main.currentPlayer},
                function (model){
                    $scope.updateBoardBasedOnRecievedGameState(model)
                    //TODO: set up the board for the next player
                    console.log('updated resources and dice roll');
                    console.log(model);
                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: endTurnPressed failed";
                }
            )
        }

        //already implemented when turn ends:
        // $scope.rollDieButtonPressed = function() {
        //     var userRes = $resource("/rollADie");
        //     userRes.save({},
        //         function (model){
        //             $scope.main.userAlreadyRolledDieThisTurn = true
        //             $scope.main.lastDieRollValue = model.currentDiceRoll
        //             $scope.main.message_to_user = "Dice roll result: " + model.currentDiceRoll
        //         }, function errorHandling(err) {
        //             $scope.main.message_to_user = "Error: rollDieButtonPressed failed";
        //         }
        //     )
        // }

        

        $scope.buildRoadButtonPressed = function() {
            var userRes = $resource("/buildRoad");
            var suggestedEdgeForRoad = $scope.main.buildRoadLocation
            userRes.save({'suggestedLocation':suggestedEdgeForRoad, 'curPlayer':$scope.main.currentPlayer},
                function (model){
                    $scope.updateBoardBasedOnRecievedGameState(model);
                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: buildRoadButtonPressed failed";
                }
            )
        }

        $scope.buildSettlementButtonPressed = function() {
            var userRes = $resource("/buildSettlement");
            var suggestedVertexForSettlement = $scope.main.buildSettlementLocation
            userRes.save({'suggestedLocation':suggestedVertexForSettlement, 'curPlayer':$scope.main.currentPlayer},
                function (model){
                    $scope.updateBoardBasedOnRecievedGameState(model);
                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: buildSettlementButtonPressed failed";
                }
            )
        }

        $scope.buildCityButtonPressed = function() {
            var userRes = $resource("/buildCity");
            var suggestedVertexForCity = $scope.main.buildCityLocation
            userRes.save({'suggestedLocation':suggestedVertexForCity, 'curPlayer':$scope.main.currentPlayer},
                function (model){
                    $scope.updateBoardBasedOnRecievedGameState(model);

                    //TODO: if city can be built, build it
                    //else continue
                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: buildCityButtonPressed failed";
                }
            )
        }

        $scope.buyDevCardButtonPressed = function() {
            var userRes = $resource("/buyCard");
            userRes.save({'curPlayer':$scope.main.currentPlayer},
                function (model){
                    console.log("model after card bought");
                    console.log(model.players[$scope.main.currentPlayer].devCards);
                    console.log(model)
                    $scope.updateBoardBasedOnRecievedGameState(model);
                    // if(model.devCardName === "victoryPoint") {
                    //     $scope.playDevCardButtonPressed("victoryPoint");
                    // }
                    //TODO: if card can be bought, build it
                    //else continue
                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: buyDevCardButtonPressed failed";
                }
            )
        }

        //note str can be one of the following three: 
        $scope.playDevCardButtonPressed = function(str) {
            var userRes = $resource("/playDevCard");
            var devCardType = str
            console.log(str +" brick "+$scope.main.devCardBrick + ", wood "+$scope.main.devCardWood+ ", sheep "+$scope.main.devCardSheep+", grain " +$scope.main.devCardGrain+", ore "+ $scope.main.devCardOre+ " loc1 "+$scope.main.devCardRoadLocation1+ " loc2 "+ $scope.main.devCardRoadLocation2)
            userRes.save({'devCardType':devCardType,
                'devCardBrick':$scope.main.devCardBrick,
                'devCardWood':$scope.main.devCardWood,
                'devCardSheep':$scope.main.devCardSheep,
                'devCardGrain':$scope.main.devCardGrain,
                'devCardOre':$scope.main.devCardOre,
                'roadLoc1':$scope.main.devCardRoadLocation1,
                'roadLoc2':$scope.main.devCardRoadLocation2,
                'curPlayer':$scope.main.currentPlayer,
                'tilePosition':$scope.main.robberLocation,
                'playerToStealFrom':$scope.main.robberPlayerToStealFrom
                },
                function (model){
                    console.log("robber location:")
                    console.log(model.robberTileLocation)
                    console.log(model)
                    $scope.updateBoardBasedOnRecievedGameState(model);
                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: playDevCardButtonPressed failed";
                }
            )
        }

        $scope.setRobberPosition = function() {
            var userRes = $resource("/setRobberPosition");
            var tilePosition = $scope.main.robberLocation
            var playerToStealFrom = $scope.main.robberPlayerToStealFrom
            userRes.save({'currentPlayer':$scope.main.currentPlayer, 'tilePosition':tilePosition, 'playerToStealFrom':playerToStealFrom},
                function (model){
                    //TODO: if robber can be moved , move it
                    //else continue
                    console.log("new board");
                    console.log(model);
                    $scope.updateBoardBasedOnRecievedGameState(model);
                    $scope.main.message_to_user = model.message;

                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: playDevCardButtonPressed failed";
                }
            )
        }

        //Functionality: not implemented yet!
        // $scope.exchangeResourcesWithBankButtonPressed = function(e) {
        //     console.log();
        // }

         $scope.showBankTradeForm = function() {
            var playerTrade = document.querySelector('.playerTradeStuff');
            playerTrade.style.display = "none";
            var bankTrade = document.querySelector(".fixedExchangeRates");
            bankTrade.style.display = "block";

            document.querySelector('.bankSubmit').style.display = "block";
            document.querySelector('.portSubmit').style.display = "none";
            document.querySelector(".fixedExchangeGive").style.display = "block";

        }

        $scope.showPlayerTradeForm = function() {
            var playerTrade = document.querySelector('.playerTradeStuff');
            playerTrade.style.display = "block";
            var bankTrade = document.querySelector(".fixedExchangeRates");
            bankTrade.style.display = "none";
        }

        $scope.playerTradeInputs = function() {
            var form = document.getElementById("trading"),
            inputs = form.getElementsByTagName("INPUT");
            $scope.showPlayerTradeForm();
        }

        $scope.bankTradeInputs = function() {
            var form = document.getElementById("trading"),
            inputs = form.getElementsByTagName("INPUT");
            $scope.showBankTradeForm();
        }

        $scope.portTradeInputs = function(port) {
            $scope.main.selectedPort = port
            console.log($scope.main.selectedPort);
            var form = document.getElementById("ports"),
            inputs = form.querySelectorAll("input");
            document.querySelector('.fixedExchangeRates').style.display = "block";
            document.querySelector('.playerTradeStuff').style.display = "none";
            document.querySelector('.bankSubmit').style.display = "none";
            document.querySelector('.portSubmit').style.display = "block";
            if(port === "three") {
                document.querySelector(".fixedExchangeGive").style.display = "block";
            } else {
                document.querySelector(".fixedExchangeGive").style.display = "none";
            }
        }

        //TODO: connect ot back end
        $scope.sendTradeMessageToUserMessage = function(){
            $scope.main.message_to_user = "This is your offer: Ore:"+$scope.main.give_ore+", Brick:"+ $scope.main.give_brick
                 + ",Grain:" + $scope.main.give_grain + ", Wood: " + $scope.main.give_wood + ", Sheep:" +$scope.main.give_sheep+". "
                 + "This is what you want: Ore:" + $scope.main.get_ore + ", Brick:" + $scope.main.get_brick 
                 + ",Grain:" + $scope.main.get_grain + ", Wood: " + $scope.main.get_wood+ ", Sheep:" + $scope.main.get_sheep 
            //get the checked users on the list:

            
            var form = document.getElementById("trading"),
            inputs = form.getElementsByTagName("INPUT"),
            arr = [];
            for (var i = 0, max = inputs.length; i < max; i += 1) {
               // Take only those inputs which are checkbox
               if (inputs[i].type === "radio" && inputs[i].checked) {
                  console.log("ADDED user to trade with: "+ i)
                  arr.push(parseInt(inputs[i].value)+1);
               }
            }

            console.log("users you want to tade with"+arr);
            var userRes = $resource("/suggestTrade");
            userRes.save({'curPlayer':$scope.main.currentPlayer,
                'tradeMessage':$scope.main.message_to_user,
                'offer': {
                    'wood':$scope.main.give_wood,
                    'sheep':$scope.main.give_sheep,
                    'brick':$scope.main.give_brick,
                    'ore':$scope.main.give_ore,
                    'grain':$scope.main.give_grain
                },
                'take': {
                    'wood':$scope.main.get_wood,
                    'sheep':$scope.main.get_sheep,
                    'brick':$scope.main.get_brick,
                    'ore':$scope.main.get_ore,
                    'grain':$scope.main.get_grain
                },
                'userToTradeWithArr':arr},
                function (model){
                    //suggest trade to others
                    console.log(model)
                    if (model.canTrade) {
                        console.log("can trade:true")
                        $scope.main.isTrading = true
                        $scope.updateBoardBasedOnRecievedGameState(model);
                        //take, offer, canTrade
                        $scope.main.offer = model.offer
                        $scope.main.take = model.take
                        $scope.main.proposer = model.proposer
                        $scope.switchToTradeModeUI()
                        
                        var playerTrade = document.querySelector(".playerTradeStuff");
                        playerTrade.style.display = "none";
                        var acceptReject = document.querySelector(".acceptReject");
                        acceptReject.style.display = "block";
                        var acceptRejectButtons = document.querySelectorAll(".acceptRejectButtons");
                        
                        acceptRejectButtons[0].style.display = "block";
                        acceptRejectButtons[1].style.display = "block";
                    } else {
                        console.log("can trade:false")
                        var playerTrade = document.querySelector(".tradeWithPlayer");
                        playerTrade.style.display = "none";
                        $scope.main.message_to_user = model.message;
                    }
                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: sendTradeMessageToUserMessage failed";
                }
            )

        }

        $scope.switchToTradeModeUI = function(){
            var buttons = document.getElementsByTagName("BUTTON");
            for (var i=0, max=buttons.length; i < max; i++) {
                // Do something with the element here
                buttons[i].style.display = "none";
            }
            var playerTrade = document.querySelector(".tradeWithPlayer");
            playerTrade.style.display = "block";
        }

        $scope.accpetOrRejectTrade = function(str) {
            var userRes = $resource("/acceptOrRejectTrade");
            userRes.save({'curPlayer':$scope.main.currentPlayer,
                'acceptOrReject':str,
                'proposer':$scope.main.proposer,
                'offer':$scope.main.offer,
                'take':$scope.main.take
                },
                function (model){
                    console.log(model)
                    $scope.updateBoardBasedOnRecievedGameState(model);
                    $scope.main.message_to_user = model.message;
                    //**** switch UI back to normal*** :
                    var buttons = document.getElementsByTagName("BUTTON");
                    for (var i=0, max=buttons.length; i < max; i++) {
                        // Do something with the element here
                        buttons[i].style.display = "block";
                    }
                    var playerTrade = document.querySelector(".tradeWithPlayer");
                    playerTrade.style.display = "none";
                    var acceptRejectButtons = document.querySelectorAll(".acceptRejectButtons");    
                    acceptRejectButtons[0].style.display = "none";
                    acceptRejectButtons[1].style.display = "none";
                    //**********************************

                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: sendTradeMessagetobankFailed failed";
            });

        }

        $scope.tradeWithBankOrPort = function(str) {
            var userRes = $resource("/tradeWithBankOrPort");
            var takeInputs = document.querySelector(".fixedExchangeTake").querySelectorAll('input');
            var youWantResource = "";
            var youGiveResource = "";
            for (var i = 0; i < takeInputs.length; i++) {
                var inp = takeInputs[i];
                if (inp.checked) {
                    youWantResource = inp.value;
                }
            };

            if(str === "bank" || str === "three") {
                var giveInputs = document.querySelector(".fixedExchangeGive").querySelectorAll('input');
                for (var i = 0; i < giveInputs.length; i++) {
                    var inp = giveInputs[i];
                    if (inp.checked) {
                        youGiveResource = inp.value;
                    }
                };
            }


             userRes.save({'curPlayer':$scope.main.currentPlayer,
                'tradeType':str,
                'youWantResource':youWantResource,
                'youGiveResource':youGiveResource},
                function (model){
                    $scope.updateBoardBasedOnRecievedGameState(model);
                    $scope.main.message_to_user = model.message;
                }, function errorHandling(err) {
                    $scope.main.message_to_user = "Error: sendTradeMessagetobankFailed failed";
            });
           
        }

    }]);