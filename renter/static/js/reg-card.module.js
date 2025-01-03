class RegCard {
    constructor(container_id) {
        this._container = document.getElementById(container_id);
        if(!this._container) { throw `DOM element #${container_id} not found`; }
        this.update();
    }

    update() {
        dj_load_partial_view("partial_reg_card", {}, {}).then(
            html => { this._container.innerHTML = html; }
        );
    }
}

export { RegCard };