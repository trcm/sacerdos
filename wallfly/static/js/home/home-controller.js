angular.module('wallfly')
  .controller('HomeController', ['$scope', '$http', '$window', 'resolveProperties', 'Property',function($scope, $http, $window, resolveProperties, Property) {
    // use the ReolveProperties method in the application
    $scope.properties = resolveProperties.data;
    // router to get all the properties from the database
    // set the user variable
    $scope.user = $window.sessionStorage.user;
    
  }]);
