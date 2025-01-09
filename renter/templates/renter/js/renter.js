var menuContent = document.getElementById('leftSidebar');
var mainContent = document.getElementById('main');
var btnClose = document.getElementById('closesidebar');

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

window.messages = new Notifications("messages-container", 0);
window.calendar_events = new Notifications("calendar-events", 1);
window.calendar = new Calendar("calendar-container");
window.reg_card = new RegCard("reg-card-container");
window.ts_chat = new TsChat("ts-chat", "markets/ws/chat/", ("WebSocket" in window) ? "{{parm_ts_greeting}}" : "{{parm_ts_old_browser_warning}}");
window.help_dialog = new HelpDialog("help-dialog");
