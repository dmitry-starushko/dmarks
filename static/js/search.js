
var searchbtn = document.getElementById('search-btn');
var searchwindow = document.getElementById('search-market-window');
var searchinput = document.getElementById('search-market-input');
var globalTimeout = null;
var maxsymbols = 3;

var closebtn = document.getElementById("search-close");

searchbtn.onclick = function() {
  searchwindow.style.display = "block";
}

closebtn.onclick = function() {
  searchwindow.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == searchwindow) {
    searchwindow.style.display = "none";
  }
}


searchinput.onkeyup = function() {
  if (searchinput.value.length <= maxsymbols) {
    return false;
  }
  if (globalTimeout != null) {
    clearTimeout(globalTimeout);
  }
  globalTimeout = setTimeout(function() {
    globalTimeout = null;
    /* send request for data search */
    alert(searchinput.value);
  }, 300);
}