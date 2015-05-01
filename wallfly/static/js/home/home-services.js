angular.module('wallfly')
  .factory('User', ['$resource', function($resource) {
    return $resource('/user/:id', {}, {
      'query': { method: 'GET'}
    });
  }]);
