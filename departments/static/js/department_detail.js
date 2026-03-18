// department_detail.js – النسخة النهائية بعد التعديلات
document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // ========== فلتر البرامج في صفحة القسم ==========
    class DepartmentProgramFilter {
        constructor() {
            this.filters = {
                selectedDate: null,
                search: ''
            };
            this.init();
        }

        init() {
            this.initCalendar();
            this.setupSearch();
            this.applyFilters();
        }

        // ---------- التقويم ----------
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
                    const dayName = this.getDayName(day);
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

                    dayDiv.addEventListener('click', () => {
                        this.handleDateSelection(dayDiv.dataset.date);
                    });

                    weekDiv.appendChild(dayDiv);
                    currentDate.setDate(currentDate.getDate() + 1);
                }
                calendarDates.appendChild(weekDiv);
            }
        }

        getDayName(dayIndex) {
            const days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'];
            return days[dayIndex];
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
            if (selectedDay) {
                selectedDay.classList.add('active', 'date-filter-active');
            }

            this.filters.selectedDate = date;
            this.applyFilters();
        }

        // ---------- البحث ----------
        setupSearch() {
            const searchInput = document.getElementById('scheduleSearch');
            const searchBtn = document.getElementById('scheduleSearchBtn');

            if (searchInput && searchBtn) {
                const performSearch = () => {
                    this.filters.search = searchInput.value.trim().toLowerCase();
                    this.applyFilters();
                };

                searchBtn.addEventListener('click', performSearch);
                searchInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') performSearch();
                });
                searchInput.addEventListener('input', function() {
                    if (this.value.trim() === '') performSearch();
                });
            }
        }

        // ---------- تطبيق الفلاتر ----------
        applyFilters() {
            const programCards = document.querySelectorAll('.program-card-new');
            let visibleCount = 0;

            programCards.forEach(card => {
                if (this.cardMatchesFilters(card)) {
                    card.closest('.program-card-link').classList.remove('hidden');
                    visibleCount++;
                } else {
                    card.closest('.program-card-link').classList.add('hidden');
                }
            });

            this.updateResultsCount(visibleCount);
            this.showNoResultsMessage(visibleCount);
        }

        cardMatchesFilters(card) {
            const programDate = card.dataset.date;
            if (!programDate) return false;

            const dateMatch = !this.filters.selectedDate || this.filters.selectedDate === programDate;

            const searchTerm = this.filters.search;
            let searchMatch = true;
            if (searchTerm) {
                const title = card.dataset.title || '';
                const description = card.dataset.description || '';
                searchMatch = title.includes(searchTerm) || description.includes(searchTerm);
            }

            return dateMatch && searchMatch;
        }

        updateResultsCount(count) {
            const countElement = document.getElementById('programsCount');
            if (countElement) countElement.textContent = count;
        }

        showNoResultsMessage(visibleCount) {
            const programsGrid = document.getElementById('programsList');
            const existingNoPrograms = programsGrid.querySelector('.no-programs');

            if (visibleCount === 0) {
                if (!existingNoPrograms) {
                    const noProgramsHTML = `
                        <div class="no-programs">
                            <i class="fas fa-inbox"></i>
                            <p>Программы не найдены. Попробуйте изменить параметры фильтрации.</p>
                        </div>
                    `;
                    programsGrid.insertAdjacentHTML('beforeend', noProgramsHTML);
                }
            } else {
                if (existingNoPrograms) existingNoPrograms.remove();
            }
        }
    }

    // تشغيل الفلتر
    new DepartmentProgramFilter();

    // ========== الكاروسيل الأرشيفي – نسخة محسّنة بالكامل ==========
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
            const containerWidth = container.offsetWidth - 80; // 40px padding on each side
            const slides = document.querySelectorAll('.carousel-slide');
            if (slides.length === 0) return 1;
            const slideWidth = slides[0].offsetWidth + 24; // 24px gap
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

        // ربط أزرار التنقل – باستخدام السيلكتورات الجديدة
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