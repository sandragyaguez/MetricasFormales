
//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

        document.addEventListener('WebComponentsReady', function() {
        //selecccionamos el componente de twitter con el querySelector
        var element= document.querySelector("twitter-timeline");
        window.setTimeout(function() {
        //recorro todos los elementos del timeline de twitter
        for (var i = 0; i<element.events.length;i++){
          //guardo el texto del tweet
          texto=element.events[i].text
          //guardo el id de cada elemento
          var id= element.events[i].id_str
          //guardo el usuario de cada post
          var user= element.events[i].user.name
          //al texto le quito cualquier etiqueta que contenga <a>
          texto = texto.replace(/<a [^>]*>([^<]*)<\/a>/g,'$1');
          //almaceno todas las variables en un diccionario
          var diccionario = {
            'id': id,
            'text': texto,
            'user': user,
            'i': i
          }
          var dicc_string = JSON.stringify(diccionario);
          //mando a mixpanel los campos recogidos en el diccionario
          mixpanel.track("master",{'value':dicc_string});

          }
      }, 2000);
      });