# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Piece(models.Model):
    _name = 'estate.piece'
    _description = 'Pièce'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    type_id = fields.Many2one('estate.type.piece', string="Type", help="Définir le type de pièce")
    propriete_id = fields.Many2one('estate.propriete', string="Propriété", required=True)
    superficie = fields.Float("Superficie (m²)")
    commodite_ids = fields.One2many('estate.commodite', 'piece_id', string='Commodités')
