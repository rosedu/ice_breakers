'use strict';


// Declare app level module which depends on filters, and services
angular.module('MyApp', [
  'ngRoute',
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
  'myApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/manager-login', {templateUrl: 'partials/manager-login.html', controller: 'ManagerLoginController'});
  $routeProvider.when('/manager-dashboard', {templateUrl: 'partials/manager-dashboard.html', controller: 'ManagerDashboardController'});
  $routeProvider.when('/partial1', {templateUrl: 'partials/partial1.html', controller: 'MyCtrl1'});
  $routeProvider.otherwise({redirectTo: '/manager-dashboard'});
}]);
