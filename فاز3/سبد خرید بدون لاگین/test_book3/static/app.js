var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})



setTimeout(function(){
    if ($('.message').length > 0) {
        $('.message').remove();
    }
}, 1000)    // 2000 millisecond


// $(document).ready(function() {
//     // messages timeout for 10 sec
//     setTimeout(function() {
//         $('.message').fadeOut('slow');
//     }, 1000); // <-- time in milliseconds, 1000 =  1 sec
//
//     // delete message
//     $('.del-msg').live('click',function(){
//         $('.del-msg').parent().attr('style', 'display:none;');
//     })
// });


$(document).ready(function(){
    console.log('hello world')
    $('#modal-btn').click(function(){
        console.log('working')
        $('.ui.modal')
        .modal('show')
        ;
    })
    $('.ui.dropdown').dropdown()
})


