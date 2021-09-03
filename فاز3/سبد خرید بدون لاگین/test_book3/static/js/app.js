
// $(".click_sabt").click(function(event) {
//     if ({{product.inventory}} < {{ 0 }} && {{item.quantity}} < {{product.inventory}}) {
//         {#print({{ product.inventory }})#}
//
//     } else {
//         alert('موجودی انبار:{{ product.inventory }} .تعداد را ویرایش یا آیتم را حذف کنید.');
//     }
//
// })

setTimeout(function(){
    if ($('.message').length > 0) {
        $('.message').remove();
    }
}, 2000)    // 2000 millisecond

$(document).ready(function() {
    // messages timeout for 10 sec
    setTimeout(function() {
        $('.message').fadeOut('slow');
    }, 1000); // <-- time in milliseconds, 1000 =  1 sec

    // delete message
    $('.del-msg').live('click',function(){
        $('.del-msg').parent().attr('style', 'display:none;');
    })
});


