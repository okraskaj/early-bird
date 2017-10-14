angular.module('starter.controllers', ['ngCordova'])

.controller('InfoCtrl', function($scope) {})

.controller('WakeupsCtrl', function($scope, GetLatestWakeups, GetLatestWakeups) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.user_data = angular.fromJson(window.localStorage["personal_data"]);
  $scope.wakeups = GetLatestWakeups.get({
    user_id: user_data.id,
    event_id: user_data.event_id,
  });
})

.controller('WakeupDetailCtrl', function($scope, $stateParams, Wakeups) {
  $scope.wakeup = Wakeups.get($stateParams.wakeupId);
})

.controller('PhotoDetailCtrl', function($scope, $stateParams, Wakeups) {

  function uploadSuccess(response) {
        alert(response);
        var data = JSON.parse(response.response);
        /*
        var clip_location = data.clip_location;
        var text = data.text;
        console.log(text, clip_location);
        document.getElementById("loader").setAttribute("class", "");
        $state.go('video', {text: text, clip_location: "http://172.16.102.47:7744/" + clip_location});
        */
    };

    function uploadError(error) {
        alert("upload error");
        console.log(error);
        // document.getElementById("loader").setAttribute("class", "");
    }

  function captureSuccess(mediaFiles) {
    console.log("capture success");
    var file = mediaFiles[0];
    var options = new FileUploadOptions();
    options.fileKey = "image";
    options.fileName = "image.jpeg";
    options.mimeType = "image/jpeg";
    options.chunkedMode = false;
    var ft = new FileTransfer();
    ft.upload(
        file.fullPath,
        encodeURI("http://10.4.180.171:5000/users/e96aa001cec042588475ca861694c5f8/photos"),
        uploadSuccess,
        uploadError,
        options
    );
    document.getElementById("loader").setAttribute("class", "visible");
    alert(mediaFiles);
  };

  function captureError(error) {
    alert(error);
  };

  $scope.record = function() {
    console.log("lets do photo started...");
    // var options = {limit: 1};
    navigator.device.capture.captureImage(captureSuccess, captureError);
  }
})

.controller('SettingsCtrl', function($scope, $http) {
  $scope.user_id = angular.fromJson(window.localStorage["personalData"]);
  $scope.mail = {};
  $scope.event = {
    name: undefined,
    wakeup_hour: 7,
    punish_points: 3,
    main_punish: 'Buy coffee for everyone.',
    punishments: [],
    dec_number: 15,
    interval: 7,
    users: [],
  };
  $scope.current_rule = {
    typ: 'punishment',
    points: 1,
    margin: 0,
    days_in_row: 0
  }

  $scope.add_punishment = function() {
    $scope.event.punishments.push(
      Object.assign({}, $scope.current_rule)
    );
  };

  $scope.remove_punishment = function(ind) {
    $scope.event.punishments.splice(ind, 1);
  };

  $scope.add_email = function() {
    if ($scope.mail.val != null) {
      $scope.event.users.push($scope.mail.val);
    }
  };

  $scope.remove_email = function(ind) {
    $scope.event.users.splice(ind, 1);
  };

  $scope.submit_form = function (is_valid) {
    var tmp = Object.assign({}, $scope.event);
    tmp['user_id'] = $scope.user_id;
    tmp['rules'] = $scope.event.punishments;
    var event_data_json = angular.toJson(tmp, true);
    $scope.post_event_data = PostEventData.post(event_data_json);

  };

});
