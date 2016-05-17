
//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos), calcular el tiempo y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)
      document.addEventListener('WebComponentsReady', function() {
        //selecccionamos el componente de twitter con el querySelector
        var element= document.querySelector("github-events");
        //Return the querystring part of a URL
        var publish_text = window.location.search
        //desplazo en uno para quitar la interrogacion y guardo desde ahi hasta el final del texto publicado
        publish_text = publish_text.slice(1, publish_text.length)
        console.log(publish_text)
        //var publish_text= publish_text.split("&")
        //console.log("El texto que tengo que encontrar es: " + publish_text);
        //timeout para dar tiempo al componente a que se cargue
        window.setTimeout(function() {
        //id del primer elemento que muestra el timeline
        var last_element_id = element.events[0].id;
        console.log(element);
        //espero a escuchar si hay algun cambio
        element.addEventListener('events-changed', function(event){
          //cojo tiempo en el momento que hay cambio
          var time=new Date().getTime();
          //para filtrar solo cambios en el la variable, no en los elementos internos
          if (!event.detail.path) {
          var haymas=true;
          console.log("entra")

          //voy a recorrer los nuevos cambios y comprobar si el event es el que queria
          for (var i = 0; i<element.events.length && haymas;i++){
            if(element.events[i].id === last_element_id){
              haymas=false;
              console.log("hay mas: " + haymas);
              //cuando no haya mas, tengo que actualizar el id al primero de la pila
              //en last_element_id tengo el id del tweet con el que voy a comparar con el id obtenido de python para comprobar que lo que se refresca en el
              //componente es lo mismo que he twitteado yo
              last_element_id=element.events[0].id;
            }
            else{
                console.log(element.events[i]);
                //comparo solo el title de la issue porque es lo unico que se ve en el componente, el body no se muestra
                //si en vez de ser una issue es un pull request o un create repositorio hacer casos por seperado
                if(element.events[i].payload.issue.title===publish_text){
                  var diccionario = {
                    'time': time,
                    'tweet':publish_text
                  }
                  var dicc_string = JSON.stringify(diccionario);
                  mixpanel.track("master",{'value':dicc_string});
                  console.log("time de escucha de cambio en ms: " + time);

                }
              }
          }
          }          
        });
      }, 2000);
      });