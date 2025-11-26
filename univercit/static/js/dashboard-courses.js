const selectAll = document.getElementById("dasshboard-course-select-all");
const courseCheckboxes = document.querySelectorAll(".dashboard-course-checkbox");
const removeCourse = document.getElementById("remove-course");
const deleteModal = document.getElementById("delete_modal");
const selectedCourseToDelete = document.getElementById("selected-course-delete")
const hiddenDeleteInput = document.getElementById("")

let anyChecked = false;

document.addEventListener("DOMContentLoaded", () => {
    selectAll.addEventListener("change", function() {
        if (this.checked) {
            courseCheckboxes.forEach(cb => {
                cb.checked = true;
            })
        } else {
            courseCheckboxes.forEach(cb => {
                cb.checked = false;
            })
        }
        updateDeleteState();
    })

    courseCheckboxes.forEach(cb => cb.addEventListener("change", updateDeleteState));


    removeCourse.addEventListener("click", () => deleteModal.showModal())
})


function updateDeleteState() {
    const selected = Array.from(courseCheckboxes)
                        .filter(cb => cb.checked)
                        .map(cb => cb.value);

    selectedCourseToDelete.value = selected.join(',');

    const anyChecked = Array.from(courseCheckboxes).some(cb => cb.checked);

    removeCourse.disabled = !anyChecked;
    removeCourse.classList.toggle("bg-red-200", anyChecked);
    removeCourse.classList.toggle("btn-disabled", anyChecked);
    removeCourse.classList.toggle("bg-red-200", !anyChecked);
    removeCourse.classList.toggle("btn-disabled", !anyChecked);
}