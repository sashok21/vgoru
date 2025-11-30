// Мобільне меню
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

// Закриття мобільного меню при кліку на посилання
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        const navMenu = document.getElementById('navMenu');
        navMenu.classList.remove('active');
    });
});

// Плавна прокрутка до секцій
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });

            // Закрити мобільне меню після кліку
            const navMenu = document.getElementById('navMenu');
            if (navMenu) {
                navMenu.classList.remove('active');
            }
        }
    });
});

// Активний пункт меню при прокрутці
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section, header');
    const navLinks = document.querySelectorAll('.nav-menu a');

    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Анімація появи елементів при прокрутці
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Спостереження за картками маршрутів
document.addEventListener('DOMContentLoaded', () => {
    const routeCards = document.querySelectorAll('.route-card');
    const featureCards = document.querySelectorAll('.feature-card');

    routeCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.animationDelay = `${index * 0.1}s`;
        observer.observe(card);
    });

    featureCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.animationDelay = `${index * 0.1}s`;
        observer.observe(card);
    });
});

// Обробка форми контактів
const contactForm = document.querySelector('.contact-form form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Дякуємо за ваше повідомлення! Ми зв\'яжемося з вами найближчим часом.');
        e.target.reset();
    });
}

// Зміна прозорості навігації при прокрутці
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.background = 'var(--white)';
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    }
});

// Кнопка прокрутки вверх
window.addEventListener('scroll', () => {
    const scrollToTop = document.querySelector('.scroll-to-top');
    if (scrollToTop) {
        if (window.scrollY > 300) {
            scrollToTop.classList.add('show');
        } else {
            scrollToTop.classList.remove('show');
        }
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const scrollToTop = document.querySelector('.scroll-to-top');
    if (scrollToTop) {
        scrollToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});

// Функції для управління AJAX запитами
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Валідація форм
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('error');
            isValid = false;
        } else {
            input.classList.remove('error');
        }
    });

    return isValid;
}

// Форматування числових значень
function formatNumber(num) {
    return new Intl.NumberFormat('uk-UA').format(num);
}

// Копіювання тексту в буфер обміну
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            alert('Скопійовано в буфер обміну!');
        });
    } else {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            alert('Скопійовано в буфер обміну!');
        } catch (err) {
            console.error('Помилка при копіюванні:', err);
        }
        document.body.removeChild(textArea);
    }
}

// Затримання виконання функції
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Пошук за формою з затримкою
const searchInput = document.querySelector('input[name="search"]');
if (searchInput) {
    searchInput.addEventListener('input', debounce(function() {
        // Автоматичний пошук після 500мс паузи
    }, 500));
}

// Навигация по вкладкам (якщо потрібна)
function openTab(tabName) {
    const tabContent = document.querySelectorAll('.tabcontent');
    tabContent.forEach(tab => {
        tab.style.display = 'none';
    });

    const tabButton = document.querySelectorAll('.tablinks');
    tabButton.forEach(btn => {
        btn.classList.remove('active');
    });

    const tab = document.getElementById(tabName);
    if (tab) {
        tab.style.display = 'block';
    }

    event.currentTarget.classList.add('active');
}

// Інітіалізація при завантаженні сторінки
document.addEventListener('DOMContentLoaded', function() {
    // Видалення splash-скрину
    const splash = document.querySelector('.splash-screen');
    if (splash) {
        splash.style.opacity = '0';
        setTimeout(() => {
            splash.style.display = 'none';
        }, 300);
    }

    // Встановлення фокусу на першому полі форми
    const firstInput = document.querySelector('input:not([type="hidden"]):not([type="submit"])');
    if (firstInput && document.activeElement === document.body) {
        firstInput.focus();
    }
});

// Обробка помилок
window.addEventListener('error', (event) => {
    console.error('Помилка:', event.message);
    // Можете додати логування на сервер тут
});

// Логування невідловлених обіцянок
window.addEventListener('unhandledrejection', (event) => {
    console.error('Невідловлена помилка промісу:', event.reason);
});