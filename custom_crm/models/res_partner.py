# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from datetime import date
from datetime import datetime

from dateutil.relativedelta import relativedelta
class resPartner(models.Model):
    _inherit = 'res.partner'

    receta = fields.Text(string='receta')
    padecimiento = fields.Text(string='Padecimiento')
    
    id_alumno = fields.Char(char = 'Id Alumno', size=13)
    income_type = fields.Selection([('Re-ingreso', 'Re-ingreso'), ('Primer Ingreso', 'Primer Ingreso'),('Traslado', 'Traslado')],required=True, string = "Tipo de ingreso")
    gender = fields.Selection([('Masculino', 'Masculino'), ('Femenino', 'Femenino')],required=True, string = "Genero")    
    account_holder = fields.Selection([('Padre', 'Padre'), ('Madre', 'Madre'),('Encargado', 'Encargado')],required=True, string = "Responsable de los pagos")
    type_transport = fields.Selection([('Familiar', 'Familiar'), ('Privado', 'Privado'),('Publico','Publico')],required=True, string = "Tipo de transporte" )
    origin = fields.Char(string='Institucion de procedencia')
    date_birth = fields.Date(string='Fecha de nacimiento')
    age = fields.Integer(string='Edad', compute='get_age')
    becado2 = fields.Selection([
        ('Si', 'Si'),
        ('No', 'No')
    ], string='Becado')
    curso_id = fields.Many2one('crm.lead.cursos',required=True)
    modalidad_id = fields.Many2one('crm.lead.modalidad',required=True)
    tipo_sangre = fields.Selection([('O+', 'O+'), ('O-', 'O-'),('A-', 'A-'),('A+', 'A+'),('B+', 'B+'),('B-', 'B-'),('AB-', 'AB-'),('AB+', 'AB+')])

    materia_retrasada = fields.Char(string='Materia')
    materia_retrasada_id = fields.Char(string='ID')
    materia_retrasada_name = fields.Char(string='Nombre')

    encargado = fields.Char(string='Nombre')
    encargado_id = fields.Char(string='ID')
    encargado_movil = fields.Char(string='Movil')
    

    father_name = fields.Char(string='Nombre del padre')
    id_padre = fields.Char()
    correo_padre = fields.Char()
    fecha_padre = fields.Date()
    movil_padre = fields.Char()
    lugar_trb_padre = fields.Char()
    tel_padre = fields.Char()

   
    
    mother_name = fields.Char(string='Nombre del padre')
    id_madre = fields.Char()
    correo_madre = fields.Char()
    fecha_madre = fields.Date()
    movil_madre = fields.Char()
    lugar_trb_madre = fields.Char()
    tel_madre = fields.Char()

    pais = fields.Many2one('res.country',required=True)
    

    def get_age(self):
        for rec in self:
            rec.age = relativedelta(datetime.now(), rec.date_birth).years
            

    
    