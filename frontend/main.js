let date = "";
let time = "";
let comment = "";
let selectedPeriod = "morning";
let calendar;

document.addEventListener("DOMContentLoaded", function() {
    initCalendar();
    setupPeriodButtons();
    showTimeButtons(selectedPeriod);
    setupTimeButtons();
    setupSubmitButton();
});

function initCalendar() {
    calendar = flatpickr(".calendar", {
        inline: true,
        locale: "uk",
        minDate: "today",
        maxDate: new Date().fp_incr(14),
        firstDayOfWeek: 1,
        disableMobile: true,
        monthSelectorType: "static", 
        yearSelectorType: "static",

        onChange: function(selectedDates, dateStr) {
            date = dateStr;
            showTimeButtons(selectedPeriod);
            checkButtonActivity();
        }
    });
}

function setupPeriodButtons() {
    const periodButtons = document.querySelectorAll(".segment");

    periodButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            periodButtons.forEach(function(btn) {
                btn.classList.remove("active");
            });

            this.classList.add('active');
            selectedPeriod = this.getAttribute("data-period");

            showTimeButtons(selectedPeriod);
        });
    });
}

function showTimeButtons(period) {
    document.querySelectorAll(".time-buttons").forEach(function(el) {
        el.classList.add("hidden")
   });

   if (date !== "") {
        const activeBlock = document.querySelector(".time-buttons." + period);
        activeBlock.classList.remove("hidden");
   }
}

function setupTimeButtons() {
    const timeButtons = document.querySelectorAll(".time");

    timeButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            timeButtons.forEach(function(btn) {
                btn.classList.remove("active");
            });

            this.classList.add("active");
            time = this.innerText;
            checkButtonActivity();
        });
    });
}

function checkButtonActivity() {
    const button = document.querySelector(".submit");

    if (date !== "" && time !== "") {
        button.classList.remove("unactive-button");
    } else {
        button.classList.add("unactive-button");
    }
}

function setupSubmitButton() {
    const button = document.querySelector(".submit");
    const input = document.querySelector(".comment");

    button.addEventListener("click", function() {
        if (button.classList.contains("unactive-button")) {
            return; 
        }

        button.classList.add("unactive-button");
        button.innerText = "Відправка..."

        const bookingData = {
            date: date,
            time: time,
            comment: input.value,
            init: tg.initData
        };

        sendData(button, bookingData);
        resetForm();
    });
}

async function sendData(button, data) {
    try {
        const response = await fetch("посилання", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            window.Telegram.WebApp.close();
        } else {
            console.error("Помилка на сервері: ", response.status);
            button.classList.remove("unactive-button");
            button.innerText = "Підтвердити бронювання";
        }
    }
    catch (error) {
        console.error("Помилка мережі:", error);
        button.classList.remove("unactive-button");
        button.innerText = "Підтвердити бронювання";
    }
}

function resetForm() {
    date = "";
    time = "";
    comment = "";
    selectedPeriod = "morning";

    const input = document.querySelector(".comment").value = "";
    calendar.clear();

    document.querySelectorAll(".segment").forEach(function(btn) {
        btn.classList.remove("active");
    });
    document.querySelector('.segment[data-period="morning"]').classList.add("active");

    document.querySelectorAll(".time").forEach(function(btn) {
        btn.classList.remove("active")
    });

    showTimeButtons(selectedPeriod);
    checkButtonActivity();
}