angular.module('wallfly')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/property/:id', {
        templateUrl: '/static/js/views/property/property.html',
        controller: 'PropertyController',
        resolve:{
	  // grab the property details from the database
	  resolvedProperty: ['$http', '$route', function($http, $route) {
	    return $http.get('/property/' + $route.current.params.id).success(function(data) {
	      return data.data;
	    });
	  }],
	  // grab all the issues for the property
	  issues: ['$http', '$route', function($http, $route) {
	    return $http.get('/issues/' + $route.current.params.id).success(function(data) {
	      return data.data;
	    });
	  }]
        }
      });
  }]); 
