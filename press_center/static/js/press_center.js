// ==================== press_center/static/js/press_center.js ====================
// النسخة النهائية مع تحسينات الكاروسيل وإصلاحات responsive ودعم السحب باللمس

document.addEventListener('DOMContentLoaded', function() {
    // عناصر النوافذ
    const applicationModal = document.getElementById('applicationModal');
    const successModal = document.getElementById('successModal');
    const unauthModal = document.getElementById('unauthModal');
    
    // الأزرار
    const redApplicationBtn = document.getElementById('redApplicationBtn');
    const blueApplicationBtn = document.getElementById('blueApplicationBtn');
    const pressHeaderApplicationBtn = document.getElementById('pressHeaderApplicationBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const closeUnauthModalBtn = document.getElementById('closeUnauthModalBtn');
    const submitApplicationBtn = document.getElementById('submitApplicationBtn');
    const successCloseBtn = document.getElementById('successCloseBtn');
    const agreementCheckbox = document.getElementById('agreementCheckbox');

    // دالة مساعدة لفتح نافذة الطلب (إذا كان المستخدم مسجلاً) أو نافذة غير المسجلين
    function openApplicationModal() {
        if (typeof isAuthenticated !== 'undefined' && isAuthenticated) {
            if (applicationModal) {
                applicationModal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            }
        } else {
            if (unauthModal) {
                unauthModal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            } else {
                // إذا لم توجد نافذة غير المسجلين، توجيه المستخدم إلى صفحة تسجيل الدخول
                window.location.href = '/login/';
            }
        }
    }

    // ربط الأزرار الموجودة
    if (redApplicationBtn) {
        redApplicationBtn.addEventListener('click', openApplicationModal);
    }
    if (blueApplicationBtn) {
        blueApplicationBtn.addEventListener('click', openApplicationModal);
    }
    if (pressHeaderApplicationBtn) {
        pressHeaderApplicationBtn.addEventListener('click', openApplicationModal);
    }

    // إغلاق نافذة غير المسجلين
    if (closeUnauthModalBtn) {
        closeUnauthModalBtn.addEventListener('click', function() {
            unauthModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
    }
    if (unauthModal) {
        unauthModal.addEventListener('click', function(e) {
            if (e.target === unauthModal) {
                unauthModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }

    // إغلاق نافذة الطلب
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            applicationModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
    }
    if (applicationModal) {
        applicationModal.addEventListener('click', function(e) {
            if (e.target === applicationModal) {
                applicationModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }

    // إغلاق نافذة النجاح
    if (successCloseBtn) {
        successCloseBtn.addEventListener('click', function() {
            successModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
    }
    if (successModal) {
        successModal.addEventListener('click', function(e) {
            if (e.target === successModal) {
                successModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }

    // إرسال النموذج
    if (submitApplicationBtn) {
        submitApplicationBtn.addEventListener('click', function() {
            if (!validateForm()) return;

            const formData = {
                organization: document.getElementById('organization').value,
                theme: document.getElementById('theme').value,
                desired_dates: document.getElementById('dates').value,
                contact_person: document.getElementById('contact').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                additional_wishes: document.getElementById('wishes').value
            };

            fetch('/press-center/submit-request/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    applicationModal.style.display = 'none';
                    if (data.request_number) {
                        document.getElementById('requestNumberValue').textContent = data.request_number;
                        document.getElementById('requestNumberSection').style.display = 'block';
                    } else {
                        document.getElementById('requestNumberSection').style.display = 'none';
                    }
                    successModal.style.display = 'flex';
                    resetForm();
                } else {
                    alert('Ошибка: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при отправке заявки');
            });
        });
    }

    // التحقق من صحة النموذج
    function validateForm() {
        const organization = document.getElementById('organization').value;
        const theme = document.getElementById('theme').value;
        const dates = document.getElementById('dates').value;
        const contact = document.getElementById('contact').value;
        const phone = document.getElementById('phone').value;
        const email = document.getElementById('email').value;

        if (!organization || !theme || !dates || !contact || !phone || !email) {
            alert('Пожалуйста, заполните все обязательные поля');
            return false;
        }
        if (!agreementCheckbox.checked) {
            alert('Пожалуйста, согласитесь с условиями пользовательского соглашения и политикой конфиденциальности');
            return false;
        }
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('Пожалуйста, введите корректный адрес электронной почты');
            return false;
        }
        return true;
    }

    // إعادة تعيين النموذج
    function resetForm() {
        document.getElementById('organization').value = '';
        document.getElementById('theme').value = '';
        document.getElementById('dates').value = '';
        document.getElementById('contact').value = '';
        document.getElementById('phone').value = '';
        document.getElementById('email').value = '';
        document.getElementById('wishes').value = '';
        document.getElementById('agreementCheckbox').checked = false;

        const fields = document.querySelectorAll('.form-field');
        fields.forEach(field => {
            field.nextElementSibling.style.top = '50%';
            field.nextElementSibling.style.fontSize = getComputedStyle(field).fontSize;
            field.nextElementSibling.style.color = 'rgba(5, 41, 70, 0.54)';
            field.nextElementSibling.style.background = 'transparent';
        });
    }

    // تفعيل التبويبات
    function initTabs() {
        const tabButtons = document.querySelectorAll('.program-tab-btn');
        const tabPanes = document.querySelectorAll('.program-tab-pane');

        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');
                tabButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                tabPanes.forEach(pane => pane.classList.remove('active'));
                const activePane = document.getElementById(tabId);
                if (activePane) activePane.classList.add('active');
            });
        });
    }
    initTabs();

    // تحريك التسميات عند التركيز على الحقول
    const fields = document.querySelectorAll('.form-field');
    fields.forEach(field => {
        if (field.value) {
            field.nextElementSibling.style.top = '0';
            field.nextElementSibling.style.fontSize = '10px';
            field.nextElementSibling.style.color = '#052946';
            field.nextElementSibling.style.background = 'white';
        }
        field.addEventListener('focus', function() {
            this.nextElementSibling.style.top = '0';
            this.nextElementSibling.style.fontSize = '10px';
            this.nextElementSibling.style.color = '#052946';
            this.nextElementSibling.style.background = 'white';
        });
        field.addEventListener('blur', function() {
            if (!this.value) {
                this.nextElementSibling.style.top = '50%';
                this.nextElementSibling.style.fontSize = getComputedStyle(this).fontSize;
                this.nextElementSibling.style.color = 'rgba(5, 41, 70, 0.54)';
                this.nextElementSibling.style.background = 'transparent';
            }
        });
    });

    // ========== الكاروسيل المحسّن مع دعم السحب (الماوس واللمس) ==========
    const track = document.getElementById('pressCarouselTrack');
    const prevBtn = document.getElementById('pressCarouselPrev');
    const nextBtn = document.getElementById('pressCarouselNext');
    const slides = document.querySelectorAll('.press-carousel-slide');

    if (slides.length > 0 && track && prevBtn && nextBtn) {
        let currentPosition = 0;
        let slideWidth = slides[0].offsetWidth + 20; // 20px gap
        let visibleSlides = getVisibleSlidesCount();
        let maxPosition = calculateMaxPosition();

        function getVisibleSlidesCount() {
            if (window.innerWidth <= 576) return 1;
            if (window.innerWidth <= 992) return 2;
            return 3;
        }

        function calculateMaxPosition() {
            return -(slideWidth * (slides.length - visibleSlides));
        }

        function updateCarouselButtons() {
            prevBtn.disabled = currentPosition >= 0;
            nextBtn.disabled = currentPosition <= maxPosition;
            prevBtn.style.opacity = currentPosition >= 0 ? '0.5' : '1';
            nextBtn.style.opacity = currentPosition <= maxPosition ? '0.5' : '1';
        }

        function updateCarousel(animate = true) {
            track.style.transition = animate ? 'transform 0.5s ease' : 'none';
            track.style.transform = `translateX(${currentPosition}px)`;
            updateCarouselButtons();
        }

        // أحداث السحب (الماوس)
        let isDragging = false;
        let startX = 0;
        let startY = 0;
        let startPosition = 0;

        track.addEventListener('mousedown', (e) => {
            e.preventDefault();
            isDragging = true;
            startX = e.pageX - track.offsetLeft;
            startY = e.pageY;
            startPosition = currentPosition;
            track.style.transition = 'none';
            track.style.cursor = 'grabbing';
        });

        track.addEventListener('touchstart', (e) => {
            e.preventDefault();
            isDragging = true;
            startX = e.touches[0].pageX - track.offsetLeft;
            startY = e.touches[0].pageY;
            startPosition = currentPosition;
            track.style.transition = 'none';
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const x = e.pageX - track.offsetLeft;
            const diff = x - startX;
            let newPos = startPosition + diff;
            if (newPos > 0) newPos = 0;
            if (newPos < maxPosition) newPos = maxPosition;
            track.style.transform = `translateX(${newPos}px)`;
        });

        window.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const x = e.touches[0].pageX - track.offsetLeft;
            const diff = x - startX;
            let newPos = startPosition + diff;
            if (newPos > 0) newPos = 0;
            if (newPos < maxPosition) newPos = maxPosition;
            track.style.transform = `translateX(${newPos}px)`;
        });

        window.addEventListener('mouseup', () => {
            if (!isDragging) return;
            isDragging = false;
            track.style.cursor = 'default';
            // التقريب إلى أقرب شريحة بعد السحب
            const transformMatrix = getComputedStyle(track).transform;
            if (transformMatrix !== 'none') {
                const matrixValues = transformMatrix.match(/matrix.*\((.+)\)/);
                if (matrixValues) {
                    const x = parseFloat(matrixValues[1].split(', ')[4]);
                    currentPosition = Math.round(x / slideWidth) * slideWidth;
                    if (currentPosition > 0) currentPosition = 0;
                    if (currentPosition < maxPosition) currentPosition = maxPosition;
                }
            }
            updateCarousel();
        });

        window.addEventListener('touchend', () => {
            if (!isDragging) return;
            isDragging = false;
            const transformMatrix = getComputedStyle(track).transform;
            if (transformMatrix !== 'none') {
                const matrixValues = transformMatrix.match(/matrix.*\((.+)\)/);
                if (matrixValues) {
                    const x = parseFloat(matrixValues[1].split(', ')[4]);
                    currentPosition = Math.round(x / slideWidth) * slideWidth;
                    if (currentPosition > 0) currentPosition = 0;
                    if (currentPosition < maxPosition) currentPosition = maxPosition;
                }
            }
            updateCarousel();
        });

        // منع السحب عند الخروج من العنصر
        track.addEventListener('mouseleave', () => {
            if (isDragging) {
                isDragging = false;
                track.style.cursor = 'default';
                updateCarousel();
            }
        });

        // تحديث القيم عند تغيير حجم النافذة
        window.addEventListener('resize', function() {
            visibleSlides = getVisibleSlidesCount();
            slideWidth = slides[0].offsetWidth + 20;
            maxPosition = calculateMaxPosition();
            
            if (currentPosition < maxPosition) currentPosition = maxPosition;
            if (currentPosition > 0) currentPosition = 0;
            
            updateCarousel(false);
        });

        // أزرار التنقل
        nextBtn.addEventListener('click', function() {
            if (currentPosition > maxPosition) {
                currentPosition -= slideWidth;
                if (currentPosition < maxPosition) currentPosition = maxPosition;
                updateCarousel();
            }
        });

        prevBtn.addEventListener('click', function() {
            if (currentPosition < 0) {
                currentPosition += slideWidth;
                if (currentPosition > 0) currentPosition = 0;
                updateCarousel();
            }
        });

        // تهيئة أولية
        updateCarousel();
    }

    // الحصول على CSRF token
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
});