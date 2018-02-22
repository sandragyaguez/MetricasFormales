

document.addEventListener('WebComponentsReady', function() {
  var element= document.querySelector("spotify-component");
  var publish_text = window.location.search;
  //desplazo en uno para quitar la interrogacion y guardo desde ahi hasta el final del texto publicado
  publish_text = publish_text.slice(1, publish_text.length);
  window.setTimeout(function() {
  //id del primer elemento que muestra el timeline
  var last_element_id = element.res[0].id;
  //espero a escuchar si hay algun cambio
  element.addEventListener('res-changed', function(event){
  //cojo tiempo en el momento que hay cambio
  var time=new Date().getTime();
   if (event.detail) {
    var haymas=true;
    //voy a recorrer los nuevos cambios y comprobar si el event es el que queria
   for (var i = 0; i<element.res.length && haymas;i++){
    data=element.res[0].name;
    for (var j=0; j<element.res[i].infoPista.length;j++){
      uris= element.res[i].infoPista[j].track.uri;
      data+=uris;
    }
   if(element.res[i].id === last_element_id){
         haymas=false;
        //cuando no haya mas, tengo que actualizar el id al primero de la pila
        //en last_element_id tengo el id del post que voy a comparar con el id obtenido de python para comprobar que lo que se refresca en el componente es lo mismo que he postead
         last_element_id=element.res[0].id;
   }
       else{
         console.log("entra");
          if((data===publish_text)){
            var diccionario = {
              'time': time,
              'post':publish_text
            }
            var dicc_string = JSON.stringify(diccionario);
            mixpanel.track("master",{'value':dicc_string});
            console.log("time de escucha de cambio en ms: " + time);
      }
       }
   }
  }        
  });
}, 10000);
});