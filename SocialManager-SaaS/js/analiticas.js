// Archivo JavaScript para la página de analíticas
document.addEventListener('DOMContentLoaded', function() {
    // Cargar Chart.js desde CDN
    const chartScript = document.createElement('script');
    chartScript.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    document.head.appendChild(chartScript);

    // Cargar DateRangePicker para filtros de fecha
    const dateRangeScript = document.createElement('script');
    dateRangeScript.src = 'https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js';
    document.head.appendChild(dateRangeScript);

    const dateRangeStyle = document.createElement('link');
    dateRangeStyle.rel = 'stylesheet';
    dateRangeStyle.href = 'https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css';
    document.head.appendChild(dateRangeStyle);

    // Cargar jQuery (requerido para DateRangePicker)
    const jqueryScript = document.createElement('script');
    jqueryScript.src = 'https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js';
    jqueryScript.onload = initializeAnalytics;
    document.head.appendChild(jqueryScript);

    // Inicializar componentes cuando jQuery esté cargado
    function initializeAnalytics() {
        // Esperar a que Chart.js esté cargado
        chartScript.onload = function() {
            // Inicializar gráficos
            initializeCharts();
            
            // Inicializar filtro de fechas
            initializeDateFilter();
            
            // Inicializar botones de exportación
            initializeExportButtons();
        };
    }

    // Variables globales para los gráficos
    let socialPerformanceChart, followersGrowthChart, engagementChart;
    let analyticsData = null;

    // Función para cargar datos desde el servidor
    function loadAnalyticsData(startDate = null, endDate = null, network = null) {
        // Construir URL con parámetros de filtro
        let url = 'php/get_analytics_data.php';
        const params = [];
        
        if (startDate) params.push(`start_date=${encodeURIComponent(startDate)}`);
        if (endDate) params.push(`end_date=${encodeURIComponent(endDate)}`);
        if (network) params.push(`network=${encodeURIComponent(network)}`);
        
        if (params.length > 0) {
            url += '?' + params.join('&');
        }

        // Mostrar indicador de carga
        document.querySelectorAll('canvas').forEach(canvas => {
            canvas.style.opacity = '0.5';
        });

        // Realizar petición AJAX
        fetch(url)
            .then(response => response.json())
            .then(data => {
                analyticsData = data;
                updateCharts(data);
                updateSummary(data.performance_summary);
                
                // Restaurar opacidad
                document.querySelectorAll('canvas').forEach(canvas => {
                    canvas.style.opacity = '1';
                });
            })
            .catch(error => {
                console.error('Error al cargar datos:', error);
                alert('Error al cargar los datos analíticos. Por favor, inténtelo de nuevo más tarde.');
                
                // Restaurar opacidad
                document.querySelectorAll('canvas').forEach(canvas => {
                    canvas.style.opacity = '1';
                });
            });
    }

    // Función para actualizar el resumen de rendimiento
    function updateSummary(summary) {
        const summaryContainer = document.querySelector('.row .card:first-child');
        if (summaryContainer) {
            const summaryContent = summaryContainer.querySelector('div[style="padding: 15px;"]');
            if (summaryContent) {
                summaryContent.innerHTML = `
                    <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                        <div style="text-align: center; flex: 1;">
                            <h3 style="color: var(--primary-color); margin: 0; font-size: 1.8rem;">${summary.followers.toLocaleString()}</h3>
                            <p style="color: var(--text-muted); margin: 5px 0 0;">Seguidores</p>
                            <span style="color: ${summary.followers_change >= 0 ? '#28a745' : '#dc3545'}; font-size: 0.8rem;">
                                <i class="fas fa-arrow-${summary.followers_change >= 0 ? 'up' : 'down'}"></i> ${Math.abs(summary.followers_change)}%
                            </span>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <h3 style="color: var(--primary-color); margin: 0; font-size: 1.8rem;">${summary.interactions.toLocaleString()}</h3>
                            <p style="color: var(--text-muted); margin: 5px 0 0;">Interacciones</p>
                            <span style="color: ${summary.interactions_change >= 0 ? '#28a745' : '#dc3545'}; font-size: 0.8rem;">
                                <i class="fas fa-arrow-${summary.interactions_change >= 0 ? 'up' : 'down'}"></i> ${Math.abs(summary.interactions_change)}%
                            </span>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <h3 style="color: var(--primary-color); margin: 0; font-size: 1.8rem;">${summary.posts}</h3>
                            <p style="color: var(--text-muted); margin: 5px 0 0;">Publicaciones</p>
                            <span style="color: ${summary.posts_change >= 0 ? '#28a745' : '#dc3545'}; font-size: 0.8rem;">
                                <i class="fas fa-arrow-${summary.posts_change >= 0 ? 'up' : 'down'}"></i> ${Math.abs(summary.posts_change)}%
                            </span>
                        </div>
                    </div>
                `;
            }
        }
    }

    // Función para inicializar los gráficos
    function initializeCharts() {
        // Gráfico de rendimiento por red social
        const socialPerformanceCtx = document.getElementById('socialPerformanceChart');
        if (socialPerformanceCtx) {
            socialPerformanceChart = new Chart(socialPerformanceCtx, {
                type: 'bar',
                data: {
                    labels: ['Facebook', 'Instagram', 'Twitter', 'LinkedIn'],
                    datasets: [{
                        label: 'Rendimiento (%)',
                        data: [0, 0, 0, 0], // Se actualizará con datos reales
                        backgroundColor: [
                            'rgba(59, 89, 152, 0.7)',  // Facebook
                            'rgba(193, 53, 132, 0.7)', // Instagram
                            'rgba(29, 161, 242, 0.7)', // Twitter
                            'rgba(0, 119, 181, 0.7)'   // LinkedIn
                        ],
                        borderColor: [
                            'rgba(59, 89, 152, 1)',
                            'rgba(193, 53, 132, 1)',
                            'rgba(29, 161, 242, 1)',
                            'rgba(0, 119, 181, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        // Gráfico de crecimiento de seguidores
        const followersGrowthCtx = document.getElementById('followersGrowthChart');
        if (followersGrowthCtx) {
            followersGrowthChart = new Chart(followersGrowthCtx, {
                type: 'line',
                data: {
                    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul'],
                    datasets: [{
                        label: 'Nuevos seguidores',
                        data: [0, 0, 0, 0, 0, 0, 0], // Se actualizará con datos reales
                        fill: false,
                        borderColor: 'rgba(110, 142, 251, 1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        // Gráfico de engagement
        const engagementCtx = document.getElementById('engagementChart');
        if (engagementCtx) {
            engagementChart = new Chart(engagementCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Me gusta', 'Comentarios', 'Compartidos', 'Vistas'],
                    datasets: [{
                        data: [0, 0, 0, 0], // Se actualizará con datos reales
                        backgroundColor: [
                            'rgba(231, 76, 60, 0.7)',  // Me gusta
                            'rgba(52, 152, 219, 0.7)', // Comentarios
                            'rgba(46, 204, 113, 0.7)', // Compartidos
                            'rgba(155, 89, 182, 0.7)'  // Vistas
                        ],
                        borderColor: [
                            'rgba(231, 76, 60, 1)',
                            'rgba(52, 152, 219, 1)',
                            'rgba(46, 204, 113, 1)',
                            'rgba(155, 89, 182, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }

        // Cargar datos iniciales
        loadAnalyticsData();
    }

    // Función para actualizar los gráficos con nuevos datos
    function updateCharts(data) {
        // Actualizar gráfico de rendimiento por red social
        if (socialPerformanceChart) {
            socialPerformanceChart.data.datasets[0].data = [
                data.social_performance.facebook.value,
                data.social_performance.instagram.value,
                data.social_performance.twitter.value,
                data.social_performance.linkedin.value
            ];
            socialPerformanceChart.update();
        }

        // Actualizar gráfico de crecimiento de seguidores
        if (followersGrowthChart) {
            followersGrowthChart.data.datasets[0].data = [
                data.followers_growth.ene,
                data.followers_growth.feb,
                data.followers_growth.mar,
                data.followers_growth.abr,
                data.followers_growth.may,
                data.followers_growth.jun,
                data.followers_growth.jul
            ];
            followersGrowthChart.update();
        }

        // Actualizar gráfico de engagement
        if (engagementChart) {
            engagementChart.data.datasets[0].data = [
                data.engagement.likes,
                data.engagement.comments,
                data.engagement.shares,
                data.engagement.views
            ];
            engagementChart.update();
        }
    }

    // Función para inicializar el filtro de fechas
    function initializeDateFilter() {
        // Crear el contenedor del filtro si no existe
        if (!document.getElementById('date-filter-container')) {
            const filterContainer = document.createElement('div');
            filterContainer.id = 'date-filter-container';
            filterContainer.className = 'card';
            filterContainer.style.marginBottom = '20px';
            
            filterContainer.innerHTML = `
                <div class="card-header">
                    <i class="fas fa-calendar"></i> Filtrar por fecha
                </div>
                <div style="padding: 20px;">
                    <input type="text" id="date-range" class="form-control" style="width: 100%; padding: 10px;" />
                    <div style="margin-top: 10px; display: flex; justify-content: flex-end;">
                        <button id="apply-filter" class="btn" style="background: var(--primary-gradient); color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer;">
                            Aplicar filtro
                        </button>
                    </div>
                </div>
            `;
            
            // Insertar el filtro al principio del contenido principal
            const mainContent = document.querySelector('.main-content');
            if (mainContent && mainContent.firstChild) {
                mainContent.insertBefore(filterContainer, mainContent.firstChild);
            }
            
            // Inicializar DateRangePicker
            $('#date-range').daterangepicker({
                opens: 'left',
                locale: {
                    format: 'DD/MM/YYYY',
                    applyLabel: 'Aplicar',
                    cancelLabel: 'Cancelar',
                    fromLabel: 'Desde',
                    toLabel: 'Hasta',
                    customRangeLabel: 'Personalizado',
                    daysOfWeek: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
                    monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                    firstDay: 1
                },
                startDate: moment().subtract(29, 'days'),
                endDate: moment(),
                ranges: {
                   'Hoy': [moment(), moment()],
                   'Ayer': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                   'Últimos 7 días': [moment().subtract(6, 'days'), moment()],
                   'Últimos 30 días': [moment().subtract(29, 'days'), moment()],
                   'Este mes': [moment().startOf('month'), moment().endOf('month')],
                   'Mes pasado': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                }
            });
            
            // Evento para aplicar el filtro
            document.getElementById('apply-filter').addEventListener('click', function() {
                const dateRange = $('#date-range').val();
                const dates = dateRange.split(' - ');
                if (dates.length === 2) {
                    const startDate = dates[0];
                    const endDate = dates[1];
                    // Llamar a la función para cargar datos filtrados
                    loadAnalyticsData(startDate, endDate);
                }
            });
            
            // Añadir selector de red social
            const networkSelector = document.createElement('div');
            networkSelector.style.marginTop = '15px';
            networkSelector.innerHTML = `
                <label for="network-filter" style="display: block; margin-bottom: 5px;">Filtrar por red social:</label>
                <select id="network-filter" class="form-control" style="width: 100%; padding: 8px; border-radius: 5px; border: 1px solid #ddd;">
                    <option value="">Todas las redes</option>
                    <option value="facebook">Facebook</option>
                    <option value="instagram">Instagram</option>
                    <option value="twitter">Twitter</option>
                    <option value="linkedin">LinkedIn</option>
                </select>
            `;
            
            const dateFilterContent = document.querySelector('#date-filter-container div[style="padding: 20px;"]');
            if (dateFilterContent) {
                dateFilterContent.insertBefore(networkSelector, document.getElementById('apply-filter').parentNode);
            }
            
            // Evento para el selector de red social
            document.getElementById('network-filter').addEventListener('change', function() {
                const network = this.value;
                const dateRange = $('#date-range').val();
                const dates = dateRange.split(' - ');
                let startDate = null;
                let endDate = null;
                
                if (dates.length === 2) {
                    startDate = dates[0];
                    endDate = dates[1];
                }
                
                // Cargar datos filtrados por red social y fechas
                loadAnalyticsData(startDate, endDate, network);
            });
            
        }
    }

    // Función para inicializar botones de exportación
    function initializeExportButtons() {
        // Crear el contenedor de botones de exportación
        if (!document.getElementById('export-buttons-container')) {
            const exportContainer = document.createElement('div');
            exportContainer.id = 'export-buttons-container';
            exportContainer.className = 'card';
            exportContainer.style.marginBottom = '20px';
            
            exportContainer.innerHTML = `
                <div class="card-header">
                    <i class="fas fa-download"></i> Exportar informes
                </div>
                <div style="padding: 20px; display: flex; gap: 10px;">
                    <button id="export-pdf" class="btn" style="background-color: #e74c3c; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer;">
                        <i class="fas fa-file-pdf"></i> PDF
                    </button>
                    <button id="export-excel" class="btn" style="background-color: #27ae60; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer;">
                        <i class="fas fa-file-excel"></i> Excel
                    </button>
                    <button id="export-image" class="btn" style="background-color: #3498db; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer;">
                        <i class="fas fa-image"></i> Imagen
                    </button>
                </div>
            `;
            
            // Insertar después del filtro de fechas
            const dateFilter = document.getElementById('date-filter-container');
            if (dateFilter && dateFilter.nextSibling) {
                dateFilter.parentNode.insertBefore(exportContainer, dateFilter.nextSibling);
            } else {
                // Si no hay filtro de fechas, insertar al principio
                const mainContent = document.querySelector('.main-content');
                if (mainContent && mainContent.firstChild) {
                    mainContent.insertBefore(exportContainer, mainContent.firstChild);
                }
            }
            
            // Eventos para los botones de exportación
            document.getElementById('export-pdf').addEventListener('click', function() {
                alert('Exportando informe en formato PDF. En una implementación real, esto generaría un PDF con los datos actuales.');
            });
            
            document.getElementById('export-excel').addEventListener('click', function() {
                alert('Exportando informe en formato Excel. En una implementación real, esto generaría un archivo Excel con los datos actuales.');
            });
            
            document.getElementById('export-image').addEventListener('click', function() {
                alert('Exportando gráficos como imágenes. En una implementación real, esto descargaría los gráficos como archivos PNG.');
            });
        }
    }
});