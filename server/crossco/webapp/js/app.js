'use strict';


// Declare app level module which depends on filters, and services
angular.module('MyApp', [
  'ngRoute',
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
  'myApp.controllers'
]).
config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.withCredentials = true;
  $routeProvider.when('/manager-login', {templateUrl: '/webapp/partials/manager-login.html', controller: 'ManagerLoginController'});
  $routeProvider.when('/manager-dashboard', {templateUrl: '/webapp/partials/manager-dashboard.html', controller: 'ManagerDashboardController'});
  $routeProvider.when('/partial1', {templateUrl: '/webapp/partials/partial1.html', controller: 'MyCtrl1'});
  $routeProvider.otherwise({redirectTo: '/manager-dashboard'});
}]);
