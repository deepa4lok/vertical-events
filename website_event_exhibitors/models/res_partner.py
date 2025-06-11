# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.safe_eval import const_eval

import logging

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = ["res.partner"]

    exhibitor_status = fields.Selection([('draft', 'Draft Exhibitor'), ('confirmed', 'Exhibitor')], 'Exhibitor?', copy=False)

    event_order_count = fields.Integer(compute="_compute_event_order_count")

    def _compute_event_order_count(self):
        order_type = self.env.ref('website_event_exhibitors.event_sale_type')
        SaleOrder = self.env["sale.order"]
        for this in self:
            this.event_order_count = SaleOrder.search_count(
                [
                    ("partner_id", "child_of", this.id),
                    ("type_id", "=", order_type.id),
                ]
            )

    def _compute_sale_order_count(self):
        super()._compute_sale_order_count()
        for this in self:
            this.sale_order_count -= this.event_order_count

    def action_view_sale_order(self):
        result = super().action_view_sale_order()
        order_type = self.env.ref('website_event_exhibitors.event_sale_type')
        result["domain"] += [("type_id", "!=", order_type.id)]
        return result

    def action_view_event_order(self):
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "website_event_exhibitors.action_orders_event"
        )
        order_type = self.env.ref('website_event_exhibitors.event_sale_type')
        result["domain"] = [
            ("partner_id", "child_of", self.ids),
            ("type_id", "=", order_type.id),
        ]
        result["context"] = dict(
            const_eval(result["context"] or "{}"), default_partner_id=self[:1].id,
            default_event_customer=self[:1].id,
        )
        return result
