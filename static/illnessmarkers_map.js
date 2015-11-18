var map;

function initialize() {
    var mapOptions = {
        zoom: 5
    };
    map = new google.maps.Map(
            document.getElementById('illness-markersmap'),
            mapOptions);


  // Define global infoWindow
  // If you do this inside the loop where you retrieve the json,
  // the windows do not automatically close when a new marker is clicked
  // and you end up with a bunch of windows opened at the same time.
  // What this does is create one infowindow and we replace the content
  // inside for each marker.
    var infoWindow = new google.maps.InfoWindow({
      width: 150
    });

  // Try HTML5 geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = new google.maps.LatLng(
                position.coords.latitude,
                position.coords.longitude);

            var infoWindow = new google.maps.InfoWindow({
                map: map,
                position: pos,
                content: 'You are here!'
            });

            var marker = new google.maps.Marker({
              position: pos,
              map: map,
              title: 'You are here!'
            });

            map.setCenter(pos);
        }, function () {
            handleNoGeolocation(true);
            });
    } else {
                // Browser doesn't support Geolocation
                handleNoGeolocation(false);
            }

        function handleNoGeolocation(errorFlag) {
            var content;

            if (errorFlag) {
                content = "Error: The Geolocation service failed.";
            } else {
                content = "Error: Your browser doesn't support geolocation.";
            }

            var options = {
                map: map,
                position: new google.maps.LatLng(32, -122),
                content: content
            };

            var infoWindow = new google.maps.InfoWindow(options);
            map.setCenter(options.position);
        }

        google.maps.event.addDomListener(window, 'load', initialize);

  // Retrieving the information with AJAX
  $.get('/illnessmarkers.json', function (userreports) {
      // Attach markers to each userreport location in returned JSON
      // JSON looks like:
      // {
      // "1": {
      //      "latitide": "37.7749295",
      //      "longitude": "-122.4194155",
      //      "report": 
      //   },...
      // }
    console.log(userreports);
    var userreport, marker, html;

    for (var key in userreports) {
          userreport = userreports[key];
          console.log(userreport);
          console.log(userreport.latitude);
          console.log(userreport.longitude);
          // Define the marker
         marker = new google.maps.Marker({
              position: new google.maps.LatLng(userreport.latitude, userreport.longitude),
              map: map,
              title: 'Alert: ' + userreport.report,
              icon: '/static/img/pinkpin.png'
          });

          // Define the content of the infoWindow
        html = (
              '<div class="window-content">' +
                  '<p><b>Latitude: </b>' + userreport.latitude + '</p>' +
                  '<p><b>Longitude: </b>' + userreport.longitude + '</p>' +
                  '<p><b>Alert: </b>' + userreport.report + '</p>' +
    
              '</div>');

          // Inside the loop we call bindInfoWindow passing it the marker,
          // map, infoWindow and contentString
        bindInfoWindow(marker, map, infoWindow, html);
      }

  });
}

  // This function is outside the for loop.
  // When a marker is clicked it closes any currently open infowindows
  // Sets the content for the new marker with the content passed through
  // then it open the infoWindow with the new content on the marker that's clicked
  function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
      });
}

google.maps.event.addDomListener(window, 'load', initialize);
