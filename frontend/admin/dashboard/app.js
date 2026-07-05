let date = "";

document.addEventListener("DOMContentLoaded", function() {
    initCalendar();
    checkButtonActivity();

    document.querySelector(".submit").addEventListener("click", redirect);
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
            checkButtonActivity();
        }
    });
}

function checkButtonActivity() {
    const button = document.querySelector(".submit");

    if (date !== "") {
        button.classList.remove("unactive-button");
    } else {
        button.classList.add("unactive-button");
    }
}

function redirect() {
    const button = document.querySelector(".submit");

    if (button.classList.contains("unactive-button")) {
        return;
    }

    window.location.href = "/admin/timescale/index.html"
}