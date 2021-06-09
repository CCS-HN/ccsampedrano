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
    MANDATORY_BILLING_FIELDS = ["name",'tipo_sangre','income_type','date_birth','account_holder','email','type_transport','curso_id','modalidad_id']
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name"]
    



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
    
    @route(['/my/account/parents'], type='http', auth='user', website=True)
    def parents(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            values = {
                'father_name':post.get('father_name') or False,
                'id_padre': post.get('id_padre') or False,
                'correo_padre':post.get('correo_padre') or False,
                'tel_padre':post.get('tel_padre') or False,
                'fecha_padre':post.get('fecha_padre') or False,
                'movil_padre':post.get('movil_padre') or False,
                'lugar_trb_padre':post.get('lugar_trb_padre') or False,
                
                'mother_name':post.get('mother_name') or False,
                'id_madre': post.get('id_madre') or False,
                'correo_madre':post.get('correo_madre') or False,
                'tel_madre':post.get('tel_madre') or False,
                'fecha_madre':post.get('fecha_madre') or False,
                'movil_madre':post.get('movil_madre') or False,
                'lugar_trb_madre':post.get('lugar_trb_madre') or False,

                'materia_retrasada': post.get('materia_retrasada') or False,
                'materia_retrasada_id': post.get('materia_retrasada_id') or False,
                'materia_retrasada_name':post.get('materia_retrasada_name') or False,
                
                'encargado': post.get('encargado') or False,
                'encargado_id': post.get('encargado_id') or False,
                'encargado_movil': post.get('encargado_movil') or False,
            }
        
            
            partner.sudo().write(values)
            if redirect:
                return request.redirect(redirect)
            return request.redirect('/my/home')

        values.update({
            'partner': partner,
            'father_name': partner.father_name,
            'correo_padre':partner.correo_padre,
            'id_padre': partner.id_padre,
            'fecha_padre': partner.fecha_padre,
            'movil_padre': partner.movil_padre,
            'lugar_trb_padre': partner.lugar_trb_padre,
            'tel_padre': partner.tel_padre,

            'mother_name': partner.mother_name,
            'id_madre': partner.id_madre,
            'correo_madre':partner.correo_madre,
            'fecha_madre': partner.fecha_madre,
            'movil_madre': partner.movil_madre,
            'lugar_trb_madre': partner.lugar_trb_madre,
            'tel_madre': partner.tel_madre,


            'materia_retrasada': partner.materia_retrasada,
            'materia_retrasada_id': partner.materia_retrasada_id,
            'materia_retrasada_name':partner.materia_retrasada_name,
            
            'encargado': partner.encargado,
            'encargado_id': partner.encargado_id,
            'encargado_movil': partner.encargado_movil,
            


            'date_birth': partner.date_birth,
            'Origen': partner.origin,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })
   
        response = request.render("custom_crm.portal_my_details_inherit_parents", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    


    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        if post.get('father_name'):
            return self.parents(redirect=None, **post)
        
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
                if post['income_type'] == 'Re-ingreso':
                    values.update({'income_type': 'Reingreso'})
                    # partner.income_type = 'Reingreso'
                if post['income_type'] == 'Primer Ingreso':
                    # partner.income_type = 'PrimerIngreso'
                    values.update({'income_type': 'PrimerIngreso'})
                if post['income_type'] == 'Traslado':
                    values.update({'income_type': 'Traslado'})
                    # partner.income_type = 'Traslado'
                
                # partner.date_birth = post['date_birth']
                partner.type_transport = post['type_transport']
                partner.account_holder = post['account_holder']
                partner.origin = post['origin']
                partner.receta = post['receta']
                partner.padecimiento = post['padecimiento']
                partner.tipo_sangre = post['tipo_sangre']
                
                
                partner.curso_id = post['curso_id']
                partner.modalidad_id = post['modalidad_id']
                # partner.income_type = post['income_type']
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        cursos = request.env['crm.lead.cursos'].sudo().search([])
        modalidad = request.env['crm.lead.modalidad'].sudo().search([])
        
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

        values.update({
            'partner': partner,
            'countries': countries,
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