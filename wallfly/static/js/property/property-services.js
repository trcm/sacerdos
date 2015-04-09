angular.module('wallfly')
  .factory('Issue', function($resource) {
    return $resource('/issues/:id', {}, {
      // create: {method: 'POST'},
      query: {method:'GET', isArray:true}
    });
  })
  .factory('Property', function($resource) {
    return $resource('/property/:id', {}, {
      query: {method:'GET'}
    });
  });

	   
	   
