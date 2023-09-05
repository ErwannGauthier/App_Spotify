let loader = document.querySelector(".loading");
let generateButton = document.querySelector(".generateButton");
window.addEventListener("load", fadeout);
generateButton.addEventListener("click", fadein);

function fadeout() {
    loader.classList.add("disappear");
}

function fadein() {
    loader.classList.remove("disappear");
    loader.style.visibility = "visible";
    loader.style.opacity = "100%";
}