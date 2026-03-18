// =====================================================
// FILE: contact_form_partial.js (مع منع الإرسال المزدوج)
// =====================================================

let isAjaxSubmitInitialized = false;

/**
 * تهيئة وظائف نموذج الاتصال الجزئي مع دعم AJAX
 */
document.addEventListener('DOMContentLoaded', function() {
    initCharCounter();
    initCooldownTimer();
    initFormValidation();
    initAjaxSubmit(); // دالة إرسال النموذج عبر AJAX
});

/**
 * عداد الأحرف للرسالة
 */
function initCharCounter() {
    const messageTextarea = document.getElementById('id_message');
    const charCount = document.getElementById('char-count');
    
    if (messageTextarea && charCount) {
        messageTextarea.addEventListener('input', function() {
            charCount.textContent = this.value.length;
            
            // تغيير اللون عند الاقتراب من الحد
            if (this.value.length > 1800) {
                charCount.style.color = '#7F1726';
                charCount.style.fontWeight = 'bold';
            } else if (this.value.length > 1500) {
                charCount.style.color = '#ff9800';
                charCount.style.fontWeight = 'bold';
            } else {
                charCount.style.color = '#666';
                charCount.style.fontWeight = 'normal';
            }
        });
        
        // تهيئة العداد
        charCount.textContent = messageTextarea.value.length;
    }
}

/**
 * إدارة عد التنازلي لمنع التكرار
 */
function initCooldownTimer() {
    const cooldownMessage = document.getElementById('cooldownMessage');
    const cooldownTimer = document.getElementById('cooldownTimer');
    const submitButton = document.getElementById('submitButton');
    
    // التحقق مما إذا كان هناك وقت تبريد مخزن
    const lastSubmission = sessionStorage.getItem('last_form_submission');
    const now = Date.now();
    const COOLDOWN_TIME = 5 * 60 * 1000; // 5 دقائق
    
    if (lastSubmission && (now - parseInt(lastSubmission)) < COOLDOWN_TIME) {
        const timeLeft = COOLDOWN_TIME - (now - parseInt(lastSubmission));
        startCooldownTimer(Math.floor(timeLeft / 1000));
    }
}

/**
 * بدء عد التنازلي
 */
function startCooldownTimer(seconds) {
    const cooldownMessage = document.getElementById('cooldownMessage');
    const cooldownTimer = document.getElementById('cooldownTimer');
    const submitButton = document.getElementById('submitButton');
    
    if (cooldownMessage && cooldownTimer && submitButton) {
        submitButton.disabled = true;
        submitButton.style.opacity = '0.5';
        cooldownMessage.style.display = 'block';
        cooldownMessage.classList.add('active');
        
        let remainingSeconds = seconds;
        
        const timerInterval = setInterval(function() {
            const minutes = Math.floor(remainingSeconds / 60);
            const secs = remainingSeconds % 60;
            
            cooldownTimer.textContent = `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
            
            if (remainingSeconds <= 0) {
                clearInterval(timerInterval);
                submitButton.disabled = false;
                submitButton.style.opacity = '1';
                cooldownMessage.style.display = 'none';
                cooldownMessage.classList.remove('active');
                sessionStorage.removeItem('last_form_submission');
            }
            
            remainingSeconds--;
        }, 1000);
    }
}

/**
 * التحقق من صحة النموذج (للواجهة فقط)
 */
function initFormValidation() {
    const contactForm = document.getElementById('contactForm');
    if (!contactForm) return;

    const emailInput = document.getElementById('id_email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            validateEmail(this);
        });
        
        emailInput.addEventListener('input', function() {
            clearEmailError(this);
        });
    }

    const messageInput = document.getElementById('id_message');
    if (messageInput) {
        messageInput.addEventListener('input', function() {
            validateMessageLength(this);
        });
    }
}

/**
 * التحقق من صحة البريد الإلكتروني
 */
function validateEmail(emailInput) {
    const email = emailInput.value.trim();
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    if (email && !emailRegex.test(email)) {
        showInlineError(emailInput, 'Пожалуйста, введите корректный адрес электронной почты.');
        return false;
    }
    
    clearInlineError(emailInput);
    return true;
}

/**
 * التحقق من طول الرسالة
 */
function validateMessageLength(messageInput) {
    const message = messageInput.value.trim();
    
    if (message.length > 0 && message.length < 10) {
        showInlineError(messageInput, `Минимальная длина: 10 символов (сейчас: ${message.length})`);
        return false;
    }
    
    clearInlineError(messageInput);
    return true;
}

/**
 * عرض خطأ أسفل الحقل
 */
function showInlineError(element, message) {
    clearInlineError(element);
    
    const errorElement = document.createElement('div');
    errorElement.className = 'inline-error-message';
    errorElement.style.color = '#7F1726';
    errorElement.style.fontSize = '0.65rem';
    errorElement.style.marginTop = '0.2rem';
    errorElement.style.marginLeft = '0.5rem';
    errorElement.style.fontFamily = "'Raleway', sans-serif";
    errorElement.textContent = message;
    
    element.style.borderColor = '#7F1726';
    element.style.backgroundColor = 'rgba(127, 23, 38, 0.05)';
    
    element.parentNode.appendChild(errorElement);
}

/**
 * مسح رسالة الخطأ
 */
function clearInlineError(element) {
    const existingError = element.parentNode.querySelector('.inline-error-message');
    if (existingError) {
        existingError.remove();
    }
    
    element.style.borderColor = '#052946';
    element.style.backgroundColor = '';
}

/**
 * مسح خطأ البريد الإلكتروني
 */
function clearEmailError(emailInput) {
    const email = emailInput.value.trim();
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    if (email && emailRegex.test(email)) {
        clearInlineError(emailInput);
    }
}

/**
 * إرسال النموذج عبر AJAX (بدون إعادة تحميل الصفحة)
 */
function initAjaxSubmit() {
    const contactForm = document.getElementById('contactForm');
    if (!contactForm || isAjaxSubmitInitialized) return;

    isAjaxSubmitInitialized = true;
    contactForm.removeEventListener('submit', handleFormSubmit);
    contactForm.addEventListener('submit', handleFormSubmit);
}

async function handleFormSubmit(e) {
    e.preventDefault();

    const nameInput = document.getElementById('id_name');
    const emailInput = document.getElementById('id_email');
    const messageInput = document.getElementById('id_message');
    const robotCheckbox = document.getElementById('id_is_robot');

    let isValid = true;

    if (nameInput && nameInput.value.trim().length < 2) {
        showInlineError(nameInput, 'Имя должно содержать не менее 2 символов.');
        isValid = false;
    }
    if (emailInput && !validateEmail(emailInput)) {
        isValid = false;
    }
    if (messageInput && messageInput.value.trim().length < 10) {
        showInlineError(messageInput, 'Сообщение слишком короткое. Минимальная длина - 10 символов.');
        isValid = false;
    }
    if (robotCheckbox && !robotCheckbox.checked) {
        showInlineError(robotCheckbox, 'Пожалуйста, подтвердите, что вы не робот.');
        isValid = false;
    }

    if (!isValid) return;

    const submitButton = document.getElementById('submitButton');
    if (submitButton) {
        if (submitButton.disabled) return;
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="submit-text-small">Отправка...</span>';
        submitButton.style.opacity = '0.7';
    }

    const formData = new FormData(contactForm);

    try {
        const response = await fetch(contactForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const html = await response.text();

        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        const newSection = tempDiv.querySelector('#contact-form-section');
        const oldSection = document.getElementById('contact-form-section');

        if (newSection && oldSection) {
            oldSection.innerHTML = newSection.innerHTML;

            const newForm = oldSection.querySelector('#contactForm');
            if (newForm) {
                // إعادة تعيين العلم للسماح بربط الحدث في النموذج الجديد
                isAjaxSubmitInitialized = false;
                initCharCounter();
                initCooldownTimer();
                initFormValidation();
                initAjaxSubmit();
            } else {
                console.log('Форма успешно отправлена!');
            }
        }

    } catch (error) {
        console.error('Error submitting form:', error);
        alert('Произошла ошибка при отправке. Пожалуйста, попробуйте еще раз.');
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML = '<span class="submit-text-small">Отправить</span><div class="submit-arrow-small">...</div>';
            submitButton.style.opacity = '1';
        }
    }
}

// إضافة الوظائف إلى النطاق العام
window.initContactFormPartial = function() {
    initCharCounter();
    initCooldownTimer();
    initFormValidation();
    initAjaxSubmit();
};

// تهيئة تلقائية عند تحميل الصفحة
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initContactFormPartial);
} else {
    initContactFormPartial();
}