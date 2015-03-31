angular.module('wallfly')
  .controller('HomeController', ['$scope', '$http', 'resolveProperties', 'Property',
				 function($scope, $http, resolveProperties, Property) {

				   $scope.properties = resolveProperties.data;

				   $scope.test = "test";
				 }]);
