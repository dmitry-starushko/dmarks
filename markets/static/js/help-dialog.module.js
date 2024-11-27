class HelpDialog {
    constructor(dialog_id, help_id) {
        this._dialog = document.getElementById(dialog_id);
        this._help_id = help_id;
        if(!this._dialog) { throw `DOM element #${dialog_id} not found`; }
        this._state = "closed"
        this._dialog.addEventListener("toggle", e => { this._state = e.newState; });
    }

    toggle() {
        if(this._state == "open") {
            this._dialog.close();
        } else {
            dj_load_partial_view("partial_help_content", {hid: this._help_id}, {}).then(
                html => {
                    debugger;
                    this._dialog.getElementsByTagName("section").item(0).innerHTML = html;
                    this._dialog.showModal();
                }
            );
        }
    }
}

export { HelpDialog };