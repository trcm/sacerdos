angular.module('wallfly')
  .controller('PropertyController', ['uiCalendarConfig', '$scope', '$http', '$window', '$modal', 'lodash', 'resolvedProperty', 'Property', 'Issue', 'Lightbox', 'issues', function(uiCalendarConfig, $scope, $http, $window, $modal, lodash, resolvedProperty, Property, Issue, Lightbox, issues) {


    $scope.user = $window.sessionStorage.user;
    $scope.issues = issues.data;
    $scope.issuesSafe = $scope.issues;
    $scope.newIssue = {};
    $scope.prop = resolvedProperty.data;
    $scope.issue = {};

    $scope.currIssues = lodash.filter($scope.issues, {"resolved" : 0});
    console.log($scope.currIssues.length);
    
    //sets the ui for the calendar app
    $scope.uiConfig = {
      calendar:{
        height:450,
        aspectRatio:1.5,
        editable: true,
        header:{
          left: 'month basicWeek basicDay agendaWeek agendaDay',
          center: 'title',
          right: 'today prev,next'
        },
        dayClick: $scope.alertEventOnClick,
	eventDrop: $scope.alertOnDrop,
        eventResize: $scope.alertOnResize
      }
    };
    // gets variables that represent the current day, month and year
    // as well as todays date
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    /* event source that contains custom events on the scope */
    $scope.events = [
      {title: 'All Day Event',start: new Date(y, m, 1)},
      {title: 'Long Event',start: new Date(y, m, d - 5),end: new Date(y, m, d - 2)},
      {id: 999,title: 'Repeating Event',start: new Date(y, m, d - 3, 16, 0),allDay: false},
      {id: 999,title: 'Repeating Event',start: new Date(y, m, d + 4, 16, 0),allDay: false},
      {title: 'Birthday Party',start: new Date(y, m, d + 1, 19, 0),end: new Date(y, m, d + 1, 22, 30),allDay: false},
      {title: 'Click for Google',start: new Date(y, m, 28),end: new Date(y, m, 29),url: 'http://google.com/'}
    ];

    $scope.eventSources = [$scope.events];



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

    // open a modal with the lightbox image inside it
    $scope.openLightboxModal = function (index) {
      Lightbox.openModal(index);
    };
    // Acutally calls the http request to save a new issue in the database
    $scope.saveIssue = function(id) {
      var u = '/issue/' + id;
      $scope.newIssue.property_id = id;
      console.log(id, $scope.newIssue);

      // add issue with image

      var fd = new FormData();

      if ($scope.newIssue['image']) {
	fd.append("severity", $scope.newIssue["severity"]);
	fd.append("description", $scope.newIssue["description"]);
	fd.append("image", $scope.newIssue["image"]);
	fd.append("property_id", $scope.newIssue.property_id);
      } else {
	fd.append("severity", $scope.newIssue["severity"]);
	fd.append("description", $scope.newIssue["description"]);
	fd.append("property_id", $scope.newIssue.property_id);
      }
      console.log(fd);
      $http.post(u, fd, {
	transformRequest: angular.identity,
	headers: {'Content-Type': undefined}
      })
	.success(function() {
	  $scope.prop = Property.query({id: id});
	  $scope.issues = Issue.query({id: id});
	  $scope.currIssues = lodash.filter($scope.issues, {"resolved" : 0});
	})
	.error(function(data) {
	  alert(data);
	});

      // save the new issue then grab the updated issues and property details
      // $http.post(u, $scope.newIssue)
      // 	.success(function() {
      // 	  $scope.prop = Property.query({id: id});
      // 	  $scope.issues = Issue.query({id: id});
      // 	})
      // 	.error(function(data) {
      // 	  alert(data);
      // 	});
    };

    // Change the issues resolution status to resolved
    $scope.resolveIssue = function(issue) {
      var id = $scope.prop.id;
      $http.put("/issue/" + issue.id, {"resolved" : 1})
	.success(function(data) {
	  // update the issue to resolved and grab the updated issues and property details
	  $scope.prop = Property.query({id: id});
	  $scope.issues = Issue.query({id: id});
	  $scope.currIssues = lodash.filter($scope.issues, {"resolved" : 0});
	});
    };

    // delete an issue from the database
    $scope.deleteIssue = function(issue) {
      var id = $scope.prop.id;
      $http.delete('/issue/' + issue.id).
	success(function(data) {
	  $scope.prop = Property.query({id: $scope.prop.id});
	  $scope.issues = Issue.query({id: id});
	  $scope.currIssues = lodash.filter($scope.issues, {"resolved" : 0});
	});
    };

  }])
  .controller('IssueCreateController', ['$scope', '$http', '$modalInstance', function($scope, $http, $modalInstance) {
    // handles the modal for the issue creation form
    $scope.issue = {};
    $scope.uploader = {};
    $scope.options = [
      { label: 'Minor', value: 1 },
      { label: 'Moderate', value: 2 },
      { label: 'Severe', value: 3 }
    ];

    $scope.ok = function() {
      // update the severity value to be a number insteal of the label name
      $scope.issue.severity = $scope.issue.severity.value;
      $scope.uploader.flow.upload();
      if ($scope.uploader.flow.files.length > 0) {
	$scope.issue.image = $scope.uploader.flow.files[0].file;
      }
      $modalInstance.close($scope.issue);
    };

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };

  }]);
