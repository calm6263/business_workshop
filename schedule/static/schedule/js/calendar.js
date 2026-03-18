// static/schedule/js/calendar.js - النسخة النهائية المعدلة

document.addEventListener('DOMContentLoaded', function() {
    // ================= Slider Functionality =================
    const mainSlider = document.getElementById('calendarSlider');
    
    if (mainSlider) {
        const slides = mainSlider.querySelectorAll('.slider-slide');
        const sliderDots = document.getElementById('sliderDots');
        const prevBtn = document.querySelector('.slider-prev');
        const nextBtn = document.querySelector('.slider-next');
        
        let currentSlide = 0;
        const totalSlides = slides.length;
        
        // Создание точек навигации
        function createSliderDots() {
            if (!sliderDots) return;
            
            sliderDots.innerHTML = '';
            
            for (let i = 0; i < totalSlides; i++) {
                const dot = document.createElement('button');
                dot.className = 'slider-dot';
                dot.setAttribute('aria-label', `Перейти к слайду ${i + 1}`);
                dot.addEventListener('click', () => goToSlide(i));
                sliderDots.appendChild(dot);
            }
            
            updateSliderDots();
        }
        
        // Обновление активных точек
        function updateSliderDots() {
            const dots = sliderDots?.querySelectorAll('.slider-dot');
            if (!dots) return;
            
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentSlide);
            });
        }
        
        // Переход к определенному слайду
        function goToSlide(slideIndex) {
            currentSlide = slideIndex;
            if (currentSlide < 0) currentSlide = totalSlides - 1;
            if (currentSlide >= totalSlides) currentSlide = 0;
            
            mainSlider.style.transform = `translateX(-${currentSlide * 100}%)`;
            updateSliderDots();
            
            // Сброс автоматического перелистывания
            resetAutoSlide();
        }
        
        // Следующий слайд
        function nextSlide() {
            goToSlide(currentSlide + 1);
        }
        
        // Предыдущий слайд
        function prevSlide() {
            goToSlide(currentSlide - 1);
        }
        
        // Добавление событий на кнопки
        if (prevBtn) prevBtn.addEventListener('click', prevSlide);
        if (nextBtn) nextBtn.addEventListener('click', nextSlide);
        
        // Создание точек
        createSliderDots();
        
        // Автоматическое перелистывание
        let autoSlideInterval;
        
        function startAutoSlide() {
            if (totalSlides > 1) {
                autoSlideInterval = setInterval(nextSlide, 5000); // каждые 5 секунд
            }
        }
        
        function resetAutoSlide() {
            clearInterval(autoSlideInterval);
            startAutoSlide();
        }
        
        // Запуск автоматического перелистывания
        startAutoSlide();
        
        // Остановка автоматического перелистывания при взаимодействии
        mainSlider.addEventListener('mouseenter', () => {
            clearInterval(autoSlideInterval);
        });
        
        mainSlider.addEventListener('mouseleave', () => {
            startAutoSlide();
        });
        
        // Поддержка перетаскивания на телефонах
        let isDragging = false;
        let startPos = 0;
        
        mainSlider.addEventListener('touchstart', (e) => {
            isDragging = true;
            startPos = e.touches[0].clientX;
            mainSlider.style.transition = 'none';
        });
        
        mainSlider.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            const currentPosition = e.touches[0].clientX;
            const diff = currentPosition - startPos;
            mainSlider.style.transform = `translateX(calc(-${currentSlide * 100}% + ${diff}px))`;
        });
        
        mainSlider.addEventListener('touchend', (e) => {
            isDragging = false;
            mainSlider.style.transition = 'transform 0.5s ease';
            
            const movedBy = e.changedTouches[0].clientX - startPos;
            
            if (movedBy < -50) {
                nextSlide();
            } else if (movedBy > 50) {
                prevSlide();
            } else {
                mainSlider.style.transform = `translateX(-${currentSlide * 100}%)`;
            }
        });
    }
    
    // ================= وظائف التنقل السفلي =================
    // وظيفة زر العودة
    document.querySelector('.back-content')?.addEventListener('click', function() {
        window.history.back();
    });

    // وظيفة زر تحميل PDF (محدثة للرابط الجديد)
    document.querySelector('.download-content')?.addEventListener('click', function() {
        // رابط تحميل PDF من السيرفر باستخدام الدالة الجديدة
        const pdfUrl = '/schedule/download-calendar-pdf/';
        window.open(pdfUrl, '_blank');
    });
    
    // ================= Calendar Functionality (النص الأصلي) =================
    class Calendar {
        constructor() {
            this.currentDate = new Date();
            this.calendarData = window.calendarData || {};
            this.monthNames = [
                'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
            ];
            this.init();
        }

        init() {
            this.createGridLines();
            this.renderCalendar();
            this.setupEventListeners();
            this.hideBorderLines();
        }

        createGridLines() {
            const calendarGrid = document.querySelector('.calendar-grid');
            if (!calendarGrid) return;

            calendarGrid.innerHTML = '';

            // احصل على ارتفاع حاوية الأيام الفعلي
            const calendarDays = document.querySelector('.calendar-days');
            const gridHeight = calendarDays ? calendarDays.offsetHeight : 300;

            for (let i = 0; i <= 6; i++) {
                const line = document.createElement('div');
                line.className = 'calendar-horizontal-line';
                line.style.top = `${(i * 100) / 6}%`;
                if (i === 6) {
                    line.classList.add('last-row');
                }
                calendarGrid.appendChild(line);
            }

            for (let i = 0; i <= 7; i++) {
                const line = document.createElement('div');
                line.className = 'calendar-vertical-line';
                line.style.left = `${(i * 100) / 7}%`;
                if (i === 0) {
                    line.classList.add('first-column');
                }
                if (i === 7) {
                    line.classList.add('last-column');
                }
                calendarGrid.appendChild(line);
            }
        }

        hideBorderLines() {
            const verticalLines = document.querySelectorAll('.calendar-vertical-line');
            const horizontalLines = document.querySelectorAll('.calendar-horizontal-line');

            if (verticalLines.length > 0) {
                verticalLines[0].classList.add('first-column');
                verticalLines[verticalLines.length - 1].classList.add('last-column');
            }

            if (horizontalLines.length > 0) {
                horizontalLines[horizontalLines.length - 1].classList.add('last-row');
            }
        }

        renderCalendar() {
            const year = this.currentDate.getFullYear();
            const month = this.currentDate.getMonth();

            // تحديث السنة والشهر بشكل منفصل
            document.getElementById('currentYear').textContent = year;
            document.getElementById('currentMonth').textContent = this.monthNames[month];

            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            let firstDayOfWeek = firstDay.getDay();
            if (firstDayOfWeek === 0) firstDayOfWeek = 7;
            const daysInMonth = lastDay.getDate();
            const prevMonthLastDay = new Date(year, month, 0).getDate();

            const calendarDays = document.getElementById('calendarDays');
            calendarDays.innerHTML = '';

            for (let i = firstDayOfWeek - 1; i > 0; i--) {
                const day = prevMonthLastDay - i + 1;
                const date = new Date(year, month - 1, day);
                const dateString = this.formatDate(date);
                this.createDayElement(day, dateString, true, calendarDays);
            }

            const today = new Date();
            const todayString = this.formatDate(today);
            
            for (let day = 1; day <= daysInMonth; day++) {
                const date = new Date(year, month, day);
                const dateString = this.formatDate(date);
                const isWeekend = date.getDay() === 0 || date.getDay() === 6;
                const isToday = dateString === todayString;
                this.createDayElement(day, dateString, false, calendarDays, isWeekend, isToday);
            }

            const totalCells = 42;
            const cellsSoFar = firstDayOfWeek - 1 + daysInMonth;
            const nextMonthDays = totalCells - cellsSoFar;

            for (let day = 1; day <= nextMonthDays; day++) {
                const date = new Date(year, month + 1, day);
                const dateString = this.formatDate(date);
                this.createDayElement(day, dateString, true, calendarDays);
            }

            setTimeout(() => this.hideBorderLines(), 0);
            setTimeout(() => this.adjustCellHeights(), 100);
        }

        createDayElement(day, dateString, isOtherMonth, container, isWeekend = false, isToday = false) {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            
            if (isOtherMonth) {
                dayElement.classList.add('other-month');
            }
            
            if (isWeekend && !isOtherMonth) {
                dayElement.classList.add('weekend');
            }
            
            if (isToday) {
                dayElement.classList.add('today');
            }

            // رقم اليوم (يظهر دائماً)
            const dayNumber = document.createElement('div');
            dayNumber.className = 'calendar-day-number';
            dayNumber.textContent = day;
            dayElement.appendChild(dayNumber);

            // الأحداث في هذا اليوم
            const events = this.calendarData[dateString] || [];
            
            if (events.length > 0) {
                // إضافة صنف للإشارة إلى وجود أحداث
                dayElement.classList.add('has-events');
                
                // إخفاء رقم اليوم الأصلي عند وجود أحداث
                dayNumber.style.display = 'none';

                // تحديد عدد الأحداث وعرض التصميم المناسب
                if (events.length === 1) {
                    // حدث واحد
                    this.createSingleEventLayout(day, events[0], dayElement);
                } else if (events.length === 2) {
                    // حدثان
                    this.createTwoEventsLayout(day, events, dayElement);
                } else {
                    // 3 أحداث أو أكثر
                    this.createMultipleEventsLayout(day, events, dayElement);
                }
                
                // تمكين النقر على الخلية فقط إذا كان هناك أحداث
                dayElement.dataset.date = dateString;
                dayElement.style.cursor = 'pointer';
                dayElement.addEventListener('click', () => {
                    this.handleDayClick(dateString);
                });
            } else {
                // إذا لم يكن هناك أحداث، نجعل المؤشر افتراضياً ولا نضيف حدث النقر
                dayElement.style.cursor = 'default';
                // إظهار رقم اليوم في المنتصف (سيتحكم CSS بهذا)
                // CSS سيعالج هذا من خلال .calendar-day:not(.has-events)
            }

            container.appendChild(dayElement);
        }

        // تصميم لحدث واحد
        createSingleEventLayout(day, event, dayElement) {
            const eventElement = document.createElement('div');
            eventElement.className = 'single-event-container';
            
            // الحدث
            const eventDiv = document.createElement('div');
            eventDiv.className = 'single-event';
            
            if (event.program_type) {
                eventDiv.classList.add(event.program_type);
            }
            
            const eventContent = document.createElement('div');
            eventContent.className = 'single-event-content';
            eventContent.textContent = event.title;
            eventContent.title = event.title;
            
            // رقم اليوم
            const eventDayNumber = document.createElement('div');
            eventDayNumber.className = 'single-event-day-number';
            eventDayNumber.textContent = day;
            
            eventDiv.appendChild(eventContent);
            eventDiv.appendChild(eventDayNumber);
            
            eventDiv.addEventListener('click', (e) => {
                e.stopPropagation();
                this.handleEventClick(event);
            });
            
            eventElement.appendChild(eventDiv);
            dayElement.appendChild(eventElement);
        }

        // تصميم لحدثين
        createTwoEventsLayout(day, events, dayElement) {
            const twoEventsContainer = document.createElement('div');
            twoEventsContainer.className = 'two-events-container';
            
            // رقم اليوم المشترك (يظهر على اليمين)
            const sharedDayNumber = document.createElement('div');
            sharedDayNumber.className = 'shared-day-number';
            sharedDayNumber.textContent = day;
            twoEventsContainer.appendChild(sharedDayNumber);
            
            // الحدث الأول (في الأعلى)
            const event1 = events[0];
            const event1Element = document.createElement('div');
            event1Element.className = 'two-events-event event-top';
            
            if (event1.program_type) {
                event1Element.classList.add(event1.program_type);
            }
            
            const event1Content = document.createElement('div');
            event1Content.className = 'two-events-content';
            event1Content.textContent = event1.title;
            event1Content.title = event1.title;
            
            event1Element.appendChild(event1Content);
            event1Element.addEventListener('click', (e) => {
                e.stopPropagation();
                this.handleEventClick(event1);
            });
            twoEventsContainer.appendChild(event1Element);
            
            // الحدث الثاني (في الأسفل)
            const event2 = events[1];
            const event2Element = document.createElement('div');
            event2Element.className = 'two-events-event event-bottom';
            
            if (event2.program_type) {
                event2Element.classList.add(event2.program_type);
            }
            
            const event2Content = document.createElement('div');
            event2Content.className = 'two-events-content';
            event2Content.textContent = event2.title;
            event2Content.title = event2.title;
            
            event2Element.appendChild(event2Content);
            event2Element.addEventListener('click', (e) => {
                e.stopPropagation();
                this.handleEventClick(event2);
            });
            twoEventsContainer.appendChild(event2Element);
            
            dayElement.appendChild(twoEventsContainer);
        }

        // تصميم لـ 3 أحداث أو أكثر
        createMultipleEventsLayout(day, events, dayElement) {
            const multiEventsContainer = document.createElement('div');
            multiEventsContainer.className = 'multi-events-container';
            
            // رقم اليوم (يظهر في الأعلى)
            const dayNumberTop = document.createElement('div');
            dayNumberTop.className = 'multi-day-number';
            dayNumberTop.textContent = day;
            multiEventsContainer.appendChild(dayNumberTop);
            
            // حاوية للأحداث
            const eventsList = document.createElement('div');
            eventsList.className = 'multi-events-list';
            
            // عرض أول حدثين فقط مع زر "المزيد"
            const maxVisibleEvents = 2;
            const visibleEvents = events.slice(0, maxVisibleEvents);
            const remainingEvents = events.length - maxVisibleEvents;
            
            visibleEvents.forEach((event, index) => {
                const eventElement = document.createElement('div');
                eventElement.className = 'multi-event';
                
                if (event.program_type) {
                    eventElement.classList.add(event.program_type);
                }
                
                const eventContent = document.createElement('div');
                eventContent.className = 'multi-event-content';
                eventContent.textContent = event.title;
                eventContent.title = event.title;
                
                eventElement.appendChild(eventContent);
                eventElement.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.handleEventClick(event);
                });
                
                eventsList.appendChild(eventElement);
            });
            
            // Если есть дополнительные события, добавляем кнопку "Еще"
            if (remainingEvents > 0) {
                const moreButton = document.createElement('div');
                moreButton.className = 'more-events-button';
                moreButton.textContent = `+${remainingEvents} أكثر`;
                moreButton.title = `انقر لعرض ${remainingEvents} حدث إضافي`;
                
                moreButton.addEventListener('click', (e) => {
                    e.stopPropagation();
                    // الانتقال إلى صفحة اليوم لعرض جميع الأحداث
                    const date = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), day);
                    const dateString = this.formatDate(date);
                    this.handleDayClick(dateString);
                });
                
                eventsList.appendChild(moreButton);
            }
            
            multiEventsContainer.appendChild(eventsList);
            dayElement.appendChild(multiEventsContainer);
        }

        adjustCellHeights() {
            const days = document.querySelectorAll('.calendar-day');
            let maxHeight = 0;
            
            days.forEach(day => {
                const eventsContainer = day.querySelector('.calendar-event-container');
                if (eventsContainer) {
                    maxHeight = Math.max(maxHeight, eventsContainer.scrollHeight);
                }
            });
            
            if (maxHeight > 0) {
                days.forEach(day => {
                    const eventsContainer = day.querySelector('.calendar-event-container');
                    if (eventsContainer) {
                        eventsContainer.style.maxHeight = `${Math.min(maxHeight, 150)}px`;
                    }
                });
            }
        }

        formatDate(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        }

        handleDayClick(dateString) {
            console.log('Выбран день:', dateString);
            window.location.href = `/schedule/?date=${dateString}`;
        }

        handleEventClick(event) {
            console.log('Событие:', event);
            if (event.slug) {
                window.location.href = `/schedule/program/${event.slug}/`;
            }
        }

        setupEventListeners() {
            document.querySelector('.prev-month')?.addEventListener('click', () => {
                this.currentDate.setMonth(this.currentDate.getMonth() - 1);
                this.renderCalendar();
            });

            document.querySelector('.next-month')?.addEventListener('click', () => {
                this.currentDate.setMonth(this.currentDate.getMonth() + 1);
                this.renderCalendar();
            });
        }
    }

    // تشغيل التقويم
    new Calendar();
});