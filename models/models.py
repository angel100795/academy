# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions

class res_partner(models.Model):
    _name ='res.partner'
    _inherit = 'res.partner'
    #is_school = fields.Boolean('Escuela')
    company_type = fields.Selection(selection_add=[('is_school', 'Escuela'),('student','Estudiante')])
    student = fields.Many2one(
        'academy.student', 
        'Estudiante')

class academy_student(models.Model):
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _name = 'academy.student'
    _description = 'Modelo de formulario para estudiantes'
    
    @api.model
    def _get_school_default(self):
        school_id = self.env['res.partner'].search([('name','=','Escuela_comodin')])
        return school_id

    name = fields.Char('Nombre',size=128,required=True, track_visibility ='onchange')
    last_name = fields.Char('Apellido',size=128)
    photo = fields.Binary('Fotografia')
    create_date = fields.Datetime('Fecha de creacion',readonly=True)
    notes = fields.Html('Comentarios')
    active = fields.Boolean('Activado')
    state = fields.Selection([('draf','Documento Borrador'),
                              ('progress','Progreso'),
                              ('done','Egresado'),], 'Estado')
    
    age = fields.Integer('Edad', copy=False)
    curp = fields.Char('Curp',size=18,copy=False)
    
    ##Relacionales

    partner_id = fields.Many2one('res.partner','Escuela',default=_get_school_default)

    calificaciones_id = fields.One2many(
        'academy.calificacion',
        'student_id',
        'Calificaciones')
    
    country = fields.Many2one('res.country','Pais', related='partner_id.country_id')

    invoice_ids = fields.Many2many('account.invoice',
                                   'student_invoice_rel',
                                   'student_id','invoice_id',
                                   'Facturas') 

    @api.one
    @api.constrains('curp')
    def _check_lines(self):
        if len(self.curp) < 18:
            raise exceptions.ValidationError("Curp debe ser de 18 caracteres")
    ###Metodo de escritura
    @api.multi
    def write(self, values):
        if 'curp' in values:
            values.update({
                'curp':values['curp'].upper(),
                })
        result = super(academy_student, self).write(values)
        return result



    @api.model
    def create(self, values):
        if values['name']:
            nombre = values['name']
            exist_ids = self.env['academy.student'].search([('name','=',self.name)])
            if exist_ids:
                values.update({
                    'name': values['name']+"(copia)",
                    })
        res = super(academy_student, self).create(values)
        partner_obj = self.env['res.partner']
        vals_to_partner = {
                'name': res['name']+" "+res['last_name'],
                'company_type': 'student',
                'student_id': res['id'],
                }
        print (vals_to_partner)
        partner_id = partner_obj.create(vals_to_partner)
        print("===>partner_id", partner_id)
        return res

    @api.multi
    def unlink(self):
        partner_obj = self.env['res.partner']
        partner_ids = partner_obj.search([('student','in',self.ids)])
        print ("Partnet ##### >>>>>",partner_ids )
        if partner_ids:
            for partner in partner_ids:
                partner.unlink()
        res = super(academy_student, self).unlink()
        return res

    _order = 'name'
    _defaults = {
        'active' : True,
        'state' : 'draf',
        }