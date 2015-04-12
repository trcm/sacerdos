angular.module('wallfly')
    .controller('CalController', function($scope) {
	$scope.uiConfig = {
		calendar:{
        	height: 450,
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
    $scope.eventSources = [];
    
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    
    
    });
