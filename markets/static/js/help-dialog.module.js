class HelpDialog {
    constructor(dialog_id) {
        this._dialog = document.getElementById(dialog_id);
        if(!this._dialog) { throw `DOM element #${dialog_id} not found`; }
    }

    toggle(help_id) {
        if(this._dialog.open) {
            this._dialog.style.opacity = "0.0";
            window.setTimeout(()=>this._dialog.close(), 450);
        } else {
            dj_load_partial_view("partial_help_content", {hid: help_id}, {}).then(
                html => {
                    this._dialog.getElementsByTagName("section").item(0).innerHTML = html;
                    this._dialog.showModal();
                    this._dialog.style.opacity = "1.0";
                }
            );
        }
    }
}

export { HelpDialog };