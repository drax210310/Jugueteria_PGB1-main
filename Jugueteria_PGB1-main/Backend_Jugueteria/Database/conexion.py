import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    """Conexión a la base de datos Jugueteria"""
    try:
        conn = pymysql.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'Uni*Bosque29'),
            database=os.getenv('DB_NAME', 'Jugueteria'),
            port=int(os.getenv('DB_PORT', 3306)),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✅ Conexión a MySQL establecida")
        return conn
    except Exception as e:
        print(f"❌ Error de conexión a MySQL: {e}")
        return None

def init_db():
    """Inicializar base de datos - crear tabla usuarios si no existe"""
    try:
        db = get_db()
        if db:
            with db.cursor() as cursor:
                # Verificar si existe tabla usuarios
                cursor.execute("SHOW TABLES LIKE 'usuarios'")
                if not cursor.fetchone():
                    print("🔄 Creando tabla usuarios...")
                    cursor.execute('''
                        CREATE TABLE usuarios (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(80) UNIQUE NOT NULL,
                            email VARCHAR(120) UNIQUE NOT NULL,
                            password VARCHAR(255) NOT NULL,
                            nombre VARCHAR(100),
                            apellido VARCHAR(100),
                            telefono VARCHAR(15),
                            direccion TEXT,
                            rol ENUM('admin', 'cliente') DEFAULT 'cliente',
                            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')
                    
                    # Crear usuario admin por defecto (contraseña: admin123)
                    cursor.execute('''
                        INSERT INTO usuarios 
                        (username, email, password, nombre, apellido, rol) VALUES
                        ('admin', 'admin@jugueteria.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj89tiM7Q.Ly', 'Admin', 'Sistema', 'admin')
                    ''')
                    print("✅ Tabla 'usuarios' creada")
                
                # Mostrar tablas existentes
                cursor.execute("SHOW TABLES")
                tablas = cursor.fetchall()
                print(f"📊 Tablas en la base de datos: {len(tablas)}")
                
            db.commit()
            db.close()
            return True
    except Exception as e:
        print(f"❌ Error al inicializar BD: {e}")
        return False

# Inicializar base de datos al importar
init_db()