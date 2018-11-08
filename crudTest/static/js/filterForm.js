var drPickier = $('#filterDate'). daterangepicker({
    "autoApply": false,
    "showDropdowns": true,
    locale: {
        format: 'DD.MM.YYYY',
        "applyLabel": "Застосувати",
        "cancelLabel": "Очистити",
        "showDropdowns": true,
        "firstDay": 1,
        "daysOfWeek": [
            "Нд",
            "Пн",
            "Вт",
            "Ср",
            "Чт",
            "Пт",
            "Сб"
        ],
        "monthNames": [
            "Січень",
            "Лютий",
            "Березень",
            "Квітень",
            "Травень",
            "Червень",
            "Липень",
            "Серпень",
            "Вересень",
            "Жовтень",
            "Листопад",
            "Грудень"
        ],
    },
    ranges: {
        'Сьогодні': [moment(), moment().add(1, 'days')],
        'Вчора': [moment().subtract(1, 'days'), moment()],
        'Тиждень': [moment().subtract(7, 'days'), moment()],
        'Місяць': [moment().subtract(30, 'days'), moment()],
        },
        "alwaysShowCalendars": true,
        "showCustomRangeLabel": false,
});


// $(function() {
//     drPickier.val('')
// });

drPickier.on('cancel.daterangepicker', function(ev, picker){
    drPickier.val('');
});

drPickier.on('apply.daterangepicker', function(){
    filter($(this))
});

drPickier.on('keyup', function(){
    filter($(this))
});

$('#filterName').on('keyup', function(){
    filter($(this))
});

$('#filterText').on('keyup', function(){
    filter($(this))
});