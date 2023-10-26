odoo.define('acrux_whatsapp_sale.conversation', function(require) {
"use strict";

var Conversation = require('whatsapp_connector.conversation');

/**
 * @class
 * @name Conversation
 * @extends Conversation
 */
Conversation.include({
    /**
     * @override
     * @see Conversation.init
     */
    init: function(parent, options) {
        this._super.apply(this, arguments);

        this.sale_order_id = this.options.sale_order_id || [false, ''];
        
    },

})

return Conversation
})
