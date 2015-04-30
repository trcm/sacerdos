angular.module('wallfly')
  .controller('HomeController', ['$scope', '$http', '$window', '$modal', 'resolveProperties', 'Property', 'User', function($scope, $http, $window, $modal, resolveProperties, Property, User) {
    // use the ReolveProperties method in the application
    $scope.properties = resolveProperties.data;
    
    if ($scope.properties.prop) {
      $scope.prop = $scope.properties.prop;
    }
    
    // router to get all the properties from the database
    // set the user variable
    $scope.user = $window.sessionStorage.user;
    console.log($window.sessionStorage.id);
    console.log($window.sessionStorage.user);

    // get type of user.  This will decide the includes for the main template
    $scope.agent = false;
    $scope.tenant = false;
    $scope.owner = false;

    switch($scope.properties.user_level) {
    case 1:
      $scope.agent = true;
      break;
    case 2:
      $scope.owner = true;
      break;
    case 3:
      $scope.tenant = true;
      break;
    }

    $scope.newProp = function() {

      var propCreate = $modal.open({
	templateUrl: 'prop-create.html',
	controller: 'PropertyCreationController'
      });

      propCreate.result.then(function(prop) {
	prop['status'] = 1;
	prop['num_tenants'] = 0;
	prop['agent_id'] = $window.sessionStorage.id;
	$http.post("/property/", prop)
	  .success(function() {
	    $scope.properties = User.query({ id:$window.sessionStorage.id });
	  })
	  .error(function() {
	    alert("Error: Unfortunately, there was a major crash during Property creation.  Please contact your System Administrator");
	  });
      });
    };
    
  }])
  .controller('PropertyCreationController', ['$scope', '$http', '$modalInstance', function($scope, $http, $modalInstance) {
    $scope.prop = {};
    
    $scope.ok = function() {
      console.log('close');
      $modalInstance.close($scope.prop);
    };

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };
    
  }]);
