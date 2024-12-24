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
window.ts_chat = new TsChat("ts-chat", "markets/ws/chat/", ("WebSocket" in window) ? "{{parm_ts_greeting}}" : "{{parm_ts_old_browser_warning}}");
window.outlet_filters = new OutletFilters();
window.help_dialog = new HelpDialog("help-dialog");
window.user_actions = new UserActions('user-dialog');
