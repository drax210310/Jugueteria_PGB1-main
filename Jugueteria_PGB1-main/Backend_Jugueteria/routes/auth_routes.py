from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from Database.conexion import get_db

auth_bp = Blueprint('auth', __name__)

def generar_token(user_id, username, rol='cliente'):
    """Generar token JWT"""
    try:
        payload = {
            'id': user_id,
            'username': username,
            'rol': rol,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        secret_key = os.getenv('JWT_SECRET', 'jwt_secret_key')
        return jwt.encode(payload, secret_key, algorithm='HS256')
    except Exception as e:
        print(f"Error generando token: {e}")
        return None

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Username, email y password son requeridos'
            }), 400
        
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            # Verificar si usuario o email ya existen
            cursor.execute(
                "SELECT id FROM usuarios WHERE username = %s OR email = %s", 
                (data['username'], data['email'])
            )
            if cursor.fetchone():
                return jsonify({
                    'success': False, 
                    'message': 'El usuario o email ya existe'
                }), 400
            
            # Hashear password
            hashed_pwd = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insertar usuario
            cursor.execute("""
                INSERT INTO usuarios (username, email, password, nombre, apellido, telefono, direccion, rol) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data['username'],
                data['email'],
                hashed_pwd,
                data.get('nombre', ''),
                data.get('apellido', ''),
                data.get('telefono', ''),
                data.get('direccion', ''),
                data.get('rol', 'cliente')
            ))
            
            user_id = cursor.lastrowid
            db.commit()
            
            # Generar token
            token = generar_token(user_id, data['username'], data.get('rol', 'cliente'))
            
            return jsonify({
                'success': True,
                'message': 'Usuario registrado exitosamente',
                'token': token,
                'user_id': user_id
            }), 201
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error en el servidor: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Username y password son requeridos'
            }), 400
        
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, email, password, nombre, apellido, telefono, direccion, rol 
                FROM usuarios WHERE username = %s
            """, (data['username'],))
            
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
                # Generar token
                token = generar_token(user['id'], user['username'], user.get('rol', 'cliente'))
                
                # Remover password de la respuesta
                user.pop('password')
                
                return jsonify({
                    'success': True,
                    'message': 'Login exitoso',
                    'token': token,
                    'user': user
                }), 200
            else:
                return jsonify({
                    'success': False, 
                    'message': 'Usuario o contraseña incorrectos'
                }), 401
                
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error en el servidor: {str(e)}'
        }), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """Verificar token JWT"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token es requerido'
            }), 400
        
        try:
            secret_key = os.getenv('JWT_SECRET', 'jwt_secret_key')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            return jsonify({
                'success': True,
                'message': 'Token válido',
                'user': {
                    'id': payload['id'],
                    'username': payload['username'],
                    'rol': payload.get('rol', 'cliente')
                }
            }), 200
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token expirado'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Token inválido'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error en el servidor: {str(e)}'
        }), 500