/*$(".foot-collapse").click(function(){
        $(".collapse").collapse('toggle');
        document.getElementById("close-footer").hidden = !document.getElementById("close-footer").hidden;
    });*/
    var map = new ol.Map({
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM({
             url: 'https://opensm.donmarkets.ru/ru/{z}/{x}/{y}.png',
             attributions:
                '<a href="httsps://donmarkets.ru">Рынки Донбасса</a> карты' ,
             crossOrigin: null
          })
       })
     ],
     target: 'map',
     controls: ol.control.defaults({
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