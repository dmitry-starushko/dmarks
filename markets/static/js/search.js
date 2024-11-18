
var searchbtn = document.getElementById('search-btn');
var searchwindow = document.getElementById('search-market-window');

/*searchbtn.addEventListener('click', function() {
    //searchwindow.classList.toggle('hide');
    alert('123');
});*/

//Choose markets level window

// Get the modal
/*var modal = document.getElementById("market-level-window");

// Get the button that opens the modal
var btn = document.getElementById("mk-level");*/

// Get the <span> element that closes the modal
var closebtn = document.getElementById("search-close");

// When the user clicks on the button, open the modal
searchbtn.onclick = function() {
  searchwindow.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
closebtn.onclick = function() {
  searchwindow.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == searchwindow) {
    searchwindow.style.display = "none";
  }

}