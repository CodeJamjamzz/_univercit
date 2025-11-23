document.addEventListener("DOMContentLoaded", () => { 
    toastError = document.getElementById("toast-error")
    if(!toastError) return;

    toastError.classList.remove('hidden')

    setTimeout(() => {
        toastError.classList.add('hidden')
    }, 5000)
})