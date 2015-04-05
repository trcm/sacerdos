angular.module('wallfly')
  .factory('Property', ['$resource', function($resource) {
    return $resource('/property/', {}, {
      'query': { method: 'GET', isArray: true}
    });
  }]);
