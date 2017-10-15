API_URL = 'http://10.4.180.124:5000/';
// API_URL = 'http://localhost:5000/';
// API_URL = 'http://52.19.238.148:5000/';

angular.module('starter.services', [])
.factory('GetLatestWakeups', function ($window, $http) {
    return {
      get: function(data) {
        $http.get(API_URL + 'events/', {params: data})
        .then(function success(response) {
          alert(JSON.stringify(response.data));
          window.localStorage.setItem("event", JSON.stringify(response.data));
          alert("Correctly get data!");
          // return response.data;
        }, function error(response) {
          console.log('fail');
          console.log(response);
        });
      },
    };
})
.factory('GetUserData', function ($window, $http) {
    return {
      get: function(user_id) {
        window.localStorage.clear();
        var user_data = window.localStorage['user_data'];
        if (user_data != null) {
          alert('GET USER DATA FROM LOCALSTORAGE!');
          // return user_data;
        }
        alert("user_data = " + user_id);
        $http.get(API_URL + 'users/' + user_id).then(
          function success(response) {
            alert(JSON.stringify(response.data));
            window.localStorage.setItem("user_data", JSON.stringify(response.data));
            alert("Correctly get user data!");
            // return response.data;
          }, function error(response) {
            window.localStorage.setItem("user_data", "");
            alert("data =", JSON.stringify(response.data));
            alert('CHUJ!');
          }
        );
      }
    };
})
.factory('PostEventData', function ($window, $http) {
    return {
      post: function(data){
        $http.post(API_URL + 'events', data)
        .then(function success(response){
          console.log('success');
          console.log(response);
          window.localStorage["event"] = respone.data;
          alert("Pomyślnie zapisano dane!");
          // return response.data;
        }, function error(response){
          console.log('fail');
          console.log(response);
        });
      },
    };
});
