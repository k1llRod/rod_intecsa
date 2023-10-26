# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GroupedProductsForInvoice(models.Model):
    _name = 'vr.grouped_products'
    
    code = fields.Char(string="Código", required=True)
    description = fields.Text(string="Descripción", required=True)
    product_uom = fields.Many2one('uom.uom', 'Unidad de Medida', required=True)
    product_uom_qty = fields.Float('Cantidad', default=1, required=True)
    total_amount = fields.Float(string="Monto Total")
    sale_id = fields.Many2one(comodel_name="sale.order")
    account_move_id = fields.Many2one('account.move')
    products_ids = fields.Many2many(
        comodel_name="sale.order.line",
        domain=lambda self:[
            ('order_id','=',self.env.context.get('ssid') or False),
            ('product_id','not in',self.env.context.get('prod') or False)
        ],
        ondelete="cascade"
    )
    edit = fields.Boolean(
        compute='get_edit'
    )
    #total_disc = fields.Float(compute='get_total_discount_percent', default=0)
    #total_discount = fields.Float('Descuento Total', default=0)
    #tot = fields.Float(default=0)
    total = fields.Float('Total', default=0)

    @api.depends('edit')
    def get_edit(self):
        self.edit = self.env.context.get('edit')

    @api.model
    def create(self, values):
        items = values.get("products_ids")
        
        # Verify unique code
        obj_vr_grouped_products = self.env['vr.grouped_products'].search([
            ('code','=',values.get('code')),
            ('sale_id','=',self.env.context.get('ssid'))
        ])
        if obj_vr_grouped_products:
            raise ValidationError("El código ya existe")

        # Verify len(items)>1        
        if len(items[0][2])<=1:
            raise ValidationError("La cantidad de productos a agrupar debe ser por lo menos 2")

        for v in items[0][2]:            
            obj_sale_order_line = self.env['sale.order.line'].browse(v)
            # if obj_sale_order_line.price_unit==0:
            #     raise ValidationError("El precio unitario de cada linea de producto no puede ser 0 (cero)")

            obj_sale_order_line.update({
                'grouped':values.get('code')
            })
        values['sale_id']=self.env.context.get('ssid')
        
        return super(GroupedProductsForInvoice, self).create(values)

    @api.constrains('total_amount')
    def _check_total_amount(self):
        if self.total_amount==0:
            raise ValidationError("El monto total NO puede ser cero")
    
    def edit_group(self):
        exist_prod=[]
        obj_so=self.env['sale.order'].browse(self.env.context.get('saleid'))
        for o in obj_so:
            obj_sol=self.env['sale.order.line'].search([
                ('order_id','=',o.id),
                ('grouped','!=',False),
                ('grouped','!=',self.code),
                ])
            for o in obj_sol:
                exist_prod.append(o.product_id.id)

        return {
            'name'      : "Editar",
            'type'      : 'ir.actions.act_window',
            'res_model' : 'vr.grouped_products',            
            'view_type' : 'form',
            'view_mode' : 'form',
            'target'    : 'new',
            'res_id'    : self.id,
            'context'   : {
                'edit': False,
                'ssid': self.env.context.get('saleid'), 
                'prod': tuple(exist_prod),
                'default_products_ids': [17]
            }
        }

    def view_group(self):
        exist_prod=[]
        obj_so=self.env['sale.order'].browse(self.sale_id.id)
        for o in obj_so:
            obj_sol=self.env['sale.order.line'].search([
                ('order_id','=',o.id),
                ('grouped','!=',False),
                ('grouped','!=',self.code),
                ])
            for o in obj_sol:
                exist_prod.append(o.product_id.id)

        return {
            'name'      : "Ver",
            'type'      : 'ir.actions.act_window',
            'res_model' : 'vr.grouped_products',
            'view_type' : 'form',
            'view_mode' : 'form',
            'target'    : 'new',
            'res_id'    : self.id,
            'context'   : {
                'edit': True,
                'ssid': self.sale_id.id,
                'prod': tuple(exist_prod),
            },
            'flags': {'form': {'mode': 'readonly', 'initial_mode': 'readonly'}},
        }

    def remove_group(self):
        obj_grouped_products = self.env['vr.grouped_products'].browse(self.id)
        obj_sale_order_line = self.env['sale.order.line'].search([('order_id','=',obj_grouped_products.sale_id.id),('grouped','=',obj_grouped_products.code)])
        for obj in obj_sale_order_line:
            obj.grouped = False

        obj_grouped_products.unlink()

    @api.onchange('products_ids')
    def _onchange_products_ids(self):            

        amount = 0
        if self.products_ids:
            for res in self.products_ids:
                amount += (res.product_uom_qty * res.price_unit)
        
        self.total_amount = amount

   # def get_total_discount(self):
    #    for line in self:
     #       subtotal = sum(line.products_ids.mapped('total_discount'))
      #      line.tot = line.total_amount - subtotal
       #     line.total = line.tot

        #return subtotal

    #def get_total_discount_percent(self):
     #   for line in self:
      #      subtotal = line.get_total_discount()
       #     line.total_disc = (100*subtotal)/line.total_amount
        #    line.total_discount = line.total_disc
