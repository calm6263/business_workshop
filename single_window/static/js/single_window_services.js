/**
 * JavaScript для страницы услуг одного окна
 * Этот файл содержит интерактивные функции страницы
 */

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация событий и функций при загрузке страницы
    initBreadcrumbArrowAnimation();
    initServiceItemHoverEffects();
    initResponsiveBehavior();
    
    // Проверка наличия основной информации
    checkBasicInfoData();
    
    // Инициализация слайдера
    initSlider();
    
    // Улучшение ссылок при загрузке страницы (адаптировано под новый дизайн)
    enhanceLinks();
    
    // إضافة تفاعلية لزر "Основные сведения"
    initBasicInfoToggle();
});

/**
 * Добавление анимации стрелки breadcrumb
 */
function initBreadcrumbArrowAnimation() {
    const breadcrumbLinks = document.querySelectorAll('.breadcrumb-link');
    
    breadcrumbLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const arrow = this.nextElementSibling;
            if (arrow && arrow.classList.contains('breadcrumb-arrow')) {
                arrow.querySelector('.arrow-top').style.transform = 'rotate(45deg) scaleX(1.2)';
                arrow.querySelector('.arrow-bottom').style.transform = 'rotate(-45deg) scaleX(1.2)';
            }
        });
        
        link.addEventListener('mouseleave', function() {
            const arrow = this.nextElementSibling;
            if (arrow && arrow.classList.contains('breadcrumb-arrow')) {
                arrow.querySelector('.arrow-top').style.transform = 'rotate(45deg) scaleX(1)';
                arrow.querySelector('.arrow-bottom').style.transform = 'rotate(-45deg) scaleX(1)';
            }
        });
    });
}

/**
 * Добавление эффектов hover для элементов услуг
 */
function initServiceItemHoverEffects() {
    const serviceItems = document.querySelectorAll('.service-item-new');
    
    serviceItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.service-icon-new i, .service-icon-new svg');
            const title = this.querySelector('.service-title-new');
            
            if (icon && icon.tagName === 'svg') {
                icon.style.transition = 'all 0.3s ease';
            }
            
            if (title) {
                title.style.textShadow = '0 2px 4px rgba(0,0,0,0.1)';
            }
        });
        
        item.addEventListener('mouseleave', function() {
            const title = this.querySelector('.service-title-new');
            if (title) {
                title.style.textShadow = 'none';
            }
        });
        
        item.addEventListener('click', function(e) {
            this.style.transform = 'translateY(-1px) scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'translateY(-3px)';
            }, 150);
            
            logServiceClick(this.getAttribute('href'));
        });
    });
}

/**
 * Логирование клика по услуге для аналитики
 */
function logServiceClick(serviceUrl) {
    console.log('Клик по услуге:', serviceUrl);
}

/**
 * Управление адаптивным поведением страницы
 */
function initResponsiveBehavior() {
    window.addEventListener('resize', debounce(function() {
        updateResponsiveLayout();
    }, 250));
    
    updateResponsiveLayout();
}

/**
 * Обновление адаптивного макета в зависимости от размера экрана
 */
function updateResponsiveLayout() {
    const screenWidth = window.innerWidth;
    // تمت إزالة الإشارات إلى الأنماط القديمة، لم يعد هناك حاجة لتحديث شيء معين هنا
    // يمكن تركها فارغة أو إضافة منطق جديد إذا لزم الأمر
}

/**
 * Проверка наличия данных основной информации
 */
function checkBasicInfoData() {
    const infoValues = document.querySelectorAll('.info-value, .info-link');
    let hasMissingData = false;
    
    infoValues.forEach(element => {
        if (element.textContent.trim() === '' || element.textContent.trim() === 'None') {
            hasMissingData = true;
            element.style.color = '#ff6b6b';
            element.innerHTML += ' <small style="font-style: italic;">(требуется)</small>';
        }
    });
    
    if (hasMissingData && console) {
        console.warn('Некоторые данные основной информации отсутствуют. Пожалуйста, проверьте панель администратора.');
    }
}

/**
 * Вспомогательная функция debounce
 */
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

/**
 * Улучшение ссылок электронной почты и документов (адаптировано под новый дизайн)
 */
function enhanceLinks() {
    const infoLinks = document.querySelectorAll('.info-link');
    
    infoLinks.forEach(link => {
        if (link.getAttribute('href') && !link.classList.contains('disabled')) {
            link.addEventListener('click', function(e) {
                if (this.href.startsWith('mailto:')) {
                    console.log('Клик по ссылке электронной почты:', this.href);
                } else {
                    console.log('Загрузка документа:', this.getAttribute('href'));
                }
            });
        } else {
            link.style.opacity = '0.6';
            link.style.cursor = 'not-allowed';
            link.addEventListener('click', function(e) {
                e.preventDefault();
                alert('Файл в настоящее время недоступен. Пожалуйста, попробуйте позже.');
            });
        }
    });
}

/**
 * Инициализация слайдера
 */
function initSlider() {
    const mainSlider = document.getElementById('mainSlider');
    const sliderDots = document.getElementById('sliderDots');
    
    if (mainSlider && sliderDots) {
        const slides = mainSlider.querySelectorAll('.slider-slide');
        let currentSlide = 0;
        const totalSlides = slides.length;
        
        function createSliderDots() {
            sliderDots.innerHTML = '';
            
            for (let i = 0; i < totalSlides; i++) {
                const dot = document.createElement('button');
                dot.className = 'slider-dot';
                dot.setAttribute('aria-label', `Перейти к слайду ${i + 1}`);
                dot.addEventListener('click', () => goToSlide(i));
                sliderDots.appendChild(dot);
            }
            
            updateSliderDots();
        }
        
        function updateSliderDots() {
            const dots = sliderDots.querySelectorAll('.slider-dot');
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentSlide);
            });
        }
        
        function goToSlide(slideIndex) {
            currentSlide = slideIndex;
            if (currentSlide < 0) currentSlide = totalSlides - 1;
            if (currentSlide >= totalSlides) currentSlide = 0;
            
            mainSlider.style.transform = `translateX(-${currentSlide * 100}%)`;
            updateSliderDots();
            resetAutoSlide();
        }
        
        function nextSlide() {
            goToSlide(currentSlide + 1);
        }
        
        function prevSlide() {
            goToSlide(currentSlide - 1);
        }
        
        document.querySelector('.slider-prev')?.addEventListener('click', prevSlide);
        document.querySelector('.slider-next')?.addEventListener('click', nextSlide);
        
        createSliderDots();
        
        let autoSlideInterval;
        
        function startAutoSlide() {
            autoSlideInterval = setInterval(nextSlide, 5000);
        }
        
        function resetAutoSlide() {
            clearInterval(autoSlideInterval);
            startAutoSlide();
        }
        
        startAutoSlide();
        
        mainSlider.addEventListener('mouseenter', () => {
            clearInterval(autoSlideInterval);
        });
        
        mainSlider.addEventListener('mouseleave', () => {
            startAutoSlide();
        });
        
        // Поддержка перетаскивания на мобильных устройствах
        let isDragging = false;
        let startPos = 0;
        
        mainSlider.addEventListener('touchstart', (e) => {
            isDragging = true;
            startPos = e.touches[0].clientX;
            mainSlider.style.transition = 'none';
        });
        
        mainSlider.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            const currentPosition = e.touches[0].clientX;
            const diff = currentPosition - startPos;
            mainSlider.style.transform = `translateX(calc(-${currentSlide * 100}% + ${diff}px))`;
        });
        
        mainSlider.addEventListener('touchend', (e) => {
            isDragging = false;
            mainSlider.style.transition = 'transform 0.5s ease';
            
            const movedBy = e.changedTouches[0].clientX - startPos;
            
            if (movedBy < -50) {
                nextSlide();
            } else if (movedBy > 50) {
                prevSlide();
            } else {
                mainSlider.style.transform = `translateX(-${currentSlide * 100}%)`;
            }
        });
    }
}

/**
 * إضافة تفاعلية لزر "Основные сведения" - تم التحديث للتصميم الجديد
 */
function initBasicInfoToggle() {
    const toggleButton = document.querySelector('.basic-info-toggle');
    const infoContent = document.querySelector('.basic-info-content');
    
    if (toggleButton && infoContent) {
        toggleButton.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(1px)';
        });
        
        toggleButton.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(0)';
        });
        
        toggleButton.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        toggleButton.addEventListener('click', function() {
            const isExpanded = infoContent.classList.contains('expanded');
            
            if (isExpanded) {
                infoContent.classList.remove('expanded');
                toggleButton.classList.remove('active');
                toggleButton.querySelector('i').style.transform = 'rotate(0deg)';
            } else {
                infoContent.classList.add('expanded');
                toggleButton.classList.add('active');
                toggleButton.querySelector('i').style.transform = 'rotate(180deg)';
            }
        });
        
        infoContent.classList.remove('expanded');
        toggleButton.classList.remove('active');
        toggleButton.querySelector('i').style.transform = 'rotate(0deg)';
    }
}

// Экспорт функций, если среда module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initBreadcrumbArrowAnimation,
        initServiceItemHoverEffects,
        enhanceLinks,
        initSlider,
        initBasicInfoToggle
    };
}