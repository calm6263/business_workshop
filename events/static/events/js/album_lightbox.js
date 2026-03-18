// events/static/events/js/album_lightbox.js

document.addEventListener('DOMContentLoaded', function() {
    // ----- GRID CLICK HANDLER -----
    const photoCards = document.querySelectorAll('.photo-card');
    const lightbox = document.getElementById('lightbox-modal');
    const track = document.getElementById('lightboxCarouselTrack');
    const slides = track ? Array.from(track.children) : [];
    const prevBtn = document.querySelector('.lightbox-prev');
    const nextBtn = document.querySelector('.lightbox-next');
    const closeBtn = document.querySelector('.lightbox-close');
    const overlay = document.querySelector('.lightbox-overlay');
    const counter = document.getElementById('lightboxCounter');

    if (!lightbox || !track || slides.length === 0) return;

    let currentIndex = 0;
    const totalSlides = slides.length;

    // ----- OPEN LIGHTBOX -----
    function openLightbox(index) {
        currentIndex = index;
        updateCarousel();
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    // ----- CLOSE LIGHTBOX -----
    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }

    // ----- UPDATE CAROUSEL POSITION & COUNTER -----
    function updateCarousel() {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
        if (counter) {
            counter.textContent = `${currentIndex + 1} / ${totalSlides}`;
        }
    }

    // ----- NAVIGATION -----
    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateCarousel();
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateCarousel();
    }

    // ----- ATTACH EVENT LISTENERS -----
    // Grid cards
    photoCards.forEach(card => {
        card.addEventListener('click', function() {
            const index = parseInt(this.dataset.index, 10);
            openLightbox(index);
        });
    });

    // Buttons
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
    if (overlay) overlay.addEventListener('click', closeLightbox);

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (!lightbox.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') prevSlide();
        if (e.key === 'ArrowRight') nextSlide();
    });

    // Touch swipe support (optional – same as old carousel)
    let startX = 0, endX = 0;
    track.addEventListener('touchstart', e => startX = e.touches[0].clientX, {passive: true});
    track.addEventListener('touchmove', e => endX = e.touches[0].clientX, {passive: true});
    track.addEventListener('touchend', () => {
        const diff = startX - endX;
        if (Math.abs(diff) > 50) {
            if (diff > 0) nextSlide();
            else prevSlide();
        }
    });
});