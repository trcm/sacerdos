angular.module('wallfly')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/property/:id', {
        templateUrl: '/static/js/views/property/property.html',
        controller: 'PropertyController',
        resolve:{
	  // this is a typical bit of code for getting data from a database when changing the url
	    // this returns all the information for a particular property
	    resolvedProperty: ['$http', '$route', function($http, $route) {
		// so it just sends a get request to tehe backend using the '/propery/:id' route
		return $http.get('/property/' + $route.current.params.id).success(function(data) {
		    // then this success callback returns the data from inside the promise from the database
		    return data.data;
		});
	    }],
	  issues: ['$http', '$route', function($http, $route) {
	    return $http.get('/issues/' + $route.current.params.id).success(function(data) {
	      return data.data;
	    });
	  }]
        }
      });
  }]); 
