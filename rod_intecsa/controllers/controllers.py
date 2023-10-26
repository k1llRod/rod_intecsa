# -*- coding: utf-8 -*-
# from odoo import http


# class RodIntecsa(http.Controller):
#     @http.route('/rod_intecsa/rod_intecsa', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_intecsa/rod_intecsa/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_intecsa.listing', {
#             'root': '/rod_intecsa/rod_intecsa',
#             'objects': http.request.env['rod_intecsa.rod_intecsa'].search([]),
#         })

#     @http.route('/rod_intecsa/rod_intecsa/objects/<model("rod_intecsa.rod_intecsa"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_intecsa.object', {
#             'object': obj
#         })
