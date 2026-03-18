// schedule/js/program_detail.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Reading Progress Indicator
    function initReadingProgress() {
        const progressContainer = document.createElement('div');
        progressContainer.className = 'reading-progress-container';
        progressContainer.innerHTML = '<div class="reading-progress-bar"></div>';
        document.body.appendChild(progressContainer);
        
        const progressBar = document.querySelector('.reading-progress-bar');
        const container = document.querySelector('.reading-progress-container');
        
        window.addEventListener('scroll', () => {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight - windowHeight;
            const scrolled = (window.scrollY / documentHeight) * 100;
            
            progressBar.style.width = `${scrolled}%`;
            
            if (window.scrollY > 100) {
                container.style.display = 'block';
            } else {
                container.style.display = 'none';
            }
        });
    }
    
    // Add ripple effect to buttons
    function initRippleEffects() {
        const buttons = document.querySelectorAll('.apply-button-simple, .submit-btn-small, .program-tab-btn, .combined-tab-btn, .module-toggle-new, .apply-button-red');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255,255,255,0.7);
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    width: ${size}px;
                    height: ${size}px;
                    top: ${y}px;
                    left: ${x}px;
                    pointer-events: none;
                `;
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }
    
    // تهيئة زر التقديم المبسط
    function initSimpleApplyButton() {
        const simpleApplyBtn = document.querySelector('.apply-button-simple');
        if (simpleApplyBtn) {
            simpleApplyBtn.addEventListener('click', function(e) {
                e.preventDefault();
                openApplicationModal();
            });
        }
    }
    
    // Program Tabs Functionality
    function initProgramTabs() {
        const tabButtons = document.querySelectorAll('.program-tab-btn');
        const tabPanes = document.querySelectorAll('.program-tab-pane');
        
        if (tabButtons.length === 0 || tabPanes.length === 0) return;
        
        function activateTab(tabId) {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            const activeButton = document.querySelector(`.program-tab-btn[data-tab="${tabId}"]`);
            const activePane = document.getElementById(`tab-${tabId}`);
            
            if (activeButton && activePane) {
                activeButton.classList.add('active');
                activePane.classList.add('active');
                localStorage.setItem('activeProgramTab', tabId);
            }
        }
        
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');
                activateTab(tabId);
            });
        });
        
        const savedTab = localStorage.getItem('activeProgramTab');
        if (savedTab) {
            activateTab(savedTab);
        } else {
            activateTab('description');
        }
    }
    
    // Initialize Combined Sections Tabs
    function initCombinedSectionsTabs() {
        const tabButtons = document.querySelectorAll('.combined-tab-btn');
        const tabPanes = document.querySelectorAll('.combined-tab-pane');
        
        if (tabButtons.length === 0 || tabPanes.length === 0) return;
        
        function activateTab(tabId) {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            const activeButton = document.querySelector(`.combined-tab-btn[data-tab="${tabId}"]`);
            const activePane = document.getElementById(`tab-${tabId}`);
            
            if (activeButton && activePane) {
                activeButton.classList.add('active');
                activePane.classList.add('active');
                localStorage.setItem('activeCombinedTab', tabId);
            }
        }
        
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');
                activateTab(tabId);
            });
        });
        
        const savedTab = localStorage.getItem('activeCombinedTab');
        if (savedTab) {
            activateTab(savedTab);
        } else {
            activateTab('curriculum');
        }
    }
    
    // تهيئة تفاعل الوحدات التعليمية
    function initCurriculumModulesNew() {
        const curriculumModules = document.querySelectorAll('.curriculum-module-new');
        
        curriculumModules.forEach(module => {
            const header = module.querySelector('.module-header-new');
            const toggle = module.querySelector('.module-toggle-new');
            const content = module.querySelector('.module-content-new');
            
            if (header && content) {
                header.addEventListener('click', function(e) {
                    if (e.target.closest('.module-toggle-new')) return;
                    toggleModule(module);
                });
                
                if (toggle) {
                    toggle.addEventListener('click', function(e) {
                        e.stopPropagation();
                        toggleModule(module);
                    });
                }
            }
        });
    }
    
    function toggleModule(module) {
        const content = module.querySelector('.module-content-new');
        
        document.querySelectorAll('.curriculum-module-new').forEach(otherModule => {
            if (otherModule !== module) {
                otherModule.classList.remove('active');
                const otherContent = otherModule.querySelector('.module-content-new');
                if (otherContent) otherContent.style.display = 'none';
            }
        });
        
        const isActive = module.classList.contains('active');
        
        if (isActive) {
            module.classList.remove('active');
            if (content) content.style.display = 'none';
        } else {
            module.classList.add('active');
            if (content) {
                content.style.display = 'block';
                content.style.animation = 'fadeIn 0.5s ease';
            }
        }
    }
    
    // تهيئة تفاعل مستندات المنهج
    function initCurriculumDocuments() {
        const documentCards = document.querySelectorAll('.curriculum-document-card-new');
        
        documentCards.forEach(card => {
            card.addEventListener('click', function(e) {
                if (e.target.tagName === 'svg' || e.target.closest('svg')) return;
                
                this.style.transform = 'translateY(0)';
                setTimeout(() => {
                    this.style.transform = 'translateY(-2px)';
                }, 150);
            });
        });
    }

    // ===== Carousel for Other Programs =====
    function initProgramsCarousel() {
        const container = document.querySelector('.other-programs-carousel-section');
        if (!container) return;

        const track = container.querySelector('.carousel-track');
        const prevBtn = container.querySelector('.carousel-arrow-left');
        const nextBtn = container.querySelector('.carousel-arrow-right');
        const dotsContainer = container.querySelector('.carousel-dots');
        
        if (!track || !prevBtn || !nextBtn) return;

        const cards = track.children;
        if (cards.length === 0) return;

        let cardWidth = cards[0].offsetWidth + parseFloat(getComputedStyle(cards[0]).marginRight) * 2;
        let gap = parseFloat(getComputedStyle(track).gap) || 24;
        let scrollAmount = cardWidth + gap;

        let maxScroll = track.scrollWidth - track.clientWidth;

        function updateButtons() {
            const scrollLeft = track.scrollLeft;
            prevBtn.disabled = scrollLeft <= 10;
            nextBtn.disabled = scrollLeft >= maxScroll - 10;
        }

        function scrollToPosition(position) {
            track.scrollTo({ left: position, behavior: 'smooth' });
        }

        // Кнопки
        prevBtn.addEventListener('click', () => {
            track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });

        nextBtn.addEventListener('click', () => {
            track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });

        track.addEventListener('scroll', updateButtons);
        window.addEventListener('resize', () => {
            cardWidth = cards[0].offsetWidth + parseFloat(getComputedStyle(cards[0]).marginRight);
            gap = parseFloat(getComputedStyle(track).gap) || 24;
            scrollAmount = cardWidth + gap;
            maxScroll = track.scrollWidth - track.clientWidth;
            updateButtons();
        });

        // Точки
        function createDots() {
            if (!dotsContainer) return;
            dotsContainer.innerHTML = '';
            const totalSlides = Math.ceil((track.scrollWidth - track.clientWidth) / scrollAmount) + 1;
            for (let i = 0; i < totalSlides; i++) {
                const dot = document.createElement('button');
                dot.classList.add('carousel-dot');
                dot.setAttribute('aria-label', `Перейти к слайду ${i + 1}`);
                dot.addEventListener('click', () => {
                    scrollToPosition(i * scrollAmount);
                });
                dotsContainer.appendChild(dot);
            }
        }

        function updateDots() {
            if (!dotsContainer) return;
            const dots = dotsContainer.children;
            const scrollLeft = track.scrollLeft;
            const activeIndex = Math.round(scrollLeft / scrollAmount);
            Array.from(dots).forEach((dot, i) => {
                dot.classList.toggle('active', i === activeIndex);
            });
        }

        // Инициализация точек
        if (dotsContainer) {
            createDots();
            updateDots();
            track.addEventListener('scroll', updateDots);
            window.addEventListener('resize', () => {
                createDots();
                updateDots();
            });
        }

        updateButtons();
    }
    // ===== END NEW =====
    
    // Initialize all effects
    function initAllEffects() {
        initReadingProgress();
        initRippleEffects();
        initSimpleApplyButton();
        initProgramTabs();
        initCombinedSectionsTabs();
        initCurriculumModulesNew();
        initCurriculumDocuments();
        initProgramsCarousel();
    }
    
    setTimeout(() => {
        initAllEffects();
    }, 100);
});

// وظائف نافذة تقديم الطلب
function openApplicationModal() {
    const applicationModal = document.getElementById('applicationModal');
    if (applicationModal) {
        applicationModal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function closeApplicationModal() {
    const applicationModal = document.getElementById('applicationModal');
    if (applicationModal) {
        applicationModal.style.display = 'none';
        document.body.style.overflow = 'auto';
        resetApplicationForm();
    }
}

function resetApplicationForm() {
    const form = document.getElementById('applicationFormElement');
    const successMessage = document.getElementById('successMessage');
    const applicationForm = document.getElementById('applicationForm');
    
    if (form) {
        form.reset();
        // إزالة class submitted عند إعادة الضبط
        form.classList.remove('submitted');
    }
    if (successMessage) successMessage.style.display = 'none';
    if (applicationForm) applicationForm.style.display = 'block';
}

// التحقق من صحة النموذج قبل الإرسال
function validateApplicationForm(form) {
    const requiredInputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    requiredInputs.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
        }
    });
    
    return isValid;
}

// معالجة تقديم النموذج
document.addEventListener('DOMContentLoaded', function() {
    const applicationForm = document.getElementById('applicationFormElement');
    const closeModal = document.querySelector('.close-modal');
    const applicationModal = document.getElementById('applicationModal');

    const newApplyButton = document.querySelector('.apply-button-simple');
    if (newApplyButton) {
        newApplyButton.addEventListener('click', function(e) {
            e.preventDefault();
            openApplicationModal();
        });
    }

    // ===== زر التقديم الأحمر الجديد =====
    const redApplyButton = document.querySelector('.apply-button-red');
    if (redApplyButton) {
        redApplyButton.addEventListener('click', function(e) {
            e.preventDefault();
            openApplicationModal();
        });
    }

    if (closeModal) {
        closeModal.addEventListener('click', closeApplicationModal);
    }

    if (applicationModal) {
        applicationModal.addEventListener('click', function(e) {
            if (e.target === applicationModal) {
                closeApplicationModal();
            }
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && applicationModal && applicationModal.style.display === 'block') {
            closeApplicationModal();
        }
    });

    if (applicationForm) {
        // إزالة class submitted عند التفاعل مع أي حقل
        const formFields = applicationForm.querySelectorAll('input, select, textarea');
        formFields.forEach(field => {
            field.addEventListener('input', function() {
                applicationForm.classList.remove('submitted');
            });
            field.addEventListener('change', function() {
                applicationForm.classList.remove('submitted');
            });
        });

        applicationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // التحقق من صحة الحقول المطلوبة
            if (!validateApplicationForm(this)) {
                // إضافة class لتمييز الحقول الفارغة
                this.classList.add('submitted');
                alert('Пожалуйста, заполните все обязательные поля.');
                return;
            }
            
            const submitBtn = this.querySelector('.submit-btn-small');
            const submitText = this.querySelector('.submit-text');
            const loadingSpinner = this.querySelector('.loading-spinner');
            const successMessage = document.getElementById('successMessage');
            const successText = document.getElementById('successText');
            const applicationFormContainer = document.getElementById('applicationForm');
            
            if (submitBtn) submitBtn.disabled = true;
            if (submitText) submitText.style.display = 'none';
            if (loadingSpinner) loadingSpinner.style.display = 'inline-block';
            
            const formData = new FormData(this);
            const programSlug = document.querySelector('input[name="program_slug"]')?.value || 
                               window.location.pathname.split('/').filter(Boolean).pop();
            
            // دمج قيم الإدارة والبرنامج وحالة التسجيل المتعدد في حقل الملاحظات
            const additionalInfoField = document.getElementById('additionalInfo');
            let additionalInfo = additionalInfoField.value;

            const departmentSelect = document.getElementById('department');
            const programSelect = document.getElementById('program');
            const multipleParticipantsCheckbox = document.getElementById('multipleParticipants');

            let extraInfo = '';

            if (departmentSelect && departmentSelect.value) {
                const deptText = departmentSelect.options[departmentSelect.selectedIndex].text;
                extraInfo += `Отделение: ${deptText}\n`;
            }
            if (programSelect && programSelect.value) {
                const progText = programSelect.options[programSelect.selectedIndex].text;
                extraInfo += `Программа: ${progText}\n`;
            }
            if (multipleParticipantsCheckbox) {
                const isChecked = multipleParticipantsCheckbox.checked;
                extraInfo += `Регистрирую нескольких участников: ${isChecked ? 'Да' : 'Нет'}\n`;
            }

            if (extraInfo) {
                additionalInfo = extraInfo + (additionalInfo ? '\n' + additionalInfo : '');
                formData.delete('additionalInfo');
                formData.append('additionalInfo', additionalInfo);
            }

            fetch(`/schedule/program/${programSlug}/apply/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (applicationFormContainer) applicationFormContainer.style.display = 'none';
                    if (successText) successText.textContent = data.message;
                    if (successMessage) successMessage.style.display = 'block';
                } else {
                    alert(data.message || 'Произошла ошибка при отправке заявки.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при отправке заявки. Пожалуйста, попробуйте еще раз.');
            })
            .finally(() => {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    if (submitText) submitText.style.display = 'inline-block';
                    if (loadingSpinner) loadingSpinner.style.display = 'none';
                }
            });
        });
    }
});

// دالة للحصول على قيمة CSRF token
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

// إضافة تأثير ripple
const style = document.createElement('style');
style.textContent = `
@keyframes ripple {
    to { transform: scale(4); opacity: 0; }
}
.reading-progress-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: transparent;
    z-index: 9999;
    display: none;
}
.reading-progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #7F1726, #052946);
    width: 0;
    transition: width 0.3s ease;
}
`;
document.head.appendChild(style);