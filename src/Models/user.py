from Connection.connection import connect, connection_select

def verificar_usuario(codigo, password):
    dataBase = connect()
    if not (isinstance(dataBase, list)):
        cursorObject = dataBase.cursor(dictionary=True) # Dictionary=True para acceder por nombre columna
        try:
            # NOTA: En un entorno real, las contraseñas deberían estar encriptadas (hash)
            stmt = f"SELECT * FROM usuarios WHERE codigo = '{codigo}' AND password = '{password}'"
            cursorObject.execute(stmt)
            usuario = cursorObject.fetchone()
            
            cursorObject.close()
            dataBase.close()
            
            if usuario:
                return {'status': 'ok', 'user': usuario}
            else:
                return {'status': 'error', 'message': 'Credenciales incorrectas'}
        except Exception as e:
            cursorObject.close()
            dataBase.close()
            return [{'status': 'error', 'message': str(e)}]
    else:
        return [{'status': 'error', 'message': 'Error de conexión a BD'}]