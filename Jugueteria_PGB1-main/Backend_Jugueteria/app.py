from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# SOLUCIÓN DEFINITIVA - Configurar paths correctamente
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Raíz del proyecto (JUGUETERA_PGB1)

# Agregar todas las rutas necesarias al path
sys.path.append(project_root)  # Raíz del proyecto
sys.path.append(current_dir)   # Directorio Backend_Jugueteria
sys.path.append(os.path.join(project_root, 'Database'))  # Carpeta Database
sys.path.append(os.path.join(project_root, 'routes'))    # Carpeta routes

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_secreta')

CORS(app)

# IMPORTACIONES CORREGIDAS con manejo de errores
try:
    print("🔍 Intentando importar blueprints...")
    
    # Importar desde routes/
    from routes.auth_routes import auth_bp
    print("✅ auth_bp importado correctamente")
    
    from routes.producto_routes import productos_bp
    print("✅ productos_bp importado correctamente")
    
    from routes.user_routes import usuarios_bp
    print("✅ usuarios_bp importado correctamente")
    
except ImportError as e:
    print(f"❌ Error crítico importando blueprints: {e}")
    print("📁 Directorio actual:", os.path.dirname(__file__))
    print("📁 Rutas en sys.path:")
    for path in sys.path:
        print(f"   - {path}")
    raise

# Registrar blueprints con prefijos correctos
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(productos_bp, url_prefix='/api')
app.register_blueprint(usuarios_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({
        'success': True,
        'message': '🚀 Backend Jugueteria funcionando!',
        'database': 'Jugueteria',
        'endpoints': {
            'auth': '/api/auth/*',
            'productos': '/api/productos/*',
            'usuarios': '/api/usuarios/*'
        }
    })

@app.route('/api/health')
def health():
    return jsonify({
        'success': True,
        'message': '✅ Servidor y base de datos activos',
        'status': 'running'
    })

@app.route('/api/debug/paths')
def debug_paths():
    """Endpoint para debuguear las rutas"""
    paths_info = {
        'current_directory': os.path.dirname(__file__),
        'project_root': project_root,
        'python_paths': sys.path,
        'files_in_routes': os.listdir(os.path.join(project_root, 'routes')) if os.path.exists(os.path.join(project_root, 'routes')) else 'NO EXISTE',
        'files_in_database': os.listdir(os.path.join(project_root, 'Database')) if os.path.exists(os.path.join(project_root, 'Database')) else 'NO EXISTE'
    }
    return jsonify(paths_info)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Servidor Flask iniciando en http://localhost:{port}")
    print(f"📁 Directorio actual: {current_dir}")
    print(f"📁 Raíz del proyecto: {project_root}")
    print("🔧 Debug mode:", debug)
    
    app.run(host='0.0.0.0', port=port, debug=debug)