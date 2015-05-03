angular.module('wallfly')
  .controller('navbarController', ['$scope', '$http', '$location', '$window', function($scope, $http, $location, $window) {
    // get type of user.  This will decide the includes for the main template
    $scope.agent = false;
    $scope.tenant = false;
    $scope.owner = false;

    var level = $window.sessionStorage.level;
    
    if (level == 1) {
      $scope.agent = true;
    } else if (level == 2) {
      $scope.owner = true;
    } else if (level == 3) {
      $scope.tenant = true;
    } else {
      $scope.other = true;
    }
    
    console.log('post switch');
    $scope.user = $window.sessionStorage.user;

    $scope.logout = function(){
      $scope.error = "Logged out";
      // token.logout();
      $http.defaults.headers.common.Authorization = '';
      delete $window.sessionStorage.token;
      delete $window.sessionStorage.user;
      delete $window.sessionStorage.level;
      $location.path('/login');
    };
  }]);
