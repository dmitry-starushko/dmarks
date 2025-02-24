class TsChat {
    constructor(ts_chat_id, path, greeting) {
        this._element = document.getElementById(this._chat_id = ts_chat_id);
        this._dialogue = document.querySelector(`#${ts_chat_id} > .tsc-dialogue`);
        this._input = document.querySelector(`#${ts_chat_id} > .tsc-input > input`);
        if(!(this._element && this._dialogue && this._input)) { throw "Unable setup chat!"; }
        this._greeting = greeting;
        this._socket = new WebSocket(this.compose_url(path));
        this.setup_events();
    }

    compose_url(path) {
        const url = new URL(path, window.location.origin);
        url.protocol = "wss";
        return url;
    }

    setup_events() {
        this._socket.onmessage = event => {this.add_phrase(JSON.parse(event.data).message, "a");};
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
        this._socket.send(JSON.stringify({'message': phrase}));
    }

    toggle() {
        if(this._element.classList.toggle("active")) {
            this._input.focus();
            if(this._greeting) {
                window.setTimeout(()=>{
                    this.add_phrase(this._greeting, "a");
                    this._greeting = null;
                }, 2000);
            }
        }
    }
}

export { TsChat };