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


    document.getElementById('mkdetails-info').addEventListener("click", () =>
    {
        mkdetailsinfo.style.display = "flex";
        sectionTabs.style.display = "none";
        /*rightPanel.style.visibility = "hidden";
        /*rightPanel.style.width = "0";
        tabsSection.style.width = "100%";*/
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


    /*function ShowRightPanel() {
            mkdetailsinfo.style.display = "none";
            sectionTabs.style.display = "flex";
            rightPanel.style.visibility = "visible";
            rightPanel.style.width = "40%";
            tabsSection.style.width = "60%";
    };

    document.getElementById('mkdetails-tp').onclick = ShowRightPanel;
    document.getElementById('mkdetails-scheme').onclick = ShowRightPanel;*/

    document.querySelector("#mkdetails-fullscreen").addEventListener("click", function (event) {
      if (document.fullscreenElement) {
        // If there is a fullscreen element, exit full screen.
        document.exitFullscreen();
        return;
      }
      // Make the .element div fullscreen.
      document.querySelector(".market-details-section").requestFullscreen();
    });


function toggleItem(elem) {
  for (var i = 0; i < elem.length; i++) {
    elem[i].addEventListener("click", function(e) {
      var current = this;
      for (var i = 0; i < elem.length; i++) {
        if (current != elem[i]) {
          elem[i].classList.remove('active');
        } /*else if (current.classList.contains('active') === true) {
          current.classList.remove('active');
        }*/ else {
          current.classList.add('active')
        }
      }
      e.preventDefault();
    });
  };
}

toggleItem(document.querySelectorAll('.buttons-tab'));

/***** sorting table ******/

/*function compareValues(a, b) {
  // return -1/0/1 based on what you "know" a and b
  // are here. Numbers, text, some custom case-insensitive
  // and natural number ordering, etc. That's up to you.
  // A typical "do whatever JS would do" is:
  return (a<b) ? -1 : (a>b) ? 1 : 0;
}

function sortTable(colnum) {
  // get all the rows in this table:
  let rows = Array.from(table.querySelectorAll(`tr`));

  // but ignore the heading row:
  rows = rows.slice(1);

  // set up the queryselector for getting the indicated
  // column from a row, so we can compare using its value:
  let qs = `td:nth-child(${colnum})`;

  // and then just... sort the rows:
  rows.sort( (r1,r2) => {
    // get each row's relevant column
    let t1 = r1.querySelector(qs);
    let t2 = r2.querySelector(qs);

    // and then effect sorting by comparing their content:
    return compareValues(t1.textContent,t2.textContent);
  });

  // and then the magic part that makes the sorting appear on-page:
  rows.forEach(row => table.appendChild(row));
}

const table = document.getElementById('mkdetails-tp-table');
if (table !== null) {
    table.querySelectorAll('.sort-th').forEach((th, position) => {
    alert('123');
      th.addEventListener('click', evt => sortTable(position));
    });
}*/

/*const headers = table.querySelectorAll('.sort-th');
const tableBody = table.querySelector('tbody');
const rows = tableBody.querySelectorAll('tr');

// Track sort directions
const directions = Array.from(headers).map(function (header) {
    return '';
});

// Transform the content of given cell in given column
const transform = function (index, content) {
    // Get the data type of column
    const type = headers[index].getAttribute('data-type');
    switch (type) {
        case 'number':
            return parseFloat(content);
        case 'string':
        default:
            return content;
    }
};

const sortColumn = function (index) {
    // Get the current direction
    const direction = directions[index] || 'asc';

    // A factor based on the direction
    const multiplier = direction === 'asc' ? 1 : -1;

    const newRows = Array.from(rows);

    newRows.sort(function (rowA, rowB) {
        const cellA = rowA.querySelectorAll('td')[index].innerHTML;
        const cellB = rowB.querySelectorAll('td')[index].innerHTML;

        const a = transform(index, cellA);
        const b = transform(index, cellB);

        switch (true) {
            case a > b:
                return 1 * multiplier;
            case a < b:
                return -1 * multiplier;
            case a === b:
                return 0;
        }
    });

    // Remove old rows
    [].forEach.call(rows, function (row) {
        tableBody.removeChild(row);
    });

    // Reverse the direction
    directions[index] = direction === 'asc' ? 'desc' : 'asc';

    // Append new row
    newRows.forEach(function (newRow) {
        tableBody.appendChild(newRow);
    });
};

[].forEach.call(headers, function (header, index) {
    header.addEventListener('click', function () {
        sortColumn(index);
    });
});*/

/*var mkdetailtabs = document.querySelectorAll('.buttons-tab')
for (i = 0; i < mkdetailtabs.length; i++) {
  mkdetailtabs[i].addEventListener('click', function(e) {
  alert('213');
      var current = this;
      for (var i = 0; i < mkdetailtabs.length; i++) {
        if (current != mkdetailtabs[i]) {
          mkdetailtabs[i].classList.remove('active');
        } else if (current.classList.contains('active') === true) {
          current.classList.remove('active');
        } else {
          current.classList.add('active')
        }
      }
      e.preventDefault();
  });
}*/

/*document.querySelectorAll('.buttons-tab').addEventListener("click", function (event) {
  toggleItem(event);
});*/