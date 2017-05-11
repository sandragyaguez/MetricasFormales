//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos), calcular el tiempo y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)
document.addEventListener('WebComponentsReady', function () {
  //selecccionamos el componente de twitter con el querySelector
  var element = document.querySelector("googleplus-timeline");
  //Return the querystring part of a URL
  var publish_text = window.location.search
  //desplazo en uno para quitar la interrogacion y guardo desde ahi hasta el final del texto publicado
  publish_text = publish_text.slice(1, publish_text.length)
  //console.log("El texto que tengo que encontrar es: " + publish_text);
  //timeout para dar tiempo al componente a que se cargue
  window.setTimeout(function () {
    //id del primer elemento que muestra el timeline

    var sortedPosts = element.timeline_posts.sort(element._sortPosts);
    last_element_id = sortedPosts[0];
    var min_size = element.timeline_posts.length;
    //espero a escuchar si hay algun cambio
    element.addEventListener('timeline_posts-changed', function (event) {
      //cojo tiempo en el momento que hay cambio
      var time = new Date().getTime();
      if (event.detail && event.detail.value && event.detail.value >= min_size) {
        var haymas = true;
        var posts = element.timeline_posts.sort(element._sortPosts);
        //voy a recorrer los nuevos cambios y comprobar si el event es el que queria
        for (var i = 0; i < posts.length && haymas; i++) {
          if (posts[i].id === last_element_id) {
            haymas = false;
            //cuando no haya mas, tengo que actualizar el id al primero de la pila
            //en last_element_id tengo el id del tweet con el que voy a comparar con el id obtenido de python para comprobar que lo que se refresca en el
            //componente es lo mismo que he twitteado yo
            last_element_id = posts[0].id;
          } else {
            //el time es el mismo para los tres tweets porque se muestran al
            // avoid char 65279 (utf8 delimiter?)
            var post_text = posts[i].object && posts[i].object.content ? posts[i].object.content.slice(0, posts[i].object.content.length - 1) : '';
            if (post_text == publish_text) {
              var diccionario = {
                'time': time,
                'post': publish_text
              }
              var dicc_string = JSON.stringify(diccionario);
              mixpanel.track("master", {
                'value': dicc_string
              });
              var publicado = posts[i].published;

            }
          }
        }
      }

    });
  }, 7000);
});