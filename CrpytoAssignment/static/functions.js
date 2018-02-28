function loadDoc(link,id,t=10000) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
       document.getElementById(id).innerHTML = this.responseText;
      }
    };
    xhttp.open("GET", link, true);
    xhttp.send();
    setTimeout('loadDoc()',t)
  }

  

  