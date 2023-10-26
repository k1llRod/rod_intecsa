from odoo import api, fields, models, _
from odoo.exceptions import UserError
import re

class InheritConfig(models.TransientModel):
    _inherit = "res.config.settings"

    name = fields.Boolean(string="Replace Existing?", default=False)

    new_product = fields.Boolean(string="Auto generate code for new product", default=False)
    seq_separate = fields.Char(string="Sequence Separator", size=1)

    name_digit = fields.Char(string="Lenght", size=1)
    name_separate = fields.Char(string="Product Name Separator", size=1)

    attrib_digit = fields.Char(string="Lenght", size=1)
    attrib_separate = fields.Char(string="Attribute Name Separator", size=1)

    categ_digit = fields.Char(string="Lenght", size=1)
    categ_separate = fields.Char(string="Category Name Separator", size=1)

    @api.onchange('name_digit','attrib_digit','categ_digit')
    def onchange_text_type(self):
        if self.enable_naming:
            if self.name_digit:
                self.check_text(self.name_digit)

        if self.enable_attrib:
            if self.attrib_digit:
                self.check_text(self.attrib_digit)

        if self.enable_categ:
            if self.categ_digit:
                self.check_text(self.categ_digit)


    def check_text(self,*digit):
        for var in digit:
            pattern = "^[0-9]{1}$"
            if not re.match(pattern, var):
                raise UserError(_(
                    "Please input only number from 1 to 9.\n"
                    "Charcters are not allowed.\n"
                    "If you save the record it will save last saved number."
                ))

    enable_naming = fields.Selection([
        ('on','Enable'),('off','Disable')
        ], default='off')

    enable_attrib = fields.Selection([
        ('on','Enable'),('off','Disable')
        ], default='off')

    enable_categ = fields.Selection([
        ('on','Enable'),('off','Disable')
        ], default='off')

    enable_seq = fields.Selection([
        ('on','Enable'),('off','Disable')
        ], default='off')

    @api.model
    def get_values(self):
        res = super(InheritConfig, self).get_values()
        ir_param = self.env['ir.config_parameter'].sudo()
        
        res.update(
            enable_naming=ir_param.get_param('auto_generate_product_code_app.enable_naming'),
            new_product=ir_param.get_param('auto_generate_product_code_app.new_product'),
            seq_separate=ir_param.get_param('auto_generate_product_code_app.seq_separate'),

            enable_attrib=ir_param.get_param('auto_generate_product_code_app.enable_attrib'),
            name_digit=ir_param.get_param('auto_generate_product_code_app.name_digit'),
            name_separate=ir_param.get_param('auto_generate_product_code_app.name_separate'),

            attrib_digit=ir_param.get_param('auto_generate_product_code_app.attrib_digit'),
            attrib_separate=ir_param.get_param('auto_generate_product_code_app.attrib_separate'),

            enable_categ=ir_param.get_param('auto_generate_product_code_app.enable_categ'),
            categ_digit=ir_param.get_param('auto_generate_product_code_app.categ_digit'),
            categ_separate=ir_param.get_param('auto_generate_product_code_app.categ_separate'),

            enable_seq=ir_param.get_param('auto_generate_product_code_app.enable_seq'),
        )

        return res

    def set_values(self):
        res = super(InheritConfig, self).set_values()
        ir_conf_param = self.env['ir.config_parameter']

        ir_conf_param.set_param('auto_generate_product_code_app.enable_naming', self.enable_naming)
        ir_conf_param.set_param('auto_generate_product_code_app.new_product', self.new_product)
        ir_conf_param.set_param('auto_generate_product_code_app.seq_separate', self.seq_separate)

        ir_conf_param.set_param('auto_generate_product_code_app.enable_attrib', self.enable_attrib)
        ir_conf_param.set_param('auto_generate_product_code_app.name_digit', self.name_digit)
        ir_conf_param.set_param('auto_generate_product_code_app.name_separate', self.name_separate)

        ir_conf_param.set_param('auto_generate_product_code_app.attrib_digit', self.attrib_digit)
        ir_conf_param.set_param('auto_generate_product_code_app.attrib_separate', self.attrib_separate)

        ir_conf_param.set_param('auto_generate_product_code_app.enable_categ', self.enable_categ)
        ir_conf_param.set_param('auto_generate_product_code_app.categ_digit', self.categ_digit)
        ir_conf_param.set_param('auto_generate_product_code_app.categ_separate', self.categ_separate)

        ir_conf_param.set_param('auto_generate_product_code_app.enable_seq', self.enable_seq)

    def generate_all_reference(self):
        template_ids = self.env['product.template'].search([])
        template_id_list = [ids.id for ids in template_ids]

        variant_ids = self.env['product.product'].search([])
        variant_id_list = [ids.id for ids in variant_ids]

        self.gen_reference(template_id_list,'product.template')
        self.gen_reference(variant_id_list,'product.product')

    def gen_reference(self,active_ids,active_model):
        name_conf = False
        attrib_conf = False
        categ_conf = False
        seq_conf = False

        ir_param = self.env['ir.config_parameter'].sudo()
        name_len = ir_param.get_param('auto_generate_product_code_app.name_digit')
        name_sep = ir_param.get_param('auto_generate_product_code_app.name_separate')

        attrib_len = ir_param.get_param('auto_generate_product_code_app.attrib_digit')
        attrib_sep = ir_param.get_param('auto_generate_product_code_app.attrib_separate')

        categ_len = ir_param.get_param('auto_generate_product_code_app.categ_digit')
        categ_sep = ir_param.get_param('auto_generate_product_code_app.categ_separate')

        naming_state = ir_param.get_param('auto_generate_product_code_app.enable_naming')
        attrib_state = ir_param.get_param('auto_generate_product_code_app.enable_attrib')
        categ_state = ir_param.get_param('auto_generate_product_code_app.enable_categ')

        seq_state = ir_param.get_param('auto_generate_product_code_app.enable_seq')
        
        if naming_state == False and attrib_state == False and categ_state == False and seq_state == False:
            raise UserError(_(
                "Please enable at least one 'Auto generate internal reference feature'."
            ))

        if naming_state == "off" and attrib_state == "off" and categ_state == "off" and seq_state == "off":
            raise UserError(_(
                "Please enable at least one 'Auto generate internal reference feature'."
            ))

        if naming_state == "on":
            if not name_len or not name_sep:
                raise UserError(_(
                    "Lenght or separator for product naming is not defined."
                ))
            else:
                name_conf = True

        if attrib_state == "on":
            if not attrib_len or not attrib_sep:
                raise UserError(_(
                    "Lenght or separator for product attribute is not defined."
                ))            
            else:
                attrib_conf = True

        if categ_state == "on":
            if not categ_len or not categ_sep:
                raise UserError(_(
                    "Lenght or separator for product category is not defined."
                ))
            else:
                categ_conf = True

        if seq_state == "on":
            seq_conf = True

        for ids in active_ids:
            value_list=[]
            attrib_ids=[]
            attribute_list=[]
            reference = ""
            product = self.env[active_model].browse(ids)

            if name_conf:
                product_name = product.name[0:int(name_len)]+name_sep
                reference += product_name

            if attrib_conf:
                if active_model == "product.product":
                    for value in product.product_template_attribute_value_ids:
                        value_list.append(value.name[0:int(attrib_len)]+attrib_sep)
                
                    if len(value_list) > 0:
                        value_names = ''.join(map(str,value_list))
                        reference += value_names
                else:
                    if product.attribute_line_ids:
                        for attrib in product.attribute_line_ids:
                            for attr_id in attrib.value_ids:
                                attrib_ids.append(attr_id.id)
                    
                    if len(attrib_ids) > 0:
                        for a_id in attrib_ids:
                            attribute_id = self.env["product.attribute.value"].browse(a_id)
                            attribute_list.append(attribute_id.name[0:int(attrib_len)]+attrib_sep)

                    if len(attrib_ids) > 0:
                        attribute_names = ''.join(map(str,attribute_list))
                        reference += attribute_names

            if categ_conf:
                category_name = product.categ_id.name[0:int(categ_len)]+categ_sep
                reference += category_name

            if seq_conf:
                name_sequence = self.env["ir.sequence"].next_by_code("reference.sequence")
                reference += name_sequence

            if active_model == "product.template":
                if product.attribute_line_ids:
                    if len(product.attribute_line_ids) == 1:
                        for attr_ids in product.attribute_line_ids:
                            if len(attr_ids.value_ids) == 1:
                                product.write({'default_code':reference})
                else:
                    if not product.default_code:
                        product.write({'default_code':reference})
                    else:
                        if self.name:
                            product.write({'default_code':reference})

            elif active_model == "product.product":
                if not product.default_code:
                    product.write({'default_code':reference})
                else:
                    if self.name:
                        product.write({'default_code':reference})

class InheritSales(models.Model):
    _inherit = "sale.order"

class GenerateCode(models.TransientModel):
    _name = "generate.code"
    _description = "Generate Internal Reference Model"

    name = fields.Boolean(string="Replace Existing?", default=False)

    def generate_reference(self, *args):
        name_conf = False
        attrib_conf = False
        categ_conf = False
        seq_conf = False

        active_model = self._context.get('active_model') or args[1]
        active_ids = self._context.get('active_ids') or [args[0]]
        
        ir_param = self.env['ir.config_parameter'].sudo()
        name_len = ir_param.get_param('auto_generate_product_code_app.name_digit')
        name_sep = ir_param.get_param('auto_generate_product_code_app.name_separate')

        attrib_len = ir_param.get_param('auto_generate_product_code_app.attrib_digit')
        attrib_sep = ir_param.get_param('auto_generate_product_code_app.attrib_separate')

        categ_len = ir_param.get_param('auto_generate_product_code_app.categ_digit')
        categ_sep = ir_param.get_param('auto_generate_product_code_app.categ_separate')

        naming_state = ir_param.get_param('auto_generate_product_code_app.enable_naming')
        attrib_state = ir_param.get_param('auto_generate_product_code_app.enable_attrib')
        categ_state = ir_param.get_param('auto_generate_product_code_app.enable_categ')

        seq_state = ir_param.get_param('auto_generate_product_code_app.enable_seq')

        if naming_state == False and attrib_state == False and categ_state == False and seq_state == False:
            raise UserError(_(
                "Please enable at least one 'Auto generate internal reference feature'."
            ))

        if naming_state == "off" and attrib_state == "off" and categ_state == "off" and seq_state == "off":
            raise UserError(_(
                "Please enable at least one 'Auto generate internal reference feature'."
            ))

        if naming_state == "on":
            if not name_len or not name_sep:
                raise UserError(_(
                    "Lenght or separator for product naming is not defined."
                ))
            else:
                name_conf = True

        if attrib_state == "on":
            if not attrib_len or not attrib_sep:
                raise UserError(_(
                    "Lenght or separator for product attribute is not defined."
                ))            
            else:
                attrib_conf = True

        if categ_state == "on":
            if not categ_len or not categ_sep:
                raise UserError(_(
                    "Lenght or separator for product category is not defined."
                ))
            else:
                categ_conf = True

        if seq_state == "on":
            seq_conf = True

        for ids in active_ids:
            value_list=[]
            attrib_ids=[]
            attribute_list=[]
            reference = ""
            product = self.env[active_model].browse(ids)

            if name_conf:
                product_name = product.name[0:int(name_len)]+name_sep
                reference += product_name

            if attrib_conf:
                if active_model == "product.product":
                    for value in product.product_template_attribute_value_ids:
                        value_list.append(value.name[0:int(attrib_len)]+attrib_sep)
                
                    if len(value_list) > 0:
                        value_names = ''.join(map(str,value_list))
                        reference += value_names
                else:
                    if product.attribute_line_ids:
                        for attrib in product.attribute_line_ids:
                            for attr_id in attrib.value_ids:
                                attrib_ids.append(attr_id.id)
                    
                    if len(attrib_ids) > 0:
                        for a_id in attrib_ids:
                            attribute_id = self.env["product.attribute.value"].browse(a_id)
                            attribute_list.append(attribute_id.name[0:int(attrib_len)]+attrib_sep)

                    if len(attrib_ids) > 0:
                        attribute_names = ''.join(map(str,attribute_list))
                        reference += attribute_names

            if categ_conf:
                category_name = product.categ_id.name[0:int(categ_len)]+categ_sep
                reference += category_name

            if seq_conf:
                name_sequence = self.env["ir.sequence"].next_by_code("reference.sequence")
                reference += name_sequence
            
            if active_model == "product.template":
                if product.attribute_line_ids:
                    if len(product.attribute_line_ids) == 1:
                        for attr_ids in product.attribute_line_ids:
                            if len(attr_ids.value_ids) == 1:
                                product.write({'default_code':reference})
                else:
                    if not product.default_code:
                        product.write({'default_code':reference})
                    else:
                        if self.name:
                            product.write({'default_code':reference})

            elif active_model == "product.product":
                if not product.default_code:
                    product.write({'default_code':reference})
                else:
                    if self.name:
                        product.write({'default_code':reference})

class InheritTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def create(self, vals):
        result = super(InheritTemplate, self).create(vals)

        ir_param = self.env['ir.config_parameter'].sudo()
        auto_code_state = ir_param.get_param('auto_generate_product_code_app.new_product')
        
        if auto_code_state:
            self.env["generate.code"].generate_reference(result.id, "product.template")

        return result

class InheritProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, vals):
        result = super(InheritProduct, self).create(vals)

        ir_param = self.env['ir.config_parameter'].sudo()
        auto_code_state = ir_param.get_param('auto_generate_product_code_app.new_product')
        
        if auto_code_state:
            self.env["generate.code"].generate_reference(result.id, "product.product")

        return result