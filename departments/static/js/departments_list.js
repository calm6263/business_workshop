// departments_list.js – النسخة النهائية (مع إضافة كاروسيل الأرشيف)
document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // ========== تهيئة القوائم المنسدلة – إصدار لا يستنسخ العناصر ==========
    function initFilterDropdowns() {
        const isMobile = window.matchMedia('(max-width: 768px)').matches;

        document.querySelectorAll('.filter-input.custom-dropdown-toggle').forEach(toggle => {
            const newToggle = toggle.cloneNode(true);
            toggle.parentNode.replaceChild(newToggle, toggle);
        });

        document.querySelectorAll('.filter-input.custom-dropdown-toggle').forEach(toggle => {
            const dropdownId = toggle.id.replace('Filter', 'Dropdown');
            const dropdown = document.getElementById(dropdownId);

            if (isMobile) {
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();

                    document.querySelectorAll('.filter-dropdown.show').forEach(d => {
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

                    document.querySelectorAll('.filter-dropdown.show').forEach(d => {
                        if (d !== dropdown) d.classList.remove('show');
                    });

                    if (dropdown) {
                        dropdown.classList.toggle('show');
                        toggle.setAttribute('aria-expanded', dropdown.classList.contains('show'));
                    }
                });
            }
        });

        document.addEventListener('click', function(e) {
            if (!e.target.closest('.filter-item')) {
                document.querySelectorAll('.filter-dropdown.show').forEach(dropdown => {
                    dropdown.classList.remove('show');
                });
                document.querySelectorAll('.filter-input[aria-expanded="true"]').forEach(toggle => {
                    toggle.setAttribute('aria-expanded', 'false');
                });
                document.querySelector('.dropdown-backdrop')?.classList.remove('active');
            }
        });

        document.querySelectorAll('.filter-dropdown').forEach(dropdown => {
            dropdown.addEventListener('click', e => e.stopPropagation());
        });
    }

    initFilterDropdowns();
    window.matchMedia('(max-width: 768px)').addEventListener('change', initFilterDropdowns);

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

    // ========== كلاس الفلتر الرئيسي ==========
    class DepartmentsFilter {
        constructor() {
            this.filters = {
                programTypes: [],
                format: 'all',
                monthYear: 'all',
                selectedDate: null,
                search: ''
            };

            this.filterMaps = { format: {}, month_year: {}, date: {}, program_type: {} };
            const filterMapsEl = document.getElementById('filterMapsJson');
            if (filterMapsEl) {
                try {
                    this.filterMaps = JSON.parse(filterMapsEl.textContent);
                    this.filterMaps.program_type = this.filterMaps.program_type || {};
                } catch(e) {
                    console.error('Invalid filter maps JSON', e);
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
            const allCheckbox = document.querySelector('#programTypeDropdown [data-value="all"] .custom-checkbox');
            if (!allCheckbox) return;
            const anyChecked = document.querySelectorAll('#programTypeDropdown .dropdown-item-custom:not([data-value="all"]) .custom-checkbox.checked').length > 0;
            allCheckbox.classList.toggle('checked', !anyChecked);
        }

        setupFilterSelections() {
            document.querySelectorAll('#programTypeDropdown .dropdown-item-custom').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const checkbox = item.querySelector('.custom-checkbox');
                    this.handleProgramTypeSelection(item.dataset.value, checkbox);
                    setTimeout(() => this.applyFilters(), 100);
                });
            });

            document.querySelectorAll('#formatDropdown .dropdown-item-custom').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const checkbox = item.querySelector('.custom-checkbox');
                    this.handleFormatSelection(item.dataset.value, checkbox, item);
                    setTimeout(() => this.applyFilters(), 100);
                });
            });

            document.querySelectorAll('#monthYearDropdown .dropdown-item-custom').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const checkbox = item.querySelector('.custom-checkbox');
                    this.handleMonthYearSelection(item.dataset.value, checkbox, item);
                    setTimeout(() => this.applyFilters(), 100);
                });
            });

            const searchInput = document.getElementById('departmentsSearch');
            const searchBtn = document.getElementById('departmentsSearchBtn');
            if (searchInput && searchBtn) {
                const performSearch = () => {
                    this.filters.search = searchInput.value.trim().toLowerCase();
                    this.applyFilters();
                };
                searchBtn.addEventListener('click', performSearch);
                searchInput.addEventListener('keypress', e => { if (e.key === 'Enter') performSearch(); });
                searchInput.addEventListener('input', function() {
                    if (this.value.trim() === '') {
                        this.filters.search = '';
                        this.applyFilters();
                    }
                }.bind(this));
            }
        }

        handleProgramTypeSelection(value, checkbox) {
            if (value === 'all') {
                const allChecked = checkbox.classList.contains('checked');
                document.querySelectorAll('#programTypeDropdown .custom-checkbox').forEach(cb => {
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
            const allCheckbox = document.querySelector('#programTypeDropdown [data-value="all"] .custom-checkbox');
            const allItems = document.querySelectorAll('#programTypeDropdown .dropdown-item-custom:not([data-value="all"])');
            const allChecked = Array.from(allItems).every(item => 
                item.querySelector('.custom-checkbox').classList.contains('checked')
            );
            if (allCheckbox) allCheckbox.classList.toggle('checked', allChecked);
        }

        updateProgramTypeText() {
            const filterText = document.querySelector('#programTypeFilter .filter-text');
            if (!filterText) return;
            const selectedCount = this.filters.programTypes.length;
            if (selectedCount === 0) {
                filterText.textContent = 'Все программы';
            } else if (selectedCount === 1) {
                const selectedType = this.filters.programTypes[0];
                const selectedItem = document.querySelector(`#programTypeDropdown [data-value="${selectedType}"] span`);
                filterText.textContent = selectedItem ? selectedItem.textContent : 'Выбрано: 1';
            } else {
                filterText.textContent = `Выбрано: ${selectedCount}`;
            }
        }

        handleFormatSelection(value, checkbox, item) {
            document.querySelectorAll('#formatDropdown .custom-checkbox').forEach(cb => cb.classList.remove('checked'));
            checkbox.classList.add('checked');
            this.filters.format = value;
            document.querySelector('#formatFilter .filter-text').textContent = item.querySelector('span').textContent;
            document.getElementById('formatDropdown')?.classList.remove('show');
            document.getElementById('formatFilter')?.setAttribute('aria-expanded', 'false');
        }

        handleMonthYearSelection(value, checkbox, item) {
            document.querySelectorAll('#monthYearDropdown .custom-checkbox').forEach(cb => cb.classList.remove('checked'));
            checkbox.classList.add('checked');
            this.filters.monthYear = value;
            document.querySelector('#monthYearFilter .filter-text').textContent = item.querySelector('span').textContent;
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

            let typeMatch = true;
            if (this.filters.programTypes.length > 0) {
                typeMatch = this.filters.programTypes.some(pt => 
                    this.filterMaps.program_type[pt]?.includes(deptId)
                );
            }

            const deptName = wrapper.querySelector('.department-title-top h3')?.textContent.toLowerCase() || '';
            const searchMatch = !this.filters.search || deptName.includes(this.filters.search);

            let formatMatch = true;
            if (this.filters.format !== 'all') {
                formatMatch = this.filterMaps.format[this.filters.format]?.includes(deptId) || false;
            }

            let monthYearMatch = true;
            if (this.filters.monthYear !== 'all') {
                monthYearMatch = this.filterMaps.month_year[this.filters.monthYear]?.includes(deptId) || false;
            }

            let dateMatch = true;
            if (this.filters.selectedDate) {
                dateMatch = this.filterMaps.date[this.filters.selectedDate]?.includes(deptId) || false;
            }

            return typeMatch && searchMatch && formatMatch && monthYearMatch && dateMatch;
        }

        updateResultsCount(count) {
            const countElement = document.getElementById('departmentsCount');
            if (countElement) countElement.textContent = count;
        }

        showNoResultsMessage(visibleCount) {
            const departmentsList = document.getElementById('departmentsList');
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

    if (document.querySelector('.departments-page')) {
        new DepartmentsFilter();
    }

    // ========== КАРУСЕЛЬ АРХИВНЫХ ПРОГРАММ ==========
    const archiveCarousel = document.getElementById('archiveCarousel');
    const carouselDots = document.getElementById('carouselDots');

    if (archiveCarousel && carouselDots) {
        const slides = archiveCarousel.querySelectorAll('.carousel-slide');
        const totalSlides = slides.length;
        let currentSlide = 0;
        let autoSlideInterval;

        function getSlidesPerView() {
            const container = document.querySelector('.carousel-container');
            if (!container) return 1;
            const containerWidth = container.offsetWidth - 80; // 40px padding left + right
            const slides = archiveCarousel.querySelectorAll('.carousel-slide');
            if (slides.length === 0) return 1;
            const slideWidth = slides[0].offsetWidth + 24; // 24px هو gap
            return Math.max(1, Math.floor(containerWidth / slideWidth));
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
            currentSlide = Math.max(0, Math.min(slideIndex, totalSlides - getSlidesPerView()));
            updateCarouselPosition();
            updateDots();
        }

        function updateCarouselPosition() {
            const slideWidth = slides[0]?.offsetWidth + 24 || 304;
            archiveCarousel.style.transition = 'transform 0.3s ease';
            archiveCarousel.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
        }

        function nextSlide() {
            const slidesPerView = getSlidesPerView();
            goToSlide(currentSlide + slidesPerView);
        }

        function prevSlide() {
            const slidesPerView = getSlidesPerView();
            goToSlide(currentSlide - slidesPerView);
        }

        document.querySelector('.carousel-arrow.carousel-next')?.addEventListener('click', nextSlide);
        document.querySelector('.carousel-arrow.carousel-prev')?.addEventListener('click', prevSlide);

        function startAutoSlide() {
            stopAutoSlide();
            autoSlideInterval = setInterval(nextSlide, 5000);
        }
        function stopAutoSlide() {
            clearInterval(autoSlideInterval);
        }

        let isDragging = false, startPos = 0, currentTranslate = 0, prevTranslate = 0;

        archiveCarousel.addEventListener('touchstart', (e) => {
            isDragging = true;
            startPos = e.touches[0].clientX;
            currentTranslate = prevTranslate;
            archiveCarousel.style.transition = 'none';
            stopAutoSlide();
        }, { passive: false });

        archiveCarousel.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const diff = e.touches[0].clientX - startPos;
            archiveCarousel.style.transform = `translateX(${currentTranslate + diff}px)`;
        }, { passive: false });

        archiveCarousel.addEventListener('touchend', (e) => {
            isDragging = false;
            archiveCarousel.style.transition = 'transform 0.3s ease';
            const movedBy = e.changedTouches[0].clientX - startPos;
            if (movedBy < -50) nextSlide();
            else if (movedBy > 50) prevSlide();
            else updateCarouselPosition();
            prevTranslate = -currentSlide * (slides[0]?.offsetWidth + 24);
            startAutoSlide();
        });

        archiveCarousel.addEventListener('mouseenter', stopAutoSlide);
        archiveCarousel.addEventListener('mouseleave', startAutoSlide);

        window.addEventListener('resize', () => {
            goToSlide(currentSlide);
            createDots();
        });

        createDots();
        goToSlide(0);
        startAutoSlide();
    }
});