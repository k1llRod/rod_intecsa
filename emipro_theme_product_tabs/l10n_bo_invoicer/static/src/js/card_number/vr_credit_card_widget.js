odoo.define('l10n_bo_invoicer_plus.credit_card', (require)=> {
    const registry = require("web.field_registry");
    const WebBasicFields = require('web.basic_fields');
    const Widget=require("web.AbstractField");

    const CreditCard = WebBasicFields.FieldChar.extend({
        template: 'l10n_bo_invoicer_plus.tmpl_credit_card',
        events: _.extend({
            'keyup': 'keyUp',
            'click': 'selectInput'
        }, Widget.prototype.events),
        init: function (parent, params) {
            this._super(...arguments);
        },
        renderElement: function() {
            this._super(...arguments);
        },
        selectInput: function(){
            this.$el.select();
        },
        setValue: function(){
            var input = this.$el.val();
            this._setValue(input);
        },
        keyUp: function(event){
            if(event.key!="ArrowRight" && event.key!="ArrowLeft" && event.key!="1" && event.key!="2" && event.key!="3" && event.key!="4" && event.key!="5" && event.key!="6" && event.key!="7" && event.key!="8" && event.key!="9" && event.key!="0"){
                // event.preventDefault();
                this.$el.val(0).select();
                this.setValue();
                return;
            }
            if(event.key=="ArrowRight" || event.key=="1" || event.key=="2" || event.key=="3" || event.key=="4" || event.key=="5" || event.key=="6" || event.key=="7" || event.key=="8" || event.key=="9" || event.key=="0"){
                if(this.name==='vr_nro_tarjeta_1'){
                    $('.vr_in_nro_credit_card:eq(1)').focus().select();
                }else if(this.name==='vr_nro_tarjeta_2'){
                    $('.vr_in_nro_credit_card:eq(2)').focus().select();
                }else if(this.name==='vr_nro_tarjeta_3'){
                    $('.vr_in_nro_credit_card:eq(3)').focus().select();
                }else if(this.name==='vr_nro_tarjeta_4'){
                    $('.vr_in_nro_credit_card:eq(4)').focus().select();
                }else if(this.name==='vr_nro_tarjeta_5'){
                    $('.vr_in_nro_credit_card:eq(5)').focus().select();
                }else if(this.name==='vr_nro_tarjeta_6'){
                    $('.vr_in_nro_credit_card:eq(6)').focus().select();
                }else if(this.name==='vr_nro_tarjeta_7'){
                    $('.vr_in_nro_credit_card:eq(7)').focus().select();
                }
            }else if(event.key=="ArrowLeft") {
                if (this.name === 'vr_nro_tarjeta_8') {
                    $('.vr_in_nro_credit_card:eq(6)').focus().select();
                } else if (this.name === 'vr_nro_tarjeta_7') {
                    $('.vr_in_nro_credit_card:eq(5)').focus().select();
                } else if (this.name === 'vr_nro_tarjeta_6') {
                    $('.vr_in_nro_credit_card:eq(4)').focus().select();
                } else if (this.name === 'vr_nro_tarjeta_5') {
                    $('.vr_in_nro_credit_card:eq(3)').focus().select();
                } else if (this.name === 'vr_nro_tarjeta_4') {
                    $('.vr_in_nro_credit_card:eq(2)').focus().select();
                } else if (this.name === 'vr_nro_tarjeta_3') {
                    $('.vr_in_nro_credit_card:eq(1)').focus().select();
                } else if (this.name === 'vr_nro_tarjeta_2') {
                    $('.vr_in_nro_credit_card:eq(0)').focus().select();
                }
            }
            this.setValue();
        }
    });
    registry.add('credit_card', CreditCard);
});