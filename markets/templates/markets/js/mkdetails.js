    // Query the element
    const resizer = document.getElementById('dragSlide');
    const leftSide = resizer.previousElementSibling;
    const rightSide = resizer.nextElementSibling;
    const resizerTP = document.getElementById('dragSlideTP');

    // The current position of mouse
    let x = 0;
    let y = 0;
    let leftWidth = 0;

    // Handle the mousedown event
    // that's triggered when user drags the resizer
    const mouseDownHandler = function (e) {
        // Get the current mouse position
        x = e.clientX;
        y = e.clientY;
        leftWidth = leftSide.getBoundingClientRect().width;

        // Attach the listeners to document
        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
    };

    const mouseMoveHandler = function (e) {
        // How far the mouse has been moved
        const dx = e.clientX - x;
        const dy = e.clientY - y;

        const newLeftWidth = ((leftWidth + dx) * 100) / resizer.parentNode.getBoundingClientRect().width;
        leftSide.style.width = newLeftWidth + '%';

        resizer.style.cursor = 'col-resize';
        document.body.style.cursor = 'col-resize';

        leftSide.style.userSelect = 'none';
        leftSide.style.pointerEvents = 'none';

        rightSide.style.userSelect = 'none';
        rightSide.style.pointerEvents = 'none';
    };

    const mouseUpHandler = function () {
        resizer.style.removeProperty('cursor');
        document.body.style.removeProperty('cursor');

        leftSide.style.removeProperty('user-select');
        leftSide.style.removeProperty('pointer-events');

        rightSide.style.removeProperty('user-select');
        rightSide.style.removeProperty('pointer-events');

        // Remove the handlers of mousemove and mouseup
        document.removeEventListener('mousemove', mouseMoveHandler);
        document.removeEventListener('mouseup', mouseUpHandler);
    };

    // Attach the handler
    resizer.addEventListener('mousedown', mouseDownHandler);



    var mkdetailsinfo = document.getElementById('mkdetails-section-info');
    var rightPanel = document.getElementById('mkdetails-tp-section-info-detail');
    var tabsSection = document.getElementById('mkdetails-tabs-section');

    var tpTab = document.getElementById('mkdetails-tp-tab');
    var schemeTab = document.getElementById('mkdetails-scheme-tab');
    var sectionTabs = document.getElementById('mkdetails-section-tabs');
    var mkdetailscontent = document.getElementById('market-details-content');
    var mkdetailsection = document.getElementById('market-details-section');


    document.getElementById('mkdetails-info').addEventListener("click", () =>
    {
        mkdetailsinfo.style.display = "flex";
        sectionTabs.style.display = "none";
    });

    document.getElementById('mkdetails-tp').addEventListener("click", () =>
    {
        mkdetailsinfo.style.display = "none";
        sectionTabs.style.display = "flex";
        tpTab.style.display = "flex";
        schemeTab.style.display = "none";
    });

    document.getElementById('mkdetails-scheme').addEventListener("click", () =>
    {
        mkdetailsinfo.style.display = "none";
        sectionTabs.style.display = "flex";
        tpTab.style.display = "none";
        schemeTab.style.display = "flex";
    });

    const fullscr = () => {
      if (document.fullscreenElement) {
        // If there is a fullscreen element, exit full screen.
        /*mkdetailscontent.style.minHeight = "calc(100vh - 300px)";
        mkdetailsection.style.padding = "20px 0";*/
        document.exitFullscreen();
        return;
      }
      // Make the .element div fullscreen.
      mkdetailsection.requestFullscreen();
      /*mkdetailsection.style.padding = "0";
      mkdetailscontent.style.minHeight = "90%";*/
    }

    document.querySelector("#mkdetails-fullscreen").addEventListener("click", function (event) {
        fullscr();
      /*if (document.fullscreenElement) {
        // If there is a fullscreen element, exit full screen.
        mkdetailscontent.style.minHeight = "calc(100vh - 300px)";
        mkdetailsection.style.padding = "20px 0";
        document.exitFullscreen();
        return;
      }
      // Make the .element div fullscreen.
      mkdetailsection.requestFullscreen();
      mkdetailsection.style.padding = "0";
      mkdetailscontent.style.minHeight = "90%";*/
    });

    /*document.addEventListener("fullscreenchange", function (event) {
        if (event.keyCode === 27) {
            alert('555');
        }
        //alert('6');
    });*/

    /*if (document.addEventListener) {
        document.addEventListener('fullscreenchange', fullscr, false);
        document.addEventListener('mozfullscreenchange', fullscr, false);
        document.addEventListener('MSFullscreenChange', fullscr, false);
        document.addEventListener('webkitfullscreenchange', fullscr, false);
        }*/


//document.addEventListener("fullscreenchange", alert('www'));
/*document.addEventListener('webkitfullscreenchange', alert('www'));
document.addEventListener('mozfullscreenchange', alert('www'));
document.addEventListener('MSFullscreenChange', alert('www'));*/

    /** Checks for keypresses on the dom */
/*document.addEventListener("keydown", function (event) {
    if (event.keyCode === 27) {
    alert('555');
    }
    alert(event.keyCode);
});*/

/*document.addEventListener(
  "keydown",
  (e) => {
    if (e.key === "Enter") {
      //alert(e.key);
    }
    alert(e.key);
  },
  false,
);*/


function toggleItem(elem) {
  for (var i = 0; i < elem.length; i++) {
    elem[i].addEventListener("click", function(e) {
      var current = this;
      for (var i = 0; i < elem.length; i++) {
        if (current != elem[i]) {
          elem[i].classList.remove('active');
        } else {
          current.classList.add('active')
        }
      }
      e.preventDefault();
    });
  };
}

toggleItem(document.querySelectorAll('.buttons-tab'));

/***** sorting table ******/

var tableHeaderItems = document.querySelectorAll('td.sort-th');

for (var i = 0; i < tableHeaderItems.length; i++) {
      tableHeaderItems[i].onclick = function(e) {
       alert(i + e.target.getAttribute("sort"));
    }
  }
