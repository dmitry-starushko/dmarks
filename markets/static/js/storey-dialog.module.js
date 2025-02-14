class StoreyDialog {
    constructor(dialog_id) {
        this._dialog = document.getElementById(dialog_id);
        if(!this._dialog) { throw `DOM element #${dialog_id} not found`; }
    }

    toggle() {
        if(this._dialog.open) {
            this._dialog.style.opacity = "0.0";
            window.setTimeout(()=>this._dialog.close(), 450);
        } else {
            this._dialog.showModal();
            this._dialog.style.opacity = "1.0";
        }
    }
}

export { StoreyDialog };