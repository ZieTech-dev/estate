# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Propriete(models.Model):
    _name = 'estate.propriete'
    _description = 'Propriété'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    type_id = fields.Many2one('estate.type.propriete', string="Type", help="Définir le type de propriété")
    superficie = fields.Float("Superficie (m²)")
    piece_ids = fields.One2many('estate.piece', 'propriete_id', string='Pièces')
    commodite_ids = fields.One2many('estate.commodite', 'propriete_id', string='Commodités')
    loyer_mensuel = fields.Integer("Loyer mensuel", required=True)
    etat = fields.Selection([
        ('libre', 'Libre'),
        ('occupee', 'Occupée'),
        ('reservee', 'Réservée'),
    ], string="État", default="libre", tracking=True)
