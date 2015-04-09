angular.module('wallfly')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/property/:id', {
        templateUrl: '/static/js/views/property/property.html',
        controller: 'PropertyController',
        resolve:{
	  resolvedProperty: ['$http', '$route', function($http, $route) {
	    return $http.get('/property/' + $route.current.params.id).success(function(data) {
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
