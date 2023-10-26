odoo.define("modules_access_rights", function(require) {
"use strict";
alert('gggggg')
    var Sidebar = require("web.Sidebar");
    var session = require("web.session");
    var core = require("web.core");
    var _t = core._t;
    var rpc = require('web.rpc');

    Sidebar.include({
        _addItems: function (sectionCode, items) {
            var _items = items;
            console.log(_items)
            alert('gggggg')
            if (!session.is_superuser && sectionCode === 'other' && items.length && session.none_export_models.includes(this.env.model) ) {
                _items = _.reject(_items, {label:_t("Export")});
            }
            if (!session.is_superuser && sectionCode === 'other' && items.length && session.none_archivable_models.includes(this.env.model) ) {
                _items = _.reject(_items, {label:_t("Archive")});
                _items = _.reject(_items, {label:_t("Unarchive")});
            }
              console.log('after',_items)

            this._super(sectionCode, _items);

        }



    })
});
