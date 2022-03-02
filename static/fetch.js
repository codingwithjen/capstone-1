$(document).ready(function() {
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

// $(document).ready(function(){
//     var cities=[];
//     function loadCities(){
//      $.getJSON('/cities', function(data, status, xhr){
//       for (var i = 0; i < data.length; i++ ) {
//        cities.push(data[i].name);
//       }
//     });
//     };
//     loadCities();
   
//     $('#city').autocomplete({
//      source: cities, 
//     }); 
   
//     $('form').on('submit', function(e){
//      $.ajax({
//       data: {
//        city:$('#city').val()
//       },
//       type: 'POST',
//       url : '/process'
//      })
//      .done(function(data){ 
//       if (data.error){
//        $('#result').text(data.error).show();
//       }
//       else {
//        $('#result').html(data.city).show()
//       }
//      })
//      e.preventDefault();
//     });
//    }); 



