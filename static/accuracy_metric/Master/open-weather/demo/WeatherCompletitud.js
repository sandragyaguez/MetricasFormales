//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

        document.addEventListener('WebComponentsReady', function() {
        //selecccionamos el componente de twitter con el querySelector
        var element= document.querySelector("open-weather");
        window.setTimeout(function() {
        console.log(element);
        //recorro todos los elementos del timeline de twitter
        //for (var i = 0; i<element.current_date.length;i++){
          var city=element.current_date.name
          var date=element.current_date.dt
          var icon=element.current_date.icon
          var temp=element.current_date.currentTemp
          var temp_max=element.current_date.maxTemp
          var temp_min=element.current_date.minTemp


          console.log(city)
          console.log(date)
          console.log(icon)
          console.log(temp)
          console.log(temp_max)
          console.log(temp_min)

          //almaceno todas las variables en un diccionario
          var diccionario = {
            'city': city,
            'fecha': date,
            'icon': icon,
            'temp': temp,
            'temp_max': temp_max,
            'temp_min':temp_min
          }
          var dicc_string = JSON.stringify(diccionario);
          //mando a mixpanel los campos recogidos en el diccionario
          mixpanel.track("master",{'value':dicc_string});

          //}
      }, 2000);
      });