angular.module('wallfly',
	       ['ngResource',
		'ngRoute',
		'ngCookies',
		'LocalStorageModule',
		'ui.bootstrap',
		'ui.date',
		'smart-table',
		'flow',
		'bootstrapLightbox',
		'angularSpinner',
		'ngLodash',
	        'ui.calendar'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      // load the default agent view
      .when('/', {
        templateUrl: 'static/js/views/home/home.html',
        controller: 'HomeController',
	resolve: {
	  // grab all the properties for the user with id 2
	  // will be changed to a dynamic lookup in future versions
	  resolveProperties: ['$http', '$location', '$window', function($http, $location, $window) {
	    // returns all the properties from the database
	    return $http.get('/user/' + $window.sessionStorage.id).success(function(data) {
	      // return $http.get('/user/2').success(function(data) {
	      return data.data;
	    }).error(function() {
	      $location.path('/login');
	    });
	  }]
	}})
    //redirect for calendar test
  .when('/calendar',{
	templateUrl: 'static/js/views/calendar.html',
	controller: 'CalController'})
      .otherwise({redirectTo: '/'});

    // redirect information for the login controller
      .when('/login', {
	templateUrl: 'static/js/views/login.html',
	controller: 'authController'})
      .otherwise({redirectTo: '/login'});
  }])
  .config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.interceptors.push('authInterceptor');
  }])
  .factory('api', function($resource){
    return {
      // grab the token for the user from the database
      token: $resource('/api-token-auth\\/', {}, {
	tok: {method: 'POST' }
      })
    };
  })
  .controller('authController', ['$scope', '$location', '$window', '$http', 'api', 'token', 'usSpinnerService', function($scope, $location, $window, $http, api, token, usSpinnerService) {

    $scope.user = token.getUser();
    // if the spinner is spinning when the user gets to the page stop it
    usSpinnerService.stop('spinner-1');

    // grab the user details from the login form
    $scope.getCredentials = function(){
      return {username: $scope.username, password: $scope.password};
    };

    $scope.errror = "";
    $scope.loginBtnTxt = "Login";

    // begin the login process
    $scope.login = function(){
      // give the user feedback indicating they are logging in and start the loading spinner
      $scope.loginBtnTxt = "Logging in...";
      usSpinnerService.spin('spinner-1');

      // grab the user token
      api.token.tok($scope.getCredentials()).
	$promise.
	then(function(data){

	  // store the user token as in the session
	  $window.sessionStorage.token = data.token;
	  // Authentication flag, will be used in a later version
	  $window.sessionStorage.Authenticated = true;

	  // grab the user detail fro mthe backend
	  // this is mainly for testin and redirection, will be removed in the next version
	  $http.get('/auth/').success(function(data) {
	    token.storeUser(data.user);
	    $window.sessionStorage.user = data.user;
	    $window.sessionStorage.level = data.level;
	    $window.sessionStorage.id = data.id;
	    $location.path('/');
	  });
	})
	.catch(function(data){
      	  // on incorrect username and password
	  // delete any session variable stored
	  delete $window.sessionStorage.token;
	  $window.sessionStorage.Authenticated = false;
	  usSpinnerService.stop('spinner-1');
	  $scope.error = "Access Denied";
	  $scope.loginBtnTxt = "Login";
	});
    };

    // logout the user and delete their session information
    $scope.logout = function(){
      $scope.error = "Logged out";
      $scope.user = undefined;
      token.logout();
      $http.defaults.headers.common.Authorization = '';
      delete $window.sessionStorage.token;
    };

  }])
// This factory was used in a pervious version of the authentication system.
// It used the localStorageService to store the token on the users system, this has been refactored to use the
// browser session instead
  .factory('token', ['$http', '$location', 'localStorageService', function($http, $location, localStorageService) {
    var token = undefined;
    return {
      store: function(tok) {
	localStorageService.cookie.set('token', tok);
	token = tok;
      },
      storeUser: function(user) {
	localStorageService.cookie.set('user', user);
      },
      getUser: function() {
	return localStorageService.cookie.get('user');
      },
      get: function() {
	return localStorageService.cookie.get('token');
      },
      authenticated: function() {
	if (!(localStorageService.cookie.get('token'))) {
	  $location.path("/login");
	}
      },
      logout: function() {
	localStorageService.cookie.clearAll();
	localStorageService.cookie.clearAll();
      }
    };
  }])
  .factory('authInterceptor', function ($rootScope, $q, $window, $location) {
    // authIntercepter is used inbetween http calls to append the Authorization
    // token to the request and also so handle invalid responses
    return {
      request: function (config) {
	config.headers = config.headers || {};
	if ($window.sessionStorage.token) {
          config.headers.Authorization = 'Token ' + $window.sessionStorage.token;
	}
	return config;
      },
      response: function (response) {
	if (response.status === 401) {
	  $location.path('/login');
	}
	return response || $q.when(response);
      }
    };
  });
