class UserActions {
    constructor(dialog_id) {
        this._dialog = document.getElementById(dialog_id);
        if(!this._dialog) { throw `DOM element #${dialog_id} not found`; }
    }

    __action__(action) {
        dj_load_partial_view("partial_user_action", {}, action).then(
            html => {
                this._dialog.getElementsByTagName("section").item(0).innerHTML = html;
                this._dialog.showModal();
                this._dialog.style.opacity = "1.0";
            }
        );
    }

    book_outlet(number) {
        this.__action__({action:"book-outlet", outlet: number});
    }

    unbook_all(number) {
        this.__action__({action:"unbook-all"});
    }

    close_dialog() {
        this._dialog.style.opacity = "0.0";
        window.setTimeout(()=>this._dialog.close(), 450);
    }
}

export { UserActions };