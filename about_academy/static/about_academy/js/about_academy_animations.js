// مؤشر تقدم القراءة
document.addEventListener('DOMContentLoaded', function() {
    // إنشاء شريط التقدم
    const progressBarContainer = document.createElement('div');
    progressBarContainer.className = 'progress-bar-container';
    progressBarContainer.innerHTML = '<div class="reading-progress-bar"></div>';
    document.body.appendChild(progressBarContainer);
    
    const progressBar = document.querySelector('.reading-progress-bar');
    const progressContainer = document.querySelector('.progress-bar-container');
    
    // عرض شريط التقدم عند التمرير
    window.addEventListener('scroll', function() {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight - windowHeight;
        const scrolled = (window.scrollY / documentHeight) * 100;
        
        progressBar.style.width = scrolled + '%';
        
        // إظهار/إخفاء شريط التقدم
        if (window.scrollY > 100) {
            progressContainer.style.display = 'block';
            setTimeout(() => {
                progressContainer.style.opacity = '1';
            }, 10);
        } else {
            progressContainer.style.opacity = '0';
            setTimeout(() => {
                progressContainer.style.display = 'none';
            }, 300);
        }
    });
    
    // تأثيرات النقاط الحمراء
    function initRedDotsAnimations() {
        const redDots = document.querySelectorAll('.red-dot-small');
        
        redDots.forEach((dot, index) => {
            // إضافة تأثيرات مختلفة
            setTimeout(() => {
                dot.classList.add('pulse');
                
                // تأثيرات إضافية بالتناوب
                if (index % 3 === 0) {
                    dot.classList.add('glow');
                } else if (index % 3 === 1) {
                    // تأثير خاص للنقاط الثانية
                    setInterval(() => {
                        dot.classList.toggle('glow');
                    }, 3000);
                }
                
                // تأثير عند المرور بالفأرة
                dot.addEventListener('mouseenter', function() {
                    this.style.transform = 'scale(1.5)';
                });
                
                dot.addEventListener('mouseleave', function() {
                    this.style.transform = 'scale(1)';
                });
            }, index * 200);
        });
    }
    
    // تأثيرات الظهور عند التمرير
    function initScrollAnimations() {
        const fadeElements = document.querySelectorAll('.highlight-item, .statistic-item, .gallery-item');
        
        fadeElements.forEach(element => {
            element.classList.add('fade-in-element');
        });
        
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    
                    // إذا كان العنصر يحتوي على أرقام، قم بتشغيل تأثير العد
                    if (entry.target.querySelector('.statistic-number')) {
                        const numberElement = entry.target.querySelector('.statistic-number');
                        animateNumber(numberElement);
                    }
                }
            });
        }, observerOptions);
        
        fadeElements.forEach(element => {
            observer.observe(element);
        });
    }
    
    // تأثيرات الأرقام (العد التصاعدي)
    function animateNumber(element) {
        if (element.classList.contains('animated')) return;
        
        element.classList.add('animated');
        const finalNumber = parseInt(element.textContent.replace(/\s/g, ''));
        const duration = 2000; // 2 seconds
        const steps = 60;
        const stepValue = finalNumber / steps;
        let currentStep = 0;
        
        // حفظ الرقم الأصلي
        element.setAttribute('data-final', finalNumber);
        
        // بدء العد من 0
        element.textContent = '0';
        
        const timer = setInterval(() => {
            currentStep++;
            const currentValue = Math.min(Math.floor(stepValue * currentStep), finalNumber);
            
            // تنسيق الأرقام بإضافة فواصل
            element.textContent = currentValue.toLocaleString('ru-RU');
            
            if (currentStep === steps) {
                clearInterval(timer);
                element.textContent = finalNumber.toLocaleString('ru-RU');
                element.classList.add('counting');
                
                // إزالة class بعد انتهاء الأنيميشن
                setTimeout(() => {
                    element.classList.remove('counting');
                }, 1500);
            }
        }, duration / steps);
    }
    
    // تأثيرات أيقونات SVG
    function initSvgAnimations() {
        // تأثير عند المرور على الأيقونات
        const icons = document.querySelectorAll('.highlight-icon, .download-arrow-simple, .submit-arrow-small');
        
        icons.forEach(icon => {
            icon.addEventListener('mouseenter', function() {
                const svg = this.querySelector('svg');
                if (svg) {
                    svg.style.transform = 'rotate(15deg) scale(1.2)';
                }
            });
            
            icon.addEventListener('mouseleave', function() {
                const svg = this.querySelector('svg');
                if (svg) {
                    svg.style.transform = '';
                }
            });
        });
        
        // تأثير النقر على الأيقونات
        document.querySelectorAll('.download-arrow-simple').forEach(arrow => {
            arrow.addEventListener('click', function(e) {
                e.preventDefault();
                const svg = this.querySelector('svg');
                if (svg) {
                    svg.style.transform = 'rotate(360deg) scale(1.5)';
                    setTimeout(() => {
                        svg.style.transform = '';
                    }, 500);
                }
            });
        });
    }
    
    // تأثيرات التحميل المتقدمة
    function initLoadingEffects() {
        // تأثير تحميل للصور
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.getAttribute('data-src');
                    img.classList.add('loaded');
                    
                    // تأثير ظهور تدريجي للصور
                    img.style.opacity = '0';
                    img.style.transition = 'opacity 0.5s ease';
                    
                    setTimeout(() => {
                        img.style.opacity = '1';
                    }, 100);
                    
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // تأثيرات الإجراءات التفاعلية
    function initInteractiveEffects() {
        // تأثير عند النقر على الأزرار
        document.querySelectorAll('button, .downloadable-file-button, .back-to-gallery-btn').forEach(button => {
            button.addEventListener('click', function(e) {
                // إنشاء تأثير موجات
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.7);
                    transform: scale(0);
                    animation: ripple-animation 0.6s linear;
                    width: ${size}px;
                    height: ${size}px;
                    top: ${y}px;
                    left: ${x}px;
                    pointer-events: none;
                `;
                
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);
                
                // إزالة العنصر بعد الأنيميشن
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
        
        // إضافة CSS للـripple
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple-animation {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // تأثيرات خاصة بقسم الإحصاء
    function initStatisticsEffects() {
        const statisticItems = document.querySelectorAll('.statistic-item');
        
        statisticItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                const number = this.querySelector('.statistic-number');
                if (number && !number.classList.contains('animated')) {
                    number.style.color = '#7F1726';
                    number.style.textShadow = '0 0 10px rgba(127, 23, 38, 0.3)';
                }
            });
            
            item.addEventListener('mouseleave', function() {
                const number = this.querySelector('.statistic-number');
                if (number && !number.classList.contains('animated')) {
                    number.style.color = '';
                    number.style.textShadow = '';
                }
            });
        });
    }
    
    // تأثيرات النموذج
    function initFormEffects() {
        const formInputs = document.querySelectorAll('.form-input-small, .form-textarea-small');
        
        formInputs.forEach(input => {
            // تأثير عند التركيز
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'translateY(-2px)';
            });
            
            // تأثير عند فقدان التركيز
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = '';
            });
            
            // تأثير عند الكتابة
            input.addEventListener('input', function() {
                if (this.value.length > 0) {
                    this.style.background = 'linear-gradient(white, white) padding-box, linear-gradient(90deg, #052946, #7F1726) border-box';
                } else {
                    this.style.background = 'linear-gradient(white, white) padding-box, linear-gradient(90deg, #7F1726, #052946) border-box';
                }
            });
        });
    }
    
    // تهيئة جميع المؤثرات
    function initAllAnimations() {
        initRedDotsAnimations();
        initScrollAnimations();
        initSvgAnimations();
        initLoadingEffects();
        initInteractiveEffects();
        initStatisticsEffects();
        initFormEffects();
        
        // تأثيرات إضافية بعد تحميل الصفحة
        setTimeout(() => {
            document.body.classList.add('page-loaded');
            
            // تأثير ظهور تدريجي للصفحة
            document.querySelector('.about-academy-page').style.opacity = '0';
            document.querySelector('.about-academy-page').style.transition = 'opacity 0.5s ease';
            
            setTimeout(() => {
                document.querySelector('.about-academy-page').style.opacity = '1';
            }, 100);
        }, 500);
    }
    
    // بدء التهيئة
    initAllAnimations();
    
    // تحديث المؤثرات عند تغيير حجم النافذة
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            // إعادة تهيئة بعض المؤثرات
            initRedDotsAnimations();
        }, 250);
    });
    
    // إضافة مؤشر التمرير السلس للتبويبات
    document.querySelectorAll('.nav-tab-hero').forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // تأثير على التبويب النشط
            document.querySelectorAll('.nav-tab-hero').forEach(t => {
                t.style.transform = '';
            });
            
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 300);
        });
    });
});