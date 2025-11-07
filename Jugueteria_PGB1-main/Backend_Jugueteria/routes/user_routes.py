from flask import Blueprint, request, jsonify
import jwt
import os
from Database.conexion import get_db

usuarios_bp = Blueprint('usuarios', __name__)

def verificar_token(token):
    """Verificar token JWT"""
    try:
        secret_key = os.getenv('JWT_SECRET', 'jwt_secret_key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except:
        return None

def obtener_usuario_actual():
    """Obtener usuario actual desde el token"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    return verificar_token(token)

@usuarios_bp.route('/usuarios/perfil', methods=['GET'])
def get_perfil():
    """Obtener perfil del usuario actual"""
    try:
        usuario_actual = obtener_usuario_actual()
        
        if not usuario_actual:
            return jsonify({
                'success': False,
                'message': 'Token inválido o expirado'
            }), 401
        
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, email, nombre, apellido, telefono, direccion, rol, fecha_creacion
                FROM usuarios WHERE id = %s
            """, (usuario_actual['id'],))
            
            usuario = cursor.fetchone()
            
            if usuario:
                return jsonify({
                    'success': True,
                    'usuario': usuario
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }), 404
                
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener perfil: {str(e)}'
        }), 500

@usuarios_bp.route('/usuarios/perfil', methods=['PUT'])
def update_perfil():
    """Actualizar perfil del usuario"""
    try:
        usuario_actual = obtener_usuario_actual()
        
        if not usuario_actual:
            return jsonify({
                'success': False,
                'message': 'Token inválido o expirado'
            }), 401
        
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({
                'success': False,
                'message': 'El email es requerido'
            }), 400
        
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE usuarios 
                SET nombre=%s, apellido=%s, telefono=%s, direccion=%s, email=%s
                WHERE id=%s
            """, (
                data.get('nombre'),
                data.get('apellido'),
                data.get('telefono'),
                data.get('direccion'),
                data.get('email'),
                usuario_actual['id']
            ))
            
            db.commit()
            return jsonify({
                'success': True,
                'message': 'Perfil actualizado exitosamente'
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar perfil: {str(e)}'
        }), 500

@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    """Obtener todos los usuarios (solo admin)"""
    try:
        usuario_actual = obtener_usuario_actual()
        
        if not usuario_actual:
            return jsonify({
                'success': False,
                'message': 'Token inválido o expirado'
            }), 401
        
        # Verificar si es admin
        if usuario_actual.get('rol') != 'admin':
            return jsonify({
                'success': False,
                'message': 'No autorizado. Se requiere rol de administrador'
            }), 403
        
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, email, nombre, apellido, telefono, direccion, rol, fecha_creacion
                FROM usuarios ORDER BY fecha_creacion DESC
            """)
            usuarios = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'usuarios': usuarios,
                'total': len(usuarios)
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener usuarios: {str(e)}'
        }), 500

@usuarios_bp.route('/usuarios/<int:user_id>', methods=['GET'])
def get_usuario(user_id):
    """Obtener un usuario específico (solo admin)"""
    try:
        usuario_actual = obtener_usuario_actual()
        
        if not usuario_actual:
            return jsonify({
                'success': False,
                'message': 'Token inválido o expirado'
            }), 401
        
        # Verificar si es admin o el mismo usuario
        if usuario_actual.get('rol') != 'admin' and usuario_actual['id'] != user_id:
            return jsonify({
                'success': False,
                'message': 'No autorizado'
            }), 403
        
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, email, nombre, apellido, telefono, direccion, rol, fecha_creacion
                FROM usuarios WHERE id = %s
            """, (user_id,))
            
            usuario = cursor.fetchone()
            
            if usuario:
                return jsonify({
                    'success': True,
                    'usuario': usuario
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }), 404
                
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener usuario: {str(e)}'
        }), 500

@usuarios_bp.route('/usuarios/<int:user_id>/rol', methods=['PUT'])
def update_rol(user_id):
    """Actualizar rol de usuario (solo admin)"""
    try:
        usuario_actual = obtener_usuario_actual()
        
        if not usuario_actual or usuario_actual.get('rol') != 'admin':
            return jsonify({
                'success': False,
                'message': 'No autorizado. Se requiere rol de administrador'
            }), 403
        
        data = request.get_json()
        nuevo_rol = data.get('rol')
        
        if nuevo_rol not in ['admin', 'cliente']:
            return jsonify({
                'success': False,
                'message': 'Rol inválido. Debe ser "admin" o "cliente"'
            }), 400
        
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE usuarios SET rol = %s WHERE id = %s
            """, (nuevo_rol, user_id))
            
            db.commit()
            return jsonify({
                'success': True,
                'message': f'Rol actualizado a {nuevo_rol}'
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar rol: {str(e)}'
        }), 500