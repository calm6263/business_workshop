document.addEventListener('DOMContentLoaded', function() {
    // ================================================
    // الكاروسيل متعدد الصور للشاشات الكبيرة
    // ================================================
    
    let currentSlide = 0;
    let itemsPerView = 3;
    let autoPlayInterval;
    
    function initMultiImageCarousel() {
        const carouselInner = document.getElementById('multiImageCarouselInner');
        const allItems = document.querySelectorAll('.multi-image-item');
        const totalItems = allItems.length;
        
        if (!carouselInner || totalItems === 0) return;
        
        // تحديث العرض
        updateCarousel();
        
        // بدء التمرير التلقائي
        startAutoPlay();
        
        // إضافة حدث لوقف التمرير عند التمرير يدوياً
        const carouselWrapper = document.querySelector('.multi-image-carousel-wrapper');
        if (carouselWrapper) {
            carouselWrapper.addEventListener('mouseenter', stopAutoPlay);
            carouselWrapper.addEventListener('mouseleave', startAutoPlay);
        }
        
        // إضافة حدث النقر للصور لفتح Lightbox
        const multiImageItems = document.querySelectorAll('.multi-image-item img');
        multiImageItems.forEach(img => {
            img.addEventListener('click', function() {
                openLightbox(this.src, this.alt);
            });
        });
    }
    
    function updateCarousel() {
        const carouselInner = document.getElementById('multiImageCarouselInner');
        const allItems = document.querySelectorAll('.multi-image-item');
        const totalItems = allItems.length;
        const totalSlides = Math.ceil(totalItems / itemsPerView);
        
        if (!carouselInner) return;
        
        // التأكد من أن الفهرس الحالي صحيح
        if (currentSlide >= totalSlides) currentSlide = totalSlides - 1;
        if (currentSlide < 0) currentSlide = 0;
        
        // حساب العرض المطلوب للتمرير
        const translateX = -(currentSlide * 100); // 100% لكل مجموعة من 3 صور
        carouselInner.style.transform = `translateX(${translateX}%)`;
    }
    
    window.moveSlide = function(direction) {
        const allItems = document.querySelectorAll('.multi-image-item');
        const totalItems = allItems.length;
        const totalSlides = Math.ceil(totalItems / itemsPerView);
        
        currentSlide += direction;
        
        if (currentSlide < 0) {
            currentSlide = totalSlides - 1;
        } else if (currentSlide >= totalSlides) {
            currentSlide = 0;
        }
        
        updateCarousel();
        resetAutoPlay();
    }
    
    window.goToSlide = function(slideIndex) {
        const allItems = document.querySelectorAll('.multi-image-item');
        const totalItems = allItems.length;
        const totalSlides = Math.ceil(totalItems / itemsPerView);
        
        if (slideIndex >= 0 && slideIndex < totalSlides) {
            currentSlide = slideIndex;
            updateCarousel();
            resetAutoPlay();
        }
    }
    
    function startAutoPlay() {
        if (window.innerWidth < 768) return;
        
        stopAutoPlay();
        autoPlayInterval = setInterval(() => {
            moveSlide(1);
        }, 5000); // 5 ثواني لكل شريحة
    }
    
    function stopAutoPlay() {
        if (autoPlayInterval) {
            clearInterval(autoPlayInterval);
            autoPlayInterval = null;
        }
    }
    
    function resetAutoPlay() {
        stopAutoPlay();
        startAutoPlay();
    }
    
    // تهيئة الكاروسيل عند تحميل الصفحة
    if (window.innerWidth >= 768) {
        initMultiImageCarousel();
    }
    
    // إعادة التهيئة عند تغيير حجم النافذة
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
            itemsPerView = 3;
            initMultiImageCarousel();
        } else {
            stopAutoPlay();
            itemsPerView = 1;
        }
    });
    
    // ================================================
    // تهيئة Bootstrap carousel للشاشات الصغيرة
    // ================================================
    
    const galleryCarousel = document.querySelector('#projectGalleryCarouselMobile');
    if (galleryCarousel && window.innerWidth < 768) {
        const carousel = new bootstrap.Carousel(galleryCarousel, {
            interval: 4000,
            wrap: true
        });
    }
    
    // ================================================
    // وظيفة Lightbox لعرض الصور بالحجم الكامل
    // ================================================
    
    function openLightbox(src, alt) {
        // إنشاء عنصر lightbox
        const lightbox = document.createElement('div');
        lightbox.id = 'imageLightbox';
        lightbox.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        // إنشاء صورة
        const img = document.createElement('img');
        img.src = src;
        img.alt = alt;
        img.style.cssText = `
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 8px;
            transform: scale(0.9);
            transition: transform 0.3s ease;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        `;
        
        // زر الإغلاق
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.style.cssText = `
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: white;
            font-size: 40px;
            cursor: pointer;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            border-radius: 50%;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        `;
        
        closeBtn.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(127, 23, 38, 0.8)';
            this.style.transform = 'rotate(90deg)';
        });
        
        closeBtn.addEventListener('mouseleave', function() {
            this.style.background = 'rgba(255, 255, 255, 0.1)';
            this.style.transform = 'rotate(0deg)';
        });
        
        closeBtn.addEventListener('click', closeLightbox);
        
        // إغلاق بالنقر خارج الصورة
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
        
        // إغلاق بمفتاح ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeLightbox();
            }
        });
        
        // إضافة العناصر
        lightbox.appendChild(img);
        lightbox.appendChild(closeBtn);
        document.body.appendChild(lightbox);
        
        // إظهار بسلاسة
        setTimeout(() => {
            lightbox.style.opacity = '1';
            img.style.transform = 'scale(1)';
        }, 10);
        
        function closeLightbox() {
            lightbox.style.opacity = '0';
            img.style.transform = 'scale(0.9)';
            
            setTimeout(() => {
                if (lightbox.parentNode) {
                    lightbox.parentNode.removeChild(lightbox);
                }
            }, 300);
        }
    }
    
    // ================================================
    // تأثيرات زر الانضمام إلى المشروع
    // ================================================
    
    const joinProjectBtn = document.querySelector('.join-project-btn');
    if (joinProjectBtn) {
        // تأثير عند المرور
        joinProjectBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 8px 20px rgba(5, 41, 70, 0.3)';
        });
        
        joinProjectBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
        
        // تأثير عند النقر
        joinProjectBtn.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(1px)';
        });
        
        joinProjectBtn.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-3px)';
        });
    }
    
    // ================================================
    // بقية الكود الأصلي
    // ================================================

    // إضافة تأثيرات للصور في المعرض
    const galleryImages = document.querySelectorAll('.gallery-image-container img');
    galleryImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // تحسينات للنماذج
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            // التحقق من أن المستخدم ليس روبوت
            const robotCheck = document.getElementById('robotCheck');
            if (!robotCheck.checked) {
                e.preventDefault();
                alert('Пожалуйста, подтвердите, что вы не робот.');
                return false;
            }
            
            // التحقق من صحة البريد الإلكتروني
            const emailField = contactForm.querySelector('input[type="email"]');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailField && !emailRegex.test(emailField.value)) {
                e.preventDefault();
                alert('Пожалуйста, введите корректный email адрес.');
                emailField.focus();
                return false;
            }
            
            // إظهار رسالة التحميل
            const submitBtn = contactForm.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Отправка...';
                submitBtn.disabled = true;
            }
        });
    }

    // تحسينات للاستجابة - إعادة ترتيب العناصر على الشاشات الصغيرة
    function handleResize() {
        const windowWidth = window.innerWidth;
        const infoItems = document.querySelectorAll('.info-item');
        
        if (windowWidth <= 768) {
            // على الشاشات الصغيرة، اجعل العناصر تظهر بشكل عمودي
            infoItems.forEach(item => {
                item.style.flexDirection = 'column';
                item.style.alignItems = 'flex-start';
                item.style.gap = '8px';
                
                const icon = item.querySelector('.info-icon');
                if (icon) {
                    icon.style.marginRight = '0';
                    icon.style.marginBottom = '8px';
                }
            });
        } else {
            // على الشاشات الكبيرة، اجعل العناصر تظهر بشكل أفقي
            infoItems.forEach(item => {
                item.style.flexDirection = 'row';
                item.style.alignItems = 'center';
                item.style.gap = '15px';
                
                const icon = item.querySelector('.info-icon');
                if (icon) {
                    icon.style.marginRight = '15px';
                    icon.style.marginBottom = '0';
                }
            });
        }
    }

    // تشغيل التحقق من الحجم عند التحميل وعند تغيير الحجم
    window.addEventListener('load', handleResize);
    window.addEventListener('resize', handleResize);

    // تحسينات للانتقال بين الصور في الكاروسيل
    if (galleryCarousel) {
        galleryCarousel.addEventListener('slide.bs.carousel', function(event) {
            // إضافة تأثير انتقالي سلس
            const activeItem = event.relatedTarget;
            const img = activeItem.querySelector('img');
            
            if (img) {
                img.style.transition = 'transform 0.5s ease';
                setTimeout(() => {
                    img.style.transform = 'scale(1)';
                }, 50);
            }
        });
    }

    // إضافة تأثيرات للبطاقات
    const memberCards = document.querySelectorAll('.member-card');
    memberCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 20px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        });
    });

    // تحسينات للوصول (accessibility)
    // إضافة أتريبيوتات ARIA للروابط
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        if (!link.getAttribute('aria-label')) {
            const linkText = link.textContent.trim();
            if (linkText) {
                link.setAttribute('aria-label', linkText);
            }
        }
    });

    // تحسينات للأزرار
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(button => {
        button.addEventListener('focus', function() {
            this.style.outline = '2px solid #7F1726';
            this.style.outlineOffset = '2px';
        });
        
        button.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });

    // تحسينات للنماذج
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });

    // ================================================
    // نافذة الانضمام إلى المشروع
    // ================================================

    // عناصر DOM
    const openJoinBtn = document.getElementById('openJoinModal');
    const joinModal = document.getElementById('joinModal');
    const closeJoinModalBtn = document.getElementById('closeJoinModal');
    const joinForm = document.getElementById('joinForm');
    const submitJoinBtn = document.getElementById('submitJoinRequest');
    const joinPersonTypeOptions = document.querySelectorAll('#joinModal .person-type-option');
    const joinPersonTypeInput = document.getElementById('joinPersonType');
    const joinIndividualFields = document.getElementById('joinIndividualFields');
    const joinLegalFields = document.getElementById('joinLegalFields');
    const joinSuccessModal = document.getElementById('joinSuccessModal');
    const joinSuccessMessageContent = document.getElementById('joinSuccessMessageContent');
    const joinRequestIdValue = document.getElementById('joinRequestIdValue');
    const closeJoinSuccessModalBtn = document.getElementById('closeJoinSuccessModal');
    const closeJoinSuccessBtn = document.getElementById('closeJoinSuccessBtn');
    const joinSuccessMessage = document.getElementById('joinSuccessMessage');
    const joinErrorMessage = document.getElementById('joinErrorMessage');
    const joinSubmitText = document.getElementById('joinSubmitText');
    const joinLoadingSpinner = document.getElementById('joinLoadingSpinner');

    // تهيئة نوع الشخص
    function initializeJoinPersonType() {
        joinPersonTypeOptions.forEach(opt => {
            if (opt.getAttribute('data-type') === 'individual') {
                opt.classList.add('active');
            } else {
                opt.classList.remove('active');
            }
        });
        
        if (joinIndividualFields) joinIndividualFields.style.display = 'block';
        if (joinLegalFields) joinLegalFields.style.display = 'none';
        if (joinPersonTypeInput) joinPersonTypeInput.value = 'individual';
        
        manageJoinRequiredFields('individual');
    }

    // إدارة الحقول المطلوبة
    function manageJoinRequiredFields(personType) {
        const allFields = [
            'join_full_name_individual', 'join_phone', 'join_email', 'join_address', 'join_comments_individual',
            'join_full_name', 'join_phone_legal', 'join_email_legal', 'join_company_name', 
            'join_inn', 'join_legal_address', 'join_kpp', 'join_comments'
        ];
        
        allFields.forEach(field => {
            const element = document.getElementById(field);
            if (element) element.required = false;
        });
        
        if (personType === 'individual') {
            const individualRequired = ['join_full_name_individual', 'join_phone', 'join_email', 'join_address'];
            individualRequired.forEach(field => {
                const element = document.getElementById(field);
                if (element) element.required = true;
            });
        } else if (personType === 'legal') {
            const legalRequired = ['join_full_name', 'join_phone_legal', 'join_email_legal', 
                                  'join_company_name', 'join_inn', 'join_legal_address'];
            legalRequired.forEach(field => {
                const element = document.getElementById(field);
                if (element) element.required = true;
            });
        }
    }

    // تفعيل النقر على خيارات النوع
    if (joinPersonTypeOptions.length > 0) {
        joinPersonTypeOptions.forEach(option => {
            option.addEventListener('click', function() {
                const selectedType = this.getAttribute('data-type');
                
                joinPersonTypeOptions.forEach(opt => {
                    opt.classList.remove('active');
                });
                
                this.classList.add('active');
                
                if (joinPersonTypeInput) joinPersonTypeInput.value = selectedType;
                
                if (selectedType === 'legal') {
                    if (joinIndividualFields) joinIndividualFields.style.display = 'none';
                    if (joinLegalFields) joinLegalFields.style.display = 'block';
                } else {
                    if (joinIndividualFields) joinIndividualFields.style.display = 'block';
                    if (joinLegalFields) joinLegalFields.style.display = 'none';
                }
                
                manageJoinRequiredFields(selectedType);
            });
        });
    }

    // فتح نافذة الانضمام
    if (openJoinBtn) {
        openJoinBtn.addEventListener('click', function() {
            if (joinModal) {
                joinModal.style.display = 'block';
                document.body.style.overflow = 'hidden';
                initializeJoinPersonType();
                joinForm.reset();
                if (joinSuccessMessage) joinSuccessMessage.style.display = 'none';
                if (joinErrorMessage) joinErrorMessage.style.display = 'none';
                
                // تمرير معرف المشروع إلى النموذج
                const projectId = this.getAttribute('data-project-id');
                if (projectId) {
                    const projectIdInput = document.getElementById('projectId');
                    if (projectIdInput) {
                        projectIdInput.value = projectId;
                    }
                }
            }
        });
    }

    // إغلاق نافذة الانضمام
    if (closeJoinModalBtn) {
        closeJoinModalBtn.addEventListener('click', closeJoinModal);
    }

    if (joinModal) {
        joinModal.addEventListener('click', function(e) {
            if (e.target === joinModal) {
                closeJoinModal();
            }
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && joinModal && joinModal.style.display === 'block') {
            closeJoinModal();
        }
    });

    function closeJoinModal() {
        if (joinModal) {
            joinModal.style.display = 'none';
            document.body.style.overflow = 'auto';
            joinForm.reset();
            initializeJoinPersonType();
        }
    }

    // إظهار/إخفاء تحميل زر الإرسال
    function showJoinLoading() {
        if (submitJoinBtn) submitJoinBtn.disabled = true;
        if (joinSubmitText) joinSubmitText.style.display = 'none';
        if (joinLoadingSpinner) joinLoadingSpinner.style.display = 'block';
    }

    function hideJoinLoading() {
        if (submitJoinBtn) submitJoinBtn.disabled = false;
        if (joinSubmitText) joinSubmitText.style.display = 'inline';
        if (joinLoadingSpinner) joinLoadingSpinner.style.display = 'none';
    }

    // إغلاق نافذة النجاح
    function closeJoinSuccessModal() {
        if (joinSuccessModal) {
            joinSuccessModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    if (closeJoinSuccessModalBtn) {
        closeJoinSuccessModalBtn.addEventListener('click', closeJoinSuccessModal);
    }

    if (closeJoinSuccessBtn) {
        closeJoinSuccessBtn.addEventListener('click', closeJoinSuccessModal);
    }

    if (joinSuccessModal) {
        joinSuccessModal.addEventListener('click', function(e) {
            if (e.target === joinSuccessModal) {
                closeJoinSuccessModal();
            }
        });
    }

    // دوال التحقق من الصحة
    function validateJoinEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }

    function validateJoinPhone(phone) {
        const phoneRegex = /^\+7\d{10}$/;
        return phoneRegex.test(phone);
    }

    function validateJoinINN(inn) {
        const innRegex = /^\d{10}|\d{12}$/;
        return innRegex.test(inn);
    }

    function validateJoinKPP(kpp) {
        const kppRegex = /^\d{9}$/;
        return kppRegex.test(kpp);
    }

    // معالجة إرسال نموذج الانضمام
    if (joinForm) {
        joinForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // التحقق من خانة الموافقة
            const agreementCheckbox = document.getElementById('join_agreement');
            if (!agreementCheckbox.checked) {
                if (joinErrorMessage) {
                    joinErrorMessage.textContent = 'Пожалуйста, согласитесь с условиями пользовательского соглашения и политикой конфиденциальности';
                    joinErrorMessage.style.display = 'block';
                    joinErrorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return;
            }
            
            const personType = joinPersonTypeInput ? joinPersonTypeInput.value : 'individual';
            
            let email, phone, inn, kpp;
            
            if (personType === 'individual') {
                email = document.getElementById('join_email').value.trim();
                phone = document.getElementById('join_phone').value.trim();
                
                if (!validateJoinEmail(email)) {
                    if (joinErrorMessage) {
                        joinErrorMessage.textContent = 'Пожалуйста, введите корректный email адрес. Пример: example@domain.com';
                        joinErrorMessage.style.display = 'block';
                        joinErrorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
                if (!validateJoinPhone(phone)) {
                    if (joinErrorMessage) {
                        joinErrorMessage.textContent = 'Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX (11 цифр). Пример: +79123456789';
                        joinErrorMessage.style.display = 'block';
                        joinErrorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
            } else {
                email = document.getElementById('join_email_legal').value.trim();
                phone = document.getElementById('join_phone_legal').value.trim();
                inn = document.getElementById('join_inn').value.trim();
                kpp = document.getElementById('join_kpp').value.trim();
                
                if (!validateJoinEmail(email)) {
                    if (joinErrorMessage) {
                        joinErrorMessage.textContent = 'Пожалуйста, введите корректный email адрес. Пример: example@domain.com';
                        joinErrorMessage.style.display = 'block';
                        joinErrorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
                if (!validateJoinPhone(phone)) {
                    if (joinErrorMessage) {
                        joinErrorMessage.textContent = 'Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX (11 цифр). Пример: +79123456789';
                        joinErrorMessage.style.display = 'block';
                        joinErrorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
                if (!validateJoinINN(inn)) {
                    if (joinErrorMessage) {
                        joinErrorMessage.textContent = 'Пожалуйста, введите корректный ИНН (10 или 12 цифр).';
                        joinErrorMessage.style.display = 'block';
                        joinErrorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
                if (kpp && !validateJoinKPP(kpp)) {
                    if (joinErrorMessage) {
                        joinErrorMessage.textContent = 'Пожалуйста, введите корректный КПП (9 цифр).';
                        joinErrorMessage.style.display = 'block';
                        joinErrorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
            }
            
            showJoinLoading();
            if (joinSuccessMessage) joinSuccessMessage.style.display = 'none';
            if (joinErrorMessage) joinErrorMessage.style.display = 'none';
            
            const formData = new FormData(joinForm);
            
            fetch(window.location.origin + "/projects/join-request/", {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('#joinForm [name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    closeJoinModal();
                    
                    if (joinSuccessMessageContent && joinRequestIdValue) {
                        joinSuccessMessageContent.textContent = data.message;
                        joinRequestIdValue.textContent = data.request_id || 'Не указан';
                        joinSuccessModal.style.display = 'block';
                        document.body.style.overflow = 'hidden';
                    }
                } else {
                    if (joinErrorMessage) {
                        joinErrorMessage.textContent = data.message;
                        joinErrorMessage.style.display = 'block';
                        joinErrorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (joinErrorMessage) {
                    joinErrorMessage.textContent = 'Произошла ошибка при отправке. Пожалуйста, попробуйте еще раз.';
                    joinErrorMessage.style.display = 'block';
                }
            })
            .finally(() => {
                hideJoinLoading();
            });
        });
    }

    // تهيئة عند تحميل الصفحة
    initializeJoinPersonType();
});