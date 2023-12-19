if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
}else{
    console.error("Geolocation is not supported")
}
function successCallback(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    document.getElementById("latitude").innerHTML = latitude;
    document.getElementById("longitude").innerHTML = longitude;
    var formData = new FormData();
    formData.append("latitude", latitude);
    formData.append("longitude", longitude);
    //var latitude = position.coords.latitude;
    //var longitude = position.coords.longitude;
    //var data ={
      //  "latitude": latitude,
       // "longitude": longitude
    //};
   
    fetch("/register/save_location", {
        method: "POST",
        mode: "cors", 
        //headers: {
           // 'Content-Type': 'application/json'
        //},
        body: formData//JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
       
    })
    .catch(error => {
        console.error("Error:", error);
    });

   
    //document.getElementById("latitude").innerHTML = latitude;
    //document.getElementById("longitude").innerHTML = longitude;
}

function errorCallback() {
    alert("Geolocation is not available in this browser.");
};
