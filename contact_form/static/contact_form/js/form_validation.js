/**
 * التحقق من النموذج ومنع التكرار - للإصدار الرئيسي
 */
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('.contact-form');
    if (!contactForm) return;

    initFormValidation(contactForm);
});

/**
 * تهيئة التحقق من النموذج
 */
function initFormValidation(form) {
    let isSubmitting = false;
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton ? submitButton.innerHTML : '';

    // منع الإرسال المزدوج
    form.addEventListener('submit', function(e) {
        if (isSubmitting) {
            e.preventDefault();
            return;
        }

        // التحقق الأساسي قبل الإرسال
        const emailField = form.querySelector('input[type="email"]');
        const messageField = form.querySelector('textarea');
        const robotCheckbox = form.querySelector('input[type="checkbox"][name*="robot"]');
        
        let isValid = true;
        
        if (emailField && !isValidEmail(emailField.value)) {
            e.preventDefault();
            showFormError(emailField, 'Пожалуйста, введите корректный адрес электронной почты.');
            isValid = false;
        }
        
        if (messageField && messageField.value.trim().length < 10) {
            e.preventDefault();
            showFormError(messageField, 'Сообщение слишком короткое. Минимальная длина - 10 символов.');
            isValid = false;
        }
        
        if (robotCheckbox && !robotCheckbox.checked) {
            e.preventDefault();
            showFormError(robotCheckbox, 'Пожалуйста, подтвердите, что вы не робот.');
            isValid = false;
        }

        if (!isValid) return;

        // تعطيل الزر أثناء الإرسال
        if (submitButton) {
            isSubmitting = true;
            submitButton.disabled = true;
            submitButton.innerHTML = '<span>Отправка...</span>';
            submitButton.style.opacity = '0.7';
        }
    });

    // التحقق من البريد الإلكتروني أثناء الكتابة
    const emailInput = form.querySelector('input[type="email"]');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            if (this.value && !isValidEmail(this.value)) {
                showFormError(this, 'Пожалуйста, введите корректный адрес электронной почты.');
            } else {
                clearFormError(this);
            }
        });
    }

    // إعادة تمكين الزر إذا كان هناك خطأ في الإرسال
    form.addEventListener('formdata', function() {
        setTimeout(function() {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
                submitButton.style.opacity = '1';
            }
        }, 3000);
    });
}

/**
 * التحقق من صحة البريد الإلكتروني
 */
function isValidEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
}

/**
 * عرض خطأ في النموذج
 */
function showFormError(element, message) {
    // إزالة أي رسالة خطأ سابقة
    clearFormError(element);
    
    // إنشاء عنصر الخطأ
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error-message';
    errorElement.style.color = '#7F1726';
    errorElement.style.fontSize = '0.8rem';
    errorElement.style.marginTop = '0.3rem';
    errorElement.style.fontFamily = "'Raleway', sans-serif";
    errorElement.textContent = message;
    
    // إضافة الحد الأحمر للحقل
    element.style.borderColor = '#7F1726';
    element.style.backgroundColor = 'rgba(127, 23, 38, 0.05)';
    
    // إضافة رسالة الخطأ بعد الحقل
    element.parentNode.appendChild(errorElement);
}

/**
 * مسح خطأ النموذج
 */
function clearFormError(element) {
    // إزالة رسالة الخطأ
    const existingError = element.parentNode.querySelector('.form-error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // إعادة الألوان الطبيعية
    element.style.borderColor = '';
    element.style.backgroundColor = '';
}

/**
 * منع الإرسال المتكرر باستخدام sessionStorage
 */
(function() {
    const FORM_COOLDOWN = 5 * 60 * 1000; // 5 دقائق بالمللي ثانية
    const STORAGE_KEY = 'last_form_submission';

    document.addEventListener('submit', function(e) {
        const form = e.target;
        if (!form.classList.contains('contact-form') && !form.id !== 'contactForm') return;

        const lastSubmission = sessionStorage.getItem(STORAGE_KEY);
        const now = Date.now();

        if (lastSubmission && (now - parseInt(lastSubmission)) < FORM_COOLDOWN) {
            e.preventDefault();
            showCooldownMessage();
            return;
        }

        // حفظ وقت الإرسال
        sessionStorage.setItem(STORAGE_KEY, now.toString());
    });

    function showCooldownMessage() {
        // البحث عن عنصر لعرض الرسالة
        let messageContainer = document.querySelector('.contact-messages');
        if (!messageContainer) {
            messageContainer = document.createElement('div');
            messageContainer.className = 'contact-messages';
            document.querySelector('.standalone-contact-container').prepend(messageContainer);
        }
        
        // إنشاء رسالة التنبيه
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-warning';
        alertDiv.textContent = 'Пожалуйста, подождите 5 минут перед отправкой следующего сообщения. Это необходимо для предотвращения спама.';
        
        messageContainer.appendChild(alertDiv);
        
        // إزالة الرسالة بعد 5 ثوانٍ
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
})();