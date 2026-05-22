document.addEventListener('DOMContentLoaded', function() {
    animateStats();
    addInteractiveEffects();
});

function animateStats() {
    const statValues = document.querySelectorAll('.stat-value');
    
    statValues.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        let currentValue = 0;
        const increment = Math.ceil(finalValue / 50);
        const duration = 1000;
        const stepTime = duration / (finalValue / increment);
        
        const counter = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                stat.textContent = finalValue;
                clearInterval(counter);
            } else {
                stat.textContent = currentValue;
            }
        }, stepTime);
    });
}

function addInteractiveEffects() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });

    const progressFills = document.querySelectorAll('.progress-fill');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.transition = 'width 1s ease-out';
            }
        });
    }, { threshold: 0.5 });

    progressFills.forEach(fill => {
        observer.observe(fill);
    });

    const topicCards = document.querySelectorAll('.topic-card');
    
    topicCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

async function updateUserStats(data) {
    try {
        const response = await fetch('/api/update_stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            updateDashboardUI(result.user_data);
        }
    } catch (error) {
        console.error('Error al actualizar estadísticas:', error);
    }
}

function updateDashboardUI(userData) {
    document.getElementById('study-time').textContent = userData.study_time;
    document.getElementById('exercises').textContent = userData.exercises_completed;
    document.getElementById('streak').textContent = userData.current_streak;
    
    updateProgressBars(userData.progress);
}

function updateProgressBars(progress) {
    for (const [nivel, temas] of Object.entries(progress)) {
        for (const [tema, valor] of Object.entries(temas)) {
            const progressBar = document.querySelector(
                `.progress-item[data-nivel="${nivel}"][data-tema="${tema}"] .progress-fill`
            );
            if (progressBar) {
                progressBar.style.width = `${valor}%`;
            }
        }
    }
}

function showAchievement(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        animation: slideIn 0.5s ease-out;
    `;
    notification.textContent = `🎉 ${message}`;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.5s ease-out';
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);