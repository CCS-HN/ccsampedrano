# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CRM(models.Model):
    _inherit = 'crm.lead'
    _description = 'CRM'

    
    id_alumno = fields.Char(related='name',store=True)
    nombre_alumno = fields.Char()
    # modalidad = fields.Char()
    modalidad_id = fields.Many2one('crm.lead.modalidad')
    curso_id = fields.Many2one('crm.lead.cursos')
    modalidad = fields.Char()
    edad = fields.Integer()
    direcc = fields.Char()
    fecha_nacimiento = fields.Date()
    genero = fields.Selection([('M', 'Masculino'), ('F', 'Femenino')])
    pais = fields.Many2one('res.country')
    alergias = fields.Text()
    padecimiento = fields.Text()
    receta = fields.Text()
    transporte = fields.Selection([('Familiar', 'Familiar'), ('Privado', 'Privado'),('Publico','Publico')])
    procedencia = fields.Char()
    correo_pri = fields.Char()
    correo_secun = fields.Char()
    tipo_ingreso = fields.Selection([('Reingreso', 'Re-ingreso'), ('PrimerIngreso', 'Primer Ingreso'),('Traslado', 'Traslado')])

    id_padre = fields.Char()
    nombre_padre = fields.Char()
    fecha_padre = fields.Date()
    movil_padre = fields.Char()
    lugar_trb_padre = fields.Char()
    tel_padre = fields.Char()

    id_madre = fields.Char()
    nombre_madre = fields.Char()
    fecha_madre = fields.Date()
    movil_madre = fields.Char()
    lugar_trb_madre = fields.Char()
    tel_madre = fields.Char()

    id_responsable = fields.Char()
    nombre_responsable = fields.Char()
    movil_responsable = fields.Char()
    lugar_trb_responsable = fields.Char()
    tel_responsable = fields.Char()

    tipo_sangre = fields.Selection([('O+', 'O+'), ('O-', 'O-'),('A-', 'A-'),('A+', 'A+'),('B+', 'B+'),('B-', 'B-'),('AB-', 'AB-'),('AB+', 'AB+')])

    materia_retrasada = fields.Char()
    id_responsable_materia = fields.Char()
    nombre_responsable_materia = fields.Char()
    id_responsable_materia2 = fields.Char()
    nombre_responsable_materia2 = fields.Char()


    reci_info = fields.Selection([('Si', 'Si'), ('No', 'No')])
    name_cc = fields.Char(related='name',store=True)
    tel = fields.Char(related='phone',store=True)
    email = fields.Char(related='email_from',store=True)
    mas_info = fields.Text()
    rango_edad = fields.Selection([('9-12', '9-12'),('13-18', '13-18'),('9-12', '19-25'),('26-35', '26-35'),('36-40', '36-40'),('41-65', '41-65'),('>65', '>65')])
    genero = fields.Selection([('M', 'Masculino'), ('F', 'Femenino')])
    localidad = fields.Selection([('San Pedro Sula', 'San Pedro Sula'), ('Cofradia', 'Cofradia'),('Pimienta', 'Pimienta'),('Taulabe', 'Taulabe'),('Villanueva', 'Villanueva'),('San Manuel', 'San Manuel'),('Siguatepeque', 'Siguatepeque'),('El Progreso', 'El Progreso'),('Quimistan', 'Quimistan'),('Jesus de Otoro', 'Jesus de Otoro'),('Otro', 'Otro')])
    taller = fields.Selection([('Facebook', 'Facebook'), ('Instagram', 'Instagram'),('Pagina Web', 'Pagina Web'), ('Correo Electronico', 'Correo Electronico'),('WhatsApp', 'WhatsApp'),('Amigo/Familiar', 'Amigo/Familiar')])
    otro_taller  = fields.Selection([('Pintura', 'Pintura'), ('Musica', 'Musica'), ('Ingles', 'Ingles'), ('Vacacional de Conversacion ', 'Vacacional de Conversacion'),('Vacacional de Ingles para niños', 'Vacacional de Ingles para niños'),('Área académica (Pre Básica, Básica y Media)', 'Área académica (Pre Básica, Básica y Media)'),('Biblioteca', 'Biblioteca'),('Culturales', 'Culturales')])

    taller_id = fields.Many2many('crm.lead.taller', string="Taller")
    otrotaller_id = fields.Many2many('crm.lead.taller.otro', string="Otro Taller")

class CRM_modalidad(models.Model):
    _name = 'crm.lead.modalidad'
    _description = 'Modalidad'

    name = fields.Char()


class CRM_cursos(models.Model):
    _name = 'crm.lead.cursos'
    _description = 'Cursos'

    name = fields.Char()
    # id_modalidad = fields.One2many('crm.lead.modalidad','id')
    id_modalidad = fields.Many2one('crm.lead.modalidad')
# class custom_crm(models.Model):
#     _name = 'custom_crm.custom_crm'
#     _description = 'custom_crm.custom_crm'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class CRM_taller(models.Model):
    _name = 'crm.lead.taller'
    _description = 'Taller'

    name = fields.Char()


class CRM_taller_otro(models.Model):
    _name = 'crm.lead.taller.otro'
    _description = 'Otro de interes Taller'

    name = fields.Char()


