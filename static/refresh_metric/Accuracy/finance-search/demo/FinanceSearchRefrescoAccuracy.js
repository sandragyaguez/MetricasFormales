
//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

document.addEventListener('WebComponentsReady', function () {
  //selecccionamos el componente de facebook con el querySelector
  var element = document.querySelector("finance-search");
  var finance = element.$$('finance-chart');

  var getQueryparams = function () {
    // This function is anonymous, is executed immediately and 
    // the return value is assigned to QueryString!
    var query_string = {};
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
      var pair = vars[i].split("=");
      // If first entry with this name
      if (typeof query_string[pair[0]] === "undefined") {
        query_string[pair[0]] = decodeURIComponent(pair[1]);
        // If second entry with this name
      } else if (typeof query_string[pair[0]] === "string") {
        var arr = [query_string[pair[0]], decodeURIComponent(pair[1])];
        query_string[pair[0]] = arr;
        // If third or later entry with this name
      } else {
        query_string[pair[0]].push(decodeURIComponent(pair[1]));
      }
    }
    return query_string;
  }
  var published = getQueryparams();

  var callback = function (event) {
    // Avoid errors
    window.setTimeout(function () {
      var refresh_time = new Date().getTime();
      var new_data = event.target.current[0];

      var same_data = true;

      for (var key in published) {
        if (published.hasOwnProperty(key)) {
          if (key !== 'id' && key !== 'Name' && (new_data[key] !== published[key] || new_data[key] === 'Error')) {
            same_data = false;
            console.info(new_data[key] + ' !== ' + published[key]);
          }
        }
      }

      if (same_data) {
        var diccionario = {
          'id': published.id,
          'time': refresh_time
        }
        var dicc_string = JSON.stringify(diccionario);
        //mando a mixpanel los campos recogidos en el diccionario
        mixpanel.track("accuracy", { 'value': dicc_string });
      }
    }.bind(this), 500);
  };
  finance.addEventListener('finance-chart-reload', function () {
    finance.addEventListener('finance-chart-ready', callback);
  });
  //almaceno todo en un diccionario
});