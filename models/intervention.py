# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Intervention(models.Model):
    _name = 'estate.intervention'
    _description = 'Intervention'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Numéro", default="Nouveau", readonly=True)
    propriete_id = fields.Many2one('estate.propriete', string="Propriété", required=True)
    piece_id = fields.Many2one('estate.piece', string="Pièce", domain="[('propriete_id', '=', propriete_id)]")
    description = fields.Text("Description du problème", required=True)
    date_prevue = fields.Date("Date prévue", default=fields.Date.today)
    date_realisation = fields.Date("Date de réalisation")
    responsable_id = fields.Many2one('res.users', string="Responsable", default=lambda self: self.env.user)
    cout_estime = fields.Float("Coût estimé")
    cout_reel = fields.Float("Coût réel")
    etat = fields.Selection([
        ('a_planifier', 'À planifier'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ], string="État", default='a_planifier', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('estate.intervention') or 'Nouveau'
        return super(Intervention, self).create(vals)
