

 document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("instagram-timeline");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.events.length)
        for (var i = 0; i<element.events.length;i++){
          console.log(i)
          var id= element.events[i].id
          var user=element.events[i].user.username
          var imagen=element.events[i].images.standard_resolution.url
          //if(element.events[i].caption!=null){
            //var texto=element.events[i].caption.text
            //texto = texto.replace(/<a [^>]*>([^<]*)<\/a>/g,'$1')
          //}
          //else{
            //texto=''
          //}
          //console.log(texto)
          var diccionario = {
            'id': id,
            'user': user,
            'image': imagen,
            //'text': texto,
            'i':i
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("master",{'value':dicc_string});

          }
      }, 2000);
      });