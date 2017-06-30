document.addEventListener("WebComponentsReady", function () {
  var wc = document.querySelector('reddit-timeline');
  window.setTimeout(function () {
    var data = wc.feed;
    var experiment_id = window.location.search.slice(1);
    for (var i = 0; i < data.length; i++) {
      var shaObj = new jsSHA("SHA-1", "TEXT");

      shaObj.update(data[i].data.title);
      var title = shaObj.getHash("HEX");

      shaObj = new jsSHA("SHA-1", "TEXT");
      shaObj.update(data[i].data.selftext);
      var text = shaObj.getHash("HEX");

      var diccionario = {
        "author": data[i].data.author,
        "title": title,
        "score": data[i].data.score,
        "num_comments": data[i].data.num_comments,
        "subreddit": data[i].data.subreddit,
        "text": text,
        "experiment": experiment_id,
        "i":i
      };

      mixpanel.track("latency", {'value':JSON.stringify(diccionario)});
    }
  }, 10000)
});