from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_selection = [
    ('1', 'BOBINAS'),
    ('2', 'BALDE'),
    ('3', 'BARRILES'),
    ('4', 'BOLSA'),
    ('5', 'BOTELLAS'),
    ('6', 'CAJA'),
    ('7', 'CARTONES'),
    ('8', 'CENTIMETRO CUADRADO'),
    ('9', 'CENTIMETRO CUBICO'),
    ('10', 'CENTIMETRO LINEAL'),
    ('11', 'CIENTO DE UNIDADES'),
    ('12', 'CILINDRO'),
    ('13', 'CONOS'),
    ('14', 'DOCENA'),
    ('15', 'FARDO'),
    ('16', 'GALON INGLES'),
    ('17', 'GRAMO'),
    ('18', 'GRUESA'),
    ('19', 'HECTOLITRO'),
    ('20', 'HOJA'),
    ('21', 'JUEGO'),
    ('22', 'KILOGRAMO'),
    ('23', 'KILOMETRO'),
    ('24', 'KILOVATIO HORA'),
    ('25', 'KIT'),
    ('26', 'LATAS'),
    ('27', 'LIBRAS'),
    ('28', 'LITRO'),
    ('29', 'MEGAWATT HORA'),
    ('30', 'METRO'),
    ('31', 'METRO CUADRADO'),
    ('32', 'METRO CUBICO'),
    ('33', 'MILIGRAMOS'),
    ('34', 'MILILITRO'),
    ('35', 'MILIMETRO'),
    ('36', 'MILIMETRO CUADRADO'),
    ('37', 'MILIMETRO CUBICO'),
    ('38', 'MILLARES'),
    ('39', 'MILLON DE UNIDADES'),
    ('40', 'ONZAS'),
    ('41', 'PALETAS'),
    ('42', 'PAQUETE'),
    ('43', 'PAR'),
    ('44', 'PIES'),
    ('45', 'PIES CUADRADOS'),
    ('46', 'PIES CUBICOS'),
    ('47', 'PIEZAS'),
    ('48', 'PLACAS'),
    ('49', 'PLIEGO'),
    ('50', 'PULGADAS'),
    ('51', 'RESMA'),
    ('52', 'TAMBOR'),
    ('53', 'TONELADA CORTA'),
    ('54', 'TONELADA LARGA'),
    ('55', 'TONELADAS'),
    ('56', 'TUBOS'),
    ('57', 'UNIDAD (BIENES)'),
    ('58', 'UNIDAD (SERVICIOS)'),
    ('59', 'US GALON (37843 L)'),
    ('60', 'YARDA'),
    ('61', 'YARDA CUADRADA'),
    ('62', 'OTRO'),
    ('63', 'ONZA TROY'),
    ('64', 'LIBRA FINA'),
    ('65', 'DISPLAY'),
    ('66', 'BULTO'),
    ('67', 'DIAS'),
    ('68', 'MESES'),
    ('69', 'QUINTAL'),
    ('70', 'ROLLO'),
    ('71', 'HORAS'),
    ('72', 'AGUJA'),
    ('73', 'AMPOLLA'),
    ('74', 'BIDON'),
    ('75', 'BOLSA'),
    ('76', 'CAPSULA'),
    ('77', 'CARTUCHO'),
    ('78', 'COMPRIMIDO'),
    ('79', 'ESTUCHE'),
    ('80', 'FRASCO'),
    ('81', 'JERINGA'),
    ('82', 'MINI BOTELLA'),
    ('83', 'SACHET'),
    ('84', 'TABLETA'),
    ('85', 'TERMO'),
    ('86', 'TUBO'),
    ('87', 'BARRIL (EEUU) 60 F'),
    ('88', 'BARRIL [42 GALONES(EEUU)]'),
    ('89', 'METRO CUBICO 68F VOL'),
    ('90', 'MIL PIES CUBICOS 14696 PSI'),
    ('91', 'MIL PIES CUBICOS 14696 PSI 68FAH'),
    ('92', 'MILLAR DE PIES CUBICOS (1000 PC)'),
    ('93', 'MILLONES DE PIES CUBICOS (1000000 PC)'),
    ('94', 'MILLONES DE PIES CUBICOS (1000000 PC)'),
    ('95', 'MILLONES DE BTU (1000000 BTU)'),
    ('96', 'UNIDAD TERMICA BRITANICA (TI) '),
    ('97', 'VASO'),
    ('98', 'TETRAPACK'),
    ('99', 'CARTOLA'),
    ('100', 'JABA'),
    ('101', 'YARDA'),
    ('102', 'BANDEJA'),
    ('103', 'TURRIL'),
    ('104', 'BLISTER'),
    ('105', 'TIRA'),
    ('106', 'MEGAWATT'),
    ('107', 'KILOWATT'),
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    vr_codigo_producto = fields.Integer(
        string='Código Producto',
    )

    vr_codigo_actividad = fields.Integer(
        string='Código Actividad',
    )

    vr_codigo_unidad_medida = fields.Selection(
        selection=_selection,
        string='Código Unidad Medida',
    )

    vr_tipo_nombre_producto = fields.Selection([
        ('internal', 'Referencia Interna'),
        ('barcode', 'Código de Barras'),
    ],
        string='Usar como nombre de Producto',
    )

    vr_nombre_producto = fields.Char(
        string='Nombre Producto',
        compute='_vr_compute_nombre_producto',
        store=True,
    )

    def get_unidad_medida_description(self, codigo):
        return list(filter(lambda x: codigo in x, _selection))[0][1]

    @api.depends('vr_tipo_nombre_producto')
    def _vr_compute_nombre_producto(self):
        for res in self:
            if res.vr_tipo_nombre_producto == 'internal':
                res.vr_nombre_producto = res.default_code
            elif res.vr_tipo_nombre_producto == 'barcode':
                res.vr_nombre_producto = res.barcode
            else:
                res.vr_nombre_producto = False

    @api.constrains('vr_nombre_producto')
    def check_internal_reference_or_barcode(self):
        for res in self:
            if not res.default_code and res.vr_tipo_nombre_producto == 'internal':
                raise ValidationError(
                    _('Es necesario establecer la referencia interna del producto en la pestaña "Información General".'))
            elif not res.barcode and res.vr_tipo_nombre_producto == 'barcode':
                raise ValidationError(
                    _('Es necesario establecer el código barcode del producto en la pestaña "Información General".'))