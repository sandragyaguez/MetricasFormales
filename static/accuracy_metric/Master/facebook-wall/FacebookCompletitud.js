


        document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("facebook-wall");
        window.setTimeout(function() {
        console.log(element);
        var list = [];
        //los linkados los saco como si fueran "normales" para poder comparar
        for (var i=0;i<element.events.length;i++){
          list.push(element.events[i]);
          if (element.events[i].linked){
            list.push(element.events[i].linked);
          }
        };
        console.log(list.length)

        
        for (var i = 0; i<list.length;i++){
          console.log(i)
          var id= list[i].id
          var user= list[i].from.name
          console.log(user)
          //objeto hash para "comprimir" textos e imagenes y poder mandarlo a Mixpanel sin ningun tipo de problemas por la limitacion de Mixpanel (255)
          var shaObj = new jsSHA("SHA-1", "TEXT");

          if(list[i].description){
            //sustituir saltos de linea por espacios
            text = list[i].description.replace(/\n+/g, ' ')
            shaObj.update(text);
            var hash = shaObj.getHash("HEX");
            var texto=hash
        }
          else if (list[i].message){
            text = list[i].message.replace(/\n+/g, ' ')
            shaObj.update(text);
            var hash = shaObj.getHash("HEX");
            var texto=hash  
          }
        else{
          var texto=''
        }
          if(list[i].picture){
            shaObj.update(list[i].picture);
            var hash = shaObj.getHash("HEX"); 
            var image=hash;
          }

          var diccionario = {
            'user': user,
            'i': i,
            'texto':texto,
            'image':image
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("master",{'value':dicc_string});
          }
      }, 5000);
      });