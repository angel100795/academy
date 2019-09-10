# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions

class academy_materia_list(models.Model):
    _name ='academy.materia.list'
    grado_id = fields.Many2one('academy.grado','ID Referencia')
    materia_id =  fields.Many2one('academy.materia','Materia',required=True)

class academy_materias(models.Model):
    _name ='academy.grado'
    _description ='Modelo Grados con un listado de materias'

    name = fields.Selection([
                            ('1','Primero'),
                            ('2','Segundo'),
                            ('3','Tercero'),
                            ('4','Cuarto'),
                            ('5','Quinto'),
                            ('6','Sexto')],
                            'Grado', required=True)
    grupo = fields.Selection([
                            ('a','A'),
                            ('b','B'),
                            ('c','C')],
                            'Grupo')

    materia_ids = fields.One2many('academy.materia.list','grado_id','Materias')

class account_move(models.Model):
    _name = 'account.move'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin','account.move']
    state = fields.Selection([('draft', 'Unposted'), ('posted', 'Posted')], string='Status',
      required=True, readonly=True, copy=False, default='draft',
      help='All manually created new journal entries are usually in the status \'Unposted\', '
           'but you can set the option to skip that status on the related journal. '
           'In that case, they will behave as journal entries automatically created by the '
           'system on document validation (invoices, bank statements...) and will be created '
           'in \'Posted\' status.', track_visibility="onchange")
    @api.multi
    def write(self, values):
        if 'state' in values:
            msg = _("Stan loona")
            self.message_post(body=msg)  
        result = super(account_move, self).write(values)
        return result

class res_partner(models.Model):
    _name ='res.partner'
    _inherit = 'res.partner'
    #is_school = fields.Boolean('Escuela')
    company_type = fields.Selection(selection_add=[('is_school', 'Escuela'),('student','Estudiante')])
    student = fields.Many2one(
        'academy.student', 
        'Estudiante')
    property_payment_term_id = fields.Many2one('account.payment.term', company_dependent=True,
        string='Customer Payment Terms',
        help="This payment term will be used instead of the default one for sales orders and customer invoices", oldname="property_payment_term", track_visibility ='onchange')
    property_supplier_payment_term_id = fields.Many2one('account.payment.term', company_dependent=True,
        string='Vendor Payment Terms',
        help="This payment term will be used instead of the default one for purchase orders and vendor bills", oldname="property_supplier_payment_term", track_visibility ='onchange')



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
    grado_id = fields.Many2one('academy.grado','Grado')

    @api.onchange('grado_id')
    def onchange_grado(self):
        print ("####### SELF Grado >>>>", self.grado_id)
        calificaciones_list = []
        for materia in self .grado_id.materia_ids:
            xval = (0,0,{
                'name': materia.materia_id.id,
                'calificacion': 5
                })
            calificaciones_list.append(xval)
        self.update({'calificaciones_id':calificaciones_list})

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