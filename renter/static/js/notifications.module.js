class Notifications {
    constructor(container_id) {
        this._container = document.getElementById(container_id);
        if(!this._container) { throw `DOM element #${container_id} not found`; }
    }
}

export { Notifications };