var markerLayerText = new ol.layer.Vector({
    title: "MarketPointText",
    visible: true,
    maxResolution: 5,
    //source: vectorSource,
    source: new ol.source.Vector({
            format: new ol.format.GeoJSON(),
            url: 'index.php?r=api/getmarkets'
          }),
    style: function(feature) {
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


var markerLayer = new ol.layer.Vector({
    title: "MarketPoint",
    visible: true,
    minResolution: 5,
    source: new ol.source.Vector({
            format: new ol.format.GeoJSON(),
            url: 'index.php?r=api/getmarkets'
          }),
    style: function(feature) {
            style = new ol.style.Style({
            image: new ol.style.Icon({
                src: 'imgs/baloon.png'
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