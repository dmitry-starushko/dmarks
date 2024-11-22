var searchbtn = document.getElementById('search-btn');
var searchwindow = document.getElementById('search-market-window');
var searchinput = document.getElementById('search-market-input');
var globalTimeout = null;
var min_symbols = 3;
var closebtn = document.getElementById("search-close");
const search_result = document.getElementById("search-market-result");

searchbtn.onclick = function() {
  searchwindow.style.display = "block";
  searchinput.focus();
}

closebtn.onclick = function() {
  searchwindow.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == searchwindow) {
    searchwindow.style.display = "none";
  }
}

searchinput.onkeyup = () => {
    if(globalTimeout) {
        clearTimeout(globalTimeout);
        globalTimeout = null;
    }
    const text = searchinput.value;
    if (text.length >= min_symbols) {
        globalTimeout = setTimeout(() => {
            globalTimeout = null;
            dj_load_partial_view("partial_filtered_markets", {}, {search_text: text})
                .then(html => {search_result.innerHTML = html;});
        }, 1000);
    }
}