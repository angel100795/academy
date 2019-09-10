# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions


class academy_calificacion(models.Model):
    _name = 'academy.calificacion'
    _description = 'Calificacion del estudiante'

    name = fields.Many2one('academy.materia', 'Materia')
    calificacion = fields.Float('Calificacion', digits=(3,2))
    student_id =fields.Many2one('academy.student','ID Ref')

    @api.one
    @api.constrains('calificacion')
    def _check_calificacion(self):
    	if self.calificacion < 5 or self.calificacion > 10:
    		raise exceptions.ValidationError("Calificacion mayor a 5 y Menor a 10")

class academy_materia(models.Model):
    _name = 'academy.materia'
    _description = 'Materias del Estudiante'
    
    name = fields.Char('Nombre')
    grado_id = fields.Many2one('academy.grado','ID Referencia')

    _sql_constraints = [('name_uniq','unique(name)',
    	'El nombre de la materia debe ser unico')]