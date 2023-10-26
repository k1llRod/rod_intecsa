odoo.define('acrux_whatsapp_sale.indicators', function(require) {
"use strict";

var Widget = require('web.Widget');
var ajax = require('web.ajax');

/**
 * Widget para manejar los inidicadores, se muestra en el tab indicadores
 *
 * @class
 * @name Indicators
 * @extends web.Widget
 *
 */
var Indicators = Widget.extend({
    jsLibs: [
        '/web/static/lib/Chart/Chart.js'
    ],
    /**
     * @override
     * @see Widget.init
     */
    init: function(parent, options) {
        this._super.apply(this, arguments);

        this.parent = parent;
        this.options = _.extend({}, options);
        this.context = _.extend({}, this.parent.context || {}, this.options.context);

        this.partner_id = this.options.partner_id;
        this.chart = null;

    },

    /**
     * @override
     * @see Widget.willStart
     */
    willStart: function() {
        return Promise.all([
            this._super(),
            ajax.loadLibs(this),
            this.getPartnerIndicator(),
        ]);
    },

    /**
     * @override
     * @see Widget.start
     */
    start: function() {
        return this._super().then(() => this._initRender());
    },

    /**
     * Hace trabajos de render
     *
     * @private
     * @returns {Promise} Para indicar que termino
     */
    _initRender: function() {
        if (this.month_last_sale_data) {
            this.$el.append(this.graph_6last_sale());
        }
        if (this.html_last_sale) {
            this.$el.append(this.html_last_sale);
        }
        return Promise.resolve();
    },

    /**
     * Consulta los indicadores del cliente y los almacena en el objeto
     *
     * @returns {Promise} De la solicitud al servidor
     */
    getPartnerIndicator: function() {
        return this._rpc({
            model: 'res.partner',
            method: 'get_chat_indicators',
            args: [[this.partner_id]],
            context: this.context
        }).then(result => {
            if (result['6month_last_sale_data']) {
                this.month_last_sale_data = result['6month_last_sale_data'];
            }
            if (result['html_last_sale']) {
                this.html_last_sale = result['html_last_sale']
            }
        })
    },

    /**
     * Construye el grafico de la venta de los últimos meses.
     *
     * @returns {Jquery} El grafico en un objeto jquery
     */
    graph_6last_sale: function() {
        let $out = $('<div>'), $canvas, context, config;
        $out.addClass('o_graph_barchart');
        this.chart = null;
        $canvas = $('<canvas/>');
        $canvas.height(150);
        $out.append($canvas);
        context = $canvas[0].getContext('2d');
        config = this._getBarChartConfig();
        this.chart = new Chart(context, config);
        return $out;
    },

    /**
     * Transforma la data, al formato de la librería chart
     * @private
     * @see web.basic_fields.JournalDashboardGraph._getBarChartConfig
     *
     * @returns {Object}
     */
    _getBarChartConfig: function() {
        var data = [];
        var backgroundColor = ['#FFD8E1', '#FFE9D3', '#FFF3D6',
            '#D3F5F5', '#CDEBFF', '#E6D9FF'];
        var borderColor = ['#FF3D67', '#FF9124', '#FFD36C',
            '#60DCDC', '#4CB7FF', '#A577FF'];
        var labels = [];
        let data_param = this.month_last_sale_data;

        data_param[0].values.forEach(pt => {
            data.push(pt.value);
            labels.push(pt.label);
        });
        return {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    fill: 'start',
                    label: data_param[0].key,
                    backgroundColor: backgroundColor,
                    borderColor: borderColor,
                }]
            },
            options: {
                legend: { display: false },
                scales: {
                    yAxes: [{ display: false }],
                },
                maintainAspectRatio: false,
                tooltips: {
                    intersect: false,
                    position: 'nearest',
                    caretSize: 0,
                    callbacks: {
                        label: (tooltipItem, data) => {
                            var label = data.datasets[tooltipItem.datasetIndex].label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += this.parent.format_monetary(tooltipItem.yLabel);
                            return label;
                        }
                    }
                },
                elements: {
                    line: {
                        tension: 0.000001
                    }
                },
            },
        };
    }
})

return Indicators
})
