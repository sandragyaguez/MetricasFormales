



 document.addEventListener('WebComponentsReady', function() {
        var element= document.querySelector("github-events");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.events.length)
        for (var i = 0; i<element.events.length;i++){
          console.log(i)
          var id= element.events[i].id
          console.log(id)
          var user=element.events[i].actor.login
          if(element.events[i].payload.commits[0].message){
            var texto=element.events[i].payload.commits[0].message
          }
          else if(element.events[i].payload.action){
            var texto=element.events[i].payload.action
          }
          else if(element.events[i].createEvent){
            var texto=element.events[i].createEvent
          }
          //MIRAR SI TENGO QUE ESPECIFICAR QUE SEA UNA ISSUE OPENENED
          else if(element.events[i].payload.issue.title){
            var texto=element.events[i].payload.issue.title
          }
          else if(element.events[i].payload.forkee){
            var texto="Realizo un fork"
          }
          else if(element.events[i].pullRequestAction){
            var texto=element.events[i].pullRequestAction
          }


  

          else{


          }
          var diccionario = {
            'id': id,
            'user': user,
            //'text': texto
            'i':i
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("master",{'value':dicc_string});

          }
      }, 2000);
      });