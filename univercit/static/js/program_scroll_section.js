const overviewSection = document.getElementById("overview-section");
const coursesSection = document.getElementById("courses-section");
const overViewLink = document.getElementById("overview-link")
const coursesLink = document.getElementById("courses-link")
const sections = document.querySelectorAll(".scroll-section");


function sectionScrollIntoView(section, block="center") {
    section.scrollIntoView({
        behavior: "smooth",
        block: block
    })
}

overViewLink.addEventListener("click", () => {
    sectionScrollIntoView(overviewSection);
})


coursesLink.addEventListener("click", () => {
    sectionScrollIntoView(coursesSection, "start");
})


function autoScrollTabSelection() {
    const windowHeight = window.innerHeight;
    const overviewRect = overviewSection.getBoundingClientRect();
    const coursesRect = coursesSection.getBoundingClientRect();

    if (overviewRect.top + 150 < windowHeight && overviewRect.bottom > 150) {
            overViewLink.classList.add("tab-active");
            coursesLink.classList.remove("tab-active");
    }
    else if (coursesRect.top + 150 < windowHeight && coursesRect.bottom > 150) {
            overViewLink.classList.remove("tab-active");
            coursesLink.classList.add("tab-active");
    }
}

window.addEventListener("scroll", autoScrollTabSelection);