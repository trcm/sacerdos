angular.module('wallfly')
  .controller('PropertyController', ['$scope', '$http', '$window', '$modal', 'resolvedProperty', 'Property', 'Issue', 'issues', function($scope, $http, $window, $modal, resolvedProperty, Property, Issue, issues) {

    
    $scope.user = $window.sessionStorage.user;
    $scope.issues = issues.data;
    $scope.issuesSafe = $scope.issues;
    $scope.newIssue = {};
    $scope.prop = resolvedProperty.data;
    $scope.issue = {};


    // opens the modal with the issue creation form
    // once the issue creation form has been completed, saves the issue in the
    // database
    $scope.createIssue = function(id) {
      var issueCreate = $modal.open({
	templateUrl: 'issue-create.html',
	controller: 'IssueCreateController'
      });

      // when the modal is closed, get the data from its form and create a new issue
      issueCreate.result.then(function(entity) {
	$scope.newIssue = entity;
	console.log(entity);
	console.log("property id " + id.id);
	$scope.saveIssue(id.id);
      });
    };
    
    // Acutally calls the http request to save a new issue in the database
    $scope.saveIssue = function(id) {
      var u = '/issue/' + id;
      $scope.newIssue.property_id = id.id;
      console.log(id, $scope.newIssue);
      // save the new issue then grab the updated issues and property details
      $http.post(u, $scope.newIssue)
      	.success(function() {
	  $scope.prop = Property.query({id: id});
	  $scope.issues = Issue.query({id: id});
      	})
	.error(function(data) {
	  alert(data);
	});
    };

    // Change the issues resolution status to resolved
    $scope.resolveIssue = function(issue) {
      var id = $scope.prop.id;
      $http.put("/issue/" + issue.id, {"resolved" : 1})
	.success(function(data) {
	  // update the issue to resolved and grab the updated issues and property details
	  $scope.prop = Property.query({id: id});
	  $scope.issues = Issue.query({id: id});
	});
    };
    
    // delete an issue from the database
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
    // handles the modal for the issue creation form
    $scope.issue = {};
    $scope.options = [
      { label: 'Minor', value: 1 },
      { label: 'Moderate', value: 2 },
      { label: 'Severe', value: 3 }
    ];
    
    $scope.ok = function() {
      // update the severity value to be a number insteal of the label name
      $scope.issue.severity = $scope.issue.severity.value;
      $modalInstance.close($scope.issue);
    };

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };
    
  }]);
