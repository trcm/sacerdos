angular.module('wallfly')
  .controller('navbarController', ['$scope', '$http', '$location', '$window', function($scope, $http, $location, $window) {
    $scope.user = $window.sessionStorage.user;
    console.log('user', $scope.user);
    $scope.logout = function(){
      $scope.error = "Logged out";
      // token.logout();
      $http.defaults.headers.common.Authorization = '';
      delete $window.sessionStorage.token;
      delete $window.sessionStorage.user;
      $location.path('/login');
    };
  }]);
