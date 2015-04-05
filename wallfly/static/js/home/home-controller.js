angular.module('wallfly')
  .controller('HomeController', ['$scope', '$http', 'resolveProperties', 'Property',
				 function($scope, $http, resolveProperties, Property) {

				   // use the ReolveProperties method in the application
				   // router to get all the properties from the database
				   $scope.properties = resolveProperties.data;
				   console.log($scope.properties);
				   $scope.test = "test";
				 }]);
