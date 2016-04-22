
 function initialize() {
	 var myLatLng = {lat: -24.658143, lng: 25.923074};
  
	 var mapProp = {
    center: myLatLng,
    zoom:6,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);

  var marker = new google.maps.Marker({
	    position: {lat: -24.658143, lng: 25.923074},
	    map: map,
	    title: 'Current location'
	  });

}
google.maps.event.addDomListener(window, 'load', initialize);