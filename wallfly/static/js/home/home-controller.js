angular.module('wallfly')
  .controller('HomeController', ['$scope', '$http', '$window', 'resolveProperties', 'Property', function($scope, $http, $window, resolveProperties, Property) {
    // use the ReolveProperties method in the application
    $scope.properties = resolveProperties.data;
    
    if ($scope.properties.prop) {
      $scope.prop = $scope.properties.prop;
    }
    
    // router to get all the properties from the database
    // set the user variable
    $scope.user = $window.sessionStorage.user;
    console.log($window.sessionStorage.user);

    // get type of user.  This will decide the includes for the main template
    $scope.agent = False;
    $scope.tenant = False;
    $scope.owner = False;

    
    
  }]);
