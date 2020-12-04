# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CRM(models.Model):
    _inherit = 'crm.lead'
    _description = 'CRM'

    
    id_alumno = fields.Char()
    nombre_alumno = fields.Char()
    # modalidad = fields.Char()
    modalidad_id = fields.Many2one('crm.lead.modalidad')
    curso_id = fields.Many2one('crm.lead.cursos')
    modalidad = fields.Char()
    edad = fields.Integer()
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
