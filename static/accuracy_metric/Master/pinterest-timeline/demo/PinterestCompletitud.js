
//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

document.addEventListener('WebComponentsReady', function() {
  //selecccionamos el componente de twitter con el querySelector
  var element= document.querySelector("pinterest-timeline");
  console.log(element)

  window.setTimeout(function() {
    var buttons =element.querySelectorAll(".itemBig" );
    console.log(buttons.length)
    //recorro todos los elementos del timeline de twitter
    for (var i=0; i<buttons.length;i++){
      console.log("entra aqui?")
      window.setTimeout(function(){
        buttons[i].click()
        console.log("va bien")
        window.setTimeout(function(){
          for(var j=0;j<element.pins_cached.length;j++){
            url=element.pins_cached[j].url;
            var diccionario = {'url': url}
            var dicc_string = JSON.stringify(diccionario);
            //mando a mixpanel los campos recogidos en el diccionario
            mixpanel.track("master",{'value':dicc_string});
          } 
        },500);
      },i*1000);
  }
})
})