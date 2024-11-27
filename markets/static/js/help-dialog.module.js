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
            this._dialog.showModal();
        }
    }
}

export { HelpDialog };