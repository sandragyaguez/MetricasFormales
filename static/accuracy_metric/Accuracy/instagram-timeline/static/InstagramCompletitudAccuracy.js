
 document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("instagram-timeline");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.events.length)
        for (var i = 0; i<element.events.length;i++){
          console.log(i)
          var id= element.events[i].id
          var user=element.events[i].user.username
          var shaObj = new jsSHA("SHA-1", "TEXT");
          var image=element.events[i].images.standard_resolution.url

          //hash para la imagen
          shaObj.update(image);
          var hash = shaObj.getHash("HEX"); 
          var imagen=hash;

          if(element.events[i].caption!=null){
            var text=element.events[i].caption.text
            var shaObj = new jsSHA("SHA-1", "TEXT");
            shaObj.update(text);
            var hash = shaObj.getHash("HEX");
            var texto=hash
            }
          else{
            var texto=''
          }
          var diccionario = {
            'id': id,
            'user': user,
            'image': imagen,
            'text': texto,
            'i':i
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("accuracy",{'value':dicc_string});

          }
      }, 2000);
      });        