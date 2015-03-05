/**
 * Created by bear on 2/9/15.
 */

// define a map with options
var map = new L.Map('map', {
    scrollWheelZoom: true,
    touchZoom: true,
    doubleClickZoom: true,
    zoomControl: true,
    dragging: true
});

// add base map tile with citation
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// set view center to be the center of Chicago
var center = new L.LatLng(41.8369, -87.6847);
map.setView(center, 10);

// create an empty featureLayer that will be loaded with geojson data
var featureLayer = new L.GeoJSON();

// set the style of featureLayer
var defaultStyle = {
    color: "#2262CC",
    weight: 2,
    opacity: 0.6,
    fillOpacity: 0.1,
    fillColor: "#2262CC"
};

var highlightStyle = {
    color: '#2262CC',
    weight: 3,
    opacity: 0.6,
    fillOpacity: 0.65,
    fillColor: '#2262CC'
};

// define a function to add style to featureLayer
var onEachFeature = function(feature, layer) {
    layer.setStyle(defaultStyle);
    (function(layer, properties) {
        // Create a mouseover event
        layer.on("mouseover", function (e) {
            // Change the style to the highlighted version
            layer.setStyle(highlightStyle);
            // Create a popup with a unique ID linked to this record
            var popup = $("<div></div>", {
                id: "popup-" + properties.ZIP,
                css: {
                    position: "absolute",
                    bottom: "85px",
                    left: "50px",
                    zIndex: 1002,
                    backgroundColor: "white",
                    padding: "8px",
                    border: "1px solid #ccc"
                }
            });
            // Insert a headline into that popup
            var hed = $("<div></div>", {
                text: "Area Zip: " + properties.ZIP,
                css: {fontSize: "16px", marginBottom: "3px"}
            }).appendTo(popup);
            // Add the popup to the map
            popup.appendTo("#map");
        });
        // Create a mouseout event that undoes the mouseover changes
        layer.on("mouseout", function (e) {
            // Start by reverting the style back
            layer.setStyle(defaultStyle);
            // And then destroying the popup
            $("#popup-" + properties.ZIP).remove();
        });

        layer.on('click',function(e) {
            $("#zip").text(properties.ZIP);
            $.post("/projects/BusinessLicense",
                {post_zip: properties.ZIP},
                function( data ) {
                    var arr = $.map(data, function(el){return el;});
                    $("#searchResult").html(arr[0]);
                    $("#recommendedLicense").html(arr[1]);
                });
        });

        // Close the "anonymous" wrapper function, and call it while passing
        // in the variables necessary to make the events work the way we want.
    })(layer, feature.properties);
};

// add geojson data and style to featureLayer
var featureLayer = L.geoJson(boundaries, {
    onEachFeature: onEachFeature
});

// add the featureLayer to map (on top of base map tile)
map.addLayer(featureLayer);
