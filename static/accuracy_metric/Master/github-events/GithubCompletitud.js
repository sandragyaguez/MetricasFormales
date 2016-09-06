//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

 document.addEventListener('WebComponentsReady', function() {
        //selecccionamos el componente de github con el querySelector
        var element= document.querySelector("github-events");
        window.setTimeout(function() {
        console.log(element);
        console.log(element.events.length)
        //recorro todos los elementos del timeline de github
        for (var i = 0; i<element.events.length;i++){
          console.log(i)
          //guardo el id de cada elemento
          var id= element.events[i].id
          console.log(id)
          //guardo el usuario de cada post
          var user=element.events[i].actor.login
          //guardo el texto segun el event que se realice
          //PushEvent (1) Realiazo un push a tal rama
          if(element.events[i].type=="PushEvent"){
            var texto=element.events[i].payload.commits[0].message
          }
          //WatchEvent (2) Empiezo a seguir el repo
          else if(element.events[i].type=="WatchEvent"){
            var texto=element.events[i].payload.action
          }
          //CreateEvent (3) Creo el repo, Creo la rama
          else if(element.events[i].type=="CreateEvent"){
            //var texto=element.events[i].createEvent
            var texto="Creo un repositorio/ Creo una rama"
          }
          //PullRequestEvent (4) Abrio la pull request, cierro la pull request
          else if(element.events[i].type=="PullRequestEvent"){
            var texto=element.events[i].payload.pull_request.title
          }
          //IssueEvent (5) Abro la issue
          else if(element.events[i].type=="IssuesEvent"){
            var texto=element.events[i].payload.issue.title
          }
          //MemberEvent (6) Anado a tal miembro en tal sitio
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
          //almaceno todo en un diccionario
          var diccionario = {
            'id': id,
            'user': user,
            'text': texto,
            'i':i
          }
          var dicc_string = JSON.stringify(diccionario);
          //mando a mixpanel los campos recogidos en el diccionario
          mixpanel.track("master",{'value':dicc_string});

          }
      }, 2000);
      });