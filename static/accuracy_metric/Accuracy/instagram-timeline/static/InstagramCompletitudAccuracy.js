
 document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("instagram-timeline");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.events.length)
        for (var i = 0; i<element.events.length;i++){
          console.log(i)
          var id= element.events[i].id
          console.log(id)
          //var user=element.events[i].actor.login
          //var texto=element.events[i].payload.commits[0].message
          //console.log(texto)
          var diccionario = {
            'id': id,
            //'user': user,
            //'text': texto
            'i':i
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("accuracy",{'value':dicc_string});

          }
      }, 2000);
      });