let fullDate = "";
let year = "";
let weekday = "";
let dateMonth = "";
let date = "";
let month = "";

initCalendar();
checkButtonActivity();
document.querySelector(".submit").addEventListener("click", redirect);

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
            fullDate = selectedDates[0];

            dateMonth = fullDate.toLocaleDateString('uk-UA', { day: 'numeric', month: 'long' });
            weekday = fullDate.toLocaleDateString('uk-UA', { weekday: 'long' });
            weekday = weekday.charAt(0).toUpperCase() + weekday.slice(1);
            year = fullDate.getFullYear();
            date = fullDate.getDate();
            month = fullDate.getMonth() + 1;
            
            checkButtonActivity();
        }
    });
}

function checkButtonActivity() {
    const button = document.querySelector(".submit");

    if (fullDate) {
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

    const fullDateInfo = {
        year: year,
        dateMonth: dateMonth,
        weekday: weekday,
        date: date,
        month: month
    }

    sessionStorage.setItem("dateInfo", JSON.stringify(fullDateInfo));
    window.location.href = "/admin/timescale/index.html"
}