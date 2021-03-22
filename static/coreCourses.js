$(document).ready(function () {

    // Edit Course
    $(document).on('click', '.editBtn', function (event) {

        event.preventDefault();

        console.log("clicked delete");

        var courseCode = $(this).parents("tr").find(".courseCodeTd").html();
        var courseTitle = $(this).parents("tr").find(".courseTitleTd").html();

        console.log(courseCode + "-" + courseTitle);

        $("#editCourseCodeInput").val(courseCode);

        $("#editCourseTitleInput").val(courseTitle);

        $('#oldCourseCode').val(courseCode);

    });

    // Delete Course
    $(document).on('click', '.deleteBtn', function (event) {

        event.preventDefault();

        console.log("clicked delete");

        var courseCode = $(this).parents("tr").find(".courseCodeTd").html();

        $("#courseDeleteInput").val(courseCode);

    });

    // Delete Course
    $(document).on('click', '.deleteBtn', function (event) {

        event.preventDefault();

        console.log("clicked delete");

        var courseCode = $(this).parents("tr").find(".courseCodeTd").html();

        $("#courseDeleteInput").val(courseCode);

    });

    // addBtn
    $(document).on('click', '#addBtn', function (event) {



        // editCourseError
        var courseCode = $(this).parents("form").find("input[name=courseCode]").val();

        var courseTitle = $(this).parents("form").find("input[name=courseTitle]").val();

        if(courseCode == "" || courseTitle == ""){
            event.preventDefault();
            $('#addCourseError').show();
            $('#addCourseError').html("The course code and title cannot be left empty");
        }

        var characterCheck = /^([a-z0-9]*[a-z]){3}[a-z0-9]*$/i;

        if(!characterCheck.test(courseCode)){
            event.preventDefault();
            $('#addCourseError').show();
            $('#addCourseError').html("The course code is invalid");
        }


    });


    // confirmEditBtn
    $(document).on('click', '#confirmEditBtn', function (event) {

        console.log("edit click");

        // editCourseError
        var courseCode = $(this).parents("form").find("input[name=editCourseCodeInput]").val();

        var courseTitle = $(this).parents("form").find("input[name=editCourseTitleInput]").val();

        if(courseCode == "" || courseTitle == ""){
            event.preventDefault();
            $('#editCourseError').show();
            $('#editCourseError').html("The course code and title cannot be left empty");
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


