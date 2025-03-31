# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date


class Location(models.Model):
    _name = 'estate.location'
    _description = 'Location'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Numéro", default="Nouveau", readonly=True)
    locataire_id = fields.Many2one('res.partner', string="Locataire", domain=[('est_un_locataire', '=', True)], required=True)
    propriete_id = fields.Many2one('estate.propriete', string="Propriété", required=True)
    date_de_reservation = fields.Date('Date de réservation', default=fields.Date.today)
    date_de_debut = fields.Date('Date de début', required=True)
    duree_en_annee = fields.Integer("Durée (années)", help="Durée de location en années", default=1)
    date_de_fin = fields.Date('Date de fin', compute="_compute_date_de_fin", store=True)
    frequence = fields.Selection([
        ('mensuelle', 'Mensuelle'),
        ('bimestrielle', 'Bimestrielle'),
        ('trimestrielle', 'Trimestrielle'),
        ('semestrielle', 'Semestrielle'),
        ('annuelle', 'Annuelle'),
    ], string="Fréquence de paiement", default='mensuelle', required=True)
    loyer = fields.Integer("Loyer", compute="_compute_loyer", store=True)
    etat = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('validee', 'Validée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ], string="État", default='brouillon', tracking=True)
    etats_des_lieux_ids = fields.One2many('estate.etat.des.lieux', 'location_id', string='États des lieux')

    @api.depends('date_de_debut', 'duree_en_annee')
    def _compute_date_de_fin(self):
        for record in self:
            if record.date_de_debut and record.duree_en_annee:
                record.date_de_fin = record.date_de_debut + relativedelta(years=record.duree_en_annee) - relativedelta(days=1)
            else:
                record.date_de_fin = False

    @api.depends('propriete_id', 'frequence')
    def _compute_loyer(self):
        for record in self:
            if record.propriete_id and record.frequence:
                base_loyer = record.propriete_id.loyer_mensuel
                freq_multipliers = {
                    'mensuelle': 1,
                    'bimestrielle': 2,
                    'trimestrielle': 3,
                    'semestrielle': 6,
                    'annuelle': 12,
                }
                record.loyer = base_loyer * freq_multipliers.get(record.frequence, 0)
            else:
                record.loyer = 0

    @api.constrains('propriete_id', 'date_de_debut', 'date_de_fin')
    def _check_date_overlap(self):
        for record in self:
            overlapping = self.search([
                ('propriete_id', '=', record.propriete_id.id),
                ('id', '!=', record.id),
                ('date_de_debut', '<=', record.date_de_fin),
                ('date_de_fin', '>=', record.date_de_debut),
                ('etat', 'not in', ['annulee', 'terminee']),
            ])
            if overlapping:
                raise ValidationError("Cette propriété est déjà louée pour cette période !")

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('estate.location') or 'Nouveau'
        return super(Location, self).create(vals)