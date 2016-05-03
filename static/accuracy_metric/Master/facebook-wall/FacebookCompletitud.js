


        document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("facebook-wall");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.events.length)
        for (var i = 0; i<element.events.length;i++){
          console.log(i)
          var id= element.events[i].id
          var user= element.events[i].from.name
          //var texto=element.events[i].description
          var diccionario = {
            'id': id,
            'user': user,
            'i': i
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("master",{'value':dicc_string});

          }
      }, 2000);
      });