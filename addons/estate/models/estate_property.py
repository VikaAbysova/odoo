"""Part of Odoo. See LICENSE file for full copyright and licensing details."""
from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property"

    name = fields.Char(string="Property Name", required=True, index='trigram')
    description = fields.Text(string="Simple description", translate=True)
    postcode = fields.Char(string="Postcode", size=10)
    date_availability = fields.Date(string="Date availability", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string="Expected price")
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=3)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(
        string="Garden orientation", 
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="This field means the garden orientation"
        )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(string="State", 
            selection=[('new', 'New'), ('received','Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold '), ('cancelled', 'Cancelled')],
            required=True, 
            default='new',
            copy=False)