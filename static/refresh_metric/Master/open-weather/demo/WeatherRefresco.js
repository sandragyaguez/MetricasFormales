//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos), calcular el tiempo y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)
      document.addEventListener('WebComponentsReady', function() {
        //selecccionamos el componente de twitter con el querySelector
        var element= document.querySelector("open-weather");
        //Return the querystring part of a URL
        var publish_text = window.location.search
        //desplazo en uno para quitar la interrogacion y guardo desde ahi hasta el final del texto publicado
        publish_text = publish_text.slice(1, publish_text.length)
        //console.log("El texto que tengo que encontrar es: " + publish_text);
        //timeout para dar tiempo al componente a que se cargue
        window.setTimeout(function() {
        //tiempo del primer elemento que muestra el timeline porque este componente no tiene ids
        var last_time = element.current_date.current_time;
        var last_date = element.current_date.current_date;
        console.log(element);
        //espero a escuchar si hay algun cambio
        element.addEventListener('data-changed', function(event){
          //cojo tiempo en el momento que hay cambio
          var time=new Date().getTime()/1000;
          if (event.detail && event.detail.value.length > 0) {
          var haymas=true;
          //voy a recorrer los nuevos cambios y comprobar si el event es el que queria
          for (var i = 0; i<element.data.length && haymas;i++){
            if(element.data[i].current_date === last_date && element.data[i].current_time === last_time){
              haymas=false;
              //cuando no haya mas, tengo que actualizar el id al primero de la pila
              //en last_element_id tengo el id del tweet con el que voy a comparar con el id obtenido de python para comprobar que lo que se refresca en el
              //componente es lo mismo que he twitteado yo
              last_date=element.data.current_date;
            }
            else{
              //a.current_date.currentTemp
              //a.current_date.minTemp
              //a.current_date.maxTemp
              //a.current_date.icon

//tengo que decodificar el texto que mando por query en la uri y decodificar el codigo de icon ya que del componente se coge como "nuboso"
                if(element.data[i].description===publish_text){
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
      }, 7000);
      });