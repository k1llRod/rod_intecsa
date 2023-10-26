odoo.define('acrux_whatsapp_sale.sale_order', function(require) {
"use strict";

var FormView = require('whatsapp_connector.form_view');

/**
 * Widget que maneja el formulario del pedido
 *
 * @class
 * @name SaleOrderForm
 * @extends web.Widget.FormView
 * @see acrux_chat.form_view
 */
var SaleOrderForm = FormView.extend({
    /**
     * @override
     * @see Widget.init
     */
    init: function(parent, options) {
        if (options) {
            options.model = 'sale.order';
            options.record = options.sale_order;
        }
        this._super.apply(this, arguments);

        this.parent = parent;
        const default_values = {
            default_partner_id: this.parent.selected_conversation.res_partner_id[0],
        }
        if (this.parent.selected_conversation.team_id[0]) {
            default_values['default_team_id'] = this.parent.selected_conversation.team_id[0]
        }
        _.defaults(this.context, default_values);
    },

    /**
     * Accciones especiales para sale.order
     *
     * @override
     * @see FormView.showAcruxFormView
    */
    _showAcruxFormView: function() {
        this._super().then(() => {
            this.moveSaleOrderNode();
            if (!this.action.context.default_partner_id) {
                let selector = 'div.o_form_sheet > .o_notebook > .o_notebook_headers';
                selector += ' > ul.nav-tabs > li';
                this.acrux_form_widget.$(selector).eq(1).find('a').trigger('click');
            }
            this.$('.oe_title > h1').css('font-size', '20px');
        });
    },

    /**
     * @override
     * @see FormView.recordUpdated
     * @returns {Promise}
     */
    recordUpdated: function(record) {
        return this._super(record).then(() => {
            this.moveSaleOrderNode();
            if (record && record.data && record.data.id) {
                let sale_order_key, partner_key, partner_id, localData;
                sale_order_key = this.acrux_form_widget.handle;
                localData = this.acrux_form_widget.model.localData;
                if (sale_order_key) {
                    partner_key = localData[sale_order_key].data.partner_id;
                }
                if (partner_key) {
                    partner_id = localData[partner_key];
                }
                this.parent.setNewPartner(partner_id);
            }
        });
    },

    /**
     * @override
     * @see FormView.recordUpdated
     * @returns {Promise}
     */
    recordChange: function(sale_order) {
        return Promise.all([
            this._super(sale_order),
            this._rpc({
                model: this.parent.model,
                method: 'write',
                args: [[this.parent.selected_conversation.id], {sale_order_id: sale_order.data.id}],
                context: this.context
            }).then(isOk => {
                if (isOk) {
                    let result = [sale_order.data.id, sale_order.data.name];
                    this.parent.selected_conversation.sale_order_id = result;
                    this.record = result;
                }
            })
        ]);
    },

    /**
     * @override
     * @return {Boolean}
     */
    makeDropable: function() {
        // solo para mantener el super
        return this._super() || true;
    },

    /**
     * @override
     * @param {Jquery} ui Elemento jquery
     * @returns {Boolean}
     */
    acceptDrop: function(ui) {
        return this._super(ui) || this._acceptSaleDrop(ui)
    },

    /**
     * Determina si aqui se maneja o no el evento
     * @param {Jquery} ui Elemento jquery
     * @returns {Boolean}
     */
    _acceptSaleDrop: function(ui) {
        return ui.hasClass('o_product_record')
    },


    /**
     * @override 
     * @param {Event} event evento de arrastre
     * @param {Jquery} ui Elemento jquery 
     * @returns {Promise}
     */
    handlerDradDrop: function(_event, ui) {
        return this._super(_event, ui).then(() => {
            if (this._acceptSaleDrop(ui.draggable)) {
                if (this.parent.selected_conversation && 
                        this.parent.selected_conversation.isMine()) {
                    let product = this.parent.product_search.find(ui.draggable.data('id'));
                    if (product) {
                        this.addProductToOrder(product);
                    }
                }
            }
        })
    },

    /**
     * mueve información del pedido al tab general
     */
    moveSaleOrderNode: function() {
        let main_group = this.acrux_form_widget.$('div.oe_title').next('div.o_group');
        let tab_general = 'div.o_form_sheet > div.o_notebook > div.tab-content > div.tab-pane';
        if (main_group.length && main_group.prev().hasClass('oe_title')) {
            main_group = main_group.detach()
            main_group.appendTo(this.acrux_form_widget.$(tab_general).first().next());
        }
    },

    /**
     * Trata de poner el pedido en modo edición y luego agregar una nueva fila
     *
     * @param {Object} product Producto para agregar al pedido
     */
    addProductToOrder: function(product) {
        if (this.acrux_form_widget.mode != 'edit') {
            this.acrux_form_widget._setMode('edit').then(() => {
                this.addRecord(product);
            });
        } else {
            this.addRecord(product);
        }
    },

    /**
     * Se es posible agrega el producto al pedido.
     * Esta función se realiza en dos paso, luego de está va addProductToOrderLine
     * Esta función coloca la orden editable, hace clic en el tab de orderline
     * y añade una linea en blanco en el pedido.
     *
     * @todo Al hacer clic en el primer tab, se espera 100 millisegundos para
     *       continuar lo mejor sería no esperar nada, porque esto podría dar 
     *       resultados inesperados
     *
     * @param {Object} product Producto para agregar al pedido
     */
    addRecord: function(product) {
        let sale_key, orderline, renderer, options;

        sale_key = this.acrux_form_widget.handle;
        renderer = this.acrux_form_widget.renderer;

        orderline = renderer.allFieldWidgets[sale_key].find(x => x.name == 'order_line');
        let link_id = orderline.$el.parent().attr('id');
        let $link = this.$('a[href$="' + link_id + '"]');
        let wait = 0;
        if (!$link.parent().hasClass('active') && !$link.hasClass('active')) {
            $link.trigger('click');
            wait = 100;
        }
        
        setTimeout(() => {
            if (orderline.renderer.addCreateLine) {
                orderline.renderer.unselectRow().then(() => {
                    options = {onSuccess: this.addProductToOrderLine.bind(this, product)}
                    orderline.renderer.trigger_up('add_record', options);
                });
            } else {
                const context = Object.assign({}, this.context, {
                    default_product_id: product.id
                })
                options = {context: [context]}
                orderline.renderer.trigger_up('add_record', options);
            }
        }, wait);
        
    },

    /**
     * Esta función agrega un producto a una liena de pedido vacía, funciona junto 
     * a la función addProductToOrder.
     *
     * @param {Object} product Producto para agregar al pedido
     */
    addProductToOrderLine: function(product) {
        let sale_key, orderline, renderer, orderline_id, product_id;

        sale_key = this.acrux_form_widget.handle;
        renderer = this.acrux_form_widget.renderer;
        orderline = renderer.allFieldWidgets[sale_key].find(x => x.name == 'order_line');
        orderline_id = orderline.renderer.getEditableRecordID();
        if (orderline_id) {
            product_id = orderline.renderer.allFieldWidgets[orderline_id]
            product_id = product_id.find(x => x.name == 'product_id');
            if (product_id) {
                product_id.reinitialize({
                    id: product.id,
                    display_name: product.name
                });
            }
        }
    },
    
    /**
     * @override
     * @see FormView._getOnSearchChatroomDomain
     * @returns {Array<Array<Object>>}
     */
    _getOnSearchChatroomDomain: function() {
        /** @type {Array} */
        let domain = this._super()
        domain.push(['conversation_id', '=', this.parent.selected_conversation.id])
        if (this.parent.selected_conversation.res_partner_id && this.parent.selected_conversation.res_partner_id[0]) {
            domain.unshift('|')
            domain.push(['partner_id', '=', this.parent.selected_conversation.res_partner_id[0]])
        }
        return domain
    },
    
})

return SaleOrderForm
})
