window.calendar = new Calendar();

/***** sidebar ********/
const menuContent = document.querySelector('.sidebarMenuInner'); // Selects the element with the class sidebarMenuInner and save into the class menuContent
content.classList.add("display-none") // add the class display-none to the content so it will not be displayed before clicking in the menu
const menuClick = document.querySelector('.sidebarIconToggle') // select the sidebarIconToggle and save into menuClick
menuClick.addEventListener('click', () => { // start an event listener to the menuClick button to wait for a click
  content.classList.toggle("display-none") // toggle the class display-none according to the user click
})