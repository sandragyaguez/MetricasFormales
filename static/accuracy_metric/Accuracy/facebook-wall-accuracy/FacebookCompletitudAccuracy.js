
//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

        document.addEventListener('WebComponentsReady', function() {
        //selecccionamos el componente de facebook con el querySelector
        var element= document.querySelector("facebook-wall");
        window.setTimeout(function() {
        console.log(element);
        var list = [];
        //facebook muestra los post creados por un usuario pero tambien los post que este tenga linkados
        //los linkados los saco como si fueran "normales" para poder comparar
        for (var i=0;i<element.events.length;i++){
          list.push(element.events[i]);
          if (element.events[i].linked){
            list.push(element.events[i].linked);
          }
        };
        console.log(list.length)
        //cuando ya tengo en la misma lista los normales y los linkados, recorro el timeline de facebook
        for (var i = 0; i<list.length;i++){
          console.log(i)
          //guardo el id de cada elemento
          var id= list[i].id
          //guardo el usuario de cada post
          var user= list[i].from.name
          console.log(user)
          //objeto hash para "comprimir" textos e imagenes y poder mandarlo a Mixpanel sin ningun tipo de problemas por la limitacion de Mixpanel (255)
          var shaObj = new jsSHA("SHA-1", "TEXT");
          //guardo el texto 
          if(list[i].description){
            shaObj.update(list[i].description);
            var hash = shaObj.getHash("HEX");
            var texto=hash
        }
          else if (list[i].message){
            shaObj.update(list[i].message);
            var hash = shaObj.getHash("HEX");
            var texto=hash  
          }
        else{
          var texto=''
        }
        //guardo la imagen
          if(list[i].picture){
          var shaObj = new jsSHA("SHA-1", "TEXT");

            shaObj.update(list[i].picture);
            var hash = shaObj.getHash("HEX"); 
            var image=hash;
          }
          else{
            var image=''
          }
          //almaceno todo en un diccionario
          var diccionario = {
            'user': user,
            'i': i,
            'texto':texto,
            'image':image
          }
          var dicc_string = JSON.stringify(diccionario);
          //mando a mixpanel los campos recogidos en el diccionario
          mixpanel.track("accuracy",{'value':dicc_string});
          }
      }, 5000);
      });




          
