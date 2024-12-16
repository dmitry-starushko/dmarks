class OutletFilters {
    constructor() {
    }

    build_filters() {
        const checkboxes_2s = document.querySelectorAll("input[type='checkbox'][data-flag='outlet-filter-2s']");
        const checkboxes_3s = document.querySelectorAll("input[type='checkbox'][data-flag='outlet-filter-3s']");

        const filters = {
            'markets': [],
            'occupation-types': [],
            'specializations': [],
            'facilities': {},
        };

        for(const cb of checkboxes_2s) {
            const kind = cb.getAttribute('data-kind');
            const pk = cb.getAttribute('data-pk');
            const chk = cb.checked;
            if(kind !== null && pk !== null && chk) { filters[kind].push(parseInt(pk)); }
        }

        for(const cb of checkboxes_3s) {
            const kind = cb.getAttribute('data-kind');
            const pk = cb.getAttribute('data-pk');
            let val = cb.getAttribute('value');
            val = val !== 'null'? (val === 'true') : null;
            if(kind !== null && pk !== null && val !== null) { filters[kind][pk] = val; }
        }

        const price_slider_min = document.getElementById('price-range-min');
        const price_slider_max = document.getElementById('price-range-max');
        if(price_slider_min && price_slider_max) {
            const p_min = parseInt(price_slider_min.value);
            const p_max = parseInt(price_slider_max.value);
            if(p_min <= p_max) {
                filters['price-range'] = {
                    min: p_min,
                    max: p_max
                }
            }
        }

        const area_slider_min = document.getElementById('area-range-min');
        const area_slider_max = document.getElementById('area-range-max');
        if(area_slider_min && area_slider_max) {
            const a_min = parseInt(area_slider_min.value);
            const a_max = parseInt(area_slider_max.value);
            if(a_min <= a_max) {
                filters['area-range'] = {
                    min: a_min,
                    max: a_max
                }
            }
        }

        const o_num = document.getElementById('search-tp-input-num').value;
        if(o_num) { filters['outlet-number'] = o_num; }
        return filters;
    }

    update_search_result(container_id) {
        console.log(this.build_filters());
    }
}

export {OutletFilters};