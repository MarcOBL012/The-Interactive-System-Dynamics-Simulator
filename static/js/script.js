/* Archivo: vensim_python_web/static/js/script.js */

// Variable global para almacenar los datos de la simulación completa
let globalCSVData = [];

// Función para cambiar entre secciones (Tabs del Sidebar)
window.showSection = function(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.style.display = 'none');

    const target = document.getElementById('section-' + sectionId);
    if (target) {
        target.style.display = 'block';
        if (sectionId === 'simulacion' || sectionId === 'completa') {
            setTimeout(() => window.dispatchEvent(new Event('resize')), 100);
        }
    }

    const links = document.querySelectorAll('.list-group-item');
    links.forEach(link => {
        link.classList.remove('active');
        if(link.getAttribute('onclick') && link.getAttribute('onclick').includes("'" + sectionId + "'")) {
            link.classList.add('active');
        }
    });
};

// Función para alternar visibilidad de líneas
window.toggleGraphLine = function(index, isVisible) {
    const container = document.getElementById('graph-container-COMPLETA');
    if (!container) return;
    
    // Filtrado robusto de líneas (ignora grids y ejes)
    const allPaths = Array.from(container.querySelectorAll('.mpld3-axes path'));
    const dataLines = allPaths.filter(path => {
        const style = window.getComputedStyle(path);
        const strokeWidth = parseFloat(style.strokeWidth) || 0;
        const strokeDash = style.strokeDasharray;
        // Solo líneas sólidas y gruesas (>1.2px)
        return (!strokeDash || strokeDash === 'none') && strokeWidth > 1.2;
    });

    if (dataLines[index]) {
        dataLines[index].style.transition = "opacity 0.3s ease";
        dataLines[index].style.opacity = isVisible ? "0.9" : "0"; 
        dataLines[index].style.visibility = isVisible ? "visible" : "hidden";
    }
};

// --- NUEVA FUNCIÓN: DESCARGAR CSV ---
window.downloadSimulationCSV = function() {
    if (!globalCSVData || globalCSVData.length === 0) {
        alert("No hay datos para exportar. Ejecute una simulación primero.");
        return;
    }

    // 1. Extraer cabeceras (keys del primer objeto)
    const headers = Object.keys(globalCSVData[0]);
    
    // 2. Construir contenido CSV
    const csvRows = [];
    csvRows.push(headers.join(',')); // Fila de cabeceras

    for (const row of globalCSVData) {
        const values = headers.map(header => {
            const escaped = ('' + row[header]).replace(/"/g, '\\"');
            return `"${escaped}"`;
        });
        csvRows.push(values.join(','));
    }

    const csvString = csvRows.join('\n');
    
    // 3. Crear Blob y descargar
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'simulacion_completa.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
};

document.addEventListener("DOMContentLoaded", function() {
    
    // Toggle Sidebar
    var el = document.getElementById("wrapper");
    var toggleButton = document.getElementById("menu-toggle");
    if (toggleButton) {
        toggleButton.onclick = function () { el.classList.toggle("toggled"); };
    }

    // Pantalla de Carga
    var loadingScreen = document.getElementById('loading');
    if (loadingScreen) {
        setTimeout(function() {
            loadingScreen.style.opacity = '0';
            setTimeout(function() { loadingScreen.style.display = 'none'; }, 500);
        }, 800);
    }

    // Checkboxes
    document.body.addEventListener('change', function(e) {
        if (e.target.classList.contains('toggle-line-check')) {
            const index = parseInt(e.target.getAttribute('data-line-index'));
            toggleGraphLine(index, e.target.checked);
        }
    });

    // Lógica de Simulación
    document.querySelectorAll('.simulation-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const targetNivel = this.getAttribute('data-target-nivel');
            const btn = this.querySelector('button[type="submit"]');
            const originalText = btn.innerHTML;
            
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Simulando...';
            btn.disabled = true;

            const params = {};
            
            // Buscar FINAL TIME (Local o Global)
            const localTimeInput = this.querySelector('input[name="FINAL TIME"]');
            if (localTimeInput && localTimeInput.value) {
                params['FINAL TIME'] = localTimeInput.value;
            } else {
                const globalTimeInput = document.getElementById('global-final-time');
                if (globalTimeInput && globalTimeInput.value) {
                    params['FINAL TIME'] = globalTimeInput.value;
                }
            }

            this.querySelectorAll('.param-input').forEach(input => {
                if (input.value !== '' && input.name !== 'FINAL TIME') {
                     params[input.name] = input.value;
                }
            });

            fetch('/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_nivel: targetNivel, params: params })
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'ok') {
                    // Actualizar Gráfico
                    const graphContainer = document.getElementById('graph-container-' + targetNivel);
                    if (graphContainer) {
                        graphContainer.innerHTML = data.graph;
                        // Reactivar scripts mpld3
                        Array.from(graphContainer.querySelectorAll("script")).forEach( oldScript => {
                            const newScript = document.createElement("script");
                            Array.from(oldScript.attributes).forEach( attr => newScript.setAttribute(attr.name, attr.value) );
                            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                            oldScript.parentNode.replaceChild(newScript, oldScript);
                        });

                        // Lógica específica para SIMULACION COMPLETA
                        if (targetNivel === 'COMPLETA') {
                            // 1. Guardar datos para CSV
                            if (data.table_data) {
                                globalCSVData = data.table_data;
                                const csvBtn = document.getElementById('btn-download-csv');
                                if(csvBtn) csvBtn.disabled = false;
                            }

                            // 2. Re-aplicar checkboxes
                            setTimeout(() => {
                                const checks = document.querySelectorAll('.toggle-line-check');
                                checks.forEach(chk => {
                                    toggleGraphLine(parseInt(chk.getAttribute('data-line-index')), chk.checked);
                                });
                            }, 300);
                        }
                    }

                    // Actualizar Tabla (Solo Individuales)
                    if (targetNivel !== 'COMPLETA') {
                        const tableBody = document.getElementById('table-body-' + targetNivel);
                        if (tableBody && data.table_data) {
                            tableBody.innerHTML = '';
                            for (const [time, value] of Object.entries(data.table_data)) {
                                tableBody.innerHTML += `<tr><td>${time}</td><td>${parseFloat(value).toFixed(2)}</td></tr>`;
                            }
                        }
                    }
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => { console.error('Error:', error); alert('Error de conexión.'); })
            .finally(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            });
        });
    });
});