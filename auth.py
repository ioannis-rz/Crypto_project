from flask import request, session, redirect, url_for, render_template, flash, current_app
from functools import wraps
from models import User, db
from zxcvbn import zxcvbn

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped


def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip = request.remote_addr

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            current_app.logger.info(f'Login exitoso - Usuario: {username}, IP: {ip}')
            return redirect(url_for('index'))
        else:
            current_app.logger.warning(f'Intento de login fallido - Usuario: {username}, IP: {ip}')
            return render_template('login.html', error='Usuario o contraseña incorrectos')

    return render_template('login.html')


def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        ip = request.remote_addr
        
        # Validaciones
        if not username or not password:
            return render_template('register.html', error='Todos los campos son obligatorios')
        
        if len(username) < 3:
            return render_template('register.html', error='El nombre de usuario debe tener al menos 3 caracteres')
        
        if len(password) < 8:
            return render_template('register.html', error='La contraseña debe tener al menos 8 caracteres')

        results = zxcvbn(password, user_inputs=[username])
        print(results.get('feedback'))
        if results['score'] < 1:
            return render_template('register.html', error = results.get('feedback').get('warning') if results.get('feedback') and results.get('feedback').get('warning') 
                                   else 'Añade algunas palabras más o símbolos')

        if password != confirm_password:
            return render_template('register.html', error='Las contraseñas no coinciden')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='El nombre de usuario ya está en uso')
        
        try:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            current_app.logger.info(f'Nuevo registro - Usuario: {username}, IP: {ip}')
            
            session['user_id'] = new_user.id
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error en registro - Usuario: {username}, IP: {ip}, Error: {str(e)}')
            return render_template('register.html', error='Error al crear la cuenta. Intenta de nuevo.')
    
    return render_template('register.html')