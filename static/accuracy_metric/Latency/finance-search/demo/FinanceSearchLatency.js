
//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

document.addEventListener('WebComponentsReady', function () {
  //selecccionamos el componente de facebook con el querySelector
  var element = document.querySelector("finance-search");
  window.setTimeout(function () {

    var data = element.$$('finance-chart').current[0];
    //almaceno todo en un diccionario

    var diccionario = {
      'Name': data.Name,
      'DaysLow': data.DaysLow,
      'DaysHigh': data.DaysHigh,
      'Date': new Date().getTime()
    }
    var dicc_string = JSON.stringify(diccionario);
    //mando a mixpanel los campos recogidos en el diccionario
    mixpanel.track("latency", { 'value': dicc_string });
  }, 10000);
});