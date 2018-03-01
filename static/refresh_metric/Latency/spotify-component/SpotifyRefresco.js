
document.addEventListener('WebComponentsReady', function () {
  var element = document.querySelector("spotify-component");
  var publish_text = window.location.search;
  //desplazo en uno para quitar la interrogacion y guardo desde ahi hasta el final del texto publicado
  publish_text = publish_text.slice(1, publish_text.length);
  var publicado=false;
  window.setTimeout(function () {
    //id del primer elemento que muestra el timeline
    //var last_element_id = element.res[0].id;
    //espero a escuchar si hay algun cambio
    element.addEventListener('res-changed', function (event) {
      var found = false;
      var time;
      if (element.res) {
        for (var i = 0; i < element.res.length && !found && !publicado; i++) {
          data = element.res[i].name;
          if (element.res[i].infoPista != undefined) {
            for (var j = 0; j < element.res[i].infoPista.length; j++) {
              uris = element.res[i].infoPista[j].track.uri;
              data += uris;
            }
          }
          if (publish_text == data) {
            found = true;
            time = new Date().getTime()/1000;            
            console.log(time);
            var diccionario = {
              'time': time,
              'post': data
            };
            var dicc_string = JSON.stringify(diccionario);
            mixpanel.track("latency", {
              'value': dicc_string,
            });
            publicado=true;
          }
        }
      } else {
        console.log("Se intenta acceder sin haber res");
      }
    });
  }, 8000);
});