odoo.define('acrux_whatsapp_sale.chat_classes', function(require) {
"use strict";

var chat = require('whatsapp_connector.chat_classes');

return _.extend(chat, {
    Indicators: require('acrux_whatsapp_sale.indicators'),
    SaleOrderForm: require('acrux_whatsapp_sale.sale_order'),
});
});