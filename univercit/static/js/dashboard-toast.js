document.addEventListener("DOMContentLoaded", () => { 
    toastError = document.getElementById("toast-error")
    toastSuccess = document.getElementById("toast-success")
    
    if(toastError) {
        toastError.classList.remove('hidden')
    
        setTimeout(() => {
            toastError.classList.add('hidden')
        }, 5000)
    } else if(toastSuccess) {
        toastSuccess.classList.remove('hidden')
        setTimeout(() => {
            toastSuccess.classList.add('hidden')
        }, 5000)
    }
})