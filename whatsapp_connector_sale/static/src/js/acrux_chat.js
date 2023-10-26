odoo.define('acrux_whatsapp_sale.acrux_chat', function(require) {
"use strict";

var chat = require('whatsapp_connector.chat_classes');
var AcruxChatAction = require('whatsapp_connector.acrux_chat').AcruxChatAction;
var session = require('web.session');
var core = require('web.core');

var _t = core._t;
var QWeb = core.qweb;


/**
 * @class
 * @name AcruxChatAction
 * @extends AcruxChatAction
 */
AcruxChatAction.include({
    events: _.extend({}, AcruxChatAction.prototype.events, {
        'click li#tab_lastes_sale': 'tabLastesSale',
        'click li#tab_order': 'tabOrder',
    }),

    /**
     * @private
     * @see AcruxChatAction._initRender
     * @override
     * @returns {Promise}
     */
    _initRender: function() {
        return this._super().then(() => {
            this.$tab_order = this.$('li#tab_order > a');
            this.$tab_content_order = this.$('div#tab_content_order > div.o_group');
            this.$tab_content_indicator = this.$('div#tab_content_lastes_sale > div.o_group')

            return session.user_has_group('sales_team.group_sale_salesman').then(hasGroup => {
                if (!hasGroup) {
                    this.$('li#tab_order').addClass('d-none');
                    this.allow_sale_order = false;
                } else {
                    this.allow_sale_order = true;
                }
            })
        });
    },

    /**
     * @override
     * @see AcruxChatAction.getRequiredViews
     * @returns {Promise}
     */
    getRequiredViews: function() {
        return this._super().then(() => {
            return this._rpc({
                model: this.model,
                method: 'check_object_reference',
                args: ['_sale', 'acrux_whatsapp_sale_order_form_view'],
                context: this.context
            }).then(result => {
                this.sale_order_view_id = result[1];
            });
        });
    },

    /**
     * Cuando se hace clic en el tab de pedido, se muestra un formulario de 
     * sale.order
     *
     * @param {Event} _event
     * @param {Object} data
     * @return {Promise}
     */
    tabOrder: function(_event, data) {
        let out = Promise.reject()

        if (this.selected_conversation) {
            if (this.selected_conversation.isMine()) {
                let sale_order_id = this.selected_conversation.sale_order_id;
                this.saveDestroyWidget('sale_order_form')
                let options = {
                    context: this.action.context,
                    sale_order: sale_order_id,
                    action_manager: this.action_manager,
                    form_name: this.sale_order_view_id,
                    searchButton: true,
                    title: _t('Order'),
                }
                this.sale_order_form = new chat.SaleOrderForm(this, options)
                this.$tab_content_order.empty()
                out = this.sale_order_form.appendTo(this.$tab_content_order)
            } else {
                this.$tab_content_order.html(QWeb.render('acrux_empty_tab', {notYourConv: true}))
            }
        } else {
            this.$tab_content_order.html(QWeb.render('acrux_empty_tab'))
        }
        out.then(() => data && data.resolve && data.resolve())
        out.catch(() => data && data.reject && data.reject())
        return out
    },

    /**
     * Cuando se hace clic en el tab de indiciadores, se muestra los indicadores
     * programados
     *
     * @param {Event} _event
     * @param {Object} data
     * @return {Promise}
     */
    tabLastesSale: function(_event, data) {
        let out = Promise.reject()

        if (this.selected_conversation) {
            if (this.selected_conversation.res_partner_id[0]) {
                this.saveDestroyWidget('indicator_widget')
                let options = { partner_id: this.selected_conversation.res_partner_id[0] };
                this.indicator_widget = new chat.Indicators(this, options);
                this.$tab_content_indicator.empty()
                out = this.indicator_widget.appendTo(this.$tab_content_indicator);
            } else {
                this.$tab_content_indicator.html(QWeb.render('acrux_empty_tab',
                    {message: _t('This conversation does not have a partner.')}))
            }
        } else {
            this.$tab_content_indicator.html(QWeb.render('acrux_empty_tab'))
        }
        out.then(() => data && data.resolve && data.resolve())
        out.catch(() => data && data.reject && data.reject())
        return out
    },

    /**
     * @override
     * @see AcruxChatAction.tabsClear
     */
    tabsClear: function() {
        this._super();
        this.saveDestroyWidget('indicator_widget')
        this.saveDestroyWidget('sale_order_form')
    },

    /**
     * Devuelve si el controlador es parte de chatroom, es util para los tabs
     * @param {String} jsId id del controllador
     * @returns {Boolean}
     */
    isChatroomTab: function(jsId) {
        return this._super(jsId) || this._isChatroomTab('sale_order_form', jsId)
    },

})

return AcruxChatAction
})
