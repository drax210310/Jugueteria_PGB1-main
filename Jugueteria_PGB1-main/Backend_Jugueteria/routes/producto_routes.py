from flask import Blueprint, request, jsonify
from Database.conexion import get_db

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET'])
def get_productos():
    """Obtener todos los productos"""
    try:
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            # Obtener productos con información de línea de producto
            cursor.execute("""
                SELECT p.*, lp.Nombre as linea_nombre 
                FROM producto p 
                LEFT JOIN linea_producto lp ON p.Id_Linea_Producto = lp.Id_Linea_Producto
                ORDER BY p.Nombre
            """)
            productos = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'productos': productos,
                'total': len(productos)
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error al obtener productos: {str(e)}'
        }), 500

@productos_bp.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    """Obtener un producto específico"""
    try:
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM producto WHERE Id_Producto = %s", (id,))
            producto = cursor.fetchone()
            
            if producto:
                return jsonify({
                    'success': True, 
                    'producto': producto
                }), 200
            else:
                return jsonify({
                    'success': False, 
                    'message': 'Producto no encontrado'
                }), 404
                
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error: {str(e)}'
        }), 500

@productos_bp.route('/productos', methods=['POST'])
def create_producto():
    """Crear nuevo producto (solo admin)"""
    try:
        data = request.get_json()
        
        if not data.get('nombre') or not data.get('precio'):
            return jsonify({
                'success': False,
                'message': 'Nombre y precio son requeridos'
            }), 400
        
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO producto (Nombre, Descripcion, Precio, Stock, Id_Linea_Producto)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data['nombre'],
                data.get('descripcion', ''),
                data['precio'],
                data.get('stock', 0),
                data.get('id_linea_producto', 1)
            ))
            
            db.commit()
            return jsonify({
                'success': True, 
                'message': 'Producto creado exitosamente',
                'id': cursor.lastrowid
            }), 201
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error al crear producto: {str(e)}'
        }), 500

@productos_bp.route('/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    """Actualizar producto (solo admin)"""
    try:
        data = request.get_json()
        
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE producto 
                SET Nombre=%s, Descripcion=%s, Precio=%s, Stock=%s, Id_Linea_Producto=%s
                WHERE Id_Producto=%s
            """, (
                data['nombre'],
                data.get('descripcion', ''),
                data['precio'],
                data.get('stock', 0),
                data.get('id_linea_producto', 1),
                id
            ))
            
            db.commit()
            return jsonify({
                'success': True, 
                'message': 'Producto actualizado exitosamente'
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error al actualizar producto: {str(e)}'
        }), 500

@productos_bp.route('/lineas-producto', methods=['GET'])
def get_lineas():
    """Obtener todas las líneas de producto"""
    try:
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM linea_producto ORDER BY Nombre")
            lineas = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'lineas': lineas,
                'total': len(lineas)
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error al obtener líneas: {str(e)}'
        }), 500

@productos_bp.route('/municipios', methods=['GET'])
def get_municipios():
    """Obtener todos los municipios"""
    try:
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM municipio ORDER BY Nombre")
            municipios = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'municipios': municipios,
                'total': len(municipios)
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error al obtener municipios: {str(e)}'
        }), 500

@productos_bp.route('/departamentos', methods=['GET'])
def get_departamentos():
    """Obtener todos los departamentos"""
    try:
        db = get_db()
        if not db:
            return jsonify({'success': False, 'message': 'Error de conexión a BD'}), 500
        
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT d.*, m.Nombre as municipio_nombre 
                FROM departamento d 
                LEFT JOIN municipio m ON d.Id_Municipio = m.Id_Municipio
                ORDER BY d.Nombre
            """)
            departamentos = cursor.fetchall()
            
            return jsonify({
                'success': True,
                'departamentos': departamentos,
                'total': len(departamentos)
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error al obtener departamentos: {str(e)}'
        }), 500