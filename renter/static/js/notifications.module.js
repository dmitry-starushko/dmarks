class Notifications {
    constructor(container_id, calendar) {
        this._container = document.getElementById(container_id);
        if(!this._container) { throw `DOM element #${container_id} not found`; }
        this._calendar = calendar;
        const date = new Date();
        this.update(date.getFullYear(), date.getMonth() + 1, date.getDate());
    }

    update(year, month, day) {
        dj_load_partial_view("partial_notifications", {year: year, month: month, day: day, calendar: this._calendar}, {}).then(
            html => { this._container.innerHTML = html; }
        );
    }
}

export { Notifications };