printDate();
backButton();
addButton();
deleteSlot();
checkButtonActivity();
inputDataChange();
addSlot();

function backButton() {
    const button = document.querySelector(".back");

    button.addEventListener("click", () => {
        window.location.href = "/admin/dashboard/index.html"
    });
}

function addButton() {
    const button = document.querySelector(".add-slot-button");
    const overlay = document.querySelector(".overlay");
    const timeWindow = document.querySelector(".time-window");

    button.addEventListener("click", () => {
        overlay.classList.add("active");
        timeWindow.classList.add("active");
    });

    overlay.addEventListener("click", () => {
        overlay.classList.remove("active");
        timeWindow.classList.remove("active");
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
    const slotCanvas = document.querySelector(".slot-canvas");

    slotCanvas.addEventListener("click", (event) => {
        const deleteButton = event.target.closest(".delete-button");

        if (deleteButton) {
            const parentSlot = deleteButton.closest(".slot");
            if (parentSlot) {
                parentSlot.remove();
            }
        }
    });
}

function checkButtonActivity() {
    const button = document.querySelector(".save-time");
    const startTime = document.querySelector(".start-time").value;
    const endTime = document.querySelector(".end-time").value;

    if (startTime && endTime) {
        button.classList.remove("unactive-button");
    } else {
        button.classList.add("unactive-button");
    }
}

function inputDataChange() {
    const startTime = document.querySelector(".start-time");
    const endTime = document.querySelector(".end-time");

    startTime.addEventListener("input", checkButtonActivity);
    endTime.addEventListener("input", checkButtonActivity);
}

function addSlot() {
    const slotCanvas = document.querySelector(".slot-canvas");
    const button = document.querySelector(".save-time");

    button.addEventListener("click", () => {
        const overlay = document.querySelector(".overlay");
        const timeWindow = document.querySelector(".time-window");

        const startTime = document.querySelector(".start-time").value;
        const endTime = document.querySelector(".end-time").value;

        if (startTime && endTime) {
            const newSlot = `
                <div class="slot">
                    <p>${startTime}-${endTime}</p>

                    <label class="switch">
                        <input type="checkbox" checked>
                        <span class="slider"></span>
                    </label>

                    <button class="delete-button">
                        <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            <line x1="10" y1="11" x2="10" y2="17"></line>
                            <line x1="14" y1="11" x2="14" y2="17"></line>
                        </svg>
                    </button>
                </div>
            `;
            
            slotCanvas.insertAdjacentHTML("beforeend", newSlot);
            overlay.classList.remove("active");
            timeWindow.classList.remove("active");
        }
    });
}