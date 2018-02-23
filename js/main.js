$(document).ready(function () {
    console.log("ready!");
    $('#alarmtickets').DataTable({
        order: [[ 0, 'des' ]],
        pageLength: 50
    });
});