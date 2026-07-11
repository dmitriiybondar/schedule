backButton();
addButton();

function backButton() {
    let button = document.querySelector(".back");

    button.addEventListener("click", () => {
        window.location.href = "/admin/dashboard/index.html"
    });
}

function addButton() {
    let button = document.querySelector(".add-slot-button");

    button.addEventListener("click", () => {
        window.location.href = "/admin/timer/index.html"
    });
}