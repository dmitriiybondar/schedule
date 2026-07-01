document.addEventListener("DOMContentLoaded", function() {
    flatpickr(".calendar", {
        inline: true,
        locale: "uk",
        minDate: "today",
        maxDate: new Date().fp_incr(14),
        firstDayOfWeek: 1,
        disableMobile: true,
        monthSelectorType: "static", 
        yearSelectorType: "static"
    });
});