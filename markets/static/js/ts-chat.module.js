class TsChat {
    constructor(ts_chat_id, greeting) {
        this._element = document.getElementById(this._chat_id = ts_chat_id);
        this._dialogue = document.querySelector(`#${ts_chat_id} > .tsc-dialogue`);
        this._input = document.querySelector(`#${ts_chat_id} > .tsc-input > input`);
        if(!(this._element && this._dialogue && this._input)) { throw "Unable initiate chat!"; }

        this._greeting = greeting;
        this._input.addEventListener("keypress", event => {
            if(event.key=="Enter") {
                event.preventDefault();
                const phrase = this._input.value.trim();
                this._input.value = "";
                this.add_phrase(phrase, "q");
                this.send_phrase(phrase);
            }
        });
    }

    add_phrase(phrase, side) {
        if(phrase) {
            const p = document.createElement("p");
            p.classList += side;
            p.innerText = phrase;
            this._dialogue.appendChild(p);
            p.scrollIntoView(false);
        }
    }

    send_phrase(phrase) {
    }

    toggle() {
        if(this._element.classList.toggle("active")) {
            this._input.focus();
            if(this._greeting) {
                window.setTimeout(()=>{
                    this.add_phrase(this._greeting, "a");
                    this._greeting = null;
                }, 3000);
            }
        }
    }
}

export { TsChat };