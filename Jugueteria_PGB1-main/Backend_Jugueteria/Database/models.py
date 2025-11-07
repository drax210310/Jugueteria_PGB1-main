from Database.conexion import get_db_connection
import bcrypt

class Usuario:
    @staticmethod
    def crear_usuario(datos):
        """Crea un nuevo usuario en la base de datos"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    # Verificar si usuario o email existen
                    cursor.execute(
                        "SELECT id FROM usuarios WHERE username = %s OR email = %s",
                        (datos['username'], datos['email'])
                    )
                    if cursor.fetchone():
                        return None, "El usuario o email ya existe"
                    
                    # Encriptar contraseña
                    hashed_pwd = bcrypt.hashpw(datos['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    # Insertar usuario
                    sql = """
                        INSERT INTO usuarios 
                        (username, email, password, nombre, apellido, telefono, direccion, rol) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        datos['username'],
                        datos['email'],
                        hashed_pwd,
                        datos.get('nombre', ''),
                        datos.get('apellido', ''),
                        datos.get('telefono', ''),
                        datos.get('direccion', ''),
                        datos.get('rol', 'cliente')
                    ))
                    
                    conexion.commit()
                    usuario_id = cursor.lastrowid
                    return usuario_id, "Usuario creado exitosamente"
                    
            except Exception as e:
                return None, f"Error: {str(e)}"
            finally:
                conexion.close()
        return None, "Error de conexión"

    @staticmethod
    def obtener_por_username(username):
        """Obtiene usuario por nombre de usuario"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, username, email, password, nombre, apellido, telefono, direccion, rol FROM usuarios WHERE username = %s",
                        (username,)
                    )
                    return cursor.fetchone()
            except Exception as e:
                print(f"Error al obtener usuario: {e}")
                return None
            finally:
                conexion.close()
        return None

    @staticmethod
    def obtener_por_id(usuario_id):
        """Obtiene usuario por ID"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, username, email, nombre, apellido, telefono, direccion, rol FROM usuarios WHERE id = %s",
                        (usuario_id,)
                    )
                    return cursor.fetchone()
            except Exception as e:
                print(f"Error al obtener usuario: {e}")
                return None
            finally:
                conexion.close()
        return None

    @staticmethod
    def actualizar(usuario_id, datos):
        """Actualiza información del usuario"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    sql = """
                        UPDATE usuarios 
                        SET nombre = %s, apellido = %s, telefono = %s, direccion = %s, email = %s
                        WHERE id = %s
                    """
                    cursor.execute(sql, (
                        datos.get('nombre'),
                        datos.get('apellido'),
                        datos.get('telefono'),
                        datos.get('direccion'),
                        datos.get('email'),
                        usuario_id
                    ))
                    conexion.commit()
                    return True, "Usuario actualizado exitosamente"
            except Exception as e:
                return False, f"Error al actualizar usuario: {str(e)}"
            finally:
                conexion.close()
        return False, "Error de conexión"

    @staticmethod
    def verificar_password(password, hashed):
        """Verifica si la contraseña coincide"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

class Producto:
    @staticmethod
    def obtener_todos():
        """Obtiene todos los productos (juguetes)"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    # Consulta para obtener productos con información de línea de producto
                    cursor.execute("""
                        SELECT p.*, lp.Nombre as linea_nombre 
                        FROM producto p 
                        LEFT JOIN linea_producto lp ON p.Id_Linea_Producto = lp.Id_Linea_Producto
                        ORDER BY p.Nombre
                    """)
                    return cursor.fetchall()
            except Exception as e:
                print(f"Error al obtener productos: {e}")
                # Si falla la consulta con join, intentar sin join
                try:
                    with conexion.cursor() as cursor:
                        cursor.execute("SELECT * FROM producto ORDER BY Nombre")
                        return cursor.fetchall()
                except:
                    return []
            finally:
                conexion.close()
        return []

    @staticmethod
    def obtener_por_id(producto_id):
        """Obtiene un producto por ID"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM producto WHERE Id_Producto = %s", (producto_id,))
                    return cursor.fetchone()
            except Exception as e:
                print(f"Error al obtener producto: {e}")
                return None
            finally:
                conexion.close()
        return None

    @staticmethod
    def crear(producto_data):
        """Crea un nuevo producto"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    # Ajustar según los campos de tu tabla producto
                    sql = """
                        INSERT INTO producto 
                        (Nombre, Descripcion, Precio, Stock, Id_Linea_Producto) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        producto_data['nombre'],
                        producto_data.get('descripcion', ''),
                        producto_data['precio'],
                        producto_data.get('stock', 0),
                        producto_data.get('id_linea_producto', 1)
                    ))
                    conexion.commit()
                    return cursor.lastrowid, "Producto creado exitosamente"
            except Exception as e:
                return None, f"Error: {str(e)}"
            finally:
                conexion.close()
        return None, "Error de conexión"

    @staticmethod
    def actualizar(producto_id, producto_data):
        """Actualiza un producto"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    sql = """
                        UPDATE producto 
                        SET Nombre=%s, Descripcion=%s, Precio=%s, Stock=%s, Id_Linea_Producto=%s
                        WHERE Id_Producto=%s
                    """
                    cursor.execute(sql, (
                        producto_data['nombre'],
                        producto_data.get('descripcion', ''),
                        producto_data['precio'],
                        producto_data.get('stock', 0),
                        producto_data.get('id_linea_producto', 1),
                        producto_id
                    ))
                    conexion.commit()
                    return True, "Producto actualizado exitosamente"
            except Exception as e:
                return False, f"Error: {str(e)}"
            finally:
                conexion.close()
        return False, "Error de conexión"

class LineaProducto:
    @staticmethod
    def obtener_todas():
        """Obtiene todas las líneas de producto"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM linea_producto ORDER BY Nombre")
                    return cursor.fetchall()
            except Exception as e:
                print(f"Error al obtener líneas de producto: {e}")
                return []
            finally:
                conexion.close()
        return []

class Venta:
    @staticmethod
    def crear(venta_data):
        """Crea una nueva venta"""
        conexion = get_db_connection()
        if conexion:
            try:
                with conexion.cursor() as cursor:
                    # Insertar venta
                    sql = """
                        INSERT INTO venta 
                        (Fecha, Total, Id_Usuario) 
                        VALUES (NOW(), %s, %s)
                    """
                    cursor.execute(sql, (
                        venta_data['total'],
                        venta_data['usuario_id']
                    ))
                    venta_id = cursor.lastrowid
                    
                    # Insertar detalles de venta
                    for detalle in venta_data['detalles']:
                        sql_detalle = """
                            INSERT INTO detalle_venta 
                            (Id_Venta, Id_Producto, Cantidad, Precio_Unitario) 
                            VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(sql_detalle, (
                            venta_id,
                            detalle['producto_id'],
                            detalle['cantidad'],
                            detalle['precio_unitario']
                        ))
                    
                    conexion.commit()
                    return venta_id, "Venta creada exitosamente"
            except Exception as e:
                return None, f"Error: {str(e)}"
            finally:
                conexion.close()
        return None, "Error de conexión"