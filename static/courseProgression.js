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
            event.preventDefault()
        }



    });

});


