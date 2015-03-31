angular.module('wallfly',
	       ['ngResource',
		'ngRoute',
		'ngCookies',
		'ui.bootstrap',
		'ui.date',
		'ngLodash'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'static/js/views/home/home.html',
        controller: 'HomeController',
	resolve: {
	  resolveProperties: ['$http', function($http) {
	    return $http.get('/property').success(function(data) {
	      return data.data;
	    });
	  }]
	}})
      .otherwise({redirectTo: '/'});
  }])
  .config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  }]);
