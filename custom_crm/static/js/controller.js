// cambiarPestanna :function (pestannas,pestanna) {
//     print('funcion cambiar pesta========================================')
//     // Obtiene los elementos con los identificadores pasados.
//     pestanna = document.getElementById(pestanna.id);
//     listaPestannas = document.getElementById(pestannas.id);
    
//     // Obtiene las divisiones que tienen el contenido de las pestañas.
//     cpestanna = document.getElementById('c'+pestanna.id);
//     listacPestannas = document.getElementById('contenido'+pestannas.id);
    
//     i=0;
//     // Recorre la lista ocultando todas las pestañas y restaurando el fondo 
//     // y el padding de las pestañas.
//     while (typeof listacPestannas.getElementsByTagName('div')[i] != 'undefined'){
//         $(document).ready(function(){
//             $(listacPestannas.getElementsByTagName('div')[i]).css('display','none');
//             $(listaPestannas.getElementsByTagName('li')[i]).css('background','');
//             $(listaPestannas.getElementsByTagName('li')[i]).css('padding-bottom','');
//         });
//         i += 1;
//     }

//     $(document).ready(function(){
//         // Muestra el contenido de la pestaña pasada como parametro a la funcion,
//         // cambia el color de la pestaña y aumenta el padding para que tape el  
//         // borde superior del contenido que esta juesto debajo y se vea de este 
//         // modo que esta seleccionada.
//         $(cpestanna).css('display','');
//         $(pestanna).css('background','dimgray');
//         $(pestanna).css('padding-bottom','2px'); 
//     });

// }



odoo.define('custom_crm.custom_crm', function (require) {
    "use strict";
    console.log('cargo-=-=-111=-==================================')
    // var form_widget = require('web.FormRenderer');
    var core = require('web.core');
    var Widget = require('web.Widget');
    
    var MyWidget = Widget.extend({
        // QWeb template to use when rendering the object
        // xmlDependencies: ["/custom_crm/views/portal_my_details.xml"],
        // template: "details_inherit_parents",
        events: {
            // events binding example
            'click .page': 'handle_click',
        },
    
        init: function(parent) {
            this._super(parent);
            // insert code to execute before rendering, for object
            // initialization
        },
        // start: function() {
        //     var sup = this._super();
        //     // post-rendering initialization code, at this point
    
        //     // allows multiplexing deferred objects
        //     return $.when(
        //         // propagate asynchronous signal from parent class
        //         sup,
        //         // return own's asynchronous signal
        //         this.rpc(/* … */))
        // },
        handle_click :function () {
            console.log('activo funcion------------------------------')
        }
    });
    
    var my_widget = new MyWidget(this);
    // Render and insert into DOM
    my_widget.appendTo(".page");
});