window.calendar = new Calendar("calendar-container");

function sidebar_open() {
  document.getElementById("main").style.marginLeft = "25%";
  document.getElementById("leftSidebar").style.width = "25%";
  document.getElementById("leftSidebar").style.display = "block";
  document.getElementById("openNav").style.display = 'none';
}
function side_close() {
  document.getElementById("main").style.marginLeft = "0%";
  document.getElementById("leftSidebar").style.display = "none";
  document.getElementById("openNav").style.display = "inline-block";
}