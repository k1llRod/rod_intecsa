odoo.define('hide_archive_unarchive_buttons.BasicView', function (require) {
    "use strict";
    var BasicView = require('web.BasicView');
    var session = require('web.session'); // Agrega esta línea para importar el módulo de sesión

    BasicView.include({
        init: function(viewInfo, params) {
            var self = this;
            this._super.apply(this, arguments);
            const model = ['res.partner'];

            // Verificar si el usuario actual es el administrador del sistema
            var isSystemAdmin = session.is_system;

            if (model.includes(self.controllerParams.modelName) && !isSystemAdmin) {
                self.controllerParams.archiveEnabled = 'False' in viewInfo.fields;
            }
        },
    });
});

