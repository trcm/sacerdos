angular.module('wallfly')
  .controller('HomeController', ['$scope', '$http', '$window', '$location', '$modal', 'resolveProperties', 'Property', 'User', function($scope, $http, $window,  $location, $modal, resolveProperties, Property, User) {
    // use the ReolveProperties method in the application
    $scope.properties = resolveProperties.data;

    if ($scope.properties.prop) {
      $scope.prop = $scope.properties.prop;
      url = "/#/property/" + $scope.prop.id;
      $window.location.href = url;
    }
    
    // router to get all the properties from the database
    // set the user variable
    $scope.user = $window.sessionStorage.user;
    // break properties in numerous arrays to display on the page

    $scope.prop_split = [];

    if (!($scope.properties.prop)) {
      console.log($scope.properties.props.length);
      for (var i = 0; i < $scope.properties.props.length; i = i + 3) {
	console.log(i);
	console.log($scope.properties.props.slice(i, i+3));
	$scope.prop_split.push($scope.properties.props.slice(i, i+3));
      }
    }
    console.log($scope.prop_split);
    
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

	var fd = new FormData();

	if (prop['property_image']) {
	  fd.append("name", prop["name"]);
	  fd.append("address", prop["address"]);
	  fd.append("property_image", prop["property_image"]);
	  fd.append("status", prop["status"]);
	  fd.append("num_tenants", prop["num_tenants"]);
	} else {
	  fd.append("name", prop["name"]);
	  fd.append("address", prop["address"]);
	  fd.append("status", prop["status"]);
	  fd.append("num_tenants", prop["num_tenants"]);
	}

	$http.post("/property/", fd, {
	  transformRequest: angular.identity,
	  headers: {'Content-Type': undefined}
	})
	  .success(function(){
	    $scope.properties = User.query({ id:$window.sessionStorage.id });
	  })
	  .error(function(){
	    alert("Error: Unfortunately, there was a major crash during Property creation.  Please contact your System Administrator");
	  });
      });
    };
    
  }])
  .controller('PropertyCreationController', ['$scope', '$http', '$modalInstance', function($scope, $http, $modalInstance) {
    $scope.prop = {};
    $scope.uploader = {}; 
    $scope.ok = function() {
      $scope.uploader.flow.upload();
      if ($scope.uploader.flow.files.length > 0) {
	$scope.prop.property_image = $scope.uploader.flow.files[0].file;
      } 
      $modalInstance.close($scope.prop);
    };

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };
    
  }]);
