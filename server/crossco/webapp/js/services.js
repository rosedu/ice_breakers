'use strict';

/* Services */

// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', ['ngResource'])
    .factory('AngularIssues', function($resource){
        return $resource('https://api.github.com/repos/angular/angular.js/issues/:number',
            {getIssue: {method: 'GET'}}
        )
    })
    .factory('User', function($resource){
        return $resource('http://sniffio.com:5000/api/my/user',
            {}
        )
    })
    .value('version', '0.1');
