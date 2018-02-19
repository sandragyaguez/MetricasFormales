
//Codigo javascript que escucha el componente para detectar los cambios (nuevos datos) y mandarlos a mixpanel
// Hay que escuchar la funcion de polymer de cuando un componente esta listo (mirar webcomponents)

document.addEventListener('WebComponentsReady', function() {
  //selecccionamos el componente de twitter con el querySelector
  var element= document.querySelector("spotify-component");
  window.setTimeout(function() {
  //recorro todos los albumes del timeline de spotify
  for (var i = 0;i<element.res.length;i++){
    namePlayList=element.res[i].name;
    createdBy=element.res[i].owner.id;
    idPlayList=element.res[i].id;
    image = element.res[i].images[0].url;
    //objeto hash para "comprimir" textos e imagenes y poder mandarlo a Mixpanel sin ningun tipo de problemas por la limitacion de Mixpanel (255)
    shaObj = new jsSHA("SHA-1", "TEXT");
    //hash para texto
    shaObj.update(image);
    image = shaObj.getHash("HEX");
    for (var j=0; j<element.res[i].infoPista.length;j++){
      songsName= element.res[i].infoPista[j].track.name;
      artistsName= element.res[i].infoPista[j].track.album.artists[0].name;
      id= element.res[i].infoPista[j].track.id;
              
      var diccionario = {
        'playList': namePlayList,
        'owner': createdBy,
        'id': idPlayList,
        'image':  image,
        'song': songsName,
        'artist': artistsName,
        'idSong': id
      }
      var dicc_string = JSON.stringify(diccionario);
      mixpanel.track("accuracy",{'value':dicc_string});
    }      
    }
}, 2000);
});