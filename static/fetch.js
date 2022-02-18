$(document).ready(function() {
        $('#id_label_single').select2({
            placeholder: 'Search a city'
            });

    $("form").on('submit', function(e) {

        
        e.preventDefault();
        // test to see if it pulls through on dev tools
        console.log('Clickity Clacked!');

        $.ajax({
            data: {
                city: $("#city").val(),
            },
            type: 'POST',
            url: '/fetch',
            success: function(data) {

                if (data.error) {
                    alert(data.error);
                }
                else {
                    console.log(data)
                    var template = $("#result_template").html();
                    var html = Mustache.render(template, data);
                    $("#result").html(html);
                    $("#flashMessage").hide();
                    console.log(data);
                }
            }
        });
    });
});

// $(document).ready(function() {
//     $("form".on('submit', function(e) {

//         e.preventDefault();
//         // test to see if it pulls through on dev tools
//         console.log('Clickity Clacked!');

//         // $('.js-example-basic-single').select2({
//             // placeholder: 'Search a city'
//             // });

//     }));
// });