class TsChat {
    constructor(ts_chat_id) {
        this._element = document.getElementById(this._chat_id = ts_chat_id);
        if(!this._element) { throw `DOM element #${parent_id} not found`; }
    }

    toggle() {
        this._element.classList.toggle("active");
    }
}

export { TsChat };