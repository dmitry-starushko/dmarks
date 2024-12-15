var searchbtn = document.getElementById('search-btn');
var searchwindow = document.getElementById('search-market-window');
var searchinput = document.getElementById('search-market-input');
var globalTimeout = null;
var min_symbols = 3;
var closebtn = document.getElementById("search-close");
const search_result = document.getElementById("search-market-result");

searchbtn.onclick = function() {
    dj_load_partial_view("partial_outlet_filters", {full: 1}, {}).then(html => { document.getElementById("outlet-search-top").innerHTML=html; });
    searchwindow.style.display = "block";
    searchinput.focus();
}

closebtn.onclick = function() {
  searchwindow.style.display = "none";
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
            dj_load_partial_view("partial_filtered_markets", {}, {search_text: text})
                .then(html => {search_result.innerHTML = html;});
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

/**** Range input price ****/
const rangeInput = document.querySelectorAll(".search-tp-price-range-input input"),
  priceInput = document.querySelectorAll(".search-tp-price-inputs input"),
  range = document.querySelector(".search-tp-price-slider .search-tp-price-progress");
let priceGap = 500;
//alert((minVal / rangeInput[0].max) * 100 + "%");
const initMin = parseInt(priceInput[0].value);
const initMax = parseInt(priceInput[1].value);
range.style.left = (initMin / rangeInput[0].max) * 100 + "%";

priceInput.forEach((input) => {
  input.addEventListener("input", (e) => {
    let minPrice = parseInt(priceInput[0].value),
      maxPrice = parseInt(priceInput[1].value);
    if (maxPrice - minPrice >= priceGap && maxPrice <= rangeInput[1].max) {
      if (e.target.className === "search-tp-input-price-min") {
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
const rangeAreaInput = document.querySelectorAll(".search-tp-area-range-input input"),
  areaInput = document.querySelectorAll(".search-tp-area-inputs input"),
  rangeArea = document.querySelector(".search-tp-area-slider .search-tp-area-progress");
let priceAreaGap = 500;

const initMinArea = parseInt(areaInput[0].value);
const initMaxArea = parseInt(areaInput[1].value);
rangeArea.style.left = (initMinArea / rangeAreaInput[0].max) * 100 + "%";
rangeArea.style.right = 100 - (initMaxArea / rangeAreaInput[1].max) * 100 + "%";

areaInput.forEach((input) => {
  input.addEventListener("input", (e) => {
    let minArea = parseInt(areaInput[0].value),
      maxArea = parseInt(areaInput[1].value);
    if (maxArea - minArea >= priceAreaGap && maxArea <= rangeAreaInput[1].max) {
      if (e.target.className === "search-tp-input-area-min") {
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
  const states = ['true', 'null', 'false']

  const i = states.indexOf(e.target.value) + 1
  e.target.value = i < states.length ? states[i] : states[0]
  switch(e.target.value) {
    case states[0]:
      e.target.checked = true
      break
    case states[1]:
      e.target.indeterminate = true
      break
    default:
      e.target.checked = false
  }

  // Sadly, e.target.value is coerced to string
  //console.log(typeof e.target.value)
}

/*document.querySelectorAll('input[name=tricheckbox]').onclick = tristateHandler*/

var triStateInputs = document.querySelectorAll('input[name=tricheckbox]')
for (i = 0; i < triStateInputs.length; i++) {
  triStateInputs[i].addEventListener('click', function(e) {
    tristateHandler(e);
  });
}


/****  Tree checkbox ******/