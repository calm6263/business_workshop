document.addEventListener('DOMContentLoaded', function() {
    // تهيئة السلايدر
    const myCarousel = document.querySelector('#projectCarousel');
    if (myCarousel) {
        const carousel = new bootstrap.Carousel(myCarousel, {
            interval: 5000,
            wrap: true
        });
    }

    // تفعيل تأثيرات الفلاتر الجديدة
    const categoryTags = document.querySelectorAll('.category-tag');
    
    categoryTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 4px 8px rgba(5, 41, 70, 0.1)';
            }
        });
        
        tag.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            }
        });
        
        tag.addEventListener('click', function(e) {
            e.preventDefault();
            
            categoryTags.forEach(t => {
                t.classList.remove('active');
                t.style.transform = 'translateY(0)';
                t.style.boxShadow = 'none';
            });
            
            this.classList.add('active');
            
            const href = this.getAttribute('href');
            if (href && href !== '#') {
                window.location.href = href;
            }
        });
    });

    // التحكم في إظهار/إخفاء الفلاتر الإضافية
    const filtersToggle = document.getElementById('toggleFilters');
    const filtersContainer = document.getElementById('filtersContainer');
    const toggleText = document.getElementById('toggleText');
    const filtersCountSpan = document.getElementById('filtersCount');
    const extraFilters = document.querySelectorAll('.extra-filter');

    if (filtersToggle && filtersContainer && toggleText && filtersCountSpan) {
        const totalFilters = document.querySelectorAll('.filter-item').length;
        const extraCount = extraFilters.length;

        toggleText.textContent = `Показать все (${extraCount})`;
        filtersCountSpan.textContent = `Фильтры (${totalFilters})`;

        filtersToggle.addEventListener('click', function() {
            const isExpanded = filtersContainer.classList.contains('expanded');
            
            if (isExpanded) {
                filtersContainer.classList.remove('expanded');
                toggleText.textContent = `Показать все (${extraCount})`;
            } else {
                filtersContainer.classList.add('expanded');
                toggleText.textContent = 'Скрыть';
            }
        });
    }

    // ===========================================
    // التحكم في اختيار نوع الشخص في النافذة المنبثقة
    // ===========================================
    const personTypeOptions = document.querySelectorAll('.person-type-option');
    const legalFieldsSection = document.getElementById('legalFields');
    const individualFieldsSection = document.getElementById('individualFields');
    const personTypeInput = document.getElementById('personType');

    function initializePersonType() {
        personTypeOptions.forEach(opt => {
            if (opt.getAttribute('data-type') === 'individual') {
                opt.classList.add('active');
            } else {
                opt.classList.remove('active');
            }
        });
        
        if (individualFieldsSection) individualFieldsSection.style.display = 'block';
        if (legalFieldsSection) legalFieldsSection.style.display = 'none';
        if (personTypeInput) personTypeInput.value = 'individual';
        manageRequiredFields('individual');
    }

    function manageRequiredFields(personType) {
        const allFields = [
            'full_name_individual', 'phone', 'email', 'address', 'comments_individual',
            'full_name', 'phone_legal', 'email_legal', 'company_name', 
            'inn', 'legal_address', 'kpp', 'comments'
        ];
        
        allFields.forEach(field => {
            const element = document.getElementById(field);
            if (element) element.required = false;
        });
        
        if (personType === 'individual') {
            const individualRequired = ['full_name_individual', 'phone', 'email']; // address not required
            individualRequired.forEach(field => {
                const element = document.getElementById(field);
                if (element) element.required = true;
            });
        } else if (personType === 'legal') {
            const legalRequired = ['full_name', 'phone_legal', 'email_legal', 
                                  'company_name', 'inn', 'legal_address'];
            legalRequired.forEach(field => {
                const element = document.getElementById(field);
                if (element) element.required = true;
            });
        }
    }

    if (personTypeOptions.length > 0) {
        personTypeOptions.forEach(option => {
            option.addEventListener('click', function() {
                const selectedType = this.getAttribute('data-type');
                
                personTypeOptions.forEach(opt => opt.classList.remove('active'));
                this.classList.add('active');
                if (personTypeInput) personTypeInput.value = selectedType;
                
                if (selectedType === 'legal') {
                    if (individualFieldsSection) individualFieldsSection.style.display = 'none';
                    if (legalFieldsSection) legalFieldsSection.style.display = 'block';
                } else {
                    if (individualFieldsSection) individualFieldsSection.style.display = 'block';
                    if (legalFieldsSection) legalFieldsSection.style.display = 'none';
                }
                
                manageRequiredFields(selectedType);
            });
        });
    }

    initializePersonType();

    // دوال التحقق من صحة البيانات
    function validateEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }

    function validatePhone(phone) {
        const phoneRegex = /^\+7\d{10}$/;
        return phoneRegex.test(phone);
    }

    function validateINN(inn) {
        const innRegex = /^\d{10}|\d{12}$/;
        return innRegex.test(inn);
    }

    function validateKPP(kpp) {
        const kppRegex = /^\d{9}$/;
        return kppRegex.test(kpp);
    }

    // دالة لتمييز الحقول الفارغة
    function highlightEmptyFields() {
        let hasEmpty = false;
        const requiredFields = document.querySelectorAll('#proposalForm [required]');
        
        requiredFields.forEach(field => {
            const container = field.closest('.input-container');
    
            // ✅ إصلاح الانهيار
            if (!container) return;
    
            if (!field.value.trim()) {
                container.classList.add('error');
                container.classList.remove('valid');
                hasEmpty = true;
            } else {
                container.classList.remove('error');
                container.classList.add('valid');
            }
        });
        
        return hasEmpty;
    }

    // إدارة نافذة اقتراح المشروع
    const modal = document.getElementById('proposalModal');
    const openBtn = document.getElementById('openProposalModal');
    const closeBtn = document.getElementById('closeModal');
    const form = document.getElementById('proposalForm');
    const submitBtn = document.getElementById('submitProposal');
    const submitText = document.getElementById('submitText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');

    if (openBtn) {
        openBtn.addEventListener('click', function() {
            if (modal) {
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
                initializePersonType();
            }
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
    
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && modal.style.display === 'block') {
            closeModal();
        }
    });

    function closeModal() {
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            resetForm();
        }
    }

    function resetForm() {
        if (form) {
            form.reset();
            if (successMessage) successMessage.style.display = 'none';
            if (errorMessage) errorMessage.style.display = 'none';
            if (submitBtn) submitBtn.disabled = false;
            if (submitText) submitText.style.display = 'inline';
            if (loadingSpinner) loadingSpinner.style.display = 'none';
            initializePersonType();
            
            // إزالة كل علامات الخطأ والتحقق
            document.querySelectorAll('.input-container').forEach(container => {
                container.classList.remove('error', 'valid');
            });
        }
    }

    function showLoading() {
        if (submitBtn) submitBtn.disabled = true;
        if (submitText) submitText.style.display = 'none';
        if (loadingSpinner) loadingSpinner.style.display = 'block';
    }

    function hideLoading() {
        if (submitBtn) submitBtn.disabled = false;
        if (submitText) submitText.style.display = 'inline';
        if (loadingSpinner) loadingSpinner.style.display = 'none';
    }

    // إرسال النموذج
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // التحقق من الموافقة على الشروط
            const agreementCheckbox = document.getElementById('agreement');
            if (!agreementCheckbox.checked) {
                if (errorMessage) {
                    errorMessage.textContent = 'Пожалуйста, согласитесь с условиями пользовательского соглашения и политикой конфиденциальности';
                    errorMessage.style.display = 'block';
                    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return;
            }
            
            // التحقق من الحقول الفارغة
            if (highlightEmptyFields()) {
                if (errorMessage) {
                    errorMessage.textContent = 'Пожалуйста, заполните все обязательные поля.';
                    errorMessage.style.display = 'block';
                    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return;
            }
            
            const personType = personTypeInput ? personTypeInput.value : 'individual';
            
            let email, phone, inn, kpp, companyName;
            
            if (personType === 'individual') {
                email = document.getElementById('email').value.trim();
                phone = document.getElementById('phone').value.trim();
                
                if (!validateEmail(email)) {
                    if (errorMessage) {
                        errorMessage.textContent = 'Пожалуйста, введите корректный email адрес. Пример: example@domain.com';
                        errorMessage.style.display = 'block';
                        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
                if (!validatePhone(phone)) {
                    if (errorMessage) {
                        errorMessage.textContent = 'Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX (11 цифр). Пример: +79123456789';
                        errorMessage.style.display = 'block';
                        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
            } else {
                email = document.getElementById('email_legal').value.trim();
                phone = document.getElementById('phone_legal').value.trim();
                inn = document.getElementById('inn').value.trim();
                kpp = document.getElementById('kpp').value.trim();
                companyName = document.getElementById('company_name').value.trim();
                
                if (!validateEmail(email)) {
                    if (errorMessage) {
                        errorMessage.textContent = 'Пожалуйста, введите корректный email адрес. Пример: example@domain.com';
                        errorMessage.style.display = 'block';
                        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
                if (!validatePhone(phone)) {
                    if (errorMessage) {
                        errorMessage.textContent = 'Пожалуйста, введите корректный номер телефона в формате +7XXXXXXXXXX (11 цифр). Пример: +79123456789';
                        errorMessage.style.display = 'block';
                        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
                if (!validateINN(inn)) {
                    if (errorMessage) {
                        errorMessage.textContent = 'Пожалуйста, введите корректный ИНН (10 или 12 цифр).';
                        errorMessage.style.display = 'block';
                        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
                
                if (kpp && !validateKPP(kpp)) {
                    if (errorMessage) {
                        errorMessage.textContent = 'Пожалуйста, введите корректный КПП (9 цифр).';
                        errorMessage.style.display = 'block';
                        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    return;
                }
            }
            
            showLoading();
            if (successMessage) successMessage.style.display = 'none';
            if (errorMessage) errorMessage.style.display = 'none';

            const formData = new FormData(form);
            formData.append('person_type', personType);
            
            if (personType === 'individual') {
                formData.append('title', 'Предложение проекта от физического лица');
                formData.append('description', `ФИО: ${document.getElementById('full_name_individual').value}\nТелефон: ${phone}\nEmail: ${email}\nАдрес: ${document.getElementById('address').value}\nКомментарии: ${document.getElementById('comments_individual').value}`);
            } else {
                formData.append('title', 'Предложение проекта от юридического лица');
                formData.append('description', `Ответственное лицо: ${document.getElementById('full_name').value}\nТелефон: ${phone}\nEmail: ${email}\nКомпания: ${companyName}\nИНН: ${inn}\nКПП: ${kpp}\nЮридический адрес: ${document.getElementById('legal_address').value}\nКомментарии: ${document.getElementById('comments').value}`);
            }

            fetch("/projects/submit-proposal/", {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    closeModal();
                    showSuccessModal(data.message, data.proposal_id);
                } else {
                    if (errorMessage) {
                        errorMessage.textContent = data.message;
                        errorMessage.style.display = 'block';
                        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (errorMessage) {
                    errorMessage.textContent = 'Произошла ошибка при отправке. Пожалуйста, попробуйте еще раз.';
                    errorMessage.style.display = 'block';
                }
            })
            .finally(() => {
                hideLoading();
            });
        });
    }

    // دالة لعرض نافذة النجاح
    function showSuccessModal(message, proposalId) {
        const successModal = document.getElementById('successModal');
        const successMessageContent = document.getElementById('successMessageContent');
        const proposalIdValue = document.getElementById('proposalIdValue');
        const closeSuccessModal = document.getElementById('closeSuccessModal');
        const closeSuccessBtn = document.getElementById('closeSuccessBtn');
        
        if (successModal && successMessageContent && proposalIdValue) {
            successMessageContent.textContent = message;
            proposalIdValue.textContent = proposalId || 'Не указан';
            successModal.style.display = 'block';
            document.body.style.overflow = 'hidden';
            
            const closeFunc = function() {
                successModal.style.display = 'none';
                document.body.style.overflow = 'auto';
                resetForm();
                closeSuccessModal.removeEventListener('click', closeFunc);
                closeSuccessBtn.removeEventListener('click', closeFunc);
                successModal.removeEventListener('click', outsideClick);
            };
            
            const outsideClick = function(e) {
                if (e.target === successModal) {
                    closeFunc();
                }
            };
            
            closeSuccessModal.addEventListener('click', closeFunc);
            closeSuccessBtn.addEventListener('click', closeFunc);
            successModal.addEventListener('click', outsideClick);
        }
    }
});