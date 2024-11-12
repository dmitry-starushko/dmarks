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



    var rightPanel = document.getElementById('mkdetails-tp-section-info-detail');
    var tabsSection = document.getElementById('mkdetails-tabs-section');


    document.getElementById('mkdetails-info').addEventListener("click", () =>
    {
        rightPanel.style.visibility = "hidden";
        rightPanel.style.width = "0";
        tabsSection.style.width = "100%";
    });

    function ShowRightPanel() {
            rightPanel.style.visibility = "visible";
            rightPanel.style.width = "40%";
            tabsSection.style.width = "60%";
    };

    document.getElementById('mkdetails-tp').onclick = ShowRightPanel;
    document.getElementById('mkdetails-scheme').onclick = ShowRightPanel;

    document.querySelector("#mkdetails-fullscreen").addEventListener("click", function (event) {
      if (document.fullscreenElement) {
        // If there is a fullscreen element, exit full screen.
        document.exitFullscreen();
        return;
      }
      // Make the .element div fullscreen.
      document.querySelector(".market-details-section").requestFullscreen();
    });