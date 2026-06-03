import os
from app import app, db
from models import User

def reset_database():
    """Borra la base de datos completamente y la recrea desde cero"""
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'instance', 'app.db')
    
    print(f"Ruta de la base de datos: {db_path}")
    
    if os.path.exists(db_path):
        print("✅ Base de datos encontrada")
        
        confirm = input("⚠️  ¿Estás seguro de BORRAR toda la base de datos? (escribe 'SI' para confirmar): ")
        
        if confirm != 'SI':
            print("❌ Operación cancelada")
            return
        
        try:
            os.remove(db_path)
            print("🗑️  Base de datos eliminada exitosamente")
        except Exception as e:
            print(f"❌ Error al eliminar: {e}")
            return
    else:
        print("⚠️  No se encontró base de datos existente")

    
    with app.app_context():
        print("🔨 Creando nueva base de datos...")
        db.create_all()
        
        test_user = User(username='admin')
        test_user.set_password('admin123')
        
        db.session.add(test_user)
        db.session.commit()
        
        print("✅ Base de datos creada exitosamente!")
        print("\n📝 Usuario de prueba creado:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🚀 Puedes iniciar la aplicación con: python app.py")


if __name__ == '__main__':
    reset_database()