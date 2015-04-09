angular.module('wallfly')
  .controller('PropertyController', ['$scope', '$http', 'resolvedProperty', function($scope, $http, resolvedProperty) {

    $scope.test = "test" ;
    $scope.prop = resolvedProperty.data;

    $scope.createIssue = function(id) {

      
      
    };
    
  }]);
