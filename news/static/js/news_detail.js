// news_detail.js - تهيئة كاروسيل الصور ووظيفة الاشتراك

function initNewsDetail() {
    // ===== تهيئة كاروسيل الصور (إذا كان موجودًا) =====
    const carouselSection = document.querySelector('.gallery-carousel-section');
    if (carouselSection) {
        const track = carouselSection.querySelector('.gallery-carousel-track');
        const slides = carouselSection.querySelectorAll('.gallery-carousel-slide');
        const prevBtn = carouselSection.querySelector('.carousel-arrow-prev');
        const nextBtn = carouselSection.querySelector('.carousel-arrow-next');
        const dots = carouselSection.querySelectorAll('.carousel-dot');

        if (track && slides.length > 0) {
            let currentIndex = 0;
            let slidesToShow = getSlidesToShow();
            const totalSlides = slides.length;
            const maxIndex = Math.max(0, totalSlides - slidesToShow);

            function getSlidesToShow() {
                return window.innerWidth <= 768 ? 1 : 2;
            }

            function updateCarousel() {
                slidesToShow = getSlidesToShow();
                const slideWidth = slides[0].offsetWidth;
                const gap = parseInt(window.getComputedStyle(track).gap) || 20;
                const maxIndex = Math.max(0, totalSlides - slidesToShow);

                if (currentIndex > maxIndex) {
                    currentIndex = maxIndex;
                }

                const translateX = -currentIndex * (slideWidth + gap);
                track.style.transform = `translateX(${translateX}px)`;

                dots.forEach((dot, i) => {
                    dot.classList.toggle('active', i === currentIndex);
                });

                if (prevBtn) prevBtn.disabled = currentIndex === 0;
                if (nextBtn) nextBtn.disabled = currentIndex >= maxIndex;
            }

            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    if (currentIndex > 0) {
                        currentIndex--;
                        updateCarousel();
                    }
                });
            }

            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    const maxIndex = Math.max(0, totalSlides - getSlidesToShow());
                    if (currentIndex < maxIndex) {
                        currentIndex++;
                        updateCarousel();
                    }
                });
            }

            dots.forEach((dot, index) => {
                dot.addEventListener('click', () => {
                    const maxIndex = Math.max(0, totalSlides - getSlidesToShow());
                    if (index <= maxIndex) {
                        currentIndex = index;
                        updateCarousel();
                    }
                });
            });

            let resizeTimeout;
            window.addEventListener('resize', () => {
                clearTimeout(resizeTimeout);
                resizeTimeout = setTimeout(() => {
                    const newSlidesToShow = getSlidesToShow();
                    const newMaxIndex = Math.max(0, totalSlides - newSlidesToShow);
                    if (currentIndex > newMaxIndex) {
                        currentIndex = newMaxIndex;
                    }
                    updateCarousel();
                }, 150);
            });

            updateCarousel();
        }
    }

    // ===== وظيفة الاشتراك في النشرة البريدية (موجودة أيضاً في الصفحة الرئيسية) =====
    const subscribeForm = document.getElementById('subscribeForm');
    if (subscribeForm) {
        subscribeForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                email: formData.get('email'),
                consent: formData.get('consent') === 'on'
            };
            const messageDiv = this.querySelector('.newsletter-message');
            
            try {
                const response = await fetch('/news/subscribe/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    messageDiv.textContent = result.message;
                    messageDiv.className = 'newsletter-message success';
                    this.reset();
                } else {
                    messageDiv.textContent = result.error || 'Произошла ошибка';
                    messageDiv.className = 'newsletter-message error';
                }
            } catch (error) {
                messageDiv.textContent = 'Ошибка соединения';
                messageDiv.className = 'newsletter-message error';
            }
        });
    }
}

// تنفيذ التهيئة عند تحميل الصفحة
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNewsDetail);
} else {
    initNewsDetail();
}