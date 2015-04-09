angular.module('wallfly')
  .controller('PropertyController', ['$scope', '$http', '$modal', 'resolvedProperty', 'Property', 'Issue', 'issues', function($scope, $http, $modal, resolvedProperty, Property, Issue, issues) {

    $scope.issues = issues.data;
    $scope.newIssue = {};
    $scope.prop = resolvedProperty.data;
    $scope.issue = {};

    $scope.options = [
      { label: 'Minor', value: 1 },
      { label: 'Moderate', value: 2 },
      { label: 'Severe', value: 3 }
    ];
    console.log($scope.options);
    console.log($scope.prop);

    $scope.saveIssue = function(id) {
      var u = '/issue/' + id;
      $scope.newIssue.property_id = id.id;
      console.log(id, $scope.newIssue);
      $http.post(u, $scope.newIssue)
      	.success(function() {
	  $scope.prop = Property.query({id: id});
	  $scope.issues = Issue.query({id: id});
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
	console.log(entity);
	console.log("property id " + id.id);
	$scope.saveIssue(id.id);
      });
    };

    $scope.deleteIssue = function(issue) {
      var id = $scope.prop.id;
      $http.delete('/issue/' + issue.id).
	success(function(data) {
	  $scope.prop = Property.query({id: $scope.prop.id});
	  $scope.issues = Issue.query({id: id});
	});
    };
    
  }])
  .controller('IssueCreateController', ['$scope', '$http', '$modalInstance', function($scope, $http, $modalInstance) {

    $scope.issue = {};

    $scope.options = [
      { label: 'Minor', value: 1 },
      { label: 'Moderate', value: 2 },
      { label: 'Severe', value: 3 }
    ];
    
    $scope.ok = function() {
      $scope.issue.severity = $scope.issue.severity.value;
      $modalInstance.close($scope.issue);
    };

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };
    
  }]);
