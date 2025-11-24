from flask import render_template, make_response, request, jsonify, session, redirect, url_for
from src.Controllers.controller import controller, simulate_new_run
from src.Models.user import verificar_usuario # Importamos el nuevo modelo

def modelRoute(app):
    
    # --- RUTA DE LOGIN ---
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            codigo = request.form.get('codigo')
            password = request.form.get('password')
            
            resultado = verificar_usuario(codigo, password)
            
            if isinstance(resultado, dict) and resultado.get('status') == 'ok':
                # Guardar datos en sesión
                session['user_id'] = resultado['user']['idUsuario']
                session['user_name'] = resultado['user']['nombre']
                return redirect(url_for('home'))
            else:
                error_msg = resultado.get('message', 'Error desconocido') if isinstance(resultado, dict) else 'Error de conexión'
                return render_template('login.html', error=error_msg)
        
        # Si ya está logueado, mandar al home
        if 'user_id' in session:
            return redirect(url_for('home'))
            
        return render_template('login.html')

    # --- RUTA DE LOGOUT ---
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    # --- RUTA HOME (PROTEGIDA) ---
    @app.route('/', methods=['GET'])
    def home():
        # VERIFICACIÓN DE SESIÓN
        if 'user_id' not in session:
            return redirect(url_for('login'))

        response = controller()
        
        if isinstance(response, list) and len(response) > 0 and isinstance(response[0], dict) and 'message' in response[0]:
             return render_template('error.html', error_message=response)
        
        if isinstance(response, dict) and 'niveles' in response:
             respuesta = make_response(render_template('template.html', 
                                                       nivel=response['niveles'], 
                                                       constantes=response['constantes'],
                                                       grafica_completa=response.get('grafica_completa'),
                                                       lista_niveles_bd=response.get('lista_niveles_bd'),
                                                       user_name=session.get('user_name'))) # Pasamos el nombre del usuario
             
             respuesta.headers['Cache-Control'] = 'public, max-age=180'
             return respuesta
             
        return render_template('error.html', error_message=[{'message': 'Error desconocido en respuesta del controlador'}])

    # --- RUTA SIMULAR (PROTEGIDA) ---
    @app.route('/simulate', methods=['POST'])
    def simulate():
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'Sesión expirada. Recargue la página.'}), 401

        data = request.get_json()
        result = simulate_new_run(data)
        return jsonify(result)