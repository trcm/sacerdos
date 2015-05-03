angular.module('wallfly')
  .factory('Issue', function($resource) {
    // simple factory to get all issues for a property
    return $resource('/issues/:id', {}, {
      // create: {method: 'POST'},
      query: {method:'GET', isArray:true}
    });
  })
  .factory('Property', function($resource) {
    // factory to get the details of a particular property
    return $resource('/property/:id', {}, {
      query: {method:'GET'}
    });
  });

	   
	   
