const HOME = window.location.href;

function updateTextInput(val) {
    document.getElementById('textInput').value=val; 
}

function resolveDistance(userLocation, placeData){
    var lat1 = placeData.latitude;
    var lat2 = userLocation.latitude;
    var lon1 = placeData.longitude;
    var lon2 = userLocation.longitude;

    const R = 6371e3; // metres
    const φ1 = lat1 * Math.PI/180; // φ, λ in radians
    const φ2 = lat2 * Math.PI/180;
    const Δφ = (lat2-lat1) * Math.PI/180;
    const Δλ = (lon2-lon1) * Math.PI/180;

    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
            Math.cos(φ1) * Math.cos(φ2) *
            Math.sin(Δλ/2) * Math.sin(Δλ/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    const d = R * c; // in metres
    return Math.round(d/1000);
}

function buttonOnClick(){
    var val = document.getElementById('customRange2').value;
    fetch(HOME + '/user_ip')
        .then((response) => response.json())
        .then((user_data) => {
            fetch(HOME + 'get_places/' + val + "/" + user_data.localisation.latitude + "/" + user_data.localisation.longitude)
                .then((response) => response.json())
                .then((data) => {
                    if ("db_response" in data){
                        if (data.db_response.length) {
                            var table = "<h3>List of found places:</h3><br>";
                            for(var element = 0; element < data.db_response.length; element++) {
                                table += "<p>" + data.db_response[element].place_name + " " + data.db_response[element].type + ", "+ resolveDistance(user_data.localisation, data.db_response[element]) +"km away from you" + "</p>";
                            }
                        }else{
                            var table = "<h3>No places found :(</h3><br>";
                        }
                    }else{
                        var table = "<h3>Could not resolve user's localisation</h3><br>";
                    }
                    document.getElementById('content').innerHTML = table;
                });
        });
}