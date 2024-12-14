class OutletFilters {
    constructor() {
    }

    build_json() {
        const checkboxes_2s = document.querySelectorAll("input:not([name='tricheckbox'])[type='checkbox'][role='outlet-filter']");
        const checkboxes_3s = document.querySelectorAll("input[name='tricheckbox'][type='checkbox'][role='outlet-filter']");
        const ranges = document.querySelectorAll("input[type='range'][role='outlet-filter']");
        const filters = {
            outlet_states: [],
            specializations: [],
            facilities: {},
            price_range: {},
            area_range: {}
        };
        // fill filters here
        return JSON.stringify(filters);
    }
}

export {OutletFilters};