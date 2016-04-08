


      document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("twitter-timeline");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.events.length)
        for (var i = 0; i<element.events.length;i++){
          texto=element.events[i].text
          console.log(texto)
          console.log(i)
          texto = texto.replace(/<a [^>]*>([^<]*)<\/a>/g,'$1');
          var diccionario = {
            'text': texto , 
            'time_created' : element.events[i].created_at
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("completitud twitter",{'value':dicc_string});

          }
      }, 2000);
      });