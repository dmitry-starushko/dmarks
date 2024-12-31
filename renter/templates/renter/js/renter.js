var menuContent = document.getElementById('leftSidebar');
var mainContent = document.getElementById('main');
var btnClose = document.getElementById('closesidebar');

{% comment %}
/*const menuContent = document.querySelector('.sidebarMenuInner'); // Selects the element with the class sidebarMenuInner and save into the class menuContent
content.classList.add("display-none") // add the class display-none to the content so it will not be displayed before clicking in the menu
let menuClick = document.querySelector('.sidebarIconToggle') // select the sidebarIconToggle and save into menuClick*/
{% endcomment %}

btnClose.addEventListener('click', () => { // start an event listener to the menuClick button to wait for a click
  if(!menuContent.classList.contains("display-none")) {
  menuContent.style.width = '55px';
  mainContent.style.marginLeft = "55px";
  }
  else  {
    menuContent.style.width = '270px';
    mainContent.style.marginLeft = "270px";
  }
  menuContent.classList.toggle("display-none"); // toggle the class display-none according to the user click
})

window.calendar_events = new Notifications("calendar-events", 1);
window.calendar = new Calendar("calendar-container");
