

 document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("googleplus-timeline");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.events.length)
        for (var i = 0; i<element.timeline_posts.length;i++){
          console.log(i)
          var id= element.timeline_posts[i].id
          console.log(id)
          var user=element.timeline_posts[i].actor.displayName
          var texto=element.timeline_posts[i].object.content
          console.log(texto)
          var diccionario = {
            'id': id,
            'user': user,
            'text': texto,
            'i':i
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("master",{'value':dicc_string});

          }
      }, 2000);
      });