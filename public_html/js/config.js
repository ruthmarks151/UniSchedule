TimTab.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'templates/home.html',
        controller: 'HomeCtrl'
      }).
      when('/TimetableBuilder', {
        templateUrl: 'templates/timetablebuilder.html',
        controller: 'TimetableCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);