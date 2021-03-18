$(document).ready(function () {

    // Delete Program
    $(document).on('click', '.deleteBtn', function (event) {

        event.preventDefault();

        console.log("clicked delete");

        var sequence = $(this).parents("tr").find(".sequence").val();
        console.log($(this).parents("tr"));
        $("#sequenceDeleteInput").val(sequence);

        var courseCode = $(this).parents("tr").find(".courseCode").val();
        console.log(courseCode);
        $("#courseDeleteInput").val(courseCode);

        $('#myModalDelete').find('.prerequisite_1').val($(this).parents("tr").find(".prerequisite_1").val())  ;
        $('#myModalDelete').find('.prerequisite_2').val($(this).parents("tr").find(".prerequisite_2").val())  ;
        $('#myModalDelete').find('.prerequisite_3').val($(this).parents("tr").find(".prerequisite_3").val())  ;
        $('#myModalDelete').find('.prerequisite_4').val($(this).parents("tr").find(".prerequisite_4").val())  ;
        $('#myModalDelete').find('.prerequisite_5').val($(this).parents("tr").find(".prerequisite_5").val())  ;

    });

    $(document).on('click', '.editBtn', function (event) {

        event.preventDefault();

        console.log("clicked edit");

        $('#editCourseError').html("");

        $("#courseEditInput").val($(this).parents("tr").find(".courseCode").val());
        $("#oldCourseEditInput").val($(this).parents("tr").find("#oldCourseCode").val());

        $("#prereq1EditInput").val($(this).parents("tr").find(".prerequisite_1").val());
        $("#prereq2EditInput").val($(this).parents("tr").find(".prerequisite_2").val());

        $("#prereq3EditInput").val($(this).parents("tr").find(".prerequisite_3").val());
        $("#prereq4EditInput").val($(this).parents("tr").find(".prerequisite_4").val());

        $("#prereq5EditInput").val($(this).parents("tr").find(".prerequisite_5").val());

        /*event.preventDefault();

        console.log("clicked edit");

        count = $(".editBtn").length;

        for (var i = 0; i < count; i++) {
            $(".cancelBtn").eq(i).click();
        }

        $(this).parents("tr").find(".courseCodeSpan").hide();
        $(this).parents("tr").find(".courseCode").show();

        $(this).parents("tr").find(".prereqSpan").hide();
        $(this).parents("tr").find(".prereqInput").show();

        $(this).parents("tr").find(".editBtn").hide();
        $(this).parents("tr").find(".deleteBtn").hide();

        $(this).parents("tr").find(".saveBtn").show();
        $(this).parents("tr").find(".cancelBtn").show();*/

    });

    $(document).on('click', '.cancelBtn', function (event) {

        event.preventDefault();

        $(this).parents("tr").find(".courseCodeSpan").show();
        $(this).parents("tr").find(".courseCode").hide();

        $(this).parents("tr").find(".prereqSpan").show();
        $(this).parents("tr").find(".prereqInput").hide();

        $(this).parents("tr").find(".editBtn").show();
        $(this).parents("tr").find(".deleteBtn").show();

        $(this).parents("tr").find(".saveBtn").hide();
        $(this).parents("tr").find(".cancelBtn").hide();
    });


    $(document).on('click', '#clearBtn', function (event) {

        event.preventDefault();

        console.log("clicked clear");

        console.log( $('#sequence').val() );

        $('#sequence').val('');
        $('#courseCode').val('');
        $('#prereqCode1').val('');
        $('#prereqCode2').val('');
        $('#prereqCode3').val('');
        $('#prereqCode4').val('');
        $('#prereqCode5').val('');

    });

    $(document).on('click', '#prereqBtn', function (event) {

        console.log("clicked prereq");

        var counter = 1;

        if ($('#prereqCode2').is(":visible")){
            counter++;
        }

        if ($('#prereqCode3').is(":visible")){
            counter++;
        }

        if ($('#prereqCode4').is(":visible")){
            counter++;
        }

        if ($('#prereqCode5').is(":visible")){
            counter++;
        }

        // Checks CSS content for display:[none|block], ignores visibility:[true|false]
        if ($('#prereqCode2').is(":hidden") && counter == 1){
            $('#prereqCode2').show();
            $('#prereqLabel2').show();
        }

        if ($('#prereqCode3').is(":hidden") && counter == 2){
            $('#prereqCode3').show();
            $('#prereqLabel3').show();
        }

        if ($('#prereqCode4').is(":hidden") && counter == 3){
            $('#prereqCode4').show();
            $('#prereqLabel4').show();
        }

        if ($('#prereqCode5').is(":hidden") && counter == 4){
            $('#prereqCode5').show();
            $('#prereqLabel5').show();
        }

        if(counter == 4){
            $('#prereqBtn').hide();
        }

    });

    // confirmEditBtn
    $(document).on('click', '#confirmEditBtn', function (event) {

        console.log("edit click");

        // editCourseError
        var courseCode = $(this).parents("form").find("input[name=courseCode]").val();

        if(courseCode == ""){
            event.preventDefault();
            $('#editCourseError').show();
            $('#editCourseError').html("The course code cannot be left empty");
        }

        var characterCheck = /^([a-z0-9]*[a-z]){3}[a-z0-9]*$/i;

        if(!characterCheck.test(courseCode)){
            event.preventDefault();
            $('#editCourseError').show();
            $('#editCourseError').html("The course code is invalid");
        }

        //alert(val);

        //console.log(val);

    });

});


