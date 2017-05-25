//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

document.addEventListener('WebComponentsReady', function () {
  //selecccionamos el componente de twitter con el querySelector
  var element = document.querySelector("traffic-incidents");
  window.setTimeout(function () {
    console.log(element);
    console.log(element.traffic_info.length)
    //recorro todos los elementos del timeline de twitter
    for (var i = 0; i < element.traffic_info.length; i++) {
      //creo hash por la limitacion de mixpanel
      var hash = sha1.create();
      var hash_input = element.traffic_info[i].description;
      hash.update(hash_input);

      tipo = element.traffic_info[i].type;
      fecha = element.traffic_info[i].lastModified;
      //almaceno todas las variables en un diccionario
      var diccionario = {
        'descripcion': hash.hex(),
        'tipo': tipo,
        'fecha': fecha,
        'i': i
      }
      var dicc_string = JSON.stringify(diccionario);
      //mando a mixpanel los campos recogidos en el diccionario
      mixpanel.track("master", {
        'value': dicc_string
      });

    }
  }, 2000);
});