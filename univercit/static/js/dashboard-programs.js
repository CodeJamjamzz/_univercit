const selectAll = document.getElementById("dasshboard-program-select-all");
const courseCheckboxes = document.querySelectorAll(".dashboard-program-checkbox");
const removeProgram = document.getElementById("remove-program");
const deleteModal = document.getElementById("delete-modal");
const selectedProgramToDelete = document.getElementById("selected-program-delete")

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


    removeProgram.addEventListener("click", () => deleteModal.showModal())
})


function updateDeleteState() {
    const selected = Array.from(courseCheckboxes)
                        .filter(cb => cb.checked)
                        .map(cb => cb.value);

    selectedProgramToDelete.value = selected.join(',');

    const anyChecked = Array.from(courseCheckboxes).some(cb => cb.checked);

    removeProgram.disabled = !anyChecked;
    removeProgram.classList.toggle("bg-red-200", anyChecked);
    removeProgram.classList.toggle("btn-disabled", anyChecked);
    removeProgram.classList.toggle("bg-red-200", !anyChecked);
    removeProgram.classList.toggle("btn-disabled", !anyChecked);
}