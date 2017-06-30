document.addEventListener("WebComponentsReady", function () {
  var target = document.querySelector('reddit-timeline');
  var last_post;
  var published_text = window.location.search.slice(1);
  target.addEventListener("feed-changed", function (e) {
    var found = false;
    var time;
    if (target.feed) {
      for (var i = 0; i < target.feed.length && !found; i++) {
        if (target.feed[i].data.selftext == published_text) {
          found = true;
          time = new Date().getTime() - target.feed[i].data.created;
        }
      }

      if (found) {
        var diccionario = {
          'time': time,
          "published_text": published_text
        };

        var dicc_string = JSON.stringify(diccionario);
        mixpanel.track("accuracy", {
          'value': dicc_string,
        });
      }
    } else {
      console.log("Se intenta acceder sin haber feed");
    }
  });
});