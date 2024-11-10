<script>
__csrf_token__ = Cookies.get('csrftoken');
async function dj_reverse(path_name, args) {
    return await (await fetch(
        "{% url 'api:info_take_path' %}", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': __csrf_token__,
            },
            body: JSON.stringify({
                path_name: path_name,
                args: args
            })
        }
    )).json();
}
</script>