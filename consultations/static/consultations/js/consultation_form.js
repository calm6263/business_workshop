document.addEventListener('DOMContentLoaded', function() {
    // Character counter for additional wishes
    const textarea = document.querySelector('textarea[name="additional_wishes"]');
    const charCount = document.getElementById('charCount');
    
    if (textarea && charCount) {
        textarea.addEventListener('input', function() {
            charCount.textContent = this.value.length;
        });
        
        // Initialize character count
        charCount.textContent = textarea.value.length;
    }
    
    // FAQ accordion functionality
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const faqItem = this.closest('.faq-item');
            const isActive = faqItem.classList.contains('active');
            
            // Close all other FAQ items
            document.querySelectorAll('.faq-item').forEach(item => {
                if (item !== faqItem) {
                    item.classList.remove('active');
                }
            });
            
            // Toggle current FAQ item
            if (!isActive) {
                faqItem.classList.add('active');
            } else {
                faqItem.classList.remove('active');
            }
        });
    });
    
    // Form validation
    const form = document.getElementById('consultationForm');
    if (form) {
        const agreementCheckbox = form.querySelector('input[name="agreed_to_terms"]');
        let isSubmitting = false; // Prevent double submission

        form.addEventListener('submit', function(e) {
            let isValid = true;
            let firstErrorField = null;
            
            // Check agreement
            if (!agreementCheckbox.checked) {
                isValid = false;
                showInlineError('agreement-error', 'Пожалуйста, согласитесь с условиями');
                if (!firstErrorField) firstErrorField = agreementCheckbox;
            } else {
                hideInlineError('agreement-error');
            }
            
            // Check direction
            const directionSelect = form.querySelector('select[name="direction"]');
            if (directionSelect && !directionSelect.value) {
                isValid = false;
                showInlineError('direction-error', 'Пожалуйста, выберите направление');
                if (!firstErrorField) firstErrorField = directionSelect;
            } else {
                hideInlineError('direction-error');
            }
            
            // Check phone
            const phoneInput = form.querySelector('input[name="contact_phone"]');
            if (phoneInput && !phoneInput.value.trim()) {
                isValid = false;
                showInlineError('phone-error', 'Пожалуйста, введите номер телефона');
                if (!firstErrorField) firstErrorField = phoneInput;
            } else {
                hideInlineError('phone-error');
            }
            
            // Check email
            const emailInput = form.querySelector('input[name="contact_email"]');
            if (emailInput && !emailInput.value.trim()) {
                isValid = false;
                showInlineError('email-error', 'Пожалуйста, введите email');
                if (!firstErrorField) firstErrorField = emailInput;
            } else {
                hideInlineError('email-error');
            }
            
            // Check date
            const dateInput = form.querySelector('input[name="date"]');
            if (dateInput && !dateInput.value) {
                isValid = false;
                showInlineError('date-error', 'Пожалуйста, выберите дату');
                if (!firstErrorField) firstErrorField = dateInput;
            } else {
                hideInlineError('date-error');
            }
            
            // Check time
            const timeInput = form.querySelector('input[name="time"]');
            if (timeInput && !timeInput.value) {
                isValid = false;
                showInlineError('time-error', 'Пожалуйста, выберите время');
                if (!firstErrorField) firstErrorField = timeInput;
            } else {
                hideInlineError('time-error');
            }
            
            if (!isValid) {
                e.preventDefault();
                // Focus on first error field
                if (firstErrorField) {
                    firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstErrorField.focus();
                }
                return false;
            }

            // Prevent double submission
            if (isSubmitting) {
                e.preventDefault();
                return false;
            }
            isSubmitting = true;
            
            // Disable only the submit button, show loading
            const submitBtn = form.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Отправка...';
                submitBtn.disabled = true;
            }
            
            // Do NOT disable other form elements – they must be sent including CSRF token
        });
        
        // Helper functions for inline errors
        function showInlineError(fieldName, message) {
            let errorElement = document.getElementById(fieldName);
            if (!errorElement) {
                errorElement = document.createElement('div');
                errorElement.id = fieldName;
                errorElement.className = 'error-message inline-error';
                errorElement.style.color = '#dc3545';
                errorElement.style.fontSize = '0.85rem';
                errorElement.style.marginTop = '0.5rem';
                
                // Insert after the field
                const field = form.querySelector(`[name="${fieldName.replace('-error', '')}"]`);
                if (field) {
                    field.parentNode.insertBefore(errorElement, field.nextSibling);
                }
            }
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
        
        function hideInlineError(fieldName) {
            const errorElement = document.getElementById(fieldName);
            if (errorElement) {
                errorElement.style.display = 'none';
            }
        }
    }
    
    // Set minimum date to today
    const dateInput = document.querySelector('input[type="date"]');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.min = today;
        
        // If date is empty, set to tomorrow
        if (!dateInput.value) {
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            dateInput.value = tomorrow.toISOString().split('T')[0];
        }
    }
    
    // Set default time to 10:00
    const timeInput = document.querySelector('input[type="time"]');
    if (timeInput && !timeInput.value) {
        timeInput.value = '10:00';
    }

    // Hero Slider Functionality
    function initHeroSlider() {
        const slides = document.querySelectorAll('.hero-slide');
        const dots = document.querySelectorAll('.slider-dot');
        const prevBtn = document.querySelector('.prev-control');
        const nextBtn = document.querySelector('.next-control');
        
        if (slides.length <= 1) {
            // Hide controls if only one slide
            if (prevBtn) prevBtn.style.display = 'none';
            if (nextBtn) nextBtn.style.display = 'none';
            if (dots.length > 0) document.querySelector('.slider-dots').style.display = 'none';
            
            // Show the single slide
            if (slides.length === 1) {
                slides[0].classList.add('active');
            }
            return;
        }
        
        let currentSlide = 0;
        
        function showSlide(index) {
            // Hide all slides
            slides.forEach(slide => {
                slide.classList.remove('active');
            });
            
            // Remove active class from all dots
            dots.forEach(dot => {
                dot.classList.remove('active');
            });
            
            // Show current slide and activate corresponding dot
            slides[index].classList.add('active');
            if (dots[index]) {
                dots[index].classList.add('active');
            }
            
            currentSlide = index;
        }
        
        function nextSlide() {
            let newIndex = currentSlide + 1;
            if (newIndex >= slides.length) {
                newIndex = 0;
            }
            showSlide(newIndex);
        }
        
        function prevSlide() {
            let newIndex = currentSlide - 1;
            if (newIndex < 0) {
                newIndex = slides.length - 1;
            }
            showSlide(newIndex);
        }
        
        // Initialize first slide
        showSlide(0);
        
        // Auto slide every 5 seconds
        let slideInterval = setInterval(nextSlide, 5000);
        
        // Event listeners for controls
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                nextSlide();
                clearInterval(slideInterval);
                slideInterval = setInterval(nextSlide, 5000);
            });
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                prevSlide();
                clearInterval(slideInterval);
                slideInterval = setInterval(nextSlide, 5000);
            });
        }
        
        // Event listeners for dots
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                showSlide(index);
                clearInterval(slideInterval);
                slideInterval = setInterval(nextSlide, 5000);
            });
        });
        
        // Pause on hover
        const slider = document.querySelector('.full-width-slider');
        if (slider) {
            slider.addEventListener('mouseenter', () => {
                clearInterval(slideInterval);
            });
            
            slider.addEventListener('mouseleave', () => {
                clearInterval(slideInterval);
                slideInterval = setInterval(nextSlide, 5000);
            });
        }
    }

    // Add red dot indicator functionality
    function initContactFieldIndicators() {
        const phoneInput = document.querySelector('input[name="contact_phone"]');
        const emailInput = document.querySelector('input[name="contact_email"]');
        
        function updateIndicator(input, innerCircle) {
            if (input && innerCircle) {
                if (input.value.trim() !== '') {
                    innerCircle.style.backgroundColor = '#7F1726';
                } else {
                    innerCircle.style.backgroundColor = 'transparent';
                }
            }
        }
        
        // Phone field indicator
        if (phoneInput) {
            const phoneInnerCircle = document.querySelector('.phone-field .icon-inner-circle');
            if (phoneInnerCircle) {
                phoneInput.addEventListener('input', function() {
                    updateIndicator(this, phoneInnerCircle);
                });
                phoneInput.addEventListener('focus', function() {
                    phoneInnerCircle.style.backgroundColor = '#7F1726';
                });
                phoneInput.addEventListener('blur', function() {
                    updateIndicator(this, phoneInnerCircle);
                });
                // Initial check
                updateIndicator(phoneInput, phoneInnerCircle);
            }
        }
        
        // Email field indicator
        if (emailInput) {
            const emailInnerCircle = document.querySelector('.email-field .icon-inner-circle');
            if (emailInnerCircle) {
                emailInput.addEventListener('input', function() {
                    updateIndicator(this, emailInnerCircle);
                });
                emailInput.addEventListener('focus', function() {
                    emailInnerCircle.style.backgroundColor = '#7F1726';
                });
                emailInput.addEventListener('blur', function() {
                    updateIndicator(this, emailInnerCircle);
                });
                // Initial check
                updateIndicator(emailInput, emailInnerCircle);
            }
        }
    }

    // CSRF token handling (optional, if needed elsewhere)
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

    // Initialize hero slider
    initHeroSlider();
    
    // Initialize contact field indicators
    initContactFieldIndicators();
    
    // Display error messages from Django
    function displayErrorMessages() {
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(error => {
            if (error.textContent.trim() !== '') {
                error.style.display = 'block';
                error.style.color = '#dc3545';
                error.style.fontSize = '0.9rem';
                error.style.marginTop = '5px';
            }
        });
    }
    
    // Run after page loads
    setTimeout(displayErrorMessages, 100);
    
    // Auto-close success messages after 10 seconds
    setTimeout(function() {
        const successAlerts = document.querySelectorAll('.alert-success');
        successAlerts.forEach(alert => {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        });
    }, 10000);
    
    // Prevent form resubmission on page refresh
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }
});