# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions

class res_partner(models.Model):
	_name ='res.partner'
	_inherit = 'res.partner'
	#is_school = fields.Boolean('Escuela')
	company_type = fields.Selection(selection_add=[('is_school', 'Escuela')])

class academy_student(models.Model):
    _name = 'academy.student'
    _description = 'Modelo de formulario para estudiantes'
    name = fields.Char('Nombre',size=128,required=True)
    last_name = fields.Char('Apellido',size=128)
    photo = fields.Binary('Fotografia')
    create_date = fields.Datetime('Fecha de creacion',readonly=True)
    notes = fields.Html('Comentarios')
    active = fields.Boolean('Activado')
    state = fields.Selection([('draf','Documento Borrador'),
    						  ('progress','Progreso'),
    						  ('done','Egresado'),], 'Estado')
    
    age = fields.Integer('Edad', required=True)
    curp = fields.Char('Curp',size=18)
    ##Relacionales

    partner_id = fields.Many2one('res.partner','Escuela')
    calificaciones_id = fields.One2many('academy.calificacion','student_id',
        'Calificaciones')
    
    country = fields.Many2one('res.country','Pais',
                                related='partner_id.country_id')


    @api.one
    @api.constrains('curp')
    def _check_lines(self):
        if len(self.curp) < 18:
            raise exceptions.ValidationError("Curp debe ser de 18 caracteres")



    _order ='name'

    _defaults = {
    	'active' : True,
    	'state' : 'draf',
    	}

# class odoo_curso/odoo_academy(models.Model):
#     _name = 'odoo_curso/odoo_academy.odoo_curso/odoo_academy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100