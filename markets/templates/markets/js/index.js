
    var map = new ol.Map({
      layers: [
        new ol.layer.Tile({
          source: new ol.source.XYZ({
             url: 'https://opensm.donmarkets.ru/ru/{z}/{x}/{y}.png',
             attributions:
                '<a href="httsps://donmarkets.ru">Рынки Донбасса</a> карты' ,
             crossOrigin: null
          })
       })
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

{% for item in items %}
alert('Рынок {{item.market_name}}: {{item.lng}}' + '-' + '{{item.lat}}');
{% endfor %}


    //var viewHeight = $(window).height();
    /*var header = $("div[data-role='header']:visible:visible");
    var navbar = $("div[data-role='navbar']:visible:visible");
    var content = $("div[data-role='content']:visible:visible");
    var contentHeight = viewHeight - header.outerHeight() - navbar.outerHeight();
    content.height(contentHeight);
    map.updateSize();*/