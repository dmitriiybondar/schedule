printDate();
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

function printDate() {
    let savedInfo = sessionStorage.getItem("dateInfo");
    let text = document.querySelector(".date");

    if (savedInfo) {
        const dateInfo = JSON.parse(savedInfo);

        let year = dateInfo.year;
        let dateMonth = dateInfo.dateMonth;
        let weekday = dateInfo.weekday;
        
        text.textContent = `${weekday}, ${dateMonth} ${year}`;
    }
}