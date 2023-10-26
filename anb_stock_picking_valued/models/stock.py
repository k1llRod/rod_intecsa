# -*- coding: utf-8 -*-
################################################################
#    License, author and contributors information in:          #
#    __openerp__.py file at the root folder of this module.    #
################################################################

from odoo import api, fields, models, _
from openerp import SUPERUSER_ID
from openerp.exceptions import Warning
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
from dateutil.relativedelta import relativedelta
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.depends('move_lines.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the picking.
        """
        for picking in self:
            if picking.picking_type_id.code not in ['incoming', 'outgoing']:
                continue
            amount_untaxed = amount_tax = 0.0
            for move in picking.move_lines:
                amount_untaxed += move.price_subtotal
                # FORWARDPORT UP TO 10.0
                if picking.company_id.\
                   tax_calculation_rounding_method == 'round_globally':
                    price = move.move_price_unit * (
                        1 - (move.discount or 0.0) / 100.0)
                    taxes = move.tax_id.compute_all(
                        price, move.picking_id.currency_id,
                        move.product_uom_qty,
                        product=move.product_id,
                        partner=picking.partner_id
                    )
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get(
                        'taxes', []))
                else:
                    amount_tax += move.price_tax
            if picking.picking_type_id.code == 'outgoing':
                pick_vals = {
                    'amount_untaxed': picking.pricelist_id.currency_id.round(
                        amount_untaxed),
                    'amount_tax': picking.pricelist_id.currency_id.round(
                        amount_tax),
                    'amount_total': amount_untaxed + amount_tax,
                }
            else:
                pick_vals = {
                    'amount_untaxed': picking.currency_id.round(
                        amount_untaxed),
                    'amount_tax': picking.currency_id.round(amount_tax),
                    'amount_total': amount_untaxed + amount_tax,
                }
            picking.update(pick_vals)

    # MAIN FIELDS

    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelist',
        required=False,
        readonly=True,
        states={
            'draft': [
                ('readonly', False)
            ],
            'sent': [
                ('readonly', False)
            ]
        },
        help='Pricelist for current stock picking.',
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True,
        required=True,
        states={
            'draft': [
                ('readonly', False)
            ],
        }
    )

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Payment Terms',
        readonly=True,
        states={
            'draft': [
                ('readonly', False)
            ],
            'sent': [
                ('readonly', False)
            ]
        },
    )

    # ORDER LINES FIELDS

    amount_untaxed = fields.Monetary(
        string='Untaxed Amount',
        store=True,
        readonly=True,
        compute='_amount_all',
        track_visibility='always',
    )

    amount_tax = fields.Monetary(
        string='Taxes',
        store=True,
        readonly=True,
        compute='_amount_all',
        track_visibility='always',
    )

    amount_total = fields.Monetary(
        string='Total',
        store=True,
        readonly=True,
        compute='_amount_all',
        track_visibility='always',
    )

    # ADDITIONAL INFO FIELDS

    client_order_ref = fields.Char(
        string='Customer/Supplier Reference',
        copy=False,
        readonly=True,
        states={
            'draft': [
                ('readonly', False)
            ],
            'sent': [
                ('readonly', False)
            ]
        },
    )

    fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string='Fiscal Position',
        readonly=True,
        states={
            'draft': [
                ('readonly', False)
            ],
            'sent': [
                ('readonly', False)
            ]
        },
    )

    def onchange_in_partner_id(self):
        if not self.partner_id:
            self.fiscal_position_id = False
            self.payment_term_id = False
            self.currency_id = False
        else:
            self.fiscal_position_id = self.env['account.fiscal.position'].\
                with_context(company_id=self.company_id.id).\
                get_fiscal_position(self.partner_id.id)
            self.payment_term_id = self.partner_id.\
                property_supplier_payment_term_id.id
            self.currency_id = self.partner_id.property_purchase_currency_id\
                .id or self.env.user.company_id.currency_id.id
        return {}

    def onchange_out_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment term
        - Invoice address
        - Delivery address
        """
        if not self.partner_id:
            self.update({
                'payment_term_id': False,
                'fiscal_position_id': False,
            })
            return
        self.fiscal_position_id = self.env['account.fiscal.position'].\
            get_fiscal_position(self.partner_id.id)
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and
            self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and
            self.partner_id.property_payment_term_id.id or False,
        }
        if self.env.user.company_id.sale_note:
            values['note'] = self.with_context(lang=self.partner_id.lang).\
                env.user.company_id.sale_note
        # if self.partner_id.user_id:
        #     values['user_id'] = self.partner_id.user_id.id
        # if self.partner_id.team_id:
        #     values['team_id'] = self.partner_id.team_id.id
        self.update(values)

    @api.onchange('partner_id')
    def onchange_partner_id_warning(self):
        if not self.partner_id:
            return
        warning = {}
        title = False
        message = False
        partner = self.partner_id
        if self.picking_type_id.code == 'incoming':
            # If partner has no warning, check its company
            if partner.purchase_warn == 'no-message' and partner.parent_id:
                partner = partner.parent_id
            if partner.purchase_warn != 'no-message':
                # Block if partner only has warning but parent company is
                # blocked
                if partner.purchase_warn != 'block' and partner.parent_id \
                   and partner.parent_id.purchase_warn == 'block':
                    partner = partner.parent_id
                title = _('Warning for %s') % partner.name
                message = partner.purchase_warn_msg
                warning = {
                    'title': title,
                    'message': message
                }
                if partner.purchase_warn == 'block':
                    self.update({'partner_id': False})
        elif self.picking_type_id.code == 'outgoing':
            # If partner has no warning, check its company
            if partner.sale_warn == 'no-message' and partner.parent_id:
                partner = partner.parent_id
            if partner.sale_warn != 'no-message':
                # Block if partner only has warning but parent company is
                # blocked
                if partner.sale_warn != 'block' and partner.parent_id and \
                   partner.parent_id.sale_warn == 'block':
                    partner = partner.parent_id
                title = ('Warning for %s') % partner.name
                message = partner.sale_warn_msg
                warning = {
                    'title': title,
                    'message': message,
                }
                if partner.sale_warn == 'block':
                    self.update({
                        'partner_id': False,
                        'pricelist_id': False,
                    })
        if warning:
            return {'warning': warning}
        return {}

    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        res = super(StockPicking, self).onchange_picking_type()
        if not res:
            res = {}
        if self.picking_type_id:
            if self.picking_type_id.code != 'outgoing':
                self.pricelist_id = False
        if self.partner_id:
            if self.picking_type_id.code == 'incoming':
                res_in = self.onchange_in_partner_id()
                if res_in:
                    res.update(res_in)
            elif self.picking_type_id.code == 'outgoing':
                res_out = self.onchange_out_partner_id()
                if res_out:
                    res.update(res_out)
        return res

    @api.onchange('pricelist_id')
    def onchange_pricelist_id(self):
        if self.picking_type_id.code == 'outgoing' and self.pricelist_id:
            self.currency_id = self.pricelist_id.currency_id.id \
                if self.pricelist_id.currency_id else False

    @api.onchange('fiscal_position_id')
    def _compute_tax_id(self):
        """
        Trigger the recompute of the taxes if the fiscal position is changed on
        the SP.
        """
        for picking in self:
            picking.move_lines._compute_tax_id()

    def _get_tax_amount_by_group(self):
        self.ensure_one()
        res = {}
        currency = self.currency_id or self.company_id.currency_id
        for move in self.move_lines:
            base_tax = 0
            for tax in move.tax_id:
                group = tax.tax_group_id
                res.setdefault(group, 0.0)
                # FORWARD-PORT UP TO SAAS-17
                price_reduce = move.move_price_unit * (
                    1.0 - move.discount / 100.0)
                taxes = tax.compute_all(
                    price_reduce + base_tax, quantity=move.product_uom_qty,
                    product=move.product_id, partner=self.partner_id
                )['taxes']
                for t in taxes:
                    res[group] += t['amount']
                if tax.include_base_amount:
                    base_tax += tax.compute_all(
                        price_reduce + base_tax, quantity=1,
                        product=move.product_id, partner=self.partner_id
                    )['taxes'][0]['amount']
        res = sorted(res.items(), key=lambda l: l[0].sequence)
        res = map(lambda l: (l[0].name, l[1]), res)
        return res

    def button_dummy(self):
        return True

    @api.model
    def _prepare_values_extra_move(self, op, product, remaining_qty):
        """
        Creates an extra move when there is no corresponding original move to
        be copied
        """
        res = super(StockPicking, self)._prepare_values_extra_move(
            op, product, remaining_qty)
        move = self.move_lines.filtered(
            lambda r: r.product_id == product and
            (r.restrict_lot_id.id in op.pack_lot_ids.mapped('lot_id').
             mapped('id') if r.restrict_lot_id else True)
        )
        if move:
            move = move[0]
        else:
            raise Warning(
                _('The selected lot for the operation is different from the '
                  'move one.'),
            )
        res.update({
            'picking_type_id': move.picking_type_id.id,
            'move_price_unit': move.move_price_unit,
            'discount': move.discount,
            'tax_id': [(6, 0, move.tax_id.mapped('id'))],
        })
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.depends('product_uom_qty', 'discount', 'move_price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the stock move.
        """
        for move in self:
            if move.picking_type_id.code not in ['incoming', 'outgoing']:
                continue
            price = move.move_price_unit * (1 - (move.discount or 0.0) / 100.0)
            taxes = move.tax_id.compute_all(
                price, move.picking_id.currency_id, move.product_uom_qty,
                product=move.product_id,
                partner=move.picking_id.partner_id
            )
            move.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.depends('move_price_unit', 'discount')
    def _get_price_reduce(self):
        for move in self:
            move.price_reduce = move.move_price_unit * (
                1.0 - move.discount / 100.0)

    @api.depends('price_total', 'product_uom_qty')
    def _get_price_reduce_tax(self):
        for move in self:
            move.price_reduce_taxinc = \
                move.price_total / move.product_uom_qty \
                if move.product_uom_qty else 0.0

    @api.depends('price_subtotal', 'product_uom_qty')
    def _get_price_reduce_notax(self):
        for move in self:
            move.price_reduce_taxexcl = \
                move.price_subtotal / move.product_uom_qty \
                if move.product_uom_qty else 0.0

    move_price_unit = fields.Float(
        string='Unit Price',
        required=True,
        digits=dp.get_precision('Product Price'),
        default=0.0,
    )

    price_subtotal = fields.Monetary(
        compute='_compute_amount',
        string='Subtotal',
        readonly=True,
        store=True,
    )

    price_tax = fields.Monetary(
        compute='_compute_amount',
        string='Taxes',
        readonly=True,
        store=True,
    )

    price_total = fields.Monetary(
        compute='_compute_amount',
        string='Total',
        readonly=True,
        store=True,
    )

    price_reduce = fields.Monetary(
        compute='_get_price_reduce',
        string='Price Reduce',
        readonly=True,
        store=True,
    )

    tax_id = fields.Many2many(
        comodel_name='account.tax',
        string='Taxes',
        domain=['|', ('active', '=', False), ('active', '=', True)],
    )

    price_reduce_taxinc = fields.Monetary(
        compute='_get_price_reduce_tax',
        string='Price Reduce Tax inc',
        readonly=True,
        store=True,
    )

    price_reduce_taxexcl = fields.Monetary(
        compute='_get_price_reduce_notax',
        string='Price Reduce Tax excl',
        readonly=True,
        store=True,
    )

    discount = fields.Float(
        string='Discount (%)',
        digits=dp.get_precision('Discount'),
        default=0.0,
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='picking_id.currency_id',
        string='Currency',
        readonly=True,
    )

    picking_type_code = fields.Selection(
        related='picking_type_id.code',
        string='Picking type code',
    )

    def _compute_tax_id(self):
        for move in self:
            if move.picking_type_id.code not in ['incoming', 'outgoing']:
                continue
            fpos = move.picking_id.fiscal_position_id or \
                move.picking_id.partner_id.property_account_position_id
            # If company_id is set, always filter taxes by the company
            if move.picking_type_id.code == 'incoming':
                taxes = move.product_id.supplier_taxes_id.filtered(
                    lambda r: not move.company_id or
                    r.company_id == move.company_id)
            elif move.picking_type_id.code == 'outgoing':
                taxes = move.product_id.taxes_id.filtered(
                    lambda r: not move.company_id or
                    r.company_id == move.company_id)
            move.tax_id = fpos.map_tax(
                taxes, move.product_id,
                move.picking_id.partner_id) if fpos else taxes

    @api.model
    def _get_date_planned(self, seller, picking=False):
        """Return the datetime value to use as Schedule Date (``date_planned``)
           for stock moves that correspond to the given product.seller_ids,
           when ordered at `date_order_str`.
           :param browse_record | False product: product.product, used to
               determine delivery delay thanks to the selected seller field
               (if False, default delay = 0)
           :param browse_record | False po: purchase.order, necessary only if
               the stock move is not yet attached to a stock picking.
           :rtype: datetime
           :return: desired Schedule Date for the stock move
        """
        date = picking.date if picking else self.picking_id.date
        if date:
            return datetime.strptime(
                date, DEFAULT_SERVER_DATETIME_FORMAT) + relativedelta(
                    days=seller.delay if seller else 0)
        else:
            return datetime.today() + relativedelta(
                days=seller.delay if seller else 0)

    @api.onchange('product_uom_qty', 'product_uom')
    def _onchange_quantity(self):
        if self.picking_type_id.code != 'incoming':
            return
        if not self.product_id:
            return
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_uom_qty,
            date=self.picking_id.date and self.picking_id.date[:10],
            uom_id=self.product_uom)
        if seller or not self.date:
            self.date = self._get_date_planned(seller).strftime(
                DEFAULT_SERVER_DATETIME_FORMAT)
        if not seller:
            return
        price_unit = self.env['account.tax']._fix_tax_included_price_company(
            seller.price, self.product_id.supplier_taxes_id, self.tax_id,
            self.company_id) if seller else 0.0
        if price_unit and seller and self.picking_id.currency_id and \
           seller.currency_id != self.picking_id.currency_id:
            price_unit = seller.currency_id.compute(
                price_unit, self.picking_id.currency_id)
        if seller and self.product_uom and \
           seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(
                price_unit, self.product_uom)
        self.move_price_unit = price_unit

    def _suggest_quantity(self):
        '''
        Suggest a minimal quantity based on the seller
        '''
        if not self.product_id:
            return
        seller_min_qty = self.product_id.seller_ids\
            .filtered(lambda r: r.name == self.picking_id.partner_id)\
            .sorted(key=lambda r: r.min_qty)
        if seller_min_qty:
            self.product_uom_qty = seller_min_qty[0].min_qty or 1.0
            self.product_uom = seller_min_qty[0].product_uom
        else:
            self.product_uom_qty = 1.0

    def onchange_in_product_id(self):
        result = {}
        if not self.product_id:
            return result
        # Reset date, price and quantity since _onchange_quantity will provide
        # default values
        # self.date_planned = datetime.today().strftime(
        #   DEFAULT_SERVER_DATETIME_FORMAT)
        self.date = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.move_price_unit = self.product_uom_qty = 0.0
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        result['domain'] = {
            'product_uom': [
                ('category_id', '=', self.product_id.uom_id.category_id.id)
            ]
        }
        product_lang = self.product_id.with_context({
            'lang': self.partner_id.lang,
            'partner_id': self.partner_id.id,
        })
        self.name = product_lang.display_name
        if product_lang.description_purchase:
            self.name += '\n' + product_lang.description_purchase
        fpos = self.picking_id.fiscal_position_id
        if self.env.uid == SUPERUSER_ID:
            company_id = self.env.user.company_id.id
            self.tax_id = fpos.map_tax(
                self.product_id.supplier_taxes_id.filtered(
                    lambda r: r.company_id.id == company_id))
        else:
            self.tax_id = fpos.map_tax(self.product_id.supplier_taxes_id)
        self._suggest_quantity()
        self._onchange_quantity()
        return result

    def _get_display_price(self, product):
        if self.picking_id.pricelist_id.discount_policy == 'with_discount':
            return product.with_context(
                pricelist=self.picking_id.pricelist_id.id).price
        final_price, rule_id = self.picking_id.pricelist_id.\
            get_product_price_rule(
                self.product_id, self.product_uom_qty or 1.0,
                self.picking_id.partner_id)
        context_partner = dict(
            self.env.context, partner_id=self.picking_id.partner_id.id,
            date=self.picking_id.date)
        base_price, currency_id = self.with_context(context_partner).\
            _get_real_price_currency(
                self.product_id, rule_id, self.product_uom_qty,
                self.product_uom, self.picking_id.pricelist_id.id)
        if currency_id != self.picking_id.pricelist_id.currency_id.id:
            base_price = self.env['res.currency'].browse(['currency_id']).\
                with_context(context_partner).compute(
                    base_price, self.picking_id.pricelist_id.currency_id)
        # negative discounts (= surcharge) are included in the display price
        return max(base_price, final_price)

    def onchange_out_product_id(self):
        if not self.product_id:
            return {
                'domain': {
                    'product_uom': []
                }
            }
        vals = {}
        domain = {
            'product_uom': [
                ('category_id', '=', self.product_id.uom_id.category_id.id)
            ]
        }
        if not self.product_uom or \
           (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = 1.0
        product = self.product_id.with_context(
            lang=self.picking_id.partner_id.lang,
            partner=self.picking_id.partner_id.id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.picking_id.date,
            pricelist=self.picking_id.pricelist_id.id,
            uom=self.product_uom.id
        )
        result = {
            'domain': domain,
        }
        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale
        vals['name'] = name
        self._compute_tax_id()
        if self.picking_id.pricelist_id and self.picking_id.partner_id:
            vals['move_price_unit'] = self.env['account.tax'].\
                _fix_tax_included_price_company(
                    self._get_display_price(product),
                    product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)
        return result

    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(StockMove, self).onchange_product_id()
        if not res:
            res = {}
        if self.picking_type_id.code == 'incoming':
            res_in = self.onchange_in_product_id()
            if res_in:
                res.update(res_in)
        elif self.picking_type_id.code == 'outgoing':
            res_out = self.onchange_out_product_id()
            if res_out:
                res.update(res_out)
        return res

    @api.onchange('product_id')
    def onchange_product_id_warning(self):
        if not self.product_id:
            return
        warning = {}
        title = False
        message = False
        product_info = self.product_id
        if self.picking_type_id.code == 'incoming':
            if product_info.purchase_line_warn != 'no-message':
                title = _('Warning for %s') % product_info.name
                message = product_info.purchase_line_warn_msg
                warning['title'] = title
                warning['message'] = message
                if product_info.purchase_line_warn == 'block':
                    self.product_id = False
        elif self.picking_type_id.code == 'outgoing':
            if product_info.sale_line_warn != 'no-message':
                title = _('Warning for %s') % product_info.name
                message = product_info.sale_line_warn_msg
                warning['title'] = title
                warning['message'] = message
                if product_info.sale_line_warn == 'block':
                    self.product_id = False
        if warning:
            return {'warning': warning}
        return {}

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if self.picking_type_id.code != 'outgoing':
            return
        if not self.product_uom or not self.product_id:
            self.move_price_unit = 0.0
            return
        if self.picking_id.pricelist_id and self.picking_id.partner_id:
            product = self.product_id.with_context(
                lang=self.picking_id.partner_id.lang,
                partner=self.picking_id.partner_id.id,
                quantity=self.product_uom_qty,
                date=self.picking_id.date,
                pricelist=self.picking_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.move_price_unit = self.env['account.tax'].\
                _fix_tax_included_price_company(
                    self._get_display_price(product), product.taxes_id,
                    self.tax_id, self.company_id)

    def _get_new_picking_values(self):
        """ Prepares a new picking for this move as it could not be assigned to
        another picking. This method is designed to be inherited."""
        vals = super(StockMove, self)._prepare_picking_assign()
        if self.procurement_id and self.procurement_id.sale_line_id and \
           self.procurement_id.sale_line_id.order_id:
            sale_order = self.procurement_id.sale_line_id.order_id
            vals.update({
                'partner_id': sale_order.partner_id.id
                if sale_order.partner_id else False,
                'client_order_ref': sale_order.client_order_ref,
                'pricelist_id': sale_order.pricelist_id.id
                if sale_order.pricelist_id else False,
                'currency_id': sale_order.currency_id.id
                if sale_order.currency_id else False,
                'payment_term_id': sale_order.payment_term_id.id
                if sale_order.payment_term_id else False,
                'fiscal_position_id': sale_order.fiscal_position_id.id
                if sale_order.fiscal_position_id else False,
                'amount_untaxed': sale_order.amount_untaxed,
                'amount_tax': sale_order.amount_tax,
                'amount_total': sale_order.amount_total,
            })
        return vals
