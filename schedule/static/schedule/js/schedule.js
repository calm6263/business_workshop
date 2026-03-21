// static/schedule/js/schedule.js
document.addEventListener('DOMContentLoaded', function() {
    // ================= FIXED FILTER DROPDOWNS INITIALIZATION =================
    function initializeFilterDropdowns() {
        if (window.innerWidth >= 992) {
            document.querySelectorAll('.filter-input.custom-dropdown-toggle').forEach(toggle => {
                toggle.removeAttribute('data-bs-toggle');
                toggle.removeAttribute('data-bs-auto-close');
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    const dropdownId = this.id.replace('Filter', 'Dropdown');
                    const dropdown = document.getElementById(dropdownId);
                    document.querySelectorAll('.filter-dropdown.show').forEach(d => {
                        if (d !== dropdown) d.classList.remove('show');
                    });
                    if (dropdown) {
                        dropdown.classList.toggle('show');
                        this.setAttribute('aria-expanded', dropdown.classList.contains('show'));
                    }
                });
            });
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.filter-item')) {
                    document.querySelectorAll('.filter-dropdown.show').forEach(dropdown => {
                        dropdown.classList.remove('show');
                    });
                    document.querySelectorAll('.filter-input[aria-expanded="true"]').forEach(toggle => {
                        toggle.setAttribute('aria-expanded', 'false');
                    });
                }
            });
            document.querySelectorAll('.filter-dropdown').forEach(dropdown => {
                dropdown.addEventListener('click', function(e) { e.stopPropagation(); });
            });
        }
    }
    initializeFilterDropdowns();
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(initializeFilterDropdowns, 250);
    });

    // ================= FIXED FILTER CLASS =================
    class FixedScheduleFilter {
        constructor() {
            this.filters = {
                programTypes: [],
                format: 'all',
                monthYear: 'all',
                selectedDate: null,
                search: ''
            };
            this.init();
        }

        init() {
            this.setupFilterSelections();
            this.initCalendar();
            this.applyFilters();
        }

        setupFilterSelections() {
            document.querySelectorAll('#programTypeDropdown .dropdown-item-custom').forEach(item => {
                item.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const checkbox = item.querySelector('.custom-checkbox');
                    this.handleProgramTypeSelection(item.dataset.value, checkbox, item);
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
        }

        handleProgramTypeSelection(value, checkbox, item) {
            if (value === 'all') {
                const allChecked = checkbox.classList.contains('checked');
                document.querySelectorAll('#programTypeDropdown .custom-checkbox').forEach(cb => {
                    cb.classList.toggle('checked', !allChecked);
                });
                if (!allChecked) {
                    try {
                        const programTypesJson = document.getElementById('programTypesJson');
                        if (programTypesJson) {
                            this.filters.programTypes = JSON.parse(programTypesJson.textContent);
                        } else {
                            this.filters.programTypes = ['professional_retraining', 'qualification_upgrade', 'seminar', 'training', 'other'];
                        }
                    } catch (e) {
                        this.filters.programTypes = ['professional_retraining', 'qualification_upgrade', 'seminar', 'training', 'other'];
                    }
                } else {
                    this.filters.programTypes = [];
                }
            } else {
                checkbox.classList.toggle('checked');
                if (checkbox.classList.contains('checked')) {
                    if (!this.filters.programTypes.includes(value)) this.filters.programTypes.push(value);
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
            const allChecked = Array.from(allItems).every(item => item.querySelector('.custom-checkbox').classList.contains('checked'));
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
            const formatText = item.querySelector('span').textContent;
            document.querySelector('#formatFilter .filter-text').textContent = formatText;
            const dropdown = document.getElementById('formatDropdown');
            if (dropdown) dropdown.classList.remove('show');
            document.getElementById('formatFilter').setAttribute('aria-expanded', 'false');
        }

        handleMonthYearSelection(value, checkbox, item) {
            document.querySelectorAll('#monthYearDropdown .custom-checkbox').forEach(cb => cb.classList.remove('checked'));
            checkbox.classList.add('checked');
            this.filters.monthYear = value;
            const monthYearText = item.querySelector('span').textContent;
            document.querySelector('#monthYearFilter .filter-text').textContent = monthYearText;
            const dropdown = document.getElementById('monthYearDropdown');
            if (dropdown) dropdown.classList.remove('show');
            document.getElementById('monthYearFilter').setAttribute('aria-expanded', 'false');
        }

        initCalendar() {
            this.generateCalendar();
            this.setupCalendarNavigation();
        }

        // توليد الجدول باستخدام التاريخ المحلي
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
                    const dayName = this.getDayName(day);
                    const dayNumber = currentDate.getDate();
                    const isWeekend = day === 5 || day === 6;
                    const year = currentDate.getFullYear();
                    const month = String(currentDate.getMonth() + 1).padStart(2, '0');
                    const dayStr = String(dayNumber).padStart(2, '0');
                    const dateStr = `${year}-${month}-${dayStr}`;
                    const isToday = this.isToday(currentDate);

                    const dayDiv = document.createElement('div');
                    dayDiv.className = `calendar-day ${isWeekend ? 'weekend' : ''} ${isToday ? 'active' : ''}`;
                    dayDiv.dataset.date = dateStr;
                    dayDiv.innerHTML = `
                        <div class="day-name">${dayName}</div>
                        <div class="day-number">${dayNumber.toString().padStart(2, '0')}</div>
                    `;
                    dayDiv.addEventListener('click', () => { this.handleDateSelection(dayDiv.dataset.date); });
                    weekDiv.appendChild(dayDiv);
                    currentDate.setDate(currentDate.getDate() + 1);
                }
                calendarDates.appendChild(weekDiv);
            }
        }

        getDayName(dayIndex) { const days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']; return days[dayIndex]; }
        
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
            const scrollAmount = 500;
            if (prevBtn && nextBtn) {
                prevBtn.addEventListener('click', () => {
                    scrollPosition = Math.max(scrollPosition - scrollAmount, 0);
                    dates.style.transform = `translateX(-${scrollPosition}px)`;
                    this.updateNavButtons(scrollPosition, dates, datesWrapper);
                });
                nextBtn.addEventListener('click', () => {
                    const maxScroll = dates.scrollWidth - datesWrapper.clientWidth;
                    scrollPosition = Math.min(scrollPosition + scrollAmount, maxScroll);
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

        // ========== عند اختيار تاريخ، نعيد ضبط فلتر الشهر/السنة ==========
        handleDateSelection(date) {
            // إزالة التحديد من جميع الأيام السابقة
            document.querySelectorAll('.calendar-day').forEach(day => day.classList.remove('active', 'date-filter-active'));
            const selectedDay = document.querySelector(`.calendar-day[data-date="${date}"]`);
            if (selectedDay) selectedDay.classList.add('active', 'date-filter-active');

            // تعيين التاريخ المختار في الفلتر
            this.filters.selectedDate = date;

            // إعادة ضبط فلتر الشهر/السنة إلى "كل الأشهر" لأن اختيار تاريخ محدد يلغيه
            if (this.filters.monthYear !== 'all') {
                this.filters.monthYear = 'all';
                // تحديث واجهة فلتر الشهر/السنة
                const monthYearFilterText = document.querySelector('#monthYearFilter .filter-text');
                if (monthYearFilterText) monthYearFilterText.textContent = 'Все месяцы';
                // إلغاء تحديد جميع خانات الاختيار في القائمة المنسدلة للشهر/السنة
                document.querySelectorAll('#monthYearDropdown .custom-checkbox').forEach(cb => cb.classList.remove('checked'));
                const allCheckbox = document.querySelector('#monthYearDropdown [data-value="all"] .custom-checkbox');
                if (allCheckbox) allCheckbox.classList.add('checked');
            }

            // تطبيق الفلاتر
            this.applyFilters();
        }

        applyFilters() {
            const programCards = document.querySelectorAll('.program-card-new');
            const monthSections = document.querySelectorAll('.month-section');
            let visibleCount = 0;

            programCards.forEach(card => {
                if (this.cardMatchesFilters(card)) {
                    card.closest('.program-card-link').classList.remove('hidden');
                    visibleCount++;
                } else {
                    card.closest('.program-card-link').classList.add('hidden');
                }
            });

            monthSections.forEach(section => {
                const visibleCards = section.querySelectorAll('.program-card-link:not(.hidden)');
                const programsCountElement = section.querySelector('.programs-count');
                const monthId = section.getAttribute('data-month-year');
                const programsContainer = document.getElementById(`programs-${monthId}`);
                const toggleBtn = section.querySelector('.month-toggle');
                if (visibleCards.length > 0) {
                    section.classList.remove('hidden');
                    if (programsCountElement) programsCountElement.textContent = `${visibleCards.length} программ`;
                    if (programsContainer) {
                        programsContainer.classList.remove('collapsed');
                        if (toggleBtn) toggleBtn.classList.remove('collapsed');
                    }
                } else {
                    section.classList.add('hidden');
                    if (programsContainer) {
                        programsContainer.classList.add('collapsed');
                        if (toggleBtn) toggleBtn.classList.add('collapsed');
                    }
                }
            });
            this.updateResultsCount(visibleCount);
        }

        cardMatchesFilters(card) {
            const programType = card.dataset.programType;
            const programFormat = card.dataset.format;
            const programDate = card.dataset.date;
            const programTitle = (card.dataset.title || '').toLowerCase();
            const programDesc = (card.dataset.description || '').toLowerCase();

            if (!programDate) return false;
            const [programYear, programMonth] = programDate.split('-');
            const programMonthYear = `${programYear}-${programMonth}`;

            const typeMatch = this.filters.programTypes.length === 0 || this.filters.programTypes.includes(programType);
            const formatMatch = this.filters.format === 'all' || this.filters.format === programFormat;
            const monthYearMatch = this.filters.monthYear === 'all' || this.filters.monthYear === programMonthYear;
            const dateMatch = !this.filters.selectedDate || this.filters.selectedDate === programDate;

            const searchTerm = this.filters.search.toLowerCase();
            const searchMatch = !searchTerm || programTitle.includes(searchTerm) || programDesc.includes(searchTerm);

            return typeMatch && formatMatch && monthYearMatch && dateMatch && searchMatch;
        }

        updateResultsCount(count) {
            const countElement = document.getElementById('programsCount');
            if (countElement) countElement.textContent = count;
        }
    }

    window.scheduleFilter = new FixedScheduleFilter();

    // ================= MONTH TOGGLE FUNCTIONALITY =================
    window.toggleMonth = function(monthId) {
        const programsContainer = document.getElementById(`programs-${monthId}`);
        const toggleBtn = document.querySelector(`.month-toggle[data-month="${monthId}"]`);
        if (programsContainer && toggleBtn) {
            programsContainer.classList.toggle('collapsed');
            toggleBtn.classList.toggle('collapsed');
        }
    };

    setTimeout(() => {
        const monthSections = document.querySelectorAll('.month-section');
        monthSections.forEach((section, index) => {
            const monthId = section.getAttribute('data-month-year');
            const programsContainer = document.getElementById(`programs-${monthId}`);
            const toggleBtn = section.querySelector('.month-toggle');
            if (programsContainer && toggleBtn) {
                if (index < 2) {
                    programsContainer.classList.remove('collapsed');
                    toggleBtn.classList.remove('collapsed');
                } else {
                    programsContainer.classList.add('collapsed');
                    toggleBtn.classList.add('collapsed');
                }
            }
        });
    }, 100);

    // ================= SLIDER FUNCTIONALITY =================
    const mainSlider = document.getElementById('mainSlider');
    if (mainSlider) {
        const slides = mainSlider.querySelectorAll('.slider-slide');
        const sliderDots = document.getElementById('sliderDots');
        const prevBtn = document.querySelector('.slider-prev');
        const nextBtn = document.querySelector('.slider-next');
        let currentSlide = 0;
        const totalSlides = slides.length;
        function createSliderDots() { sliderDots.innerHTML = ''; for (let i=0; i<totalSlides; i++) { const dot = document.createElement('button'); dot.className = 'slider-dot'; dot.setAttribute('aria-label', `Перейти к слайду ${i+1}`); dot.addEventListener('click', () => goToSlide(i)); sliderDots.appendChild(dot); } updateSliderDots(); }
        function updateSliderDots() { const dots = sliderDots.querySelectorAll('.slider-dot'); dots.forEach((dot, index) => { dot.classList.toggle('active', index === currentSlide); }); }
        function goToSlide(slideIndex) { currentSlide = slideIndex; if (currentSlide < 0) currentSlide = totalSlides - 1; if (currentSlide >= totalSlides) currentSlide = 0; mainSlider.style.transform = `translateX(-${currentSlide * 100}%)`; updateSliderDots(); resetAutoSlide(); }
        function nextSlide() { goToSlide(currentSlide + 1); }
        function prevSlide() { goToSlide(currentSlide - 1); }
        if (prevBtn) prevBtn.addEventListener('click', prevSlide);
        if (nextBtn) nextBtn.addEventListener('click', nextSlide);
        createSliderDots();
        let autoSlideInterval;
        function startAutoSlide() { autoSlideInterval = setInterval(nextSlide, 5000); }
        function resetAutoSlide() { clearInterval(autoSlideInterval); startAutoSlide(); }
        startAutoSlide();
        mainSlider.addEventListener('mouseenter', () => { clearInterval(autoSlideInterval); });
        mainSlider.addEventListener('mouseleave', () => { startAutoSlide(); });
        let isDragging = false, startPos = 0;
        mainSlider.addEventListener('touchstart', (e) => { isDragging = true; startPos = e.touches[0].clientX; mainSlider.style.transition = 'none'; });
        mainSlider.addEventListener('touchmove', (e) => { if (!isDragging) return; const diff = e.touches[0].clientX - startPos; mainSlider.style.transform = `translateX(calc(-${currentSlide * 100}% + ${diff}px))`; });
        mainSlider.addEventListener('touchend', (e) => { isDragging = false; mainSlider.style.transition = 'transform 0.5s ease'; const movedBy = e.changedTouches[0].clientX - startPos; if (movedBy < -50) nextSlide(); else if (movedBy > 50) prevSlide(); else mainSlider.style.transform = `translateX(-${currentSlide * 100}%)`; });
    }

    // ================= ARCHIVE CAROUSEL =================
    const archiveCarousel = document.getElementById('archiveCarousel');
    const carouselDots = document.getElementById('carouselDots');
    if (archiveCarousel && carouselDots) {
        const slides = archiveCarousel.querySelectorAll('.carousel-slide');
        const totalSlides = slides.length;
        let currentSlide = 0;
        function getSlidesPerView() { if (window.innerWidth >= 1200) return 4; if (window.innerWidth >= 992) return 3; if (window.innerWidth >= 768) return 2; return 1; }
        function createDots() { carouselDots.innerHTML = ''; const slidesPerView = getSlidesPerView(); const dotsCount = Math.ceil(totalSlides / slidesPerView); for (let i=0; i<dotsCount; i++) { const dot = document.createElement('button'); dot.className = 'carousel-dot'; dot.setAttribute('aria-label', `Перейти к слайду ${i+1}`); dot.addEventListener('click', () => goToSlide(i)); carouselDots.appendChild(dot); } updateDots(); }
        function updateDots() { const dots = carouselDots.querySelectorAll('.carousel-dot'); const slidesPerView = getSlidesPerView(); const activeDotIndex = Math.floor(currentSlide / slidesPerView); dots.forEach((dot, index) => { dot.classList.toggle('active', index === activeDotIndex); }); }
        function goToSlide(slideIndex) { const slidesPerView = getSlidesPerView(); currentSlide = slideIndex * slidesPerView; if (currentSlide >= totalSlides) currentSlide = 0; updateCarouselPosition(); updateDots(); }
        function updateCarouselPosition() { const slidesPerView = getSlidesPerView(); const slideWidth = slides[0].offsetWidth + 24; if (currentSlide + slidesPerView > totalSlides) currentSlide = totalSlides - slidesPerView; if (currentSlide < 0) currentSlide = 0; const translateX = -currentSlide * slideWidth; archiveCarousel.style.transform = `translateX(${translateX}px)`; }
        function nextSlide() { const slidesPerView = getSlidesPerView(); currentSlide += slidesPerView; if (currentSlide >= totalSlides) currentSlide = 0; updateCarouselPosition(); updateDots(); }
        function prevSlide() { const slidesPerView = getSlidesPerView(); currentSlide -= slidesPerView; if (currentSlide < 0) currentSlide = totalSlides - slidesPerView; if (currentSlide < 0) currentSlide = 0; updateCarouselPosition(); updateDots(); }
        document.querySelector('.carousel-next')?.addEventListener('click', nextSlide);
        document.querySelector('.carousel-prev')?.addEventListener('click', prevSlide);
        createDots();
        window.addEventListener('resize', () => { updateCarouselPosition(); createDots(); });
        let isDragging = false, startPos = 0, currentTranslate = 0, prevTranslate = 0;
        archiveCarousel.addEventListener('touchstart', (e) => { isDragging = true; startPos = e.touches[0].clientX; archiveCarousel.style.transition = 'none'; });
        archiveCarousel.addEventListener('touchmove', (e) => { if (!isDragging) return; const diff = e.touches[0].clientX - startPos; archiveCarousel.style.transform = `translateX(${currentTranslate + diff}px)`; });
        archiveCarousel.addEventListener('touchend', (e) => { isDragging = false; archiveCarousel.style.transition = 'transform 0.3s ease'; const movedBy = e.changedTouches[0].clientX - startPos; if (movedBy < -50) nextSlide(); else if (movedBy > 50) prevSlide(); else updateCarouselPosition(); });
        let autoSlideInterval = setInterval(nextSlide, 5000);
        archiveCarousel.addEventListener('mouseenter', () => { clearInterval(autoSlideInterval); });
        archiveCarousel.addEventListener('mouseleave', () => { autoSlideInterval = setInterval(nextSlide, 5000); });
    }

    // ================= SEARCH FUNCTIONALITY =================
    const searchInput = document.getElementById('scheduleSearch');
    const searchBtn = document.getElementById('scheduleSearchBtn');
    if (searchInput && searchBtn && window.scheduleFilter) {
        const performSearch = () => {
            window.scheduleFilter.filters.search = searchInput.value.trim();
            window.scheduleFilter.applyFilters();
        };
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', function(e) { if (e.key === 'Enter') performSearch(); });
        searchInput.addEventListener('input', function() { if (this.value.trim() === '') performSearch(); });
    }

    // ================= FIX FOR MOBILE FILTER DROPDOWNS =================
    function setupMobileFilterDropdowns() {
        if (window.innerWidth <= 768) {
            const filterToggles = document.querySelectorAll('.filter-input.custom-dropdown-toggle');
            const backdrop = document.createElement('div');
            backdrop.className = 'dropdown-backdrop';
            document.body.appendChild(backdrop);
            filterToggles.forEach(toggle => {
                const newToggle = toggle.cloneNode(true);
                toggle.parentNode.replaceChild(newToggle, toggle);
                newToggle.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    const dropdownId = this.id.replace('Filter', 'Dropdown');
                    const dropdown = document.getElementById(dropdownId);
                    document.querySelectorAll('.filter-dropdown.show').forEach(d => { if (d !== dropdown) d.classList.remove('show'); });
                    if (dropdown) {
                        dropdown.classList.toggle('show');
                        backdrop.classList.toggle('active', dropdown.classList.contains('show'));
                    }
                });
            });
            backdrop.addEventListener('click', function() {
                document.querySelectorAll('.filter-dropdown.show').forEach(dropdown => dropdown.classList.remove('show'));
                this.classList.remove('active');
            });
            document.querySelectorAll('.filter-dropdown .dropdown-item-custom').forEach(item => {
                item.addEventListener('click', function(e) {
                    setTimeout(() => {
                        const dropdown = this.closest('.filter-dropdown');
                        if (dropdown) dropdown.classList.remove('show');
                        backdrop.classList.remove('active');
                    }, 300);
                });
            });
        }
    }
    if (window.innerWidth <= 768) setupMobileFilterDropdowns();
    window.addEventListener('resize', function() { if (window.innerWidth <= 768) setupMobileFilterDropdowns(); });

    // ================= CALENDAR ICON CLICK =================
    const calendarIcon = document.querySelector('.filter-icon');
    if (calendarIcon) calendarIcon.addEventListener('click', () => { window.location.href = '/schedule/calendar/'; });
});