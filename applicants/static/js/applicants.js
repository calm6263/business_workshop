// applicants.js
document.addEventListener('DOMContentLoaded', function() {
    // Валидация email
    function validateEmail(email) {
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return re.test(email);
    }

    // Валидация телефона
    function validatePhone(phone) {
        const re = /^[\+]?[0-9\s\-\(\)]{10,}$/;
        return re.test(phone);
    }

    // Функция проверки формы перед отправкой
    function validateForm(formData) {
        const errors = [];

        if (!formData.get('contact_person') || formData.get('contact_person').trim().length < 2) {
            errors.push('Введите корректное имя');
        }

        if (!validatePhone(formData.get('phone'))) {
            errors.push('Введите корректный номер телефона');
        }

        if (!validateEmail(formData.get('email'))) {
            errors.push('Введите корректный email');
        }

        return errors;
    }

    // Плавная прокрутка к целевому блоку
    function scrollToTarget(targetId) {
        const targetElement = document.getElementById(targetId);

        if (!targetElement) {
            console.warn(`Элемент с id '${targetId}' не найден`);
            return;
        }

        const headerHeight = document.querySelector('header')?.offsetHeight || 0;
        const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;

        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });

        history.pushState(null, null, `#${targetId}`);
    }

    // Обработка кликов по прямоугольникам на hero-секции
    const heroRectangles = document.querySelectorAll('.hero-rectangle');

    if (heroRectangles.length > 0) {
        heroRectangles.forEach(rectangle => {
            rectangle.addEventListener('click', function() {
                const targetId = this.getAttribute('data-target');

                heroRectangles.forEach(r => r.classList.remove('active'));
                this.classList.add('active');

                scrollToTarget(targetId);

                setTimeout(() => {
                    this.classList.remove('active');
                }, 1500);
            });

            rectangle.addEventListener('mouseenter', function() {
                if (!this.classList.contains('active')) {
                    this.classList.add('hover-active');
                }
            });

            rectangle.addEventListener('mouseleave', function() {
                this.classList.remove('hover-active');
            });
        });
    }

    // Основные элементы
    const applicationBtn = document.querySelector('.application-btn');
    const applicationModal = document.getElementById('applicationModal');
    const confirmationModal = document.getElementById('confirmationModal');
    const applicationForm = document.getElementById('applicationForm');

    // Кнопки закрытия
    const modalClose = document.getElementById('modalClose');
    const confirmationClose = document.getElementById('confirmationClose');
    const confirmationOkBtn = document.getElementById('confirmationOkBtn');

    // Оверлеи
    const modalOverlay = document.getElementById('modalOverlay');
    const confirmationOverlay = document.getElementById('confirmationOverlay');

    // Открытие окна заявки (с проверкой типа пользователя)
    if (applicationBtn && applicationModal) {
        applicationBtn.addEventListener('click', function(e) {
            e.preventDefault();

            if (window.userAuthenticated) {
                // Проверка типа пользователя
                if (window.userType && ['regular', 'student', 'company'].includes(window.userType)) {
                    applicationModal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                } else {
                    // Показать окно "тип пользователя не разрешён"
                    const notAllowedModal = document.getElementById('userTypeNotAllowedModal');
                    if (notAllowedModal) {
                        notAllowedModal.classList.add('active');
                        document.body.style.overflow = 'hidden';
                    } else {
                        // fallback: обычный alert
                        alert('Подавать заявки могут только обычные пользователи, студенты и компании.');
                    }
                }
            } else {
                // Не авторизован - показать окно авторизации
                const methodModal1 = document.getElementById('methodModal1');
                if (methodModal1) {
                    methodModal1.classList.add('active');
                    document.body.style.overflow = 'hidden';
                } else {
                    applicationModal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            }
        });
    }

    // Закрытие окон
    function closeApplicationModal() {
        if (applicationModal) {
            applicationModal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }

    function closeConfirmationModal() {
        if (confirmationModal) {
            confirmationModal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }

    function closeMethodModal(modal) {
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }

    if (modalClose) modalClose.addEventListener('click', closeApplicationModal);
    if (modalOverlay) modalOverlay.addEventListener('click', closeApplicationModal);

    if (confirmationClose) confirmationClose.addEventListener('click', closeConfirmationModal);
    if (confirmationOkBtn) confirmationOkBtn.addEventListener('click', closeConfirmationModal);
    if (confirmationOverlay) confirmationOverlay.addEventListener('click', closeConfirmationModal);

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeApplicationModal();
            closeConfirmationModal();
        }
    });

    // Отправка формы заявки
    if (applicationForm) {
        applicationForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const agreement = document.getElementById('agreement');
            if (!agreement.checked) {
                alert('Пожалуйста, согласитесь с условиями пользовательского соглашения');
                return;
            }

            const formData = new FormData(applicationForm);
            const errors = validateForm(formData);

            if (errors.length > 0) {
                alert(errors.join('\n'));
                return;
            }

            // Блокировка кнопки отправки
            const submitBtn = applicationForm.querySelector('.submit-application-btn');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="btn-text">Отправка...</span>';

            fetch(applicationForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 429) {
                        return response.json().then(data => {
                            throw new Error(data.message || 'Превышен лимит заявок');
                        });
                    }
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const confirmationNumber = document.getElementById('confirmationNumber');
                    if (confirmationNumber) {
                        confirmationNumber.innerHTML = `Номер Вашей заявки: <strong>${data.application_number}</strong>`;
                    }

                    closeApplicationModal();
                    if (confirmationModal) {
                        confirmationModal.classList.add('active');
                    }

                    applicationForm.reset();
                } else {
                    alert('Ошибка: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка: ' + error.message);
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            });
        });
    }

    // Предотвращение закрытия модалок при клике на содержимое
    const modalContents = document.querySelectorAll('.modal-content, .confirmation-content');
    modalContents.forEach(content => {
        if (content) {
            content.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    });

    // Прокрутка к образовательным программам
    const educationalProgramsLink = document.getElementById('educationalProgramsLink');
    const educationalProgramsSection = document.getElementById('educationalPrograms');

    if (educationalProgramsLink && educationalProgramsSection) {
        educationalProgramsLink.addEventListener('click', function() {
            educationalProgramsSection.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Кнопки "Подать заявление" на карточках программ (если есть)
    const programApplyBtns = document.querySelectorAll('.program-apply-btn');

    programApplyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const programSlug = this.getAttribute('data-program-slug');
            if (programSlug) {
                window.location.href = `/schedule/program/${programSlug}/`;
            }
        });
    });

    // Защита от XSS в поле поиска
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            this.value = this.value.replace(/[<>]/g, '');
        });
    }

    // ===== Инициализация карусели "Интересные программы" =====
    function initInterestingCarousel() {
        const carousel = document.getElementById('interestingCarousel');
        const carouselDots = document.getElementById('interestingCarouselDots');
        const prevBtn = document.querySelector('.interesting-carousel-section .carousel-prev');
        const nextBtn = document.querySelector('.interesting-carousel-section .carousel-next');

        if (!carousel || !carouselDots || !prevBtn || !nextBtn) return;

        const slides = carousel.querySelectorAll('.carousel-slide');
        const totalSlides = slides.length;
        let currentSlide = 0;
        let autoSlideInterval;

        function getSlidesPerView() {
            return window.innerWidth < 768 ? 1 : 2;
        }

        function createDots() {
            carouselDots.innerHTML = '';
            const slidesPerView = getSlidesPerView();
            const pages = Math.max(1, Math.ceil(totalSlides / slidesPerView));
            for (let i = 0; i < pages; i++) {
                const dot = document.createElement('button');
                dot.className = 'carousel-dot';
                dot.setAttribute('aria-label', `Перейти к слайду ${i + 1}`);
                dot.addEventListener('click', () => goToSlide(i * slidesPerView));
                carouselDots.appendChild(dot);
            }
            updateDots();
        }

        function updateDots() {
            const dots = carouselDots.querySelectorAll('.carousel-dot');
            const slidesPerView = getSlidesPerView();
            const activePage = Math.floor(currentSlide / slidesPerView);
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === activePage);
            });
        }

        function goToSlide(slideIndex) {
            const slidesPerView = getSlidesPerView();
            currentSlide = Math.max(0, Math.min(slideIndex, totalSlides - slidesPerView));
            updateCarouselPosition();
            updateDots();
        }

        function updateCarouselPosition() {
            const slideWidth = slides[0]?.offsetWidth + 24 || 304;
            carousel.style.transition = 'transform 0.3s ease';
            carousel.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
        }

        function nextSlide() {
            const slidesPerView = getSlidesPerView();
            goToSlide(currentSlide + slidesPerView);
        }

        function prevSlide() {
            const slidesPerView = getSlidesPerView();
            goToSlide(currentSlide - slidesPerView);
        }

        prevBtn.addEventListener('click', prevSlide);
        nextBtn.addEventListener('click', nextSlide);

        function startAutoSlide() {
            stopAutoSlide();
            autoSlideInterval = setInterval(nextSlide, 5000);
        }

        function stopAutoSlide() {
            clearInterval(autoSlideInterval);
        }

        // Поддержка свайпа
        let isDragging = false, startPos = 0, currentTranslate = 0, prevTranslate = 0;

        carousel.addEventListener('touchstart', (e) => {
            isDragging = true;
            startPos = e.touches[0].clientX;
            currentTranslate = prevTranslate;
            carousel.style.transition = 'none';
            stopAutoSlide();
        }, { passive: false });

        carousel.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const diff = e.touches[0].clientX - startPos;
            carousel.style.transform = `translateX(${currentTranslate + diff}px)`;
        }, { passive: false });

        carousel.addEventListener('touchend', (e) => {
            isDragging = false;
            carousel.style.transition = 'transform 0.3s ease';
            const movedBy = e.changedTouches[0].clientX - startPos;
            if (movedBy < -50) nextSlide();
            else if (movedBy > 50) prevSlide();
            else updateCarouselPosition();
            prevTranslate = -currentSlide * (slides[0]?.offsetWidth + 24);
            startAutoSlide();
        });

        carousel.addEventListener('mouseenter', stopAutoSlide);
        carousel.addEventListener('mouseleave', startAutoSlide);

        window.addEventListener('resize', () => {
            goToSlide(currentSlide);
            createDots();
        });

        createDots();
        goToSlide(0);
        startAutoSlide();
    }

    initInterestingCarousel();

    // ===== Инициализация фильтров (из departments_list.js) =====
    function initFilterDropdowns() {
        const isMobile = window.matchMedia('(max-width: 768px)').matches;
        const filtersContainer = document.querySelector('.applicants-filters');

        if (!filtersContainer) return;

        // Пересоздаём toggle-элементы, чтобы избежать дублирования обработчиков
        filtersContainer.querySelectorAll('.filter-input.custom-dropdown-toggle').forEach(toggle => {
            const newToggle = toggle.cloneNode(true);
            toggle.parentNode.replaceChild(newToggle, toggle);
        });

        filtersContainer.querySelectorAll('.filter-input.custom-dropdown-toggle').forEach(toggle => {
            const dropdownId = toggle.id.replace('Filter', 'Dropdown');
            const dropdown = document.getElementById(dropdownId);

            if (isMobile) {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();

                    filtersContainer.querySelectorAll('.filter-dropdown.show').forEach(d => {
                        if (d !== dropdown) d.classList.remove('show');
                    });

                    if (dropdown) {
                        dropdown.classList.toggle('show');
                        document.querySelector('.dropdown-backdrop')?.classList.toggle('active', dropdown.classList.contains('show'));
                    }
                });
            } else {
                toggle.removeAttribute('data-bs-toggle');
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();

                    filtersContainer.querySelectorAll('.filter-dropdown.show').forEach(d => {
                        if (d !== dropdown) d.classList.remove('show');
                    });

                    if (dropdown) {
                        dropdown.classList.toggle('show');
                        toggle.setAttribute('aria-expanded', dropdown.classList.contains('show'));
                    }
                });
            }
        });

        // Закрытие при клике вне фильтров
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.applicants-filters .filter-item')) {
                filtersContainer.querySelectorAll('.filter-dropdown.show').forEach(dropdown => {
                    dropdown.classList.remove('show');
                });
                filtersContainer.querySelectorAll('.filter-input[aria-expanded="true"]').forEach(toggle => {
                    toggle.setAttribute('aria-expanded', 'false');
                });
                document.querySelector('.dropdown-backdrop')?.classList.remove('active');
            }
        });

        filtersContainer.querySelectorAll('.filter-dropdown').forEach(dropdown => {
            dropdown.addEventListener('click', e => e.stopPropagation());
        });
    }

    initFilterDropdowns();
    window.matchMedia('(max-width: 768px)').addEventListener('change', initFilterDropdowns);

    // Создание backdrop для мобильных
    if (!document.querySelector('.dropdown-backdrop')) {
        const backdrop = document.createElement('div');
        backdrop.className = 'dropdown-backdrop';
        document.body.appendChild(backdrop);
        backdrop.addEventListener('click', function() {
            document.querySelectorAll('.filter-dropdown.show').forEach(dropdown => {
                dropdown.classList.remove('show');
            });
            this.classList.remove('active');
        });
    }

    // Основной класс фильтра
    class DepartmentsFilter {
        constructor() {
            this.container = document.querySelector('.applicants-filters');
            this.filters = {
                programTypes: [],
                format: 'all',
                monthYear: 'all',
                selectedDate: null
            };

            this.filterMaps = { format: {}, month_year: {}, date: {}, program_type: {} };
            const filterMapsEl = document.getElementById('filterMapsJson');
            if (filterMapsEl) {
                try {
                    this.filterMaps = JSON.parse(filterMapsEl.textContent);
                    this.filterMaps.program_type = this.filterMaps.program_type || {};
                } catch(e) {
                    console.error('Ошибка парсинга filterMapsJson', e);
                }
            }

            this.init();
        }

        init() {
            this.setupFilterSelections();
            this.initCalendar();
            this.syncAllProgramCheckbox();
            this.applyFilters();
        }

        syncAllProgramCheckbox() {
            const allCheckbox = this.container.querySelector('#programTypeDropdown [data-value="all"] .custom-checkbox');
            if (!allCheckbox) return;
            const anyChecked = this.container.querySelectorAll('#programTypeDropdown .dropdown-item-custom:not([data-value="all"]) .custom-checkbox.checked').length > 0;
            allCheckbox.classList.toggle('checked', !anyChecked);
        }

        setupFilterSelections() {
            // Фильтр по типу программы
            this.container.querySelectorAll('#programTypeDropdown .dropdown-item-custom').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const checkbox = item.querySelector('.custom-checkbox');
                    this.handleProgramTypeSelection(item.dataset.value, checkbox);
                    setTimeout(() => this.applyFilters(), 100);
                });
            });

            // Фильтр по месяцу/году
            this.container.querySelectorAll('#monthYearDropdown .dropdown-item-custom').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const checkbox = item.querySelector('.custom-checkbox');
                    this.handleMonthYearSelection(item.dataset.value, checkbox, item);
                    setTimeout(() => this.applyFilters(), 100);
                });
            });

            // Фильтр по формату
            this.container.querySelectorAll('#formatDropdown .dropdown-item-custom').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const checkbox = item.querySelector('.custom-checkbox');
                    this.handleFormatSelection(item.dataset.value, checkbox, item);
                    setTimeout(() => this.applyFilters(), 100);
                });
            });
        }

        handleProgramTypeSelection(value, checkbox) {
            if (value === 'all') {
                const allChecked = checkbox.classList.contains('checked');
                this.container.querySelectorAll('#programTypeDropdown .custom-checkbox').forEach(cb => {
                    cb.classList.toggle('checked', !allChecked);
                });
                if (!allChecked) {
                    const typesJson = document.getElementById('programTypesJson');
                    this.filters.programTypes = typesJson ? JSON.parse(typesJson.textContent) : [];
                } else {
                    this.filters.programTypes = [];
                }
            } else {
                checkbox.classList.toggle('checked');
                if (checkbox.classList.contains('checked')) {
                    if (!this.filters.programTypes.includes(value)) {
                        this.filters.programTypes.push(value);
                    }
                } else {
                    this.filters.programTypes = this.filters.programTypes.filter(type => type !== value);
                }
                this.updateAllCheckbox();
            }
            this.updateProgramTypeText();
        }

        updateAllCheckbox() {
            const allCheckbox = this.container.querySelector('#programTypeDropdown [data-value="all"] .custom-checkbox');
            const allItems = this.container.querySelectorAll('#programTypeDropdown .dropdown-item-custom:not([data-value="all"])');
            const allChecked = Array.from(allItems).every(item => 
                item.querySelector('.custom-checkbox').classList.contains('checked')
            );
            if (allCheckbox) allCheckbox.classList.toggle('checked', allChecked);
        }

        updateProgramTypeText() {
            const filterText = this.container.querySelector('#programTypeFilter .filter-text');
            if (!filterText) return;
            const selectedCount = this.filters.programTypes.length;
            if (selectedCount === 0) {
                filterText.textContent = 'Все программы';
            } else if (selectedCount === 1) {
                const selectedType = this.filters.programTypes[0];
                const selectedItem = this.container.querySelector(`#programTypeDropdown [data-value="${selectedType}"] span`);
                filterText.textContent = selectedItem ? selectedItem.textContent : 'Выбрано: 1';
            } else {
                filterText.textContent = `Выбрано: ${selectedCount}`;
            }
        }

        handleFormatSelection(value, checkbox, item) {
            this.container.querySelectorAll('#formatDropdown .custom-checkbox').forEach(cb => cb.classList.remove('checked'));
            checkbox.classList.add('checked');
            this.filters.format = value;
            this.container.querySelector('#formatFilter .filter-text').textContent = item.querySelector('span').textContent;
            document.getElementById('formatDropdown')?.classList.remove('show');
            document.getElementById('formatFilter')?.setAttribute('aria-expanded', 'false');
        }

        handleMonthYearSelection(value, checkbox, item) {
            this.container.querySelectorAll('#monthYearDropdown .custom-checkbox').forEach(cb => cb.classList.remove('checked'));
            checkbox.classList.add('checked');
            this.filters.monthYear = value;
            this.container.querySelector('#monthYearFilter .filter-text').textContent = item.querySelector('span').textContent;
            document.getElementById('monthYearDropdown')?.classList.remove('show');
            document.getElementById('monthYearFilter')?.setAttribute('aria-expanded', 'false');
        }

        initCalendar() {
            this.generateCalendar();
            this.setupCalendarNavigation();
        }

        generateCalendar() {
            const calendarDates = document.getElementById('calendarDates');
            if (!calendarDates) return;
            const today = new Date();
            calendarDates.innerHTML = '';

            let currentDate = new Date(today);
            const dayOfWeek = currentDate.getDay();
            const diff = currentDate.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
            currentDate.setDate(diff);

            for (let week = 0; week < 4; week++) {
                const weekDiv = document.createElement('div');
                weekDiv.className = 'calendar-week';
                for (let day = 0; day < 7; day++) {
                    const dayName = ['пн','вт','ср','чт','пт','сб','вс'][day];
                    const dayNumber = currentDate.getDate();
                    const isWeekend = day === 5 || day === 6;
                    const isToday = this.isToday(currentDate);

                    const dayDiv = document.createElement('div');
                    dayDiv.className = `calendar-day ${isWeekend ? 'weekend' : ''} ${isToday ? 'today' : ''}`;
                    dayDiv.dataset.date = currentDate.toISOString().split('T')[0];
                    dayDiv.innerHTML = `
                        <div class="day-name">${dayName}</div>
                        <div class="day-number">${dayNumber.toString().padStart(2, '0')}</div>
                    `;
                    dayDiv.addEventListener('click', () => this.handleDateSelection(dayDiv.dataset.date));
                    weekDiv.appendChild(dayDiv);
                    currentDate.setDate(currentDate.getDate() + 1);
                }
                calendarDates.appendChild(weekDiv);
            }
        }

        isToday(date) {
            const today = new Date();
            return date.getDate() === today.getDate() &&
                   date.getMonth() === today.getMonth() &&
                   date.getFullYear() === today.getFullYear();
        }

        setupCalendarNavigation() {
            const datesWrapper = document.querySelector('.calendar-dates-wrapper');
            const dates = document.querySelector('.calendar-dates');
            const prevBtn = document.querySelector('.prev-btn');
            const nextBtn = document.querySelector('.next-btn');

            let scrollPosition = 0;
            if (prevBtn && nextBtn && datesWrapper) {
                const scrollAmount = () => datesWrapper.clientWidth * 0.8;

                prevBtn.addEventListener('click', () => {
                    scrollPosition = Math.max(scrollPosition - scrollAmount(), 0);
                    dates.style.transform = `translateX(-${scrollPosition}px)`;
                    this.updateNavButtons(scrollPosition, dates, datesWrapper);
                });
                nextBtn.addEventListener('click', () => {
                    const maxScroll = dates.scrollWidth - datesWrapper.clientWidth;
                    scrollPosition = Math.min(scrollPosition + scrollAmount(), maxScroll);
                    dates.style.transform = `translateX(-${scrollPosition}px)`;
                    this.updateNavButtons(scrollPosition, dates, datesWrapper);
                });
                this.updateNavButtons(scrollPosition, dates, datesWrapper);
            }
        }

        updateNavButtons(scrollPosition, dates, datesWrapper) {
            const prevBtn = document.querySelector('.prev-btn');
            const nextBtn = document.querySelector('.next-btn');
            const maxScroll = dates.scrollWidth - datesWrapper.clientWidth;
            if (prevBtn) prevBtn.disabled = scrollPosition <= 0;
            if (nextBtn) nextBtn.disabled = scrollPosition >= maxScroll;
        }

        handleDateSelection(date) {
            document.querySelectorAll('.calendar-day').forEach(day => {
                day.classList.remove('active', 'date-filter-active');
            });
            const selectedDay = document.querySelector(`.calendar-day[data-date="${date}"]`);
            if (selectedDay) selectedDay.classList.add('active', 'date-filter-active');

            this.filters.selectedDate = date;
            this.applyFilters();
        }

        applyFilters() {
            const departmentWrappers = document.querySelectorAll('.department-card-wrapper');
            let visibleCount = 0;

            departmentWrappers.forEach(wrapper => {
                if (this.cardMatchesFilters(wrapper)) {
                    wrapper.classList.remove('hidden');
                    visibleCount++;
                } else {
                    wrapper.classList.add('hidden');
                }
            });

            this.updateResultsCount(visibleCount);
            this.showNoResultsMessage(visibleCount);
        }

        cardMatchesFilters(wrapper) {
            const deptId = parseInt(wrapper.dataset.departmentId);
            if (!deptId) return false;

            // Фильтр по типу программы
            let typeMatch = true;
            if (this.filters.programTypes.length > 0) {
                typeMatch = this.filters.programTypes.some(pt => 
                    this.filterMaps.program_type[pt]?.includes(deptId)
                );
            }

            // Фильтр по месяцу/году
            let monthYearMatch = true;
            if (this.filters.monthYear !== 'all') {
                monthYearMatch = this.filterMaps.month_year[this.filters.monthYear]?.includes(deptId) || false;
            }

            // Фильтр по формату
            let formatMatch = true;
            if (this.filters.format !== 'all') {
                formatMatch = this.filterMaps.format[this.filters.format]?.includes(deptId) || false;
            }

            // Фильтр по дате
            let dateMatch = true;
            if (this.filters.selectedDate) {
                dateMatch = this.filterMaps.date[this.filters.selectedDate]?.includes(deptId) || false;
            }

            return typeMatch && formatMatch && monthYearMatch && dateMatch;
        }

        updateResultsCount(count) {
            const countElement = document.getElementById('departmentsCount');
            if (countElement) countElement.textContent = count;
        }

        showNoResultsMessage(visibleCount) {
            const departmentsList = document.getElementById('departmentsList');
            if (!departmentsList) return;
            const existingNoDepts = departmentsList.querySelector('.no-departments');
            if (visibleCount === 0) {
                if (!existingNoDepts) {
                    const noDeptsHTML = `
                        <div class="col-12">
                            <div class="no-departments">
                                <i class="fas fa-inbox"></i>
                                <p>Отделения не найдены. Попробуйте изменить параметры фильтрации.</p>
                            </div>
                        </div>
                    `;
                    departmentsList.insertAdjacentHTML('beforeend', noDeptsHTML);
                }
            } else {
                if (existingNoDepts) existingNoDepts.remove();
            }
        }
    }

    if (document.querySelector('.department-card-wrapper')) {
        new DepartmentsFilter();
    }

    // ===== Управление модальными окнами для знаков вопроса =====
    const methodQuestionMarks = document.querySelectorAll('.method-question');
    const methodModals = {
        modal1: document.getElementById('methodModal1'),
        modal2: document.getElementById('methodModal2'),
        modal3: document.getElementById('methodModal3')
    };

    methodQuestionMarks.forEach((mark, index) => {
        mark.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            const modalId = this.getAttribute('data-modal') || `methodModal${index + 1}`;
            const modal = document.getElementById(modalId);

            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });

    document.querySelectorAll('.method-modal').forEach(modal => {
        const closeBtn = modal.querySelector('.method-modal-close');
        const overlay = modal.querySelector('.modal-overlay');

        if (closeBtn) {
            closeBtn.addEventListener('click', () => closeMethodModal(modal));
        }
        if (overlay) {
            overlay.addEventListener('click', () => closeMethodModal(modal));
        }
    });

    // إغلاق نافذة عدم السماح
    const notAllowedModal = document.getElementById('userTypeNotAllowedModal');
    if (notAllowedModal) {
        const closeBtn = notAllowedModal.querySelector('.method-modal-close');
        const overlay = notAllowedModal.querySelector('.modal-overlay');
        if (closeBtn) closeBtn.addEventListener('click', () => closeMethodModal(notAllowedModal));
        if (overlay) overlay.addEventListener('click', () => closeMethodModal(notAllowedModal));
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.method-modal.active').forEach(modal => {
                closeMethodModal(modal);
            });
        }
    });

    document.querySelectorAll('.method-modal-content').forEach(content => {
        content.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });

    // Обработка кнопок внутри модальных окон (Показать на карте, Поделиться, Авторизоваться)
    document.querySelectorAll('.method-modal').forEach(modal => {
        const btn = modal.querySelector('.method-modal-btn');
        if (!btn) return;

        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const buttonText = this.textContent.trim();

            if (buttonText.includes('Показать на карте')) {
                const address = encodeURIComponent('г. Москва, Садовая-Спасская 19к1');
                const mapUrl = `https://www.google.com/maps/search/?api=1&query=${address}`;
                window.open(mapUrl, '_blank');
            }
            else if (buttonText.includes('Поделиться')) {
                const shareData = {
                    title: 'ФТА НИЯУ МИФИ',
                    text: 'Наша почта: info.fta@mail.ru',
                    url: window.location.href
                };

                if (navigator.share) {
                    navigator.share(shareData).catch(err => {
                        console.log('Поделиться отменено или ошибка:', err);
                    });
                } else {
                    navigator.clipboard?.writeText('info.fta@mail.ru').then(() => {
                        alert('Email скопирован: info.fta@mail.ru');
                    }).catch(() => {
                        window.location.href = 'mailto:info.fta@mail.ru';
                    });
                }
            }
            else if (buttonText.includes('Авторизироваться')) {
                window.location.href = '/accounts/login/';
            }
        });
    });

    // ===== Поиск и статус авторизации =====
    const searchBtn = document.querySelector('.search-btn');
    const snilsSearchModal = document.getElementById('snilsSearchModal');

    if (searchBtn) {
        searchBtn.addEventListener('click', function(e) {
            if (!window.userAuthenticated) {
                e.preventDefault();
                if (snilsSearchModal) {
                    snilsSearchModal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            } else {
                console.log('Пользователь авторизован, выполняется поиск');
            }
        });
    }

    if (snilsSearchModal) {
        const closeBtn = snilsSearchModal.querySelector('.method-modal-close');
        const overlay = snilsSearchModal.querySelector('.modal-overlay');

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                snilsSearchModal.classList.remove('active');
                document.body.style.overflow = 'auto';
            });
        }

        if (overlay) {
            overlay.addEventListener('click', () => {
                snilsSearchModal.classList.remove('active');
                document.body.style.overflow = 'auto';
            });
        }

        const authBtn = document.getElementById('snilsAuthBtn');
        if (authBtn) {
            authBtn.addEventListener('click', function() {
                window.location.href = '/accounts/login/';
            });
        }
    }
});