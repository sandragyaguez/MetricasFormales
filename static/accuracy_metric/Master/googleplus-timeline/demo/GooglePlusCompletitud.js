

 document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("googleplus-timeline");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.timeline_posts.length)
        for (var i = 0; i<element.timeline_posts.length;i++){
          console.log(i)
          var id= element.timeline_posts[i].id
          var user=element.timeline_posts[i].actor.displayName
          var texto=element.timeline_posts[i].object.content
          texto = texto.replace(/<a [^>]*>([^<]*)<\/a>/g,'$1');
          //objeto hash para "comprimir" textos e imagenes y poder mandarlo a Mixpanel sin ningun tipo de problemas por la limitacion de Mixpanel (255)
          var shaObj = new jsSHA("SHA-1", "TEXT");
          shaObj.update(texto);
          var hash = shaObj.getHash("HEX");
          var texto=hash
          var publ=element.timeline_posts[i].published;
          var diccionario = {
            'id': id,
            'user': user,
            'text': texto,
            'i':i,
            'publish':publ
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("master",{'value':dicc_string});

          }
      }, 2000);
      });