//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos), calcular el tiempo y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)
      document.addEventListener('WebComponentsReady', function() {
        //selecccionamos el componente de twitter con el querySelector
        var element= document.querySelector("open-weather");
        //Return the querystring part of a URL
        var publish_text = window.location.search
        //desplazo en uno para quitar la interrogacion y guardo desde ahi hasta el final del texto publicado
        publish_text = publish_text.slice(1, publish_text.length)
        //decodifico lo que viene en la URI ya que en el codigo python lo codifico por restriccion de la api
        publish_text=decodeURIComponent(publish_text)
        //quito las comillas dobles que me vienen de la api, con una expresion regular
        publish_text=publish_text.replace(/'/g,'"')
        //aqui tengo x objetos que contienen la temperatura, la maxima, la minima y el icono
        publish_text=JSON.parse(publish_text)

        //timeout para dar tiempo al componente a que se cargue
        window.setTimeout(function() {
        //tiempo del primer elemento que muestra el timeline porque este componente no tiene ids (current_date coge el actual y coge el objeto entero)
        var last_time = element.current_date.current_time;
        var last_date = element.current_date.current_date;
        console.log(element);
        var length=element.data.length
        //espero a escuchar si hay algun cambio
        element.addEventListener('data-changed', function(event){
          //cojo tiempo en el momento que hay cambio
          var time=new Date().getTime()/1000;
          if (event.detail && event.detail.value == length) {
          var haymas=true;
          //voy a recorrer los nuevos cambios y comprobar si el event es el que queria
          for (var i = 0; i<element.data.length && haymas;i++){
            if(element.data[i].current_date === last_date && element.data[i].current_time === last_time){
              haymas=false;
              //cuando no haya mas, tengo que actualizar el id al primero de la pila
              //en last_element_id tengo el id del tweet con el que voy a comparar con el id obtenido de python para comprobar que lo que se refresca en el
              //componente es lo mismo que he twitteado yo
              last_date=element.data.current_date;
            }
            else{
              var dia = new Date();
              var dd=dia.getDate();
              if(element.data[i].dt.getDate()===dd){
                for (var i=0; i<publish_text.length;i++){
                    if(element.data[i].currentTemp===publish_text[i].temp && element.data[i].icon===publish_text[i].icon && element.data[i].maxTemp===publish_text[i].max && element.data[i].minTemp===publish_text[i].min){
                    var diccionario = {
                    'time': time,
                    'post':publish_text
                  }
                
                }
              }
                var dicc_string = JSON.stringify(diccionario);
                mixpanel.track("master",{'value':dicc_string}); 
                console.log("time de escucha de cambio en ms: " + time);
                  

                }
              }
          }
          } 
        });
      }, 7000);
      });