// home.js - نسخة متوافقة مع HTMX
function initCarousels() {
    const bestCarousel = document.getElementById('bestCarousel');
    const bestPrevBtn = document.querySelector('.prev-best');
    const bestNextBtn = document.querySelector('.next-best');

    if (bestCarousel && bestPrevBtn && bestNextBtn) {
        bestPrevBtn.addEventListener('click', () => scrollCarousel(bestCarousel, -320));
        bestNextBtn.addEventListener('click', () => scrollCarousel(bestCarousel, 320));
    }

    const newCarousel = document.getElementById('newCarousel');
    const newPrevBtn = document.querySelector('.prev-new');
    const newNextBtn = document.querySelector('.next-new');

    if (newCarousel && newPrevBtn && newNextBtn) {
        newPrevBtn.addEventListener('click', () => scrollCarousel(newCarousel, -320));
        newNextBtn.addEventListener('click', () => scrollCarousel(newCarousel, 320));
    }

    const earlyCarousel = document.getElementById('earlyCarousel');
    const earlyPrevBtn = document.querySelector('.prev-early');
    const earlyNextBtn = document.querySelector('.next-early');

    if (earlyCarousel && earlyPrevBtn && earlyNextBtn) {
        earlyPrevBtn.addEventListener('click', () => scrollCarousel(earlyCarousel, -320));
        earlyNextBtn.addEventListener('click', () => scrollCarousel(earlyCarousel, 320));
    }
}

function scrollCarousel(carousel, amount) {
    if (carousel) {
        carousel.scrollBy({ left: amount, behavior: 'smooth' });
    }
}

// دوال عامة للاستخدام في onclick
window.scrollBest = (direction) => scrollCarousel(document.getElementById('bestCarousel'), direction * 320);
window.scrollNew = (direction) => scrollCarousel(document.getElementById('newCarousel'), direction * 320);
window.scrollEarly = (direction) => scrollCarousel(document.getElementById('earlyCarousel'), direction * 320);

// تهيئة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', initCarousels);

// إعادة تهيئة بعد تحديث HTMX
document.addEventListener('htmx:afterSwap', function(evt) {
    if (evt.detail.target && evt.detail.target.id === 'journal-content') {
        initCarousels();
    }
});