const overviewSection = document.getElementById("overview-section");
const filesSection = document.getElementById("files-section");
const discussionsSection = document.getElementById("discussions-section");
const overViewLink = document.getElementById("overview-link")
const filesLink = document.getElementById("files-link")
const discussionsLink = document.getElementById("discussions-link")
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


filesLink.addEventListener("click", () => {
    sectionScrollIntoView(filesSection);
})


discussionsLink.addEventListener("click", () => {
    sectionScrollIntoView(discussionsSection);
})


function autoScrollTabSelection() {
    const windowHeight = window.innerHeight;
    const overviewRect = overviewSection.getBoundingClientRect();
    const filesRect = filesSection.getBoundingClientRect();
    const discussionsRect = discussionsSection.getBoundingClientRect();

    if (overviewRect.top + 150 < windowHeight && overviewRect.bottom > 150) {
            overViewLink.classList.add("tab-active");
            filesLink.classList.remove("tab-active");
            discussionsLink.classList.remove("tab-active");
    }
    else if (filesRect.top + 150 < windowHeight && filesRect.bottom > 150) {
            overViewLink.classList.remove("tab-active");
            filesLink.classList.add("tab-active");
            discussionsLink.classList.remove("tab-active");
    }
    else if (discussionsRect.top + 150 < windowHeight && discussionsRect.bottom > 150) {
            overViewLink.classList.remove("tab-active");
            filesLink.classList.remove("tab-active");
            discussionsLink.classList.add("tab-active");
    }
}

window.addEventListener("scroll", autoScrollTabSelection);