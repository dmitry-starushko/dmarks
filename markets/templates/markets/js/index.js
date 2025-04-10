{% load thumbnail %}

var view = new ol.View({
       projection: 'EPSG:4326',
       center: [37.902, 48.038],
       zoom:11,
       maxZoom:17,
       minZoom:8
});

var map = new ol.Map({
      layers: [
        new ol.layer.Tile({
          source: new ol.source.XYZ({
             url: 'https://opensm.donmarkets.ru/ru/{z}/{x}/{y}.png',
             attributions: '<a href="https://donmarkets.ru">Рынки Донбасса</a> карты' ,
             crossOrigin: null
          })
       }),
     ],
     target: 'map',
     controls: ol.control.defaults.defaults({
        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
          collapsible: false
        })
     }),
    view: view
 });

// Marks

// Popup
const mappopup = document.getElementById("popup-market-card").cloneNode(true);
const mappopupOverlay = new ol.Overlay({
 element: mappopup,
 positioning: "bottom-center",
 offset: [0, -25],
});
map.addOverlay(mappopupOverlay);

 map.addEventListener("click", function (event) {
     hide(mappopup, 200);
     document.querySelectorAll('.map-marker').forEach(e => e.classList.remove('active'));
 });

function createMarker(position, title, text, img, url, id) {
 const marker = document.getElementById("map-marker").cloneNode(true);
 marker.name = 'mrk' + id;
 marker.title = title;
 const markerOverlay = new ol.Overlay({
   element: marker,
   positioning: "bottom-center",
   position: position,
 });
 map.addOverlay(markerOverlay);

 marker.addEventListener("click", function (event) {
   if (!event.target.classList.contains('toggle')) return;
	// Prevent default link behavior
	event.preventDefault();
    document.querySelectorAll('.map-marker').forEach(e => e.classList.remove('active'));
	mappopupOverlay.setPosition(position);
    mappopup.querySelector("#popup-market-card-title").textContent = title;
    mappopup.querySelector("#popup-market-card-title").title = title;
    mappopup.querySelector("#popup-market-card-text").textContent = text;
    mappopup.querySelector("#popup-market-img").setAttribute('src', img);
    mappopup.querySelector("#popup-market-url").setAttribute('href', url);
    mappopup.querySelector("#popup-market-url-icon").setAttribute('href', url);
    show(mappopup, 200);
    view.setZoom(15);
    view.setCenter(mappopupOverlay.getPosition());
    event.target.classList.add("active");
 });
}

// Show an element
var show = function (elem, timing) {

	// Get the transition timing
	timing = timing ? timing : 350;

	// Get the natural height of the element
	var getHeight = function () {
		elem.style.display = 'block'; // Make it visible
		var height = elem.scrollHeight + 'px'; // Get it's height
		elem.style.display = ''; //  Hide it again
		return height;
	};

	var height = getHeight(); // Get the natural height
	elem.style.height = height; // Update the max-height

	window.setTimeout(function () {
		elem.style.height = '';
	}, timing);

};

// Hide an element
var hide = function (elem, timing) {

	// Get the transition timing
	timing = timing ? timing : 350;

	// Set the height back to 0
	window.setTimeout(function () {
		elem.style.height = '0px';
	}, 50);

	// When the transition is complete, hide it
	window.setTimeout(function () {
		elem.style.display = 'none'; //  Hide it again
	}, timing);
};

var toggle = function (elem, timing) {
	if (elem.classList.contains('is-visible')) {
		hide(elem, timing);
		return;
	}
	show(elem, timing);
};

{% for item in items %}
createMarker(["{{item.lng}}".replace(',', '.'), "{{item.lat}}".replace(',', '.')],
            '{{item.mk_full_name}}',
            '{{item.mk_full_address}}',
            '{% thumbnail item.image 100x100 crop %}',
            "{% url 'markets:market_details' mpk=item.id show='info' %}",
            '{{item.id}}');
{% endfor %}

if({{iid}}) {
    document.querySelector('[name="mrk{{iid}}"]').click();
}
