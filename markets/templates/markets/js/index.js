{% load thumbnail %}

var markerLayer = new ol.layer.Vector({
    title: "MarketPoint1",
    visible: true,
    minResolution: 5,
    source: new ol.source.Vector({
            format: new ol.format.GeoJSON(),
            url: 'https://maps.donmarkets.ru/index.php?r=api/getmarkets'/*,
            crossOrigin: null*/
          }),
    style: function(feature) {
            style = new ol.style.Style({
            image: new ol.style.Icon({
                src: 'https://maps.donmarkets.ru/imgs/baloon.png'
            }),
            /*fill: new ol.style.Fill({
              color: '#eeeeee',
            }),
            stroke: new ol.style.Stroke({
              color: 'rgba(255, 255, 255, 0.7)',
              width: 2,
            }),*/
          });
          return style;
        }
});

var markerLayerText = new ol.layer.Vector({
    title: "MarketPointText",
    visible: true,
    maxResolution: 5,
    //source: vectorSource,
    source: new ol.source.Vector({
            format: new ol.format.GeoJSON(),
            url: 'https://maps.donmarkets.ru/index.php?r=api/getmarkets',
            crossOrigin: "anonymous"
          }),
    style: function(feature) {
{% comment %}
//            style = style = new ol.style.Style({
//            image: new ol.style.RegularShape({
//                fill: new ol.style.Fill({
//                  color: '#3399CC'
//                }),
//                stroke: new ol.style.Stroke({
//                  color: '#fff'
//                }),
//                radius: 60 / Math.SQRT2,
//                radius2: 30,
//                points: 4,
//                angle: 0,
//                scale: [1, 0.5],
//              }),
//            text: new ol.style.Text({
//                text: feature.get('label'),
//                fill: new ol.style.Fill({
//                  color: '#fff'
//                })
//              })
//          });
//          return style;
{% endcomment %}
            style = new ol.style.Style({
            image: new ol.style.RegularShape({
                fill: new ol.style.Fill({
                  //color: '#3399CC'
                  color: 'rgba(51, 153, 204, 0.5)'
                }),
                stroke: new ol.style.Stroke({
                  color: '#fff',
                  width: 1
                }),
                //radius: 60 / Math.SQRT2,
                radius: 50 / Math.SQRT2,
                radius2: 50,
                points: 4,
                angle: 0,
                scale: [1, 0.5],
              }),
//            image: new ol.style.Icon({
//                src: '/imgs/baloon.png'
//            }),
            text: new ol.style.Text({
                text: feature.get('label').replace("(","\n("),
                font: 'bold 11px Arial, Verdana, Helvetica, sans-serif',
                fill: new ol.style.Fill({
                  color: '#FFF'
                }),
                stroke: new ol.style.Stroke({
                  color: '#848484',
                  lineCap: 'round',
                  lineJoin: 'round',
                  width: 8,
                }),
              })
          });
          return style;
        }
});


// Add vector layer with a feature and a style using an icon
var vectorLayer = new ol.layer.Vector({
source: new ol.source.Vector({
  features: [
    new ol.Feature({
      geometry: new ol.geom.Point(
        ol.proj.fromLonLat([37.902, 48.038])
      ),
      name: 'The center of the world'
    })
  ]
}),
style: new ol.style.Style({
  image: new ol.style.Icon({
    anchor: [0.5, 46],
    anchorXUnits: 'fraction',
    anchorYUnits: 'pixels',
    src: 'http://openlayers.org/en/latest/examples/data/icon.png'
  })
})
});


var map = new ol.Map({
      layers: [
        new ol.layer.Tile({
          source: new ol.source.XYZ({
             url: 'https://opensm.donmarkets.ru/ru/{z}/{x}/{y}.png',
             attributions:
                '<a href="httsps://donmarkets.ru">Рынки Донбасса</a> карты' ,
             crossOrigin: null
          })
       }),
       markerLayer/*,
       markerLayerText*/
     ],
     target: 'map',
     controls: ol.control.defaults.defaults({
        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
          collapsible: false
        })
     }),
    view: new ol.View({
       projection: 'EPSG:4326',
       center: [37.902, 48.038],
       zoom:11,
       maxZoom:17,
       minZoom:8
    })
 });


 //map.addLayer(markerLayer);

/*const mposition = [37,902, 48,038];


// Маркер
const markerTemplate = document.getElementById("marker");
const marker = markerTemplate.content.cloneNode(true);
const markerOverlay = new ol.Overlay({
 element: marker,
 positioning: "bottom-center",
 position: mposition,
});

// Попап
const popupTemplate = document.getElementById("popup");
const popup = popupTemplate.content.cloneNode(true);
const popupOverlay = new ol.Overlay({
 element: popup,
 positioning: "bottom-center",
 offset: [0, -36],
 position: mposition,
});
map.addOverlay(popupOverlay);

map.addOverlay(markerOverlay);*/


// Попап
const mappopup = document.getElementById("popup-market-card").cloneNode(true);
const mappopupOverlay = new ol.Overlay({
 element: mappopup,
 positioning: "bottom-center",
 offset: [0, -25],
});
map.addOverlay(mappopupOverlay);

 map.addEventListener("click", function (event) {
     //mappopup.style.display = '';
     hide(mappopup, 200);
 });


// Функция создания маркеров
// По клику на маркер, покажется попап
function createMarker(position, title, text, img, url) {
//console.log(market);
 const marker = document.getElementById("map-marker").cloneNode(true);
 const markerOverlay = new ol.Overlay({
   element: marker,
   positioning: "bottom-center",
   position: position,
 });
 map.addOverlay(markerOverlay);



 /*marker.addEventListener("click", function () {
   mappopupOverlay.setPosition(position);
   mappopup.querySelector("#popup-market-card-title").textContent = title;
   mappopup.querySelector("#popup-market-card-text").textContent = text;
   mappopup.querySelector("#popup-market-card-img").textContent = "<img src='{% thumbnail " . img . " 100x100 crop %}' />";
   //mappopup.querySelector("#popup-market-card-img").textContent = img;
   //mappopup.querySelector("#popup-market-url").setAttribute('href', url);
   //mappopup.querySelector("#popup-market-img").setAttribute('src', img);
 });*/

 marker.addEventListener("click", function (event) {

   if (!event.target.classList.contains('toggle')) return;

	// Prevent default link behavior
	event.preventDefault();

	// Get the content
	/*var content = document.querySelector("event.target.hash");
	if (!content) return;

	// Get the timing
	var timing;
	if (content.classList.contains('show-fast')) {
		timing = 100;
	}
	if (content.classList.contains('show-slow')) {
		timing = 2000;
	}*/

	// Toggle the content
	//hide(mappopup, 0);

	mappopupOverlay.setPosition(position);
    mappopup.querySelector("#popup-market-card-title").textContent = title;
    mappopup.querySelector("#popup-market-card-text").textContent = text;
    //mappopup.querySelector("#popup-market-card-img").textContent = "<img src='/media/markets/logo_rd_100.png.100x100_q85_crop.png'>";
    mappopup.querySelector("#popup-market-img").setAttribute('src', img);
    mappopup.querySelector("#popup-market-url").setAttribute('href', url);
    mappopup.querySelector("#popup-market-url-icon").setAttribute('href', url);
    show(mappopup, 200);

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
	//elem.classList.add('is-visible'); // Make the element visible
	elem.style.height = height; // Update the max-height

	// Once the transition is complete, remove the inline max-height so the content can scale responsively
	window.setTimeout(function () {
		elem.style.height = '';
	}, timing);

};

// Hide an element
var hide = function (elem, timing) {

	// Get the transition timing
	timing = timing ? timing : 350;

	// Give the element a height to change from
	//elem.style.height = elem.scrollHeight + 'px';
	//elem.style.height = '0';

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

	// If the element is visible, hide it
	if (elem.classList.contains('is-visible')) {
		hide(elem, timing);
		return;
	}

	// Otherwise, show it
	show(elem, timing);

};


// Создание маркеров аэропортов
// Аэропорты хранятся в .json файле
/*airports.forEach((airport) => {
 createMarker(airport.position, airport.title);
});*/

/*createMarker(mposition, '123');*/

{% for item in items %}
console.log('{% thumbnail item.image 100x100 crop %}');
createMarker(["{{item.lng}}".replace(',', '.'), "{{item.lat}}".replace(',', '.')],
            '{{item.mk_full_name | truncatechars:32}}',
            '{{item.mk_full_address}}',
            '{% thumbnail item.image 100x100 crop %}', "{% url 'markets:market_details' mpk=item.id show='info' %}");
{% endfor %}

if({{iid}}) {
    window.setTimeout(() => alert("Я страничка, и я должна показать рынок #{{iid}}!"), 500);
}
    //var viewHeight = $(window).height();
    /*var header = $("div[data-role='header']:visible:visible");
    var navbar = $("div[data-role='navbar']:visible:visible");
    var content = $("div[data-role='content']:visible:visible");
    var contentHeight = viewHeight - header.outerHeight() - navbar.outerHeight();
    content.height(contentHeight);
    map.updateSize();*/