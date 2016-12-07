//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)


document.addEventListener('WebComponentsReady', function() {
  //selecccionamos el componente de pinterest con el querySelector
  var element= document.querySelector("pinterest-timeline");
  function geti(i,buttons){
  return function(){
       buttons[i].click()
          window.setTimeout(function(){
            contador=0;      
            for(var j=0;j<element.pins_cache.length;j++){
              url=element.pins_cache[j].url;
              contador++;
              mixpanel.track("accuracy",{'value':url});
            }
            console.log(contador) 
          },500);
  }
}
  window.setTimeout(function() {
    var buttons =element.querySelectorAll(".itemBig");
    //recorro todos los botones del timeline de pinterest
    for (var i=0; i<buttons.length;i++){
      window.setTimeout(geti(i,buttons),i*1000);
  }
},1000);
})