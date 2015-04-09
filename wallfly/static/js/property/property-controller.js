angular.module('wallfly')
  .controller('PropertyController', ['$scope', '$http', '$modal', 'resolvedProperty', 'Issue', 'issues', function($scope, $http, $modal, resolvedProperty, Issue, issues) {

    $scope.issues = issues.data;
    $scope.newIssue = {};
    $scope.prop = resolvedProperty.data;

    console.log($scope.prop);

    $scope.saveIssue = function(id) {
      var u = '/issue/' + id;
      $scope.newIssue.property_id = id.id;
      console.log(id, $scope.newIssue);
      $http({
	method: 'POST',
	url: u,
	data: $scope.newIssue}).success(function(data) {
	  console.log(data);
	});
    };

    // opens the modal with the issue creation form
    $scope.createIssue = function(id) {
      console.log(id);
      var issueCreate = $modal.open({
	templateUrl: 'issue-create.html',
	controller: 'IssueCreateController'
      });

      issueCreate.result.then(function(entity) {
	$scope.newIssue = entity;
	console.log("property id " + id.id);
	$scope.saveIssue(id.id);
      });
    };
  }])
  .controller('IssueCreateController', ['$scope', '$http', '$modalInstance', function($scope, $http, $modalInstance) {

    $scope.issue = {};
    
    $scope.ok = function() {
      $modalInstance.close($scope.issue);
    };

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };
    
  }]);
