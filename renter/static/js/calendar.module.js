class Calendar {
    constructor(container_id) {
        this._container = document.getElementById(container_id);
        if(!this._container) { throw `DOM element #${container_id} not found`; }
        const date = new Date();
        this._year = date.getFullYear();
        this._month = date.getMonth() + 1;
        this.update();
        if(window.calendar_events) {
            window.calendar_events.update(this._year, this._month, date.getDate());
        }
    }

    update() {
        const date = new Date();
        dj_load_partial_view("partial_calendar", {year: this._year, month: this._month}, {year: date.getFullYear(), month: date.getMonth() + 1, day: date.getDate()}).then(
            html => { this._container.innerHTML = html; }
        );
    }

    prev_month() {
        if (--this._month == 0) {
            this._month = 12;
            this._year--;
        }
        this.update();
    }

    next_month() {
        if (++this._month == 13) {
            this._month = 1;
            this._year++;
        }
        this.update();
    }

    day_click(y, m, d) {
        if(window.calendar_events) {
            window.calendar_events.update(y, m, d);
        }
    }
}

export { Calendar };