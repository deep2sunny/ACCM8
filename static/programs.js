$(document).ready(function () {

    // $(document).on('click', '.editBtn', function()

    $(document).on('click', '.editBtn', function () {

        count = $(".editBtn").length;

        for (var i = 0; i < count; i++) {
            $(".cancelBtn").eq(i).click();
        }

        var _index = $('.editBtn').index(this);

        var nameValue = $('.programNameSpan').eq(_index).html();
        $('.programNameSpan').eq(_index).hide();
        $('.programNameEditInputTag').eq(_index).show();
        $('.programNameEditInputTag').eq(_index).val(nameValue);

        var codeValue = $('.programCodeSpan').eq(_index).html();
        $('.programCodeSpan').eq(_index).hide();
        $('.programCodeEditInputTag').eq(_index).show();
        $('.programCodeEditInputTag').eq(_index).val(codeValue);

        $('.editBtn').eq(_index).hide();
        $('.deleteBtn').eq(_index).hide();

        $('.saveBtn').eq(_index).show();
        $('.cancelBtn').eq(_index).show();

        //console.log($('.programNameEditInputTag'));

    });


    $(document).on('click', '.cancelBtn', function () {

        var _index = $('.cancelBtn').index(this);

        $('.programNameSpan').eq(_index).show();
        $('.programNameEditInputTag').eq(_index).hide();

        $('.programCodeSpan').eq(_index).show();
        $('.programCodeEditInputTag').eq(_index).hide();

        $('.editBtn').eq(_index).show();
        $('.deleteBtn').eq(_index).show();

        $('.saveBtn').eq(_index).hide();
        $('.cancelBtn').eq(_index).hide();

    });


    $(document).on('click', '.saveBtn', function (event) {

        $('#sucessConfirmation').hide();
        $('#errorConfirmation').hide();

        event.preventDefault();

        var _index = $('.saveBtn').index(this);

        // $(".cancelBtn").eq(_index).click();

        var programCode = $('.programCodeEditInputTag').eq(_index).val();

        var oldProgramCode = $('.programCodeSpan').eq(_index).html();

        var programName = $('.programNameEditInputTag').eq(_index).val();

        if (programCode == "" || programName == "") {
            $('#errorConfirmation').show();
            $('#errorConfirmation').html("All the form fields must be filled out");
        } 
        else {

            requestData = {
                oldProgramCode: oldProgramCode,
                programCode: programCode,
                programName: programName
            };

            $.ajax({
                type: "POST",
                url: "/administrator/programs/updateProgram",
                data: JSON.stringify(requestData),
                dataType: "json",
                contentType: 'application/json;charset=UTF-8',
                success: function (response) {

                    if (response !== null) {
                        if (response.status == "1") {

                            $('.programCodeEditInputTag').eq(_index).val(programCode);
                            $('.programNameEditInputTag').eq(_index).val(programName);

                            $('.programCodeSpan').eq(_index).html(programCode);
                            $('.programNameSpan').eq(_index).html(programName);

                            $('#sucessConfirmation').show();
                            $('#sucessConfirmation').html(response.message);

                            $(this).parents("tr").css("background","#f0fac8");

                        } else if (response.status == "0") {

                            $('#sucessConfirmation').show();
                            $('#errorConfirmation').html(response.message);
                        }

                    }
                },
                error: function (event, request, settings) {
                    window.alert('AjaxError' + ' : ' + settings);
                }
            });
        }

        $(this).parents("tr").find(".cancelBtn").click();

    });

    function addToDisplayTable(latestCode, latestName) {

        var cell1 = $('<td>');
        var span = $('<span>').html(latestCode);
        span.attr("class", "programCodeSpan");
        cell1.append(span);
        var codeHiddenInputTag = $('<input>');
        codeHiddenInputTag.attr({
            "type": "text",
            "class": "form-control programCodeEditInputTag",
            "name": "editProgramCode",
            "style": "display:none;",
            "value": latestCode
        });

        cell1.append(codeHiddenInputTag);

        // ****

        var cell2 = $('<td>');
        var span = $('<span>').html(latestName);
        span.attr("class", "programNameSpan");
        cell2.append(span);
        var nameHiddenInputTag = $('<input>');
        nameHiddenInputTag.attr({
            "type": "text",
            "class": "form-control programNameEditInputTag",
            "name": "editProgramName",
            "style": "display:none;",
            "value": latestName
        });

        cell2.append(nameHiddenInputTag);

        // ***

        var cell3 = $('<td>');

        var editButton = $('<button>');
        editButton.html("Edit");
        editButton.attr({
            "type": "button",
            "class": "btn btn-primary editBtn"
        });
        cell3.append(editButton);

        // <button type="button" class="btn btn-primary saveBtn" style="display:none;">Save</button>
        var saveBtn = $('<button>');

        saveBtn.html("Save");
        saveBtn.attr({
            "type": "button",
            "class": "btn btn-success saveBtn",
            "style": "display:none;"
        });
        cell3.append(saveBtn);

        // *****

        var cell4 = $('<td>');

        var deleteButton = $('<button>');
        deleteButton.html("Delete");
        deleteButton.attr({
            "type": "button",
            "class": "btn btn-danger deleteBtn"
        });
        cell4.append(deleteButton);

        // <button type="button" class="btn btn-primary cancelBtn" style="display:none;">Cancel</button>
        var cancelBtn = $('<button>');
        cancelBtn.html("Cancel");
        cancelBtn.attr({
            "type": "button",
            "class": "btn btn-primary cancelBtn",
            "style": "display:none;"
        });
        cell4.append(cancelBtn);


        var row = $('<tr>');
        row.append(cell1);
        row.append(cell2);
        row.append(cell3);
        row.append(cell4);

        $('#tableBody').append(row);

    }

    $('#createProgramForm').on('submit', function (event) {

        programCode = $('#programCode').val();
        programName = $('#programName').val();
        

        $('#sucessConfirmation').hide();
        $('#errorConfirmation').hide();


        if (programCode == "" || programName == "" ) {
            $('#errorConfirmation').show();
            $('#errorConfirmation').html("All the form fields must be filled out");
        } 
        
        else {

            $.ajax({
                type: "POST",
                url: "/administrator/programs/createProgram",
                data: {
                    programCode: programCode,
                    programName: programName,
                },
                dataType: "json",
                success: function (response) {

                    if (response !== null) {
                        if (response.status == "1") {

                            addToDisplayTable(programCode, programName);

                            $("#clearBtn").click();

                            $('#sucessConfirmation').show();

                            $('#sucessConfirmation').html(response.message);

                        } else if (response.status == "0") {

                            $('#errorConfirmation').show();

                            $('#errorConfirmation').html(response.message);
                        }

                    }
                },
                error: function (event, request, settings) {
                    window.alert('AjaxError' + ' : ' + settings);
                }
            });
        }

        event.preventDefault();

    });

    // Delete Program
    $(document).on('click', '.deleteBtn', function () {

        $('#sucessConfirmation').hide();
        $('#errorConfirmation').hide();

        var _index = $('.deleteBtn').index(this);

        var _deleteButtonClicked = $(this);

        var userResponse1 = confirm("Are you sure you want to delete this Program?");

        if (userResponse1) {
            var userResponse2 = confirm("Please confirm again, are you sure you want to delete this Program?");
        }

        var _row = $('#tableBody').children()[_index];

        if (userResponse1 && userResponse2) {

            var programCode = $('.programCodeSpan').eq(_index).html();

            $.ajax({
                type: "POST",
                url: "/administrator/programs/deleteProgram",
                data: JSON.stringify({
                    programCode: programCode
                }),
                dataType: "json",
                contentType: 'application/json;charset=UTF-8',
                success: function (response) {

                    if (response !== null) {

                        console.log(response);

                        if (response.status == "1") {

                            $('#sucessConfirmation').show();

                            $('#sucessConfirmation').html(response.message);
                            _deleteButtonClicked.parents("tr").remove();


                        } else if (response.status == "0") {

                            $('#errorConfirmation').show();

                            $('#errorConfirmation').html(response.message);
                        }

                    }
                },
                error: function (event, request, settings) {
                    window.alert('AjaxError' + ' : ' + settings);
                }
            });
        }

    });

});

