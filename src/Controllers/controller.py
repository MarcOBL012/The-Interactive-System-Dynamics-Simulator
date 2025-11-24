from src.Models.model import getModelAll
import pysd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import urllib3
import os
import mpld3
from mpld3 import plugins
from decouple import config
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN: Variables específicas que quieres controlar ---
VARIABLES_CONTROL = [
    'Tasa Compra',
    'tasa Venta',
    'Tasa obsolencia',
    'Efectividad por difusion',
    'Gastos por difusion',
    'Demanda por cliente',
    'Control de operaciones deseado',
    'Captacion por cliente actual',
    'Tiempo de permanencia promedio'
]

def load_model_file():
    ruta_archivo = os.path.join('assets/vensim', 'document.mdl')
    if not os.path.exists(ruta_archivo):
         try:
            url = config('APP_URL_VENSIM')
            http = urllib3.PoolManager()
            resp = http.request('GET', url)
            with open(ruta_archivo, 'wb') as archivo:
                archivo.write(resp.data)
         except Exception as e:
             print(f"Error descargando modelo: {e}")
    return pysd.read_vensim(ruta_archivo)

def get_model_constants(model):
    
    constants_list = []
    try:
        import re
        def to_pysd_name(name):
            return re.sub(r'[^a-zA-Z0-9]', '_', name).lower()

        for var_name in VARIABLES_CONTROL:
            try:
                py_name = to_pysd_name(var_name)
                if hasattr(model.components, py_name):
                    val = getattr(model.components, py_name)()
                    constants_list.append({'name': var_name, 'value': float(val)})
                else:
                     doc = model.doc()
                     row = doc[doc['Real Name'] == var_name]
                     if not row.empty:
                         actual_py_name = row.iloc[0]['Py Name']
                         val = getattr(model.components, actual_py_name)()
                         constants_list.append({'name': var_name, 'value': float(val)})
            except Exception as e:
                print(f"No se pudo leer valor inicial para '{var_name}': {e}")
                constants_list.append({'name': var_name, 'value': 0.0})

    except Exception as e:
        print(f"Error general obteniendo constantes: {e}")

    return constants_list

def generate_combined_graph_html(stocks, niveles_config):
    # Crear figura más ancha para la vista completa
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Iterar sobre todos los niveles configurados en la BD
    for item in niveles_config:
        # item estructura: [id, title, labelX, labelY, pos, nameNivel, color]
        name_nivel = item[5]
        color = item[6]
        
        if name_nivel in stocks.columns:
            # Graficar cada línea. 
            # IMPORTANTE: Usamos el label igual al name_nivel para identificarlo luego
            ax.plot(stocks[name_nivel], label=name_nivel, linewidth=2.5, color=color, alpha=0.8)

    ax.set_title("Comportamiento Global del Sistema", loc='center', fontsize=14)
    ax.set_xlabel("Tiempo (Meses)", fontsize=10)
    ax.set_ylabel("Valor", fontsize=10)
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    
    # Añadimos leyenda interactiva nativa de mpld3 por si acaso, 
    # aunque haremos checkboxes externos en HTML
    interactive_legend = plugins.InteractiveLegendPlugin(
        plot_elements=ax.get_lines(),
        labels=[l.get_label() for l in ax.get_lines()],
        start_visible=True
    )
    plugins.connect(fig, interactive_legend)
    
    graph_html = mpld3.fig_to_html(fig)
    plt.close(fig)
    return graph_html

def generate_graph_html(stocks, info_nivel):
    fig, ax = plt.subplots()
    data = stocks[info_nivel['nameNivel']]
    
    ax.plot(data, label=info_nivel['nameNivel'], linewidth=3.0, color=info_nivel['nameColor'])
    ax.set_title(info_nivel['title'], loc='center', fontsize=12)
    ax.set_ylabel(info_nivel['nameLabelY'], fontsize=10)
    ax.set_xlabel(info_nivel['nameLabelX'], fontsize=10)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    ax.legend(loc='best', fontsize=9)
    
    graph_html = mpld3.fig_to_html(fig)
    plt.close(fig)
    return graph_html

def controller():
    try:
        model = load_model_file()
        constants = get_model_constants(model)
        response_bd = getModelAll()

        if isinstance(response_bd, list) and len(response_bd) > 0 and isinstance(response_bd[0], dict) and 'message' in response_bd[0]:
             return response_bd

        nivel = {}
        stocks = model.run()
        
        # 1. Generar gráficos individuales (Lógica existente)
        for item in response_bd:
            try:
                info_nivel = {
                    "title": item[1], "nameLabelX": item[2], "nameLabelY": item[3], 
                    "nameNivel": item[5], "nameColor": item[6]
                }
                if info_nivel['nameNivel'] in stocks.columns:
                    nivel[info_nivel['nameNivel']] = {
                        'data': stocks[info_nivel['nameNivel']], 
                        'graph': generate_graph_html(stocks, info_nivel),
                        'info': info_nivel
                    }
            except:
                pass
        
        # 2. NUEVO: Generar gráfico combinado
        grafica_completa = generate_combined_graph_html(stocks, response_bd)

        # Retornamos todo, incluyendo la nueva gráfica completa y la lista pura de niveles para los checkboxes
        return {
            'niveles': nivel, 
            'constantes': constants, 
            'grafica_completa': grafica_completa,
            'lista_niveles_bd': response_bd # Pasamos la lista cruda para iterar checkboxes fácilmente
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return [{'message': f'Error interno: {str(e)}'}]

def simulate_new_run(params_received):
    try:
        model = load_model_file()
        target_nivel = params_received.get('target_nivel')
        
        new_params = {}
        final_time_val = None 

        for k, v in params_received.get('params', {}).items():
            try:
                val = float(v)
                if k == 'FINAL TIME':
                    final_time_val = val
                else:
                    new_params[k] = val
            except:
                pass
                
        print(f"--- DEBUG: Simulando '{target_nivel}'...")
        
        if final_time_val is not None:
            stocks = model.run(params=new_params, final_time=final_time_val)
        else:
            stocks = model.run(params=new_params)
        
        # CASO ESPECIAL: SIMULACION COMPLETA
        if target_nivel == 'COMPLETA':
            response_bd = getModelAll()
            combined_graph = generate_combined_graph_html(stocks, response_bd)
            
            # --- NUEVO: PREPARAR DATA PARA CSV ---
            # 1. Filtramos solo las columnas configuradas en la BD (evita exportar variables internas basura)
            cols_bd = [item[5] for item in response_bd if item[5] in stocks.columns]
            
            # 2. Preparamos el DataFrame para exportar: incluimos el índice (Tiempo) como columna
            df_export = stocks[cols_bd].copy()
            df_export.reset_index(inplace=True) # Esto convierte el índice 'Time' en una columna normal
            
            # 3. Convertimos a lista de diccionarios para que JS lo entienda fácil
            # Ejemplo: [{'index': 0, 'Ventas': 10}, {'index': 1, 'Ventas': 15}, ...]
            csv_data = df_export.to_dict(orient='records')

            return {
                'status': 'ok',
                'graph': combined_graph,
                'table_data': csv_data # ¡Aquí enviamos los datos para el CSV!
            }

        # CASO NORMAL (Individual)
        response_bd = getModelAll()
        info_nivel = next((
            {"title": i[1], "nameLabelX": i[2], "nameLabelY": i[3], "nameNivel": i[5], "nameColor": i[6]} 
            for i in response_bd if i[5] == target_nivel
        ), None)
        
        if info_nivel:
            table_data = stocks[target_nivel].to_dict()
            return {
                'status': 'ok', 
                'graph': generate_graph_html(stocks, info_nivel),
                'table_data': table_data
            }
        
        return {'status': 'error', 'message': 'Nivel no encontrado'}

    except Exception as e:
        print(f"Error en simulación: {e}")
        return {'status': 'error', 'message': str(e)}