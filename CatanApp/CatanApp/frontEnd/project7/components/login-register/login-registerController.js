'use strict';


cs142App.controller('LoginRegisterController', ['$scope','$routeParams', '$resource','$location','$rootScope',
    function ($scope , $routeParams, $resource, $location, $rootScope) {
        $scope.main.titleText = "Please Login";
        $location.path("/users");
        $scope.login_name = "";
        $scope.error_text = "";
        $scope.password = ""; 
 
        $scope.updateLoginName = function ($event){
            var userRes = $resource("/admin/login");
            console.log("password is:" , $scope.password);
            console.log("login_name is:" , $scope.login_name);
            userRes.save({login_name: $scope.login_name, password: $scope.password}, function (model){
                $scope.main.isUserLoggedIn = true;
                console.log("success");
                $location.path("/users/" + model.id);
                $scope.main.helloMessage = "Hi "+ model.first_name +" "+model.last_name;
                $rootScope.$broadcast("OpenSesame");
            }, function errorHandling(err) {
                $scope.login_name = "";
                $scope.password = "";
                $scope.error_text = "Error: "+ err.data;
            });

        };
        // $scope.userList = window.cs142models.userListModel();
        
        // $rootScope.$broadcast(‘OpenSesame’, 

        //new scope variables for registration:
        $scope.first_name = "";
        $scope.last_name = "";
        $scope.location_registration = "";
        $scope.description_registration = "";
        $scope.occupation = "";
        $scope.password_one = "";
        $scope.password_two = "";
        $scope.login_name_registration = "";

        $scope.error_text_registration = "";

        $scope.registerNewUser = function () {
            //check for errors: 
            if ($scope.password_one !== $scope.password_two) {
                $scope.error_text_registration = "Error: Passwords are not matching please enter the same password.";
                return;
            } else if ($scope.password_one.length === 0 ){
                $scope.error_text_registration = "Error: Please enter a password.";
                return;
            } else if ( $scope.first_name.length === 0) {
                $scope.error_text_registration = "Error: Please enter your first name.";
                return;
            } else if ($scope.last_name.length === 0){
                $scope.error_text_registration = "Error: Please enter your last name.";
                return;
            } else if ($scope.login_name_registration.length === 0) {
                $scope.error_text_registration = "Error: Please enter your desired Login Name.";
                return;
            }
            //post to back end
            var res = $resource("/user");
            res.save({ 
                login_name: $scope.login_name_registration , 
                first_name: $scope.first_name , 
                last_name:  $scope.last_name , 
                location: $scope.location_registration , 
                description: $scope.description_registration , 
                occupation: $scope.occupation , 
                password: $scope.password_one 

            }, function (model){
                console.log("new registration was successfull.");
                $scope.first_name = "";
                $scope.last_name = "";
                $scope.location_registration = "";
                $scope.description_registration = "";
                $scope.occupation = "";
                $scope.password_one = "";
                $scope.password_two = "";
                $scope.login_name_registration = "";

                $scope.error_text_registration = "New registration was successfull!";
                $location.path('/login-register');

            }, function errorHandling(err){
                console.log('Failed to register new user');
                $scope.error_text_registration = 'Error: ' + err.data;
            });
        };
       
    }]);
