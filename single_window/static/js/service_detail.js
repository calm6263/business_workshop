document.addEventListener('DOMContentLoaded', function() {
    // عناصر DOM
    const faqItemsNew = document.querySelectorAll('.faq-item-new');
    const serviceModal = document.getElementById('serviceModal');
    const confirmationModal = document.getElementById('confirmationModal');
    const loginRequiredModal = document.getElementById('loginRequiredModal');
    const openServiceOrLoginModal = document.getElementById('openServiceOrLoginModal');
    const closeModal = document.querySelector('.close-modal');
    const closeConfirmation = document.getElementById('closeConfirmation');
    const serviceForm = document.getElementById('serviceRequestForm');
    const requestNumberSpan = document.getElementById('requestNumber');
    const submitButton = document.querySelector('.submit-button');
    const textInputs = serviceForm ? serviceForm.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"]') : [];

    // تهيئة عناصر FAQ الجديدة
    function initializeFAQNew() {
        faqItemsNew.forEach(function(item) {
            const question = item.querySelector('.faq-question-new');
            const answer = item.querySelector('.faq-answer-new');
            
            // تهيئة الحالة - مطوي افتراضياً
            answer.style.maxHeight = '0';
            
            question.addEventListener('click', function() {
                const isActive = item.classList.contains('active');
                
                // إغلاق جميع العناصر الأخرى
                faqItemsNew.forEach(function(otherItem) {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                        const otherAnswer = otherItem.querySelector('.faq-answer-new');
                        otherAnswer.style.maxHeight = '0';
                    }
                });
                
                if (!isActive) {
                    // فتح العنصر الحالي
                    item.classList.add('active');
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                    
                    // إعادة حساب الارتفاع بعد فتح المحتوى
                    setTimeout(() => {
                        if (item.classList.contains('active')) {
                            answer.style.maxHeight = answer.scrollHeight + 'px';
                        }
                    }, 100);
                } else {
                    // طي العنصر الحالي
                    item.classList.remove('active');
                    answer.style.maxHeight = '0';
                }
            });
        });
    }

    // التحكم في نافذة التسجيل المطلوب (مُحدّث للتصميم الجديد)
    function initializeModalControls() {
        if (openServiceOrLoginModal) {
            openServiceOrLoginModal.addEventListener('click', function(e) {
                e.preventDefault();
                
                const userAuthenticated = this.getAttribute('data-user-authenticated') === 'true';
                
                if (userAuthenticated) {
                    // للمستخدمين المسجلين: فتح نافذة الخدمة
                    const userEmail = this.getAttribute('data-user-email') || '';
                    const userName = this.getAttribute('data-user-name') || '';
                    
                    if (userEmail) {
                        document.getElementById('email').value = userEmail;
                    }
                    if (userName && userName.trim() !== '') {
                        document.getElementById('contactPerson').value = userName;
                    }
                    
                    serviceModal.style.display = 'block';
                    document.body.style.overflow = 'hidden';
                } else {
                    // للمستخدمين غير المسجلين: فتح نافذة التسجيل المطلوب (التصميم الجديد)
                    loginRequiredModal.style.display = 'flex';
                    loginRequiredModal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            });
        }

        // إغلاق نافذة الخدمة
        if (closeModal) {
            closeModal.addEventListener('click', function() {
                serviceModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            });
        }

        // إغلاق نافذة التسجيل المطلوب (باستخدام زر الإغلاق الجديد)
        const closeLoginModalBtn = document.querySelector('#loginRequiredModal .modal-close-btn');
        if (closeLoginModalBtn) {
            closeLoginModalBtn.addEventListener('click', function() {
                loginRequiredModal.style.display = 'none';
                loginRequiredModal.classList.remove('active');
                document.body.style.overflow = 'auto';
            });
        }

        // إغلاق نافذة التأكيد
        if (closeConfirmation) {
            closeConfirmation.addEventListener('click', function() {
                confirmationModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            });
        }

        // إغلاق النوافذ عند النقر على الـ overlay
        window.addEventListener('click', function(e) {
            if (e.target === serviceModal || e.target.classList.contains('modal-overlay') && e.target.closest('#serviceModal')) {
                serviceModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
            if (e.target === confirmationModal || e.target.classList.contains('modal-overlay') && e.target.closest('#confirmationModal')) {
                confirmationModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
            // للنافذة الجديدة: overlay هو عنصر منفصل، نتحقق إذا كان الـ target هو الـ overlay داخل loginRequiredModal
            if (loginRequiredModal && loginRequiredModal.style.display === 'flex') {
                if (e.target.classList.contains('modal-overlay') && e.target.closest('#loginRequiredModal')) {
                    loginRequiredModal.style.display = 'none';
                    loginRequiredModal.classList.remove('active');
                    document.body.style.overflow = 'auto';
                }
            }
        });

        // إغلاق بالضغط على ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                if (serviceModal.style.display === 'block') {
                    serviceModal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }
                if (confirmationModal.style.display === 'block') {
                    confirmationModal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }
                if (loginRequiredModal.style.display === 'flex') {
                    loginRequiredModal.style.display = 'none';
                    loginRequiredModal.classList.remove('active');
                    document.body.style.overflow = 'auto';
                }
            }
        });
    }

    // معالجة إرسال النموذج
    function initializeFormSubmission() {
        if (!serviceForm) return;
        
        serviceForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // التحقق من الموافقة على الشروط
            const agreementCheckbox = document.getElementById('agreement');
            if (!agreementCheckbox.checked) {
                alert('Пожалуйста, согласитесь с условиями пользовательского соглашения');
                return;
            }

            // تعطيل زر الإرسال أثناء المعالجة
            submitButton.disabled = true;
            submitButton.textContent = 'Отправка...';

            try {
                // جمع البيانات من النموذج
                const formData = {
                    service_type: document.getElementById('serviceType').value,
                    format: document.getElementById('format').value,
                    contact_person: document.getElementById('contactPerson').value,
                    phone: document.getElementById('phone').value,
                    email: document.getElementById('email').value,
                    additional_info: document.getElementById('additionalInfo').value,
                    agreed_to_terms: agreementCheckbox.checked
                };

                // إرسال البيانات إلى الخادم
                const submitUrl = serviceForm.getAttribute('data-submit-url');
                const response = await fetch(submitUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (data.success) {
                    // عرض رقم الطلب
                    if (requestNumberSpan) {
                        requestNumberSpan.textContent = data.request_number;
                    }
                    
                    // إظهار نافذة التأكيد
                    serviceModal.style.display = 'none';
                    if (confirmationModal) {
                        confirmationModal.style.display = 'block';
                    }
                    
                    // إعادة تعيين النموذج
                    serviceForm.reset();
                    
                    // إعادة تحميل الصفحة بعد 3 ثوانٍ لتحديث قائمة الطلبات
                    setTimeout(function() {
                        window.location.reload();
                    }, 3000);
                } else {
                    alert('Ошибка при отправке заявки: ' + data.error);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Произошла ошибка при отправке заявки');
            } finally {
                // إعادة تمكين زر الإرسال
                submitButton.disabled = false;
                submitButton.textContent = 'Отправить';
            }
        });

        // منع إرسال النموذج عند الضغط على Enter في الحقول النصية
        textInputs.forEach(input => {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                }
            });
        });
    }

    // إضافة تأثير النقر على زر التقديم
    function initializeButtonEffects() {
        if (openServiceOrLoginModal) {
            openServiceOrLoginModal.addEventListener('mousedown', function() {
                this.style.transform = 'translateY(-1px) scale(0.98)';
            });

            openServiceOrLoginModal.addEventListener('mouseup', function() {
                this.style.transform = 'translateY(-2px) scale(1)';
            });

            openServiceOrLoginModal.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(-2px) scale(1)';
            });
        }
    }

    // تهيئة السلايدر
    function initializeSlider() {
        const mainSlider = document.getElementById('mainSlider');
        const sliderDots = document.getElementById('sliderDots');
        
        if (mainSlider && sliderDots) {
            const slides = mainSlider.querySelectorAll('.slider-slide');
            let currentSlide = 0;
            const totalSlides = slides.length;
            
            if (totalSlides <= 1) return; // لا داعي للسلايدر إذا كان هناك شريحة واحدة فقط
            
            // إنشاء نقاط السلايدر
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
            
            // تحديث النقاط النشطة
            function updateSliderDots() {
                const dots = sliderDots.querySelectorAll('.slider-dot');
                dots.forEach((dot, index) => {
                    dot.classList.toggle('active', index === currentSlide);
                });
            }
            
            // الانتقال إلى شريحة محددة
            function goToSlide(slideIndex) {
                currentSlide = slideIndex;
                if (currentSlide < 0) currentSlide = totalSlides - 1;
                if (currentSlide >= totalSlides) currentSlide = 0;
                
                mainSlider.style.transform = `translateX(-${currentSlide * 100}%)`;
                updateSliderDots();
                
                // إعادة ضبط السلايدر التلقائي
                resetAutoSlide();
            }
            
            // الشريحة التالية
            function nextSlide() {
                goToSlide(currentSlide + 1);
            }
            
            // الشريحة السابقة
            function prevSlide() {
                goToSlide(currentSlide - 1);
            }
            
            // إضافة الأحداث للأزرار
            const prevButton = document.querySelector('.slider-prev');
            const nextButton = document.querySelector('.slider-next');
            
            if (prevButton) {
                prevButton.addEventListener('click', prevSlide);
            }
            
            if (nextButton) {
                nextButton.addEventListener('click', nextSlide);
            }
            
            // إنشاء النقاط
            createSliderDots();
            
            // السلايدر التلقائي
            let autoSlideInterval;
            
            function startAutoSlide() {
                autoSlideInterval = setInterval(nextSlide, 5000); // كل 5 ثوانٍ
            }
            
            function resetAutoSlide() {
                clearInterval(autoSlideInterval);
                startAutoSlide();
            }
            
            // بدء السلايدر التلقائي
            startAutoSlide();
            
            // إيقاف السلايدر التلقائي عند التفاعل
            mainSlider.addEventListener('mouseenter', () => {
                clearInterval(autoSlideInterval);
            });
            
            mainSlider.addEventListener('mouseleave', () => {
                startAutoSlide();
            });
        }
    }

    // تهيئة جميع المكونات
    initializeFAQNew();
    initializeModalControls();
    initializeFormSubmission();
    initializeButtonEffects();
    initializeSlider();
});