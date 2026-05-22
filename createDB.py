
from app import app, db
from models import User

with app.app_context():
    db.drop_all()
    db.create_all()
    
    test_user = User(username='admin')
    test_user.set_password('admin123')
    
    db.session.add(test_user)
    db.session.commit()
    
    print("Base de datos creada exitosamente!")
    print("Usuario de prueba creado:")
    print("  Username: admin")
    print("  Password: admin123")