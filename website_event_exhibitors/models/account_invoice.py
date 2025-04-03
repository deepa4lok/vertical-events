# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)

class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    lock_prices = fields.Boolean("Lock", copy=False, default=False)


