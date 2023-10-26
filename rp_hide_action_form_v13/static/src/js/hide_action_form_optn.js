odoo.define('rp_hide_action_form_v13.hide_action_form_optn', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var session = require('web.session');
    var core = require('web.core');
    var _t = core._t;

    FormController.include({

        willStart: function () {
            var self = this;
            var def1 = this.getSession().user_has_group('rp_hide_action_form_v13.group_archive_access').then(function (has_archive_group) {
                self.has_archive_group = has_archive_group;
            });
            var def2 = this.getSession().user_has_group('rp_hide_action_form_v13.group_delete_access').then(function (has_delete_group) {
                self.has_delete_group = has_delete_group;
            });
            var def3 = this.getSession().user_has_group('rp_hide_action_form_v13.group_duplicate_access').then(function (has_duplicate_group) {
                self.has_duplicate_group = has_duplicate_group;
            });
            return Promise.all([def1, def2, def3]);
        },

        /**
         * Show or hide the sidebar according to the actual_mode
         * @private
         */
        _updateSidebar: function () {
            var self = this
            this._super.apply(this, arguments);
            if (this.sidebar && this.mode === 'readonly') {
                if (!this.has_archive_group) {
                    this.sidebar.items.other = _.reject(this.sidebar.items.other, function (item) {
                        return item.label === 'Archive';
                    });
                }
                if (!this.has_delete_group) {
                    this.sidebar.items.other = _.reject(this.sidebar.items.other, function (item) {
                        return item.label === 'Delete';
                    });
                }
                if (!this.has_duplicate_group) {
                    this.sidebar.items.other = _.reject(this.sidebar.items.other, function (item) {
                        return item.label === 'Duplicate';
                    });
                }
                this.sidebar.items.other;
                this._updateEnv();
            }
        },
    });
});
