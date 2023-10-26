from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VrPrepareData(models.Model):
    _name = "vr.prepare.data"

    @staticmethod
    def get_payment_methods():
        return [
            ('1', 'EFECTIVO'),
            ('2', 'TARJETA'),
            ('3', 'CHEQUE'),
            ('4', 'VALES'),
            ('5', 'OTROS'),
            ('6', 'PAGO POSTERIOR'),
            ('7', 'TRANSFERENCIA BANCARIA'),
            ('8', 'DEPOSITO EN CUENTA'),
            ('9', 'TRANSFERENCIA SWIFT'),
            ('10', 'EFECTIVO-TARJETA'),
            ('11', 'EFECTIVO-CHEQUE'),
            ('12', 'EFECTIVO-VALES'),
            ('13', 'EFECTIVO-TRANSFERENCIA BANCARIA'),
            ('14', 'EFECTIVO-DEPOSITO EN CUENTA'),
            ('15', 'EFECTIVO-TRANSFERENCIA SWIFT'),
            ('16', 'TARJETA-CHEQUE'),
            ('17', 'TARJETA-VALES'),
            ('18', 'TARJETA-TRANSFERENCIA BANCARIA'),
            ('19', 'TARJETA-DEPOSITO EN CUENTA'),
            ('20', 'TARJETA-TRANSFERENCIA SWIFT'),
            ('21', 'VALES-TRANSFERENCIA BANCARIA'),
            ('22', 'VALES-TDEPOSITO EN CUENTA'),
            ('23', 'VALES-TRANSFERENCIA SWIFT'),
            ('24', 'TRANSFERENCIA BANCARIA-DEPOSITO EN CUENTA'),
            ('25', 'TRANSFERENCIA BANCARIA-TRANSFERENCIA SWIFT'),
            ('26', 'DEPOSITO EN CUENTA-TRANSFERENCIA SWIFT'),
            ('27', 'GIFT-CARD'),
            ('28', 'GIFT-CARD EFECTIVO'),
            ('29', 'GIFT-CARD TARJETA'),
            ('30', 'GIFT-CARD OTROS'),
            ('31', 'CANAL DE PAGO'),
            ('32', 'BILLETERA MOVIL'),
            ('33', 'PAGO ONLINE'),
            ('34', 'EFECTIVO - PAGO POSTERIOR'),
            ('35', 'EFECTIVO - GIFT CARD'),
            ('36', 'EFECTIVO - CANAL PAGO'),
            ('37', 'EFECTIVO - BILLETERA MOVIL'),
            ('38', 'EFECTIVO - PAGO ONLINE'),
            ('39', 'TARJETA - PAGO POSTERIOR'),
            ('40', 'TARJETA - GIFT'),
            ('41', 'TARJETA - CANAL PAGO'),
            ('42', 'TARJETA - BILLETERA MOVIL'),
            ('43', 'TARJETA - PAGO ONLINE'),
            ('44', 'CHEQUE - VALES'),
            ('45', 'CHEQUE - PAGO POSTERIOR'),
            ('46', 'CHEQUE - TRANSFERENCIA'),
            ('47', 'CHEQUE - DEPOSITO'),
            ('48', 'CHEQUE - SWIFT'),
            ('49', 'CHEQUE - GIFT'),
            ('50', 'CHEQUE - CANAL PAGO'),
            ('51', 'CHEQUE - BILLETERA'),
            ('52', 'CHEQUE - PAGO ONLINE'),
            ('53', 'VALES - GIFT'),
            ('54', 'VALES - CANAL DE PAGO'),
            ('55', 'VALES - BILLETERA'),
            ('56', 'VALES - PAGO ONLINE'),
            ('57', 'PAGO POSTERIOR - TRANSFERENCIA'),
            ('58', 'PAGO POSTERIOR - DEPOSITO'),
            ('59', 'PAGO POSTERIOR - SWIFT'),
            ('60', 'PAGO POSTERIOR - GIFT'),
            ('61', 'PAGO POSTERIOR - CANAL'),
            ('62', 'PAGO POSTERIOR - BILLETERA'),
            ('63', 'PAGO POSTERIOR - PAGO ONLINE'),
            ('64', 'TRANSFERENCIA - GIFT'),
            ('65', 'TRANSFERENCIA - CANAL'),
            ('66', 'TRANSFERENCIA - BILLETERA'),
            ('67', 'TRANSFERENCIA - PAGO ONLINE'),
            ('68', 'DEPOSITO - GIFT'),
            ('69', 'DEPOSITO - CANAL '),
            ('70', 'DEPOSITO - BILLETERA'),
            ('71', 'DEPOSITO - PAGO ONLINE'),
            ('72', 'SWIFT - GIFT'),
            ('73', 'SWIFT - CANAL'),
            ('74', 'SWIFT - BILLETERA'),
            ('75', 'SWIFT - PAGO ONLINE'),
            ('76', 'GIFT - CANAL DE PAGO'),
            ('77', 'GIFT - BILLETERA'),
            ('78', 'GIFT - PAGO ONLINE'),
            ('79', 'CANAL DE PAGO - BILLETERA'),
            ('80', 'CANAL DE PAGO - PAGO ONLINE'),
            ('81', 'BILLETERA - PAGO ONLINE'),
            ('82', 'EFECTIVO - TARJETA - PAGO POSTERIOR'),
            ('83', 'EFECTIVO - TARJETA - TRANSFERENCIA BANCARIA'),
            ('84', 'EFECTIVO - TARJETA - DEPOSITO EN CUENTA'),
            ('85', 'EFECTIVO - TARJETA - TRANSFERENCIA SWIFT'),
            ('86', 'EFECTIVO - TARJETA - GIFT-CARD'),
            ('87', 'EFECTIVO - TARJETA - CANAL DE PAGO'),
            ('88', 'EFECTIVO - TARJETA - BILLETERA MOVIL'),
            ('89', 'EFECTIVO - TARJETA - PAGO ONLINE'),
            ('90', 'EFECTIVO - CHEQUE - PAGO POSTERIOR'),
            ('91', 'EFECTIVO - CHEQUE - TRANSFERENCIA BANCARIA'),
            ('92', 'EFECTIVO - CHEQUE - DEPOSITO EN CUENTA'),
            ('93', 'EFECTIVO - CHEQUE - TRANSFERENCIA SWIFT'),
            ('94', 'EFECTIVO - CHEQUE - GIFT-CARD'),
            ('95', 'EFECTIVO - CHEQUE - CANAL DE PAGO'),
            ('96', 'EFECTIVO - CHEQUE - BILLETERA MOVIL'),
            ('97', 'EFECTIVO - CHEQUE - PAGO ONLINE'),
            ('98', 'EFECTIVO - VALES - PAGO POSTERIOR'),
            ('99', 'EFECTIVO - VALES - TRANSFERENCIA BANCARIA'),
            ('100', 'EFECTIVO - VALES - DEPOSITO EN CUENTA'),
            ('101', 'EFECTIVO - VALES - TRANSFERENCIA SWIFT'),
            ('102', 'EFECTIVO - VALES - GIFT-CARD'),
            ('103', 'EFECTIVO - VALES - CANAL DE PAGO'),
            ('104', 'EFECTIVO - VALES - BILLETERA MOVIL'),
            ('105', 'EFECTIVO - VALES - PAGO ONLINE'),
            ('106', 'EFECTIVO - PAGO POSTERIOR - TRANSFERENCIA BANCARIA'),
            ('107', 'EFECTIVO - PAGO POSTERIOR - DEPOSITO EN CUENTA'),
            ('108', 'EFECTIVO - PAGO POSTERIOR - TRANSFERENCIA SWIFT'),
            ('109', 'EFECTIVO - PAGO POSTERIOR - GIFT-CARD'),
            ('110', 'EFECTIVO - PAGO POSTERIOR - CANAL DE PAGO'),
            ('111', 'EFECTIVO - PAGO POSTERIOR - BILLETERA MOVIL'),
            ('112', 'EFECTIVO - PAGO POSTERIOR - PAGO ONLINE'),
            ('113', 'EFECTIVO - TRANSFERENCIA - DEPOSITO EN CUENTA'),
            ('114', 'EFECTIVO - TRANSFERENCIA - TRANSFERENCIA SWIFT'),
            ('115', 'EFECTIVO - TRANSFERENCIA - GIFT-CARD'),
            ('116', 'EFECTIVO - TRANSFERENCIA - CANAL DE PAGO'),
            ('117', 'EFECTIVO - TRANSFERENCIA - BILLETERA MOVIL'),
            ('118', 'EFECTIVO - TRANSFERENCIA - PAGO ONLINE'),
            ('119', 'EFECTIVO - DEPOSITO EN CUENTA - TRANSFERENCIA SWIFT'),
            ('120', 'EFECTIVO - DEPOSITO EN CUENTA - GIFT-CARD'),
            ('121', 'EFECTIVO - DEPOSITO EN CUENTA - CANAL DE PAGO'),
            ('122', 'EFECTIVO - DEPOSITO EN CUENTA - BILLETERA MOVIL'),
            ('123', 'EFECTIVO - DEPOSITO EN CUENTA - PAGO ONLINE'),
            ('124', 'EFECTIVO - SWIFT - GIFT-CARD'),
            ('125', 'EFECTIVO - SWIFT - CANAL DE PAGO'),
            ('126', 'EFECTIVO - SWIFT - BILLETERA MOVIL'),
            ('127', 'EFECTIVO - SWIFT - PAGO ONLINE'),
            ('128', 'EFECTIVO - GIFT CARD - CANAL DE PAGO'),
            ('129', 'EFECTIVO - GIFT CARD - BILLETERA MOVIL'),
            ('130', 'EFECTIVO - GIFT CARD - PAGO ONLINE'),
            ('131', 'EFECTIVO - CANAL PAGO - BILLETERA MOVIL'),
            ('132', 'EFECTIVO - CANAL PAGO - PAGO ONLINE'),
            ('133', 'EFECTIVO - BILLETERA MOVIL - PAGO ONLINE'),
            ('134', 'TARJETA - CHEQUE - PAGO POSTERIOR'),
            ('135', 'TARJETA - CHEQUE - TRANSFERENCIA BANCARIA'),
            ('136', 'TARJETA - CHEQUE - DEPOSITO EN CUENTA'),
            ('137', 'TARJETA - CHEQUE - TRANSFERENCIA SWIFT'),
            ('138', 'TARJETA - CHEQUE - GIFT-CARD'),
            ('139', 'TARJETA - CHEQUE - CANAL DE PAGO'),
            ('140', 'TARJETA - CHEQUE - BILLETERA MOVIL'),
            ('141', 'TARJETA - CHEQUE - PAGO ONLINE'),
            ('142', 'TARJETA - VALES - PAGO POSTERIOR'),
            ('143', 'TARJETA - VALES - TRANSFERENCIA BANCARIA'),
            ('144', 'TARJETA - VALES - DEPOSITO EN CUENTA'),
            ('145', 'TARJETA - VALES - TRANSFERENCIA SWIFT'),
            ('146', 'TARJETA - VALES - GIFT-CARD'),
            ('147', 'TARJETA - VALES - CANAL DE PAGO'),
            ('148', 'TARJETA - VALES - BILLETERA MOVIL'),
            ('149', 'TARJETA - VALES - PAGO ONLINE'),
            ('150', 'TARJETA - PAGO POSTERIOR - TRANSFERENCIA BANCARIA'),
            ('151', 'TARJETA - PAGO POSTERIOR - DEPOSITO EN CUENTA'),
            ('152', 'TARJETA - PAGO POSTERIOR - TRANSFERENCIA SWIFT'),
            ('153', 'TARJETA - PAGO POSTERIOR - GIFT-CARD'),
            ('154', 'TARJETA - PAGO POSTERIOR - CANAL DE PAGO'),
            ('155', 'TARJETA - PAGO POSTERIOR - BILLETERA MOVIL'),
            ('156', 'TARJETA - PAGO POSTERIOR - PAGO ONLINE'),
            ('157', 'TARJETA - TRANSFERENCIA - DEPOSITO EN CUENTA'),
            ('158', 'TARJETA - TRANSFERENCIA - TRANSFERENCIA SWIFT'),
            ('159', 'TARJETA - TRANSFERENCIA - GIFT-CARD'),
            ('160', 'TARJETA - TRANSFERENCIA - CANAL DE PAGO'),
            ('161', 'TARJETA - TRANSFERENCIA - BILLETERA MOVIL'),
            ('162', 'TARJETA - TRANSFERENCIA - PAGO ONLINE'),
            ('163', 'TARJETA - DEPOSITO - TRANSFERENCIA SWIFT'),
            ('164', 'TARJETA - DEPOSITO - GIFT-CARD'),
            ('165', 'TARJETA - DEPOSITO - CANAL DE PAGO'),
            ('166', 'TARJETA - DEPOSITO - BILLETERA MOVIL'),
            ('167', 'TARJETA - DEPOSITO - PAGO ONLINE'),
            ('168', 'TARJETA - SWIFT - GIFT-CARD'),
            ('169', 'TARJETA - SWIFT - CANAL DE PAGO'),
            ('170', 'TARJETA - SWIFT - BILLETERA MOVIL'),
            ('171', 'TARJETA - SWIFT - PAGO ONLINE'),
            ('172', 'TARJETA - GIFT - CANAL DE PAGO'),
            ('173', 'TARJETA - GIFT - BILLETERA MOVIL'),
            ('174', 'TARJETA - GIFT - PAGO ONLINE'),
            ('175', 'TARJETA - CANAL PAGO - BILLETERA MOVIL'),
            ('176', 'TARJETA - CANAL PAGO - PAGO ONLINE'),
            ('177', 'TARJETA - BILLETERA MOVIL - PAGO ONLINE'),
            ('178', 'CHEQUE - VALES - PAGO POSTERIOR'),
            ('179', 'CHEQUE - VALES - TRANSFERENCIA BANCARIA'),
            ('180', 'CHEQUE - VALES - DEPOSITO EN CUENTA'),
            ('181', 'CHEQUE - VALES - TRANSFERENCIA SWIFT'),
            ('182', 'CHEQUE - VALES - GIFT-CARD'),
            ('183', 'CHEQUE - VALES - CANAL DE PAGO'),
            ('184', 'CHEQUE - VALES - BILLETERA MOVIL'),
            ('185', 'CHEQUE - VALES - PAGO ONLINE'),
            ('186', 'CHEQUE - PAGO POSTERIOR - TRANSFERENCIA BANCARIA'),
            ('187', 'CHEQUE - PAGO POSTERIOR - DEPOSITO EN CUENTA'),
            ('188', 'CHEQUE - PAGO POSTERIOR - TRANSFERENCIA SWIFT'),
            ('189', 'CHEQUE - PAGO POSTERIOR - GIFT-CARD'),
            ('190', 'CHEQUE - PAGO POSTERIOR - CANAL DE PAGO'),
            ('191', 'CHEQUE - PAGO POSTERIOR - BILLETERA MOVIL'),
            ('192', 'CHEQUE - PAGO POSTERIOR - PAGO ONLINE'),
            ('193', 'CHEQUE - TRANSFERENCIA - DEPOSITO EN CUENTA'),
            ('194', 'CHEQUE - TRANSFERENCIA - TRANSFERENCIA SWIFT'),
            ('195', 'CHEQUE - TRANSFERENCIA - GIFT-CARD'),
            ('196', 'CHEQUE - TRANSFERENCIA - CANAL DE PAGO'),
            ('197', 'CHEQUE - TRANSFERENCIA - BILLETERA MOVIL'),
            ('198', 'CHEQUE - TRANSFERENCIA - PAGO ONLINE'),
            ('199', 'CHEQUE - DEPOSITO - TRANSFERENCIA SWIFT'),
            ('200', 'CHEQUE - DEPOSITO - GIFT-CARD'),
            ('201', 'CHEQUE - DEPOSITO - CANAL DE PAGO'),
            ('202', 'CHEQUE - DEPOSITO - BILLETERA MOVIL'),
            ('203', 'CHEQUE - DEPOSITO - PAGO ONLINE'),
            ('204', 'CHEQUE - SWIFT - GIFT-CARD'),
            ('205', 'CHEQUE - SWIFT - CANAL DE PAGO'),
            ('206', 'CHEQUE - SWIFT - BILLETERA MOVIL'),
            ('207', 'CHEQUE - SWIFT - PAGO ONLINE'),
            ('208', 'CHEQUE - GIFT - CANAL DE PAGO'),
            ('209', 'CHEQUE - GIFT - BILLETERA MOVIL'),
            ('210', 'CHEQUE - GIFT - PAGO ONLINE'),
            ('211', 'CHEQUE - CANAL PAGO - BILLETERA MOVIL'),
            ('212', 'CHEQUE - CANAL PAGO - PAGO ONLINE'),
            ('213', 'CHEQUE - BILLETERA - PAGO ONLINE'),
            ('214', 'VALES - SWIFT - TRANSFERENCIA BANCARIA'),
            ('215', 'VALES - SWIFT - DEPOSITO EN CUENTA'),
            ('216', 'VALES - SWIFT - TRANSFERENCIA SWIFT'),
            ('217', 'VALES - SWIFT - GIFT-CARD'),
            ('218', 'VALES - SWIFT - CANAL DE PAGO'),
            ('219', 'VALES - SWIFT - BILLETERA MOVIL'),
            ('220', 'VALES - SWIFT - PAGO ONLINE'),
            ('221', 'VALES - GIFT - DEPOSITO EN CUENTA'),
            ('222', 'VALES - GIFT - TRANSFERENCIA SWIFT'),
            ('223', 'VALES - GIFT - GIFT-CARD'),
            ('224', 'VALES - GIFT - CANAL DE PAGO'),
            ('225', 'VALES - GIFT - BILLETERA MOVIL'),
            ('226', 'VALES - GIFT - PAGO ONLINE'),
            ('227', 'VALES - CANAL DE PAGO - TRANSFERENCIA SWIFT'),
            ('228', 'VALES - CANAL DE PAGO - GIFT-CARD'),
            ('229', 'VALES - CANAL DE PAGO - CANAL DE PAGO'),
            ('230', 'VALES - CANAL DE PAGO - BILLETERA MOVIL'),
            ('231', 'VALES - CANAL DE PAGO - PAGO ONLINE'),
            ('232', 'VALES - BILLETERA - GIFT-CARD'),
            ('233', 'VALES - BILLETERA - CANAL DE PAGO'),
            ('234', 'VALES - BILLETERA - BILLETERA MOVIL'),
            ('235', 'VALES - BILLETERA - PAGO ONLINE'),
            ('236', 'VALES - PAGO ONLINE - CANAL DE PAGO'),
            ('237', 'VALES - PAGO ONLINE - BILLETERA MOVIL'),
            ('238', 'VALES - PAGO ONLINE - PAGO ONLINE'),
            ('239', 'PAGO POSTERIOR - TRANSFERENCIA - DEPOSITO EN CUENTA'),
            ('240', 'PAGO POSTERIOR - TRANSFERENCIA - TRANSFERENCIA SWIFT'),
            ('241', 'PAGO POSTERIOR - TRANSFERENCIA - GIFT-CARD'),
            ('242', 'PAGO POSTERIOR - TRANSFERENCIA - CANAL DE PAGO'),
            ('243', 'PAGO POSTERIOR - TRANSFERENCIA - BILLETERA MOVIL'),
            ('244', 'PAGO POSTERIOR - TRANSFERENCIA - PAGO ONLINE'),
            ('245', 'PAGO POSTERIOR - DEPOSITO - TRANSFERENCIA SWIFT'),
            ('246', 'PAGO POSTERIOR - DEPOSITO - GIFT-CARD'),
            ('247', 'PAGO POSTERIOR - DEPOSITO - CANAL DE PAGO'),
            ('248', 'PAGO POSTERIOR - DEPOSITO - BILLETERA MOVIL'),
            ('249', 'PAGO POSTERIOR - DEPOSITO - PAGO ONLINE'),
            ('250', 'PAGO POSTERIOR - SWIFT - GIFT-CARD'),
            ('251', 'PAGO POSTERIOR - SWIFT - CANAL DE PAGO'),
            ('252', 'PAGO POSTERIOR - SWIFT - BILLETERA MOVIL'),
            ('253', 'PAGO POSTERIOR - SWIFT - PAGO ONLINE'),
            ('254', 'PAGO POSTERIOR - GIFT - CANAL DE PAGO'),
            ('255', 'PAGO POSTERIOR - GIFT - BILLETERA MOVIL'),
            ('256', 'PAGO POSTERIOR - GIFT - PAGO ONLINE'),
            ('257', 'PAGO POSTERIOR - CANAL - BILLETERA MOVIL'),
            ('258', 'PAGO POSTERIOR - CANAL - PAGO ONLINE'),
            ('259', 'PAGO POSTERIOR - BILLETERA - PAGO ONLINE'),
            ('260', 'TRANSFERENCIA - DEPOSITO  - TRANSFERENCIA SWIFT'),
            ('261', 'TRANSFERENCIA - DEPOSITO  - GIFT-CARD'),
            ('262', 'TRANSFERENCIA - DEPOSITO  - CANAL DE PAGO'),
            ('263', 'TRANSFERENCIA - DEPOSITO  - BILLETERA MOVIL'),
            ('264', 'TRANSFERENCIA - DEPOSITO  - PAGO ONLINE'),
            ('265', 'TRANSFERENCIA - SWIFT - GIFT-CARD'),
            ('266', 'TRANSFERENCIA - SWIFT - CANAL DE PAGO'),
            ('267', 'TRANSFERENCIA - SWIFT - BILLETERA MOVIL'),
            ('268', 'TRANSFERENCIA - SWIFT - PAGO ONLINE'),
            ('269', 'TRANSFERENCIA - GIFT - CANAL DE PAGO'),
            ('270', 'TRANSFERENCIA - GIFT - BILLETERA MOVIL'),
            ('271', 'TRANSFERENCIA - GIFT - PAGO ONLINE'),
            ('272', 'TRANSFERENCIA - CANAL - BILLETERA MOVIL'),
            ('273', 'TRANSFERENCIA - CANAL - PAGO ONLINE'),
            ('274', 'TRANSFERENCIA - BILLETERA - PAGO ONLINE'),
            ('275', 'DEPOSITO - SWIFT - GIFT-CARD'),
            ('276', 'DEPOSITO - SWIFT - CANAL DE PAGO'),
            ('277', 'DEPOSITO - SWIFT - BILLETERA MOVIL'),
            ('278', 'DEPOSITO - SWIFT - PAGO ONLINE'),
            ('279', 'DEPOSITO - GIFT - CANAL DE PAGO'),
            ('280', 'DEPOSITO - GIFT - BILLETERA MOVIL'),
            ('281', 'DEPOSITO - GIFT - PAGO ONLINE'),
            ('282', 'DEPOSITO - CANAL  - BILLETERA MOVIL'),
            ('283', 'DEPOSITO - CANAL  - PAGO ONLINE'),
            ('284', 'DEPOSITO - BILLETERA - PAGO ONLINE'),
            ('285', 'SWIFT - GIFT - CANAL DE PAGO'),
            ('286', 'SWIFT - GIFT - BILLETERA MOVIL'),
            ('287', 'SWIFT - GIFT - PAGO ONLINE'),
            ('288', 'SWIFT - CANAL - BILLETERA MOVIL'),
            ('289', 'SWIFT - CANAL - PAGO ONLINE'),
            ('290', 'SWIFT - BILLETERA - PAGO ONLINE'),
            ('291', 'GIFT - CANAL DE PAGO - BILLETERA MOVIL'),
            ('292', 'GIFT - CANAL DE PAGO - PAGO ONLINE'),
            ('293', 'GIFT - BILLETERA - PAGO ONLINE'),
            ('294', 'CANAL DE PAGO - BILLETERA - PAGO ONLINE'),
            ('295', 'DEBITO AUTOMATICO'),
            ('296', 'DEBITO AUTOMATICO - EFECTIVO'),
            ('297', 'DEBITO AUTOMATICO -TARJETA'),
            ('298', 'DEBITO AUTOMATICO - CHEQUE'),
            ('299', 'DEBITO AUTOMATICO -  VALE'),
            ('300', 'DEBITO AUTOMATICO -  PAGO POSTERIOR'),
            ('301', 'DEBITO AUTOMATICO -  TRANSFERENCIA BANCARIA'),
            ('302', 'DEBITO AUTOMATICO -  DEPOSITO EN CUENTA'),
            ('303', 'DEBITO AUTOMATICO -  TRANSFERENCIA SWIFT'),
            ('304', 'DEBITO AUTOMATICO -  GIFT CARD'),
            ('305', 'DEBITO AUTOMATICO -  CANAL DE PAGO'),
            ('306', 'DEBITO AUTOMATICO -  BILLETERA MOVIL'),
            ('307', 'DEBITO AUTOMATICO -  PAGO ONLINE'),
            ('308', 'DEBITO AUTOMATICO - OTRO')
        ]

    @staticmethod
    def prepare_data_for_invoice(obj_inv, use_native_discount=False):
        data = {
            'codigo_sucursal': str(obj_inv.vr_warehouse_id.vr_codigo_sucursal),
            'codigo_pos': "0",
            'razon_social': obj_inv.vr_razon_social,
            'tipo_documento_identidad': obj_inv.vr_tipo_documento_identidad,
            'nit_cliente': obj_inv.vr_nit_ci,
            'extension': str(obj_inv.vr_extension) if obj_inv.vr_extension else '',
            'codigo_cliente': obj_inv.partner_id.id,
            'metodo_pago': str(obj_inv.vr_metodo_pago),
            'nro_tarjeta': obj_inv.vr_nro_tarjeta if obj_inv.vr_nro_tarjeta else '',
            'codigo_moneda': obj_inv.vr_warehouse_id.vr_tipo_moneda,
            'tipo_cambio': 1,
            'monto_gift_card': 0,
            'descuento_adicional': 0,
            'usuario': str(obj_inv.env.user.id),
            'correo_cliente': obj_inv.partner_id.email or '',
        }
        detalle = []
        for line in obj_inv.invoice_line_ids.filtered(lambda l: l.price_unit > 0 and l.display_type != 'line_note' and l.display_type != 'line_section'):
            if not line.product_id.vr_codigo_producto:
                raise ValidationError(
                    _('El producto "%s" necesita estar homologado.', line.name))
            if not line.product_id.vr_codigo_actividad:
                raise ValidationError(
                    _('El producto "%s" necesita estar homologado.', line.name))
            if not line.product_id.vr_codigo_unidad_medida:
                raise ValidationError(_('El producto %s necesita la Unidad de Medida homologada.', line.name))
            if use_native_discount:
                if line.discount == 100:
                    raise ValidationError(
                        _('No puede existir una linea de venta con cien por ciento de descuento (%s).', line.name))
            else:
                if line.disc == 100:
                    raise ValidationError(_('No puede existir una linea de venta con cien por ciento de descuento (%s).', line.name))
            # DESCUENTO
            if use_native_discount:
                discount = round((line.price_unit * line.quantity) * (line.discount / 100), ndigits=2)
            else:
                discount = round((line.price_unit * line.quantity) * (line.disc / 100), ndigits=2)
            detalle.append({
                'codigo_producto': str(line.product_id.vr_codigo_producto),
                'codigo_producto_cliente': line.product_id.vr_nombre_producto,
                'codigo_actividad': str(line.product_id.vr_codigo_actividad),
                'descripcion': line.name,
                'cantidad': line.quantity,
                'unidad_medida': line.product_id.vr_codigo_unidad_medida,
                'precio_unitario': line.price_unit,
                'monto_descuento': discount
            })
        data['detalle'] = detalle
        return data

    @staticmethod
    def prepare_data_for_invoice_offline(obj_inv, order, use_native_discount=True):
        data = {
            'codigo_sucursal': str(obj_inv.config_id.vr_codigo_sucursal),
            'codigo_pos': str(obj_inv.config_id.vr_codigo_pos),
            'razon_social': order['vr_razon_social_cliente'],
            'tipo_documento_identidad': order['vr_tipo_documento_identidad'],
            'nit_cliente': order['vr_nit_ci'],
            'extension': str(order['vr_extension']),
            'codigo_cliente': obj_inv.partner_id.id,
            'metodo_pago': str(obj_inv.vr_metodo_pago),
            'nro_tarjeta': obj_inv.vr_nro_tarjeta if obj_inv.vr_nro_tarjeta else '',
            'codigo_moneda': obj_inv.vr_warehouse_id.vr_tipo_moneda,
            'tipo_cambio': 1,
            'monto_gift_card': 0,
            'descuento_adicional': 0,
            'usuario': str(obj_inv.env.user.id),
            'correo_cliente': 'carlosnorbertolf@gmail.com',
        }
        detalle = []
        for line in obj_inv.invoice_line_ids.filtered(
                lambda l: l.price_unit > 0 and l.display_type != 'line_note' and l.display_type != 'line_section'):
            if not line.product_id.vr_codigo_producto:
                raise ValidationError(
                    _('El producto "%s" necesita estar homologado.', line.name))
            if not line.product_id.vr_codigo_actividad:
                raise ValidationError(
                    _('El producto "%s" necesita estar homologado.', line.name))
            if not line.product_id.vr_codigo_unidad_medida:
                raise ValidationError(
                    _('El producto %s necesita la Unidad de Medida homologada.', line.name))
            # DESCUENTO
            if use_native_discount:
                discount = round((line.price_unit * line.quantity) * (line.discount / 100), ndigits=2)
            else:
                discount = round((line.price_unit * line.quantity) * (line.disc / 100), ndigits=2)
            detalle.append({
                'codigo_producto': str(line.product_id.vr_codigo_producto),
                'codigo_producto_cliente': line.product_id.vr_nombre_producto,
                'codigo_actividad': str(line.product_id.vr_codigo_actividad),
                'descripcion': line.name,
                'cantidad': line.quantity,
                'unidad_medida': line.product_id.vr_codigo_unidad_medida,
                'precio_unitario': line.price_unit,
                'monto_descuento': discount
            })
        data['detalle'] = detalle
        return data

    @staticmethod
    def prepare_data_for_cancellation(obj_inv, pos=False):
        if obj_inv.vr_codigo_motivo:
            data = {
                'codigo_sucursal': str(obj_inv.vr_warehouse_id.vr_codigo_sucursal) if not pos else str(obj_inv.config_id.vr_codigo_sucursal),
                'codigo_pos': '0' if not pos else str(obj_inv.config_id.vr_codigo_pos),
                'codigo_recepcion': obj_inv.vr_codigo_recepcion,
                'motivo_anulacion': obj_inv.vr_codigo_motivo,
            }
            return data
        else:
            raise ValidationError(_('Debe elegir un motivo de anulación en el formulario.'))

    @staticmethod
    def prepare_data_for_get_pdf(obj_inv, type, pos=False):
        data = {
            'codigo_sucursal': str(obj_inv.vr_warehouse_id.vr_codigo_sucursal) if not pos else str(
                obj_inv.config_id.vr_codigo_sucursal),
            'codigo_pos': '0' if not pos else str(obj_inv.config_id.vr_codigo_pos),
            'codigo_recepcion': obj_inv.vr_codigo_recepcion,
            'type': type,
        }
        if not obj_inv.vr_codigo_recepcion:
            data['customer_order_id'] = obj_inv.id
        return data

    @staticmethod
    def prepare_data_for_get_xml(obj_inv, pos=False):
        data = {
            'codigo_sucursal': str(obj_inv.vr_warehouse_id.vr_codigo_sucursal) if not pos else str(
                obj_inv.config_id.vr_codigo_sucursal),
            'codigo_pos': '0' if not pos else str(obj_inv.config_id.vr_codigo_pos),
            'codigo_recepcion': obj_inv.vr_codigo_recepcion,
        }
        if not obj_inv.vr_codigo_recepcion:
            data['customer_order_id'] = obj_inv.id
        return data