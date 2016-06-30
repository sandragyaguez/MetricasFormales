 


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
          //PushEvent (1) Realiazo un push a tal rama
          if(element.events[i].type=="PushEvent"){
            var texto=element.events[i].payload.commits[0].message
          }
          //WatchEvent (2) Empezo a seguir el repo
          else if(element.events[i].type=="WatchEvent"){
            var texto=element.events[i].payload.action
          }
          //CreateEvent (3) Creo el repo, Creo la rama
          else if(element.events[i].type=="CreateEvent"){
            //var texto=element.events[i].createEvent
            var texto="Creo un repositorio/ Creo una rama"
          }
          //PullRequestEvent (4) Abrio la pull request, cerro la pull request
          else if(element.events[i].type=="PullRequestEvent"){
            var texto=element.events[i].payload.pull_request.title
          }
          //IssueEvent (5) Abrio la issue
          else if(element.events[i].type=="IssuesEvent"){
            var texto=element.events[i].payload.issue.title
          }
          //MemberEvent (6) Anadio a tal miembro en tal sitio
          else if(element.events[i].type=="MemberEvent"){
            var texto=element.events[i].payload.action
          }
          //ForkEvent (14) Realizo un fork (meto el mensaje a pelo porque no hay nada que comparar sino)
          else if(element.events[i].type=="ForkEvent"){
            var texto="Realizo un fork"
          }
          else{
            var texto=''
          }
          var diccionario = {
            'id': id,
            'user': user,
            'text': texto,
            'i':i
          }
          var dicc_string = JSON.stringify(diccionario);
          mixpanel.track("latency",{'value':dicc_string});

          }
      }, 2000);
      });