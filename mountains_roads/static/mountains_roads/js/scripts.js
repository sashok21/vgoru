document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initMessages();
    initScrollAnimations();
});

function initNavbar() {
    const toggle = document.querySelector('.navbar__toggle');
    const menu = document.querySelector('.navbar__menu');
    const navbar = document.querySelector('.navbar');

    if (toggle && menu) {
        toggle.addEventListener('click', () => {
            const isOpen = menu.classList.toggle('navbar__menu--open');
            toggle.setAttribute('aria-expanded', String(isOpen));
        });

        menu.querySelectorAll('.navbar__link').forEach(link => {
            link.addEventListener('click', () => {
                menu.classList.remove('navbar__menu--open');
                toggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('navbar--scrolled', window.scrollY > 40);
        }, { passive: true });
    }
}

function initMessages() {
    const container = document.querySelector('.messages');
    if (!container) return;
    setTimeout(() => {
        container.style.transition = 'opacity 0.4s';
        container.style.opacity = '0';
        setTimeout(() => container.remove(), 400);
    }, 5000);
}

function initScrollAnimations() {
    const cards = document.querySelectorAll('.card, .feature-card');
    if (!cards.length) return;

    if (!('IntersectionObserver' in window)) {
        cards.forEach(card => card.classList.add('animate-fade-in-up'));
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                entry.target.style.animationDelay = `${i * 60}ms`;
                entry.target.classList.add('animate-fade-in-up');
                entry.target.style.opacity = '';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.01, rootMargin: '0px 0px 0px 0px' });

    cards.forEach(card => {
        observer.observe(card);
    });
}

function toggleFavorite(url) {
    sendToggle(url, (data) => {
        const btn = document.querySelector('.action-btn--favorite');
        if (!btn) return;
        btn.classList.toggle('is-active', data.is_favorite);
        btn.innerHTML = data.is_favorite
            ? '<i class="fa-solid fa-heart-crack"></i> Видалити з улюблених'
            : '<i class="fa-solid fa-heart"></i> Додати до улюблених';
    });
}

function toggleCompleted(url) {
    sendToggle(url, (data) => {
        const btn = document.querySelector('.action-btn--completed');
        if (!btn) return;
        btn.classList.toggle('is-active', data.is_completed);
        btn.innerHTML = data.is_completed
            ? '<i class="fa-solid fa-xmark"></i> Позначити як не пройдено'
            : '<i class="fa-solid fa-check"></i> Позначити як пройдено';
    });
}

function sendToggle(url, onSuccess) {
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrf ? csrf.value : '',
        },
    })
    .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
    })
    .then(onSuccess)
    .catch(err => console.error('Toggle failed:', err));
}