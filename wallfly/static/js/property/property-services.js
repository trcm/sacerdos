angular.module('wallfly')
  .factory('Issue', function($resource) {
    return {
      issue: $resource('/issue/:id', {id: '@id'}, {
	create: {method: 'POST'}
      })
    };
  });

