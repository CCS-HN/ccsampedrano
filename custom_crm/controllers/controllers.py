# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import pytz

from odoo import http
from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied
from odoo.addons.http_routing.models.ir_http import url_for
from odoo.http import content_disposition, Controller, request, route
from odoo.modules.module import get_module_resource
from odoo.tools import ustr
from odoo.tools.translate import _
from odoo.addons.portal.controllers.portal import CustomerPortal

class CustomerPortalInherit(CustomerPortal):
    # MANDATORY_BILLING_FIELDS = ["name", "phone", "email", "street", "city", "country_id","new_data"]
    MANDATORY_BILLING_FIELDS = ["id_alumno", "name",'tipo_sangre','income_type','date_birth','account_holder','email','type_transport','curso_id','modalidad_id']
    
    MANDATORY_BILLING_FIELDS_PARTNER = [
        "father_name","id_padre","correo_padre","tel_padre","fecha_padre","movil_padre","lugar_trb_padre",    
    ]
    MANDATORY_BILLING_FIELDS_MOTHER = [
       "mother_name","id_madre","correo_madre","tel_madre","fecha_madre","movil_madre","lugar_trb_madre"
    ]
    MANDATORY_BILLING_FIELDS_ENCARGADO = [
        "encargado","encargado_id","encargado_movil"
    ]
    MANDATORY_BILLING_FIELDS_MATERIA = [
        "materia_retrasada","materia_retrasada_id","materia_retrasada_name"  
    ]
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name"]
    
    def details_form_validate_encargado(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS_ENCARGADO:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        partner = request.env.user.partner_id
        if data.get("vat") and partner and partner.vat != data.get("vat"):
            if partner.can_edit_vat():
                if hasattr(partner, "check_vat"):
                    if data.get("country_id"):
                        data["vat"] = request.env["res.partner"].fix_eu_vat_number(int(data.get("country_id")), data.get("vat"))
                    partner_dummy = partner.new({
                        'vat': data['vat'],
                        'country_id': (int(data['country_id'])
                                       if data.get('country_id') else False),
                    })
                    try:
                        partner_dummy.check_vat()
                    except ValidationError:
                        error["vat"] = 'error'
            else:
                error_message.append(_('Changing VAT number is not allowed once document(s) have been issued for your account. Please contact us directly for this operation.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        # unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        # if unknown:
        #     error['common'] = 'Unknown field'
        #     error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message


    def details_form_validate_materia(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS_MATERIA:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        partner = request.env.user.partner_id
        if data.get("vat") and partner and partner.vat != data.get("vat"):
            if partner.can_edit_vat():
                if hasattr(partner, "check_vat"):
                    if data.get("country_id"):
                        data["vat"] = request.env["res.partner"].fix_eu_vat_number(int(data.get("country_id")), data.get("vat"))
                    partner_dummy = partner.new({
                        'vat': data['vat'],
                        'country_id': (int(data['country_id'])
                                       if data.get('country_id') else False),
                    })
                    try:
                        partner_dummy.check_vat()
                    except ValidationError:
                        error["vat"] = 'error'
            else:
                error_message.append(_('Changing VAT number is not allowed once document(s) have been issued for your account. Please contact us directly for this operation.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        # unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        # if unknown:
        #     error['common'] = 'Unknown field'
        #     error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message
    
    
    def details_form_validate_mother(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS_MOTHER:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        partner = request.env.user.partner_id
        if data.get("vat") and partner and partner.vat != data.get("vat"):
            if partner.can_edit_vat():
                if hasattr(partner, "check_vat"):
                    if data.get("country_id"):
                        data["vat"] = request.env["res.partner"].fix_eu_vat_number(int(data.get("country_id")), data.get("vat"))
                    partner_dummy = partner.new({
                        'vat': data['vat'],
                        'country_id': (int(data['country_id'])
                                       if data.get('country_id') else False),
                    })
                    try:
                        partner_dummy.check_vat()
                    except ValidationError:
                        error["vat"] = 'error'
            else:
                error_message.append(_('Changing VAT number is not allowed once document(s) have been issued for your account. Please contact us directly for this operation.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        # unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        # if unknown:
        #     error['common'] = 'Unknown field'
        #     error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message


    def details_form_validate_partner(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS_PARTNER:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        partner = request.env.user.partner_id
        if data.get("vat") and partner and partner.vat != data.get("vat"):
            if partner.can_edit_vat():
                if hasattr(partner, "check_vat"):
                    if data.get("country_id"):
                        data["vat"] = request.env["res.partner"].fix_eu_vat_number(int(data.get("country_id")), data.get("vat"))
                    partner_dummy = partner.new({
                        'vat': data['vat'],
                        'country_id': (int(data['country_id'])
                                       if data.get('country_id') else False),
                    })
                    try:
                        partner_dummy.check_vat()
                    except ValidationError:
                        error["vat"] = 'error'
            else:
                error_message.append(_('Changing VAT number is not allowed once document(s) have been issued for your account. Please contact us directly for this operation.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        # unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        # if unknown:
        #     error['common'] = 'Unknown field'
        #     error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        partner = request.env.user.partner_id
        if data.get("vat") and partner and partner.vat != data.get("vat"):
            if partner.can_edit_vat():
                if hasattr(partner, "check_vat"):
                    if data.get("country_id"):
                        data["vat"] = request.env["res.partner"].fix_eu_vat_number(int(data.get("country_id")), data.get("vat"))
                    partner_dummy = partner.new({
                        'vat': data['vat'],
                        'country_id': (int(data['country_id'])
                                       if data.get('country_id') else False),
                    })
                    try:
                        partner_dummy.check_vat()
                    except ValidationError:
                        error["vat"] = 'error'
            else:
                error_message.append(_('Changing VAT number is not allowed once document(s) have been issued for your account. Please contact us directly for this operation.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        # unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        # if unknown:
        #     error['common'] = 'Unknown field'
        #     error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message
    
    
    @route(['/my/account/mother'], type='http', auth='user', website=True)
    def mother(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })
        
        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate_mother(post)
            values.update({'error': error, 'error_message': error_message})
            if not error:
                values = {
                    'mother_name':post.get('mother_name') or False,
                    'id_madre': post.get('id_madre') or False,
                    'correo_madre':post.get('correo_madre') or False,
                    'tel_madre':post.get('tel_madre') or False,
                    'fecha_madre':post.get('fecha_madre') or False,
                    'movil_madre':post.get('movil_madre') or False,
                    'lugar_trb_madre':post.get('lugar_trb_madre') or False,
                }
            
                
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/account/encargado')

        
        values.update({
            'partner': partner,
            
            'mother_name': partner.mother_name,
            'id_madre': partner.id_madre,
            'correo_madre':partner.correo_madre,
            'fecha_madre': partner.fecha_madre,
            'movil_madre': partner.movil_madre,
            'lugar_trb_madre': partner.lugar_trb_madre,
            'tel_madre': partner.tel_madre,
            
            'part':False,
            'mother':True,
            'encar':False,
            'materia':False,

            'Origen': partner.origin,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })
        response = request.render("custom_crm.portal_my_details_inherit_mother", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    
    
    @route(['/my/account/parents'], type='http', auth='user', website=True)
    def parents(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })
        
        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate_partner(post)
            values.update({'error': error, 'error_message': error_message})
            if not error:
                values = {
                    'father_name':post.get('father_name') or False,
                    'id_padre': post.get('id_padre') or False,
                    'correo_padre':post.get('correo_padre') or False,
                    'tel_padre':post.get('tel_padre') or False,
                    'fecha_padre':post.get('fecha_padre') or False,
                    'movil_padre':post.get('movil_padre') or False,
                    'lugar_trb_padre':post.get('lugar_trb_padre') or False,
                }
            
                
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/account/mother')

        values.update({
            'partner': partner,
            'father_name': partner.father_name,
            'correo_padre':partner.correo_padre,
            'id_padre': partner.id_padre,
            'fecha_padre': partner.fecha_padre,
            'movil_padre': partner.movil_padre,
            'lugar_trb_padre': partner.lugar_trb_padre,
            'tel_padre': partner.tel_padre,

            
            'part':True,
            'mother':False,
            'encar':False,
            'materia':False,

            

            'date_birth': partner.date_birth,
            'Origen': partner.origin,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })
   
        response = request.render("custom_crm.portal_my_details_inherit_parents", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
       
    
 
    @route(['/my/account/encargado'], type='http', auth='user', website=True)
    def encargado(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })
        
        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate_encargado(post)
            values.update({'error': error, 'error_message': error_message})
            if not error:
                values = {
                    'encargado': post.get('encargado') or False,
                    'encargado_id': post.get('encargado_id') or False,
                    'encargado_movil': post.get('encargado_movil') or False,
                }
            
                
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/account/materia')

        values.update({
            'partner': partner,
            

            'encargado': partner.encargado,
            'encargado_id': partner.encargado_id,
            'encargado_movil': partner.encargado_movil,
            
            'part':False,
            'mother':False,
            'encar':True,
            'materia':False,

            'date_birth': partner.date_birth,
            'Origen': partner.origin,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })
   
        response = request.render("custom_crm.portal_my_details_inherit_encargado", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    
    
    @route(['/my/account/materia'], type='http', auth='user', website=True)
    def materia(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })
        
        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate_materia(post)
            values.update({'error': error, 'error_message': error_message})
            if not error:
                values = {
                   
                    'materia_retrasada': post.get('materia_retrasada') or False,
                    'materia_retrasada_id': post.get('materia_retrasada_id') or False,
                    'materia_retrasada_name':post.get('materia_retrasada_name') or False,
                    
                }
            
               
                partner.sudo().write(values)
                
                request.env['crm.lead'].sudo().create({
                    'partner_id': partner.id,
                    'name': partner.id_alumno + ' opportunity',
                    'nombre_alumno': partner.name,
                    'correo_del_estudiante':partner.email,
                    'direcc':partner.street,
                    'pais':partner.pais.id if partner.pais else 96,
                    'padecimiento':partner.padecimiento,
                    'receta':partner.receta,
                    'becado2':partner.becado2,
                    'genero':partner.gender,


                    'materia_retrasada': partner.materia_retrasada,
                    'id_responsable_materia': partner.materia_retrasada_id,
                    'nombre_responsable_materia':partner.materia_retrasada_name,
                    
                    'tipo_ingreso': 'Re-ingreso', #partner.income_type or 'Re-ingreso',
                    'becado2':partner.becado2,
                    'tipo_sangre':partner.tipo_sangre,
                    'titular_cuenta':partner.account_holder,
                    'curso_id':partner.curso_id.id,
                    'modalidad_id': partner.modalidad_id.id,
                    'fecha_nacimiento': partner.date_birth,
                    'edad': partner.age,
                    'procedencia': partner.origin,
                    'transporte':partner.type_transport,

                    'nombre_responsable': partner.encargado,
                    'id_responsable': partner.encargado_id,
                    'movil_responsable': partner.encargado_movil,

                    'nombre_padre': partner.father_name,
                    'correo_pri':partner.correo_padre,
                    'id_padre': partner.id_padre,
                    'fecha_padre': partner.fecha_padre,
                    'movil_padre': partner.movil_padre,
                    'lugar_trb_padre': partner.lugar_trb_padre,
                    'tel_padre': partner.tel_padre,

                    'nombre_madre': partner.mother_name,
                    'id_madre': partner.id_madre,
                    'correo_secun':partner.correo_madre,
                    'fecha_madre': partner.fecha_madre,
                    'movil_madre': partner.movil_madre,
                    'lugar_trb_madre': partner.lugar_trb_madre,
                    'tel_madre': partner.tel_madre,
                    
                })
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        values.update({
            'partner': partner,
            'materia_retrasada': partner.materia_retrasada,
            'materia_retrasada_id': partner.materia_retrasada_id,
            'materia_retrasada_name':partner.materia_retrasada_name,
            
            'part':False,
            'mother':False,
            'encar':False,
            'materia':True,

            'Origen': partner.origin,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })
   
        response = request.render("custom_crm.portal_my_details_inherit_materia", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    



    @route(['/my/account/student'], type='http', auth='user', website=True)
    def student(self, redirect=None, **post):
        
        # print('datos antes ====================',post,self)
        
        # if post.get('father_name'):
        #     return self.parents(redirect=None, **post)
        
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['pais', 'state_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                
                partner.receta = post['receta']
                partner.padecimiento = post['padecimiento']
                values.update({'income_type': post['income_type']})
                
                # partner.date_birth = post['date_birth']
                partner.type_transport = post['type_transport']
                partner.account_holder = post['account_holder']
                partner.origin = post['origin']
                partner.receta = post['receta']
                partner.padecimiento = post['padecimiento']
                partner.tipo_sangre = post['tipo_sangre']
                
                
                partner.curso_id = post['curso_id']
                partner.pais = post['countries'] or False
                partner.street = post['street']
                partner.modalidad_id = post['modalidad_id']
                partner.gender = post['gender']
                # partner.income_type = post['income_type']
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/account/parents')
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        cursos = request.env['crm.lead.cursos'].sudo().search([])
        modalidad = request.env['crm.lead.modalidad'].sudo().search([])
        
        gender = []
        income_type = []
        type_transport = []
        becado2=[]
        tipo_sangre = []
        account_holder = []

        account_holder.append('Padre')
        account_holder.append('Madre')
        account_holder.append('Encargado')

        tipo_sangre.append('O+')
        tipo_sangre.append('O-')
        tipo_sangre.append('A-')
        tipo_sangre.append('A+')
        tipo_sangre.append('B+')
        tipo_sangre.append('B-')
        tipo_sangre.append('AB-')
        tipo_sangre.append('AB+')

        becado2.append('Si')
        becado2.append('No')

        income_type.append('Re-ingreso')
        income_type.append('Primer Ingreso')
        income_type.append('Traslado')

        type_transport.append('Familiar')
        type_transport.append('Privado')
        type_transport.append('Publico')
        
        gender.append('Masculino')
        gender.append('Femenino')



        values.update({
            'gender':gender,
            'partner': partner,
            'student': True,
            'countries': countries,
            'street':partner.street,
            'income_type': income_type,
            'becado2':becado2,
            'tipo_sangre':tipo_sangre,
            'account_holder':account_holder,
            'cursos':cursos,
            'modalidad': modalidad,
            'id_alumno': partner.id_alumno,
            'date_birth': partner.date_birth,
            'Origen': partner.origin,
            'type_transport':type_transport,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })
        response = request.render("custom_crm.portal_my_details_student", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        
        # print('datos antes ====================',post,self)
        
        # if post.get('father_name'):
        #     return self.parents(redirect=None, **post)
        
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['country_id', 'state_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                
                partner.receta = post['receta']
                partner.padecimiento = post['padecimiento']
                values.update({'income_type': post['income_type']})
                
                # partner.date_birth = post['date_birth']
                partner.type_transport = post['type_transport']
                partner.account_holder = post['account_holder']
                partner.origin = post['origin']
                partner.receta = post['receta']
                partner.padecimiento = post['padecimiento']
                partner.tipo_sangre = post['tipo_sangre']
                
                
                partner.curso_id = post['curso_id']
                partner.pais = post['countries'] or False
                partner.street = post['street']
                partner.modalidad_id = post['modalidad_id']
                partner.gender = post['gender']
                # partner.income_type = post['income_type']
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        cursos = request.env['crm.lead.cursos'].sudo().search([])
        modalidad = request.env['crm.lead.modalidad'].sudo().search([])
        
        gender = []
        income_type = []
        type_transport = []
        becado2=[]
        tipo_sangre = []
        account_holder = []

        account_holder.append('Padre')
        account_holder.append('Madre')
        account_holder.append('Encargado')

        tipo_sangre.append('O+')
        tipo_sangre.append('O-')
        tipo_sangre.append('A-')
        tipo_sangre.append('A+')
        tipo_sangre.append('B+')
        tipo_sangre.append('B-')
        tipo_sangre.append('AB-')
        tipo_sangre.append('AB+')

        becado2.append('Si')
        becado2.append('No')

        income_type.append('Re-ingreso')
        income_type.append('Primer Ingreso')
        income_type.append('Traslado')

        type_transport.append('Familiar')
        type_transport.append('Privado')
        type_transport.append('Publico')
        
        gender.append('Masculino')
        gender.append('Femenino')



        values.update({
            'gender':gender,
            'partner': partner,
            'countries': countries,
            'street':partner.street,
            'income_type': income_type,
            'becado2':becado2,
            'tipo_sangre':tipo_sangre,
            'account_holder':account_holder,
            'cursos':cursos,
            'modalidad': modalidad,
            'date_birth': partner.date_birth,
            'Origen': partner.origin,
            'type_transport':type_transport,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })
        response = request.render("custom_crm.portal_my_details_inherit", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    
    
    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        return request.render("custom_crm.portal_my_home", values)