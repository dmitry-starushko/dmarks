    const resizer = document.getElementById('dragSlide');
    const leftSide = resizer.previousElementSibling;
    const rightSide = resizer.nextElementSibling;
    const resizerTP = document.getElementById('dragSlideTP');

    let x = 0;
    let y = 0;
    let leftWidth = 0;

    const mouseDownHandler = function (e) {
        x = e.clientX;
        y = e.clientY;
        leftWidth = leftSide.getBoundingClientRect().width;
        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
    };

    const mouseMoveHandler = function (e) {
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

        document.removeEventListener('mousemove', mouseMoveHandler);
        document.removeEventListener('mouseup', mouseUpHandler);
    };

    resizer.addEventListener('mousedown', mouseDownHandler);

    var mkdetailsinfo = document.getElementById('mkdetails-section-info');
    var rightPanel = document.getElementById('mkdetails-tp-section-info-detail');
    var tabsSection = document.getElementById('mkdetails-tabs-section');
    var tpTab = document.getElementById('mkdetails-tp-tab');
    var schemeTab = document.getElementById('mkdetails-scheme-tab');
    var sectionTabs = document.getElementById('mkdetails-section-tabs');

    document.getElementById('mkdetails-info').addEventListener("click", () => {
        mkdetailsinfo.style.display = "flex";
        sectionTabs.style.display = "none";
    });

    document.getElementById('mkdetails-tp').addEventListener("click", () => {
        mkdetailsinfo.style.display = "none";
        sectionTabs.style.display = "flex";
        tpTab.style.visibility = "visible";
        tpTab.style.width = "60%";
        schemeTab.style.visibility = "hidden";
        schemeTab.style.width = "0";
        var tp_table_rows = document.querySelectorAll('tr.table-tp-row');
        scrollItem(tp_table_rows);
    });

    document.getElementById('mkdetails-scheme').addEventListener("click", () => {
        mkdetailsinfo.style.display = "none";
        sectionTabs.style.display = "flex";
        tpTab.style.visibility = "hidden";
        tpTab.style.width = "0";
        schemeTab.style.visibility = "visible";
        schemeTab.style.width = "60%";
    });

function scrollItem(rows){
    for (const tr of rows) {
        if(tr.classList.contains('selected')) {
            tr.scrollIntoView({
                behavior: 'auto',
                block: 'center'
            });
            break;
        }
    }
}

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