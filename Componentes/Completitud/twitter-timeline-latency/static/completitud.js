
      //function sleep(milliseconds){
        //var start = new Date().getTime();
        //while ((new Date().getTime() - start) <= milliseconds);
      //}

      document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("twitter-timeline");
        window.setTimeout(function() {
        console.log(element);
        //sleep(10000);
        console.log(element.events.length)
        for (var i = 0; i<element.events.length;i++){
          texto=element.events[i].text
          console.log(texto)
          console.log(i)
          var d=new Date(element.events[i].created_at).getTime()
          console.log(d)
          console.log(typeof(d))
          texto = texto.replace(/<a [^>]*>([^<]*)<\/a>/g,'$1');
          var diccionario = { 
            'time_created' : d,
            'text': texto
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("completitud twitter latency",{'value':dicc_string});

          }
      }, 2000);
      });