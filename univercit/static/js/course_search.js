document.addEventListener("DOMContentLoaded", () => {
    const search_input = document.getElementById("course-search")
    const container = document.getElementById("courses-container")
    const search_form = document.getElementById("search-form")

    if (!search_input) return;

    let timeout;   

    search_form.addEventListener("submit", function(e) {
        e.preventDefault();
    });

    search_input.addEventListener("input", function() {
        clearTimeout(timeout);
        const query = this.value

        timeout = setTimeout(() => {
            fetch(`?query=${encodeURIComponent(query)}`)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newCourses = doc.getElementById('courses-container');
                    container.innerHTML = newCourses.innerHTML;
                })
                .catch(err => console.error(err));
        }, 300);
    })
})