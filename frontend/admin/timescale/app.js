printDate();
backButton();
addButton();
deleteSlot();

function backButton() {
    const button = document.querySelector(".back");

    button.addEventListener("click", () => {
        window.location.href = "/admin/dashboard/index.html"
    });
}

function addButton() {
    const button = document.querySelector(".add-slot-button");

    button.addEventListener("click", () => {
        window.location.href = "/admin/timer/index.html"
    });
}

function printDate() {
    const savedInfo = sessionStorage.getItem("dateInfo");
    let text = document.querySelector(".date");

    if (savedInfo) {
        const dateInfo = JSON.parse(savedInfo);

        let year = dateInfo.year;
        let dateMonth = dateInfo.dateMonth;
        let weekday = dateInfo.weekday;
        
        text.textContent = `${weekday}, ${dateMonth} ${year}`;
    }
}

function deleteSlot() {
    const deleteButtons = document.querySelectorAll(".delete-button");

    deleteButtons.forEach(button => {
        button.addEventListener("click", el => {
            const parentSlot = el.target.closest(".slot");
            if (parentSlot) {
                parentSlot.remove();
            }
        });
    });
}