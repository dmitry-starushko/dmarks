async function copy_absolute_url_by_id(link_id) {
    if (navigator.clipboard) {
    const link_element = document.getElementById(link_id);
        if (!link_element) { throw new Error(`Элемент с id "${link_id}" не найден.`); }
        const relative_link = link_element.getAttribute("href");
        const absolute_url = new URL(relative_link, window.location.href).toString();
        await navigator.clipboard.writeText(absolute_url);
    } else {
        alert(`Упс, кажется, ваш браузер не поддерживает работу с буфером обмена.
Не переживайте! Просто скопируйте ссылку вручную — это займет всего пару секунд.
Спасибо за понимание!`);
    }
}