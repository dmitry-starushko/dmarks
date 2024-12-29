class Calendar {
    constructor(container_id) {
        this._container = document.getElementById(container_id);
        if(!this._container) { throw `DOM element #${container_id} not found`; }
        const date = new Date();
        this._year = date.getFullYear();
        this._month = date.getMonth() + 1;
        this.update();
    }

    update() {
        const date = new Date();
        dj_load_partial_view("partial_calendar", {year: this._year, month: this._month}, {year: date.getFullYear(), month: date.getMonth() + 1, day: date.getDate()}).then(
            html => { this._container.innerHTML = html; }
        );
    }
}

export { Calendar };