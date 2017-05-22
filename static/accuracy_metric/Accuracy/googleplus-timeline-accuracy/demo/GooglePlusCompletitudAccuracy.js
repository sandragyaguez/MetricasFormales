
//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)
 document.addEventListener('WebComponentsReady', function() {
        //selecccionamos el componente de googleplus con el querySelector
        var element= document.querySelector("googleplus-timeline");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.timeline_posts.length)
        //recorro todos los elementos del timeline de googleplus
        for (var i = 0; i<element.timeline_posts.length;i++){
          console.log(i)
          //guardo el usuario de cada post
          var user=element.timeline_posts[i].actor.displayName
          console.log(user)
          //guardo el texto que contiene cada post
          var texto=element.timeline_posts[i].object.content
          //objeto hash para "comprimir" textos e imagenes y poder mandarlo a Mixpanel sin ningun tipo de problemas por la limitacion de Mixpanel (255)
          var shaObj = new jsSHA("SHA-1", "TEXT");
          //hash para texto
          shaObj.update(texto);
          var hash = shaObj.getHash("HEX");
          var texto=hash
          //guardo el tiempo de publicacion y paso ese tiempo al mismo formato que lo recibo de la api de googleplus
          var publ=Math.floor((element.timeline_posts[i].published)/1000);
          console.log(publ)
          //almaceno todos los campos en un diccionario
          var diccionario = {
            'user': user,
            'text': texto,
            'i':i,
            'publish':publ
          }
          var dicc_string = JSON.stringify(diccionario);
          //mando a mixpanel los campos recogidos en el diccionario
          mixpanel.track("accuracy",{'value':dicc_string});

          }
      }, 2000);
      });


    
          
        
          
