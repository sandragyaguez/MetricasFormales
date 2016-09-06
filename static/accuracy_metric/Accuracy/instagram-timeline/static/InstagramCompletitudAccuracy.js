
//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

 document.addEventListener('WebComponentsReady', function() {
        //selecccionamos el componente de instagram con el querySelector
        var element= document.querySelector("instagram-timeline");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.events.length)
        //recorro todos los elementos del timeline de instagram
        for (var i = 0; i<element.events.length;i++){
          console.log(i)
          //guardo el id de cada elemento
          var id= element.events[i].id
          //guardo el usuario de cada elemento
          var user=element.events[i].user.username
          //creo un objeto hash para posteriormente poder "reducir" el tamano de algunos campos
          var shaObj = new jsSHA("SHA-1", "TEXT");
          //guardo la imagen de cada post
          var image=element.events[i].images.standard_resolution.url

          //hash para la imagen
          shaObj.update(image);
          var hash = shaObj.getHash("HEX"); 
          var imagen=hash;

          if(element.events[i].caption!=null){
            //en cado de no estar vacio el campo caption, guardo el texto del post
            var text=element.events[i].caption.text
            var shaObj = new jsSHA("SHA-1", "TEXT");
            //hash para el texto
            shaObj.update(text);
            var hash = shaObj.getHash("HEX");
            var texto=hash
            }
          else{
            var texto=''
          }
          //almaceno todas las variables en un diccionario
          var diccionario = {
            'id': id,
            'user': user,
            'image': imagen,
            'text': texto,
            'i':i
          }
          var dicc_string = JSON.stringify(diccionario);
          //mando a mixpanel los campos recogidos en el diccionario
          mixpanel.track("accuracy",{'value':dicc_string});

          }
      }, 5000);
      });        