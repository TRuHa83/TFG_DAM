const btnScrollTop = document.getElementById("btnScrollTop");

window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
        btnScrollTop.classList.add("show");

    } else {
        btnScrollTop.classList.remove("show");
    }
});

btnScrollTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

