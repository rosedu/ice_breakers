'use strict';

/* Controllers */

angular.module('myApp.controllers', []).
  controller('ManagerLoginController', ['$scope', '$location', function() {



  }])
  .controller('ManagerDashboardController', ['$scope', 'User', function($scope, User) {

        $scope.datanew = {};

        User.query(function(response) {

            $scope.datanew.users = response.objects;

        });

  }])
    .controller('MyCtrl1', ['$scope', 'AngularIssues', function($scope, AngularIssues) {

        $scope.data = {};

        AngularIssues.query(function(response) {

            $scope.data.issues = response;

        });

    }]);
