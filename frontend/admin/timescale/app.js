backButton();

function backButton() {
    let button = document.querySelector(".back");

    button.addEventListener("click", () => {
        window.location.href = "/admin/dashboard/index.html"
    });
}