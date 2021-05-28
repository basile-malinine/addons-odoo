var hzUrlTest = null;
odoo.define('hotels.settings', function(require) {
    $(document).ready(function() {
        var rpc = require('web.rpc');

        hzUrlTest = function () {
            alert('In function hzUrlTest...');
            rpc.query({
                model: 'res.config.settings',
                method: 'test_url',
                args: [[]]
            });
        }
    })
});
