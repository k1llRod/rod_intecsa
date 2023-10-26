odoo.define('whatsapp_connector_sale.product_search', function(require) {
"use strict";

var ProductSearch = require('whatsapp_connector.product_search');


/**
 *
 * @class
 * @name ProductSearch
 * @extends whatsapp.ProductSearch
 */
ProductSearch.include({
    events: _.extend({}, ProductSearch.prototype.events, {
        'click .acrux_product_shop': 'productOptions',
    }),

    /**
     * @override
     * @param {String} product el producto a procesar
     * @param {Event} event el evento que se ejecutó
     * @return {Promise}
     */
    doProductOption: function(product, event) {
        let out
        if (event.target.classList.contains('acrux_product_shop')) {
            if (this.parent.$tab_order.hasClass('active')) {
                this.parent.sale_order_form.addProductToOrder(product)
            } else {
                this.parent.$tab_order.trigger('click', {
                    resolve: () => this.parent.sale_order_form.addProductToOrder(product)
                })
            }
            out = Promise.resolve()
        } else {
            out = this._super(product, event)
        }
        return out
    },

    /**
     * Busca los productos y los muestra
     * @return {Promise}
     */
    searchProduct: function() {
        return this._super().then(() => {
            if (!this.parent.allow_sale_order) {
                this.$product_items.find('button.acrux_product_shop').addClass('d-none')
            }
        })
    },
})

return ProductSearch
})
