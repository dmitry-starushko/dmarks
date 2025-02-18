var searchbtn = document.getElementById('search-btn');
var searchwindow = document.getElementById('search-market-window');
var searchinput = document.getElementById('search-market-input');
var globalTimeout = null;
var min_symbols = 3;
var closebtn = document.getElementById("search-close");
const search_result = document.getElementById("search-market-result");
const outlet_search_result = document.getElementById("outlet-search-result");

const clear_search_controls = () => {
    searchinput.value = "";
    search_result.innerHTML = "";
    outlet_search_result.innerHTML = "";
};

if (searchbtn !== null) {
    searchbtn.onclick = function() {
        dj_load_partial_view("partial_outlet_filters", {full: 1}, {}).then(html => {
            document.getElementById("outlet-search-top").innerHTML=html;
            window.setup_outlet_search();
        });
        clear_search_controls();
        searchwindow.style.display = "block";
        searchinput.focus();
    }
}

closebtn.onclick = function() {
  searchwindow.style.display = "none";
  window.setTimeout(clear_search_controls);
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
            document.querySelector(".search-market-top > img").classList.add("pulsation");
            if(searchinput.abort_controller) searchinput.abort_controller.abort('obsolete');
            searchinput.abort_controller = new AbortController();
            dj_load_partial_view("partial_filtered_markets", {}, {search_text: text}, searchinput.abort_controller.signal)
                .then(html => {
                    searchinput.abort_controller = null;
                    search_result.innerHTML = html;
                    document.querySelector(".search-market-top > img").classList.remove("pulsation");
                });
        }, 1000);
    }
}

var searchmkbtn = document.getElementById('search-market-btn');
var searchtpbtn = document.getElementById('search-tp-btn');
var searchmksection = document.getElementById('search-section-market');
var searchtpsection = document.getElementById('search-section-tp');

searchmkbtn.onclick = function() {

  searchmksection.style.display = "block";
  searchtpsection.style.display = "none";
}

searchtpbtn.onclick = function() {
  searchtpsection.style.display = "block";
  searchmksection.style.display = "none";
}

const barOuter = document.querySelector(".bar-outer");
const options = document.querySelectorAll(".bar-grey .option");
let current = 1;
options.forEach((option, i) => (option.index = i + 1));
options.forEach(option =>
                option.addEventListener("click", function() {
  barOuter.className = "bar-outer";
  barOuter.classList.add(`pos${option.index}`);
  if (option.index > current) {
    barOuter.classList.add("right");
  } else if (option.index < current) {
    barOuter.classList.add("left");
  }
  current = option.index;
}));

window.setup_outlet_search = () => {
    /**** Range input price ****/
    const rangeInput = document.querySelectorAll(".search-tp-price-range-input input");
    const priceInput = document.querySelectorAll(".search-tp-price-inputs input");
    const range = document.querySelector(".search-tp-price-slider .search-tp-price-progress");
    let priceGap = 1;
    const initMin = parseInt(priceInput[0].value);
    const initMax = parseInt(priceInput[1].value);
    range.style.left = (initMin / rangeInput[0].max) * 100 + "%";
    range.style.right = 100 - (initMax / rangeInput[1].max) * 100 + "%";

    priceInput.forEach((input) => {
      input.addEventListener("input", (e) => {
        let minPrice = parseInt(priceInput[0].value),
          maxPrice = parseInt(priceInput[1].value);
        if (maxPrice - minPrice >= priceGap && maxPrice <= rangeInput[1].max) {
          if (e.target.classList.contains("search-tp-input-price-min")) {
            rangeInput[0].value = minPrice;
            range.style.left = (minPrice / rangeInput[0].max) * 100 + "%";
          } else {
            rangeInput[1].value = maxPrice;
            range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
          }
        }
      });
    });

    rangeInput.forEach((input) => {
      input.addEventListener("input", (e) => {
        let minVal = parseInt(rangeInput[0].value),
          maxVal = parseInt(rangeInput[1].value);
        if (maxVal - minVal < priceGap) {
          if (e.target.className === "search-tp-price-range-min") {
            rangeInput[0].value = maxVal - priceGap;
          } else {
            rangeInput[1].value = minVal + priceGap;
          }
        } else {
          priceInput[0].value = minVal;
          priceInput[1].value = maxVal;
          range.style.left = (minVal / rangeInput[0].max) * 100 + "%";
          range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
      });
    });

    /**** Range input area ****/
    const rangeAreaInput = document.querySelectorAll(".search-tp-area-range-input input");
    const areaInput = document.querySelectorAll(".search-tp-area-inputs input");
    const rangeArea = document.querySelector(".search-tp-area-slider .search-tp-area-progress");
    let priceAreaGap = 1;

    const initMinArea = parseInt(areaInput[0].value);
    const initMaxArea = parseInt(areaInput[1].value);
    rangeArea.style.left = (initMinArea / rangeAreaInput[0].max) * 100 + "%";
    rangeArea.style.right = 100 - (initMaxArea / rangeAreaInput[1].max) * 100 + "%";

    areaInput.forEach((input) => {
      input.addEventListener("input", (e) => {
        let minArea = parseInt(areaInput[0].value),
          maxArea = parseInt(areaInput[1].value);
        if (maxArea - minArea >= priceAreaGap && maxArea <= rangeAreaInput[1].max) {
        if (e.target.classList.contains("search-tp-input-area-min")) {
            rangeAreaInput[0].value = minArea;
            rangeArea.style.left = (minArea / rangeAreaInput[0].max) * 100 + "%";
          } else {
            rangeAreaInput[1].value = maxArea;
            rangeArea.style.right = 100 - (maxArea / rangeAreaInput[1].max) * 100 + "%";
          }
        }
      });
    });

    rangeAreaInput.forEach((input) => {
      input.addEventListener("input", (e) => {
        let minAreaVal = parseInt(rangeAreaInput[0].value),
          maxAreaVal = parseInt(rangeAreaInput[1].value);
        if (maxAreaVal - minAreaVal < priceAreaGap) {
          if (e.target.className === "search-tp-area-range-min") {
            rangeAreaInput[0].value = maxAreaVal - priceAreaGap;
          } else {
            rangeAreaInput[1].value = minAreaVal + priceAreaGap;
          }
        } else {
          areaInput[0].value = minAreaVal;
          areaInput[1].value = maxAreaVal;
          rangeArea.style.left = (minAreaVal / rangeAreaInput[0].max) * 100 + "%";
          rangeArea.style.right = 100 - (maxAreaVal / rangeAreaInput[1].max) * 100 + "%";
        }
      });
    });


    /***** Tristate checkbox ******/
    function tristateHandler(e) {
      const states = ['null', 'true', 'false']

      const i = (states.indexOf(e.target.value) + 1) % states.length;
      e.target.value = states[i];
      switch(i) {
        case 0:
          e.target.indeterminate = true
          break
        case 1:
          e.target.checked = true
          break
        case 2:
          e.target.checked = false
          break
      }
    }

    for (const cb of document.querySelectorAll('input[name=tricheckbox]')) {
      cb.value = 'null'
      cb.indeterminate = true;
      cb.addEventListener('click', function(e) {
        tristateHandler(e);
      });
    }

    var loccheckboxes = document.querySelectorAll('input.tploc');

  for (var i = 0; i < loccheckboxes.length; i++) {
      loccheckboxes[i].onclick = function(e) {

      var root = e.target.closest("li.parent");
      var mainroot = root.closest('ul').closest("li.parent");
      var children = e.target.closest("li").querySelectorAll("input.tpnode");
      var checkedCount = root.querySelectorAll("ul")[0].querySelectorAll("input.tpnode").length;

      for (var i = 0; i < children.length; i++) {
            children[i].checked = this.checked;
        }

      root.querySelectorAll("input.tpnode")[0].checked = root.querySelectorAll("ul")[0].querySelectorAll("input.tpnode:checked").length > 0;
      root.querySelectorAll("input.tpnode")[0].indeterminate = root.querySelectorAll("ul")[0].querySelectorAll("input.tpnode:checked").length > 0 && checkedCount > root.querySelectorAll("ul")[0].querySelectorAll("input.tpnode:checked").length;

      if(mainroot !== null) {
          mainroot.querySelectorAll("input.tploc")[0].checked = mainroot.querySelectorAll("input.tpnode:checked").length > 0;
          mainroot.querySelectorAll("input.tploc")[0].indeterminate = mainroot.querySelectorAll("input.tpnode:checked").length > 0 && mainroot.querySelectorAll("input.tpnode").length > mainroot.querySelectorAll("input.tpnode:checked").length;
      }
    }
  }

    window.outlet_filters.setup_listeners();
};