document.addEventListener('DOMContentLoaded', () => {
    const drawerCheckbox = document.getElementById('my-drawer');

    if (!drawerCheckbox) return;

    const savedState = localStorage.getItem('isDrawerOpen');
    
    if (savedState !== null) {
        drawerCheckbox.checked = (savedState === 'true');
    }

    drawerCheckbox.addEventListener('change', () => {
        localStorage.setItem('isDrawerOpen', drawerCheckbox.checked);
    });

    const navLinks = document.querySelectorAll('.drawer-side ul li a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 1024) { 
                drawerCheckbox.checked = false;
                localStorage.setItem('isDrawerOpen', 'false');
            }
        });
    });
});