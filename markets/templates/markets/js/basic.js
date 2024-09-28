function click_footer() {
    if (document.getElementById("footer-collapse").classList.contains("show")) {
        document.getElementById("footer-collapse").classList.remove("show")
    }
    else {
        document.getElementById("footer-collapse").classList.add("show")
    }
    document.getElementById("close-footer").hidden = !document.getElementById("close-footer").hidden;
};

document.getElementById('about-btn').onclick = click_footer;
document.getElementById('close-footer').onclick = click_footer;
