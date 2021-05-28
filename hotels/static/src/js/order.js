function testUrlHz() {
    $.ajax({
        url: 'http://frichono.ru/oda/action',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
        },
//        dataType: 'text',
        method: 'GET',
        error: function(x) {
            console.log(x);
            console.log(this);
        },
        success: function(x){
            console.log(x);
        }
    });
};

//odoo.define('hotels.settings', function(require) {
//    $(document).ready(function() {
//        setTimeout(function() {
//            var test = $('#test_ajax').html();
//            alert(test);
//        }, 1000);
//        $('#test_ajax').click(function() {
//            $.ajax({
//                url: 'http://frichono.ru/oda/action',
//                method: 'post',
//                data: {'odoo_url': $("input[name='url_hz']")},
//                success: function(data){
//                    alert(data);
//                }
//            });
//        });
//    });
//});
