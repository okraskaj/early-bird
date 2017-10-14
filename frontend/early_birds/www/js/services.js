API_ADDRESS = ''
angular.module('starter.services', [])

.factory('Wakeups', function() {
  // Might use a resource here that returns a JSON array

  // Some fake testing data
  // TODO: GET HERE for event wakeups!
  var wakeups = [{
    id: 0,
    name: 'Ben Sparrow',
    lastText: 'You on your way?',
    face: 'img/ben.png'
  }, {
    id: 1,
    name: 'Max Lynx',
    lastText: 'Hey, it\'s me',
    face: 'img/max.png'
  }, {
    id: 2,
    name: 'Adam Bradleyson',
    lastText: 'I should buy a boat',
    face: 'img/adam.jpg'
  }, {
    id: 3,
    name: 'Perry Governor',
    lastText: 'Look at my mukluks!',
    face: 'img/perry.png'
  }, {
    id: 4,
    name: 'Mike Harrington',
    lastText: 'This is wicked good ice cream.',
    face: 'img/mike.png'
  }];

  return {
    all: function() {
      return wakeups;
    },
    remove: function(wakeup) {
      wakeups.splice(wakeups.indexOf(wakeup), 1);
    },
    get: function(id_) {
      for (var i = 0; i < wakeups.length; i++) {
        if (wakeups[i].id === parseInt(id_)) {
          return wakeups[i];
        }
      }
      return null;
    }
  };
})
.factory('PostEventData', function ($window, $http) {
    return {
      post: function(data){
        $http.post(API_ADDRESS + '/events/', data)
        .then(function success(response){
          console.log('success');
          console.log(response);
          window.localStorage["event"] = data;
          alert("Pomyślnie zapisano dane!");
        }, function error(response){
          console.log('fail');
          console.log(response);
        });
      },
    };
});
