$(document).ready(function () {

$('forms').on('submit', function(event){

    $.ajax({
    data : {
        command :$('#commands').val()
    },
    type : 'POST'
    url: '/profile'
    })
    });

event.preventDefault(data);

  });
});