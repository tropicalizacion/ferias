// Get the user's location

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(passPosition);
        navigator.geolocation.watchPosition(passPosition);
    } else {
        alert("El navegador no es compatible con la funcionalidad de geolocalización para hacer una búsqueda de ferias cerca de su ubicación actual.");
    }
}

function passPosition(position) {
    var longitude = position.coords.longitude;
    var latitude = position.coords.latitude;

    console.log("Cerca de mí");
    console.log("Latitud: " + latitude);
    console.log("Longitud: " + longitude);

    document.getElementById("my-longitude").value = longitude;
    document.getElementById("my-latitude").value = latitude;
}

// Autocomplete for the location input

function getAutocompleteSuggestions() {
    const input = document.getElementById("some-place").value;
    const service = new google.maps.places.AutocompleteService();
    const options = { types: ["geocode"] };
    service.getPlacePredictions({ input, options }, displaySuggestions);
}

function displaySuggestions(predictions, status) {
    if (status !== google.maps.places.PlacesServiceStatus.OK) {
        console.error("Error en mostrar sugerencias de lugares: ", status);
        return;
    }

    const suggestedPlacesList = document.getElementById("suggested-places");
    suggestedPlacesList.innerHTML = "";

    predictions.forEach(prediction => {
        const placeName = prediction.description;
        const listItem = document.createElement("li");
        listItem.textContent = placeName;
        listItem.addEventListener("click", function () {
            document.getElementById("some-place").value = placeName;
            suggestedPlacesList.innerHTML = "";
            geocodeSelectedPlace(placeName);
        });

        suggestedPlacesList.appendChild(listItem);
    });
}

// Geocode the selected place

function geocodeSelectedPlace(placeName) {

    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: placeName }, function (results, status) {
        if (status === "OK") {
            const latitude = results[0].geometry.location.lat();
            const longitude = results[0].geometry.location.lng();

            console.log("Cerca de: " + placeName);
            console.log("Latitud: " + latitude);
            console.log("Longitud: " + longitude);

            document.getElementById("some-latitude").value = latitude;
            document.getElementById("some-longitude").value = longitude;
        } else {
            console.error("Error al conectarse con el API de Google: " + status);
        }
    });
}

// Build the query string for the search form

$(document).ready(function () {

    makeQueryString();

    $('input[name="location"], select[name="day"], input[name="size"], input[name="size_s"], input[name="size_m"], input[name="size_l"], input[name="size_xl"], input[name="fairground"], input[name="indoor"], input[name="parking"], input[name="food"], input[name="drinks"], input[name="handicrafts"], input[name="butcher"], input[name="dairy"], input[name="seafood"], input[name="garden_centre"], input[name="florist"]').change(function () {
        makeQueryString();
    });

    function makeQueryString() {
        var locationValue = $('input[name="location"]:checked').val();
        var dayValue = $("#day").val();
        var sizeValue = $('input[name="size"]:checked').val();
        var sizeSValue = $('#size-s').prop('checked') ? $('#size-s').val() : '';
        var sizeMValue = $('#size-m').prop('checked') ? $('#size-m').val() : '';
        var sizeLValue = $('#size-l').prop('checked') ? $('#size-l').val() : '';
        var sizeXLValue = $('#size-xl').prop('checked') ? $('#size-xl').val() : '';
        var fairgroundValue = $('input[name="fairground"]:checked').val();
        var indoorValue = $('input[name="indoor"]:checked').val();
        var parkingValue = $('input[name="parking"]:checked').val();
        var foodValue = $('input[name="food"]:checked').val();
        var drinksValue = $('input[name="drinks"]:checked').val();
        var handicraftsValue = $('input[name="handicrafts"]:checked').val();
        var butcherValue = $('input[name="butcher"]:checked').val();
        var dairyValue = $('input[name="dairy"]:checked').val();
        var seafoodValue = $('input[name="seafood"]:checked').val();
        var gardenCentreValue = $('input[name="garden_centre"]:checked').val();
        var floristValue = $('input[name="florist"]:checked').val();

        var statusText = "";

        // Location
        if (locationValue === "my_location") {
            statusText += "cerca de mí";
        } else if (locationValue === "some_location") {
            const placeNameText = document.getElementById("some-place").value;
            statusText += "cerca de " + placeNameText;
        } else if (locationValue === "any_location") {
            statusText += "en cualquier lugar del país";
        }

        // Day of the week
        if (dayValue === "Mo") {
            statusText += ", abierta los lunes";
        } else if (dayValue === "Tu") {
            statusText += ", abierta los martes";
        } else if (dayValue === "We") {
            statusText += ", abierta los miércoles";
        } else if (dayValue === "Th") {
            statusText += ", abierta los jueves";
        } else if (dayValue === "Fr") {
            statusText += ", abierta los viernes";
        } else if (dayValue === "Sa") {
            statusText += ", abierta los sábados";
        } else if (dayValue === "Su") {
            statusText += ", abierta los domingos";
        } else if (dayValue === "any_day") {
            statusText += ", abierta cualquier día";
        }

        // Size
        if (sizeValue === "any_size") {
            statusText += ", de cualquier tamaño";
        } else if (sizeValue === "some_size") {
            statusText += ", de tamaño específico";
        }

        // Infrastucture
        if (fairgroundValue === "True") {
            statusText += ", con campo ferial";
        }
        if (indoorValue === "True") {
            statusText += ", bajo techo";
        }
        if (parkingValue === "surface") {
            statusText += ", con estacionamiento";
        }

        // Amenities
        if (foodValue === "True") {
            statusText += ", con comidas";
        }
        if (drinksValue === "True") {
            statusText += ", con bebidas y jugos";
        }
        if (handicraftsValue === "True") {
            statusText += ", con artesanías";
        }
        if (butcherValue === "True") {
            statusText += ", con carnicería";
        }
        if (dairyValue === "True") {
            statusText += ", con productos lácteos";
        }
        if (seafoodValue === "True") {
            statusText += ", con pescadería";
        }
        if (gardenCentreValue === "True") {
            statusText += ", con venta de plantas";
        }
        if (floristValue === "True") {
            statusText += ", con floristería";
        }

        $("#status").text(statusText);
        $("#query-text").val(statusText);
    }
});

// Disable the "some place" input if the user selects "any location" or "my location"

var anyLocation = document.getElementById("any-location");
var myLocation = document.getElementById("my-location");
var someLocation = document.getElementById("some-location");
var somePlace = document.getElementById("some-place");

anyLocation.addEventListener("change", function () {
    if (anyLocation.checked) {
        somePlace.disabled = true;
    }
});

myLocation.addEventListener("change", function () {
    if (myLocation.checked) {
        somePlace.disabled = true;
    }
});

someLocation.addEventListener("change", function () {
    if (someLocation.checked) {
        somePlace.disabled = false;
        somePlace.focus();
    }
});

// Disable the size checkboxes if the user selects "any size"

var anySize = document.getElementById("any-size");
var someSize = document.getElementById("some-size");
var sizeS = document.getElementById("size-s");
var sizeM = document.getElementById("size-m");
var sizeL = document.getElementById("size-l");
var sizeXL = document.getElementById("size-xl");

anySize.addEventListener("change", function () {
    if (anySize.checked) {
        sizeS.disabled = true;
        sizeM.disabled = true;
        sizeL.disabled = true;
        sizeXL.disabled = true;
    }
});

someSize.addEventListener("change", function () {
    if (someSize.checked) {
        sizeS.disabled = false;
        sizeM.disabled = false;
        sizeL.disabled = false;
        sizeXL.disabled = false;
    }
});
