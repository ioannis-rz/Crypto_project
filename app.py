from flask import Flask, render_template, session, redirect, url_for, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sslify import SSLify
from datetime import datetime
import os

# PEPPER = os.environ.get("PASSWORD_PEPPER")
# if not PEPPER:
#     raise RuntimeError("PASSWORD_PEPPER environment variable not set")

app = Flask(__name__)
sslify = SSLify(app)
app.secret_key = 'tu_clave_secreta_aqui_cambiarla_en_produccion'

base_dir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(base_dir, 'instance')
os.makedirs(instance_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_dir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

limiter = Limiter(app=app, key_func=get_remote_address)

from models import db, Progress, UserStats
from auth import login_required, login, register

db.init_app(app)

login = limiter.limit("15 per minute", methods=["POST"])(login)
register = limiter.limit("15 per minute", methods=["POST"])(register)

# Rutas de autenticación
app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])


def get_user_stats(user_id):
    """Obtiene las estadísticas del usuario desde la base de datos"""
    stats = UserStats.query.filter_by(user_id=user_id).first()
    
    if not stats:
        stats = UserStats(user_id=user_id)
        db.session.add(stats)
        db.session.commit()
    
    return {
        'study_time': stats.study_time,
        'exercises_completed': stats.exercises_completed,
        'current_streak': stats.current_streak,
        'last_activity_date': stats.last_activity_date.strftime('%Y-%m-%d') if stats.last_activity_date else None
    }


def get_user_progress(user_id):
    """Obtiene el progreso del usuario desde la base de datos"""
    progress_data = {
        'primaria': {
            'aritmetica': 0,
            'geometria': 0,
            'algebra': 0,
            'estadistica': 0,
        },
        'secundaria': {
            'aritmetica': 0,
            'geometria': 0,
            'algebra': 0,
            'trigonometria': 0
        }
    }
    
    progress_records = Progress.query.filter_by(user_id=user_id).all()
    
    for record in progress_records:
        if record.level in progress_data and record.subject in progress_data[record.level]:
            progress_data[record.level][record.subject] = record.percentage
    
    return progress_data


@app.route('/')
@login_required
def index():
    """Página principal - Dashboard"""
    user_id = session.get('user_id')
    
    user_stats = get_user_stats(user_id)
    progress_data = get_user_progress(user_id)
    
    user_data = {
        'study_time': user_stats['study_time'],
        'exercises_completed': user_stats['exercises_completed'],
        'current_streak': user_stats['current_streak'],
        'progress': progress_data
    }
    
    return render_template('dashboard.html', 
                         user_data=user_data,
                         user_stats=user_stats, 
                         progress_data=progress_data)


@app.route('/menu')
@login_required
def menu():
    """Menú principal"""
    return render_template('menu.html')


@app.route('/tema/<nivel>/<tema>')
@login_required
def tema(nivel, tema):
    """Página de actividades por tema"""
    return render_template('actividades.html', nivel=nivel, tema=tema)


@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/update_stats', methods=['POST'])
@login_required
def update_stats():
    """API para actualizar estadísticas del usuario"""
    data = request.json
    user_id = session.get('user_id')
    
    stats = UserStats.query.filter_by(user_id=user_id).first()
    if not stats:
        stats = UserStats(user_id=user_id)
        db.session.add(stats)
    
    if 'study_time' in data:
        stats.study_time += data['study_time']
    
    if 'exercise_completed' in data:
        stats.exercises_completed += 1
    
    today = datetime.now().date()
    if stats.last_activity_date:
        days_diff = (today - stats.last_activity_date).days
        if days_diff == 1:
            stats.current_streak += 1
        elif days_diff > 1:
            stats.current_streak = 1
    else:
        stats.current_streak = 1
    
    stats.last_activity_date = today
    
    if 'progress' in data:
        nivel = data['progress'].get('nivel')
        tema = data['progress'].get('tema')
        increase = data['progress'].get('increase', 10)
        
        if nivel and tema:
            progress = Progress.query.filter_by(
                user_id=user_id,
                level=nivel,
                subject=tema
            ).first()
            
            if not progress:
                progress = Progress(
                    user_id=user_id,
                    level=nivel,
                    subject=tema,
                    percentage=min(increase, 100)
                )
                db.session.add(progress)
            else:
                progress.percentage = min(progress.percentage + increase, 100)
    
    db.session.commit()
    
    user_stats = get_user_stats(user_id)
    progress_data = get_user_progress(user_id)
    
    return jsonify({
        'success': True,
        'user_stats': user_stats,
        'progress_data': progress_data
    })


@app.route('/api/reset_progress', methods=['POST'])
@login_required
def reset_progress():
    """API para reiniciar todo el progreso del usuario"""
    user_id = session.get('user_id')
    
    try:
        stats = UserStats.query.filter_by(user_id=user_id).first()
        if stats:
            stats.study_time = 0
            stats.exercises_completed = 0
            stats.current_streak = 0
            stats.last_activity_date = None
        
        Progress.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Progreso reiniciado correctamente'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, ssl_context=('self_signed_certificate.pem', 'private_key.pem'))