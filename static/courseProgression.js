$(document).ready(function () {

    // Delete Program
    $(document).on('click', '.deleteBtn', function (event) {

        var userResponse1 = confirm("Are you sure you want to delete this Program?");

        if (userResponse1) {
            var userResponse2 = confirm("Please confirm again, are you sure you want to delete this Program?");
        }
        else{
            event.preventDefault()
        }

        if (userResponse2 == false){
            event.preventDefault();
        }

    });

    $(document).on('click', '.editBtn', function (event) {

        event.preventDefault();

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
        $(this).parents("tr").find(".cancelBtn").show();

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

});


