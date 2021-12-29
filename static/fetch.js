$(document).ready(function() {
    $("form").submit(function(e){

        e.preventDefault();
        console.log('Clickity Clacked!');

        $a.jax({
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
                    var template = $("result_template").html()      
                    var html = Mustache.to_html(template, data);
                    $("#result").html(html);
                    $("#flashMessage").hide();
                    console.log(data)
                }
            }

        });
    });
});