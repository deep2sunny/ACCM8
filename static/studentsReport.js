$(document).ready(function () {
    $('#reportForm').on('submit', function (event) {
/*
        $('#reportTables').hide();

        var level = $('#level').val();
        var pid = $('#version').val();
        var programCode = $('#program').val();

        console.log(level + "-" + pid + "-" + programCode);

        

        requestData = {
            programCode: programCode,
            pid: pid,
            level: level,
        };

        console.log(requestData);

        $.ajax({
            type: "POST",
            url: "/administrator/studentsreport/generatereport",
            data: JSON.stringify(requestData),
            dataType: "json",
            contentType: 'application/json;charset=UTF-8',
            success: function (response) {

                if (response !== null) {
                    if (response.status == "1") {

                        console.log("show table");

                        $('#reportTables').show();

                    } else if (response.status == "0") {

                        $('#reportTables').hide();

                        $('#errorConfirmation').show();

                        $('#errorConfirmation').html(response.message);
                    }

                }
            },
            error: function (event, request, settings) {
                window.alert('AjaxError' + ' : ' + settings);
            }
        });

        event.preventDefault();
*/
    });
});


