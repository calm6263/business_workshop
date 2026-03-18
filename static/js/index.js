document.addEventListener('DOMContentLoaded', function() {
    // خدمة البطاقات الجديدة مع SVG
    const serviceCards = document.querySelectorAll('.svg-card');
    const modal = document.getElementById('developmentModal');
    const closeModalBtn = document.getElementById('closeModalBtn');

    // دوال التحكم بالمودال
    function closeModal() {
        if (modal) {
            modal.style.display = 'none';
        }
    }

    function openModal() {
        if (modal) {
            modal.style.display = 'flex'; // المودال يستخدم flex للتمركز
        }
    }

    // إغلاق المودال عند النقر على زر الإغلاق
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }

    // إغلاق المودال عند النقر على الخلفية (الـ overlay)
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }

    // معالجة النقر على بطاقات الخدمات
    serviceCards.forEach(card => {
        card.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            if (url && url !== '#') {
                window.location.href = url;
            } else {
                openModal(); // فتح المودال إذا لم يوجد رابط صالح
            }
        });

        // إضافة مؤشر يد عند التحويم
        card.style.cursor = 'pointer';
    });

    // التحكم في بطاقات الأخبار (باستخدام المحدد الجديد .news-card-new)
    const newsWrapper = document.querySelector('.news-cards-wrapper');
    const newsCards = document.querySelectorAll('.news-card-new');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    let currentIndex = 0;

    function updateCardsPerView() {
        if (window.innerWidth < 768) {
            return 1; // شاشات صغيرة: بطاقة واحدة
        } else if (window.innerWidth < 992) {
            return 2; // شاشات متوسطة: بطاقتين
        } else if (window.innerWidth < 1400) {
            return 2; // شاشات كبيرة متوسطة: بطاقتين
        } else {
            return 3; // شاشات كبيرة جداً: 3 بطاقات
        }
    }

    function updateSlidePosition() {
        const cardsPerView = updateCardsPerView();
        const cardWidth = newsCards[0] ? newsCards[0].offsetWidth + 20 : 0; // حساب العرض مع المسافة
        const translateX = -currentIndex * cardWidth;
        newsWrapper.style.transform = `translateX(${translateX}px)`;

        // إدارة حالة أزرار التنقل
        if (prevBtn) {
            prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
            prevBtn.style.cursor = currentIndex === 0 ? 'not-allowed' : 'pointer';
        }

        if (nextBtn) {
            const maxIndex = Math.max(0, newsCards.length - cardsPerView);
            nextBtn.style.opacity = currentIndex >= maxIndex ? '0.5' : '1';
            nextBtn.style.cursor = currentIndex >= maxIndex ? 'not-allowed' : 'pointer';
        }
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const cardsPerView = updateCardsPerView();
            const maxIndex = Math.max(0, newsCards.length - cardsPerView);
            if (currentIndex < maxIndex) {
                currentIndex++;
                updateSlidePosition();
            }
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (currentIndex > 0) {
                currentIndex--;
                updateSlidePosition();
            }
        });
    }

    // إضافة مستمع الحدث لتغيير حجم النافذة
    window.addEventListener('resize', function() {
        const cardsPerView = updateCardsPerView();
        const maxIndex = Math.max(0, newsCards.length - cardsPerView);
        if (currentIndex > maxIndex) {
            currentIndex = maxIndex;
        }
        updateSlidePosition();
    });

    // التهيئة الأولية
    if (newsCards.length > 0) {
        updateSlidePosition();
    }

    // إضافة مؤشر يد للنقر على البطاقات التفاعلية
    const interactiveCards = document.querySelectorAll('.svg-card, .news-card-new');
    interactiveCards.forEach(card => {
        card.style.cursor = 'pointer';
    });

    // جعل البطاقة بأكملها قابلة للنقر (باستثناء الزر)
    document.querySelectorAll('.news-card-new').forEach(card => {
        card.addEventListener('click', function(e) {
            // إذا كان النقر على الرابط داخل البطاقة، لا نتدخل
            if (e.target.closest('a')) return;
            const url = this.dataset.url;
            if (url && url !== '#') {
                window.location.href = url;
            }
        });
    });

    // إضافة event listener لأزرار "Читать" (لمنع تنشيط حدث البطاقة)
    const readButtons = document.querySelectorAll('.news-read-btn-new');
    readButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // منع تفعيل click على البطاقة
            // الرابط يعمل طبيعي
        });
    });

    // ===== دالة محسنة لضبط بطاقات الأخبار (غير ضرورية مع البطاقات الجديدة، لكن نحتفظ بها للمرونة) =====
    function setupNewsCards() {
        // يمكن إبقاؤها فارغة أو حذفها
    }

    // استدعاء الدالة عند تحميل الصفحة وعند تغيير الحجم
    window.addEventListener('load', setupNewsCards);
    window.addEventListener('resize', setupNewsCards);

    // تهيئة فورية بعد تحميل DOM
    setTimeout(setupNewsCards, 100);

    // دالة لتعديل قسم Поступающим عند إخفاء الصورة
    function adjustApplicantsLayout() {
        const applicantsImage = document.querySelector('.applicants-image');
        const applicantsText = document.querySelector('.applicants-section .col-lg-8');

        if (window.innerWidth < 992) {
            // على الشاشات المتوسطة والصغيرة
            if (applicantsText) {
                applicantsText.style.maxWidth = '100%';
                applicantsText.style.flex = '0 0 100%';
            }
        } else {
            // على الشاشات الكبيرة
            if (applicantsText) {
                applicantsText.style.maxWidth = '';
                applicantsText.style.flex = '';
            }
        }
    }

    // استدعاء الدالة عند تحميل الصفحة وعند تغيير الحجم
    window.addEventListener('load', adjustApplicantsLayout);
    window.addEventListener('resize', adjustApplicantsLayout);

    // ===== دالة لتحسين أداء الكاروسيل على الشاشات الصغيرة =====
    function optimizeCarouselForMobile() {
        const carousel = document.querySelector('.full-width-carousel');
        if (window.innerWidth <= 768 && carousel) {
            // تحسين مؤشرات الكاروسيل للشاشات الصغيرة
            const indicators = carousel.querySelectorAll('.carousel-indicators button');
            indicators.forEach(indicator => {
                indicator.style.width = '8px';
                indicator.style.height = '8px';
                indicator.style.margin = '0 3px';
            });
        }
    }

    // استدعاء دالة تحسين الكاروسيل
    window.addEventListener('load', optimizeCarouselForMobile);
    window.addEventListener('resize', optimizeCarouselForMobile);

    // ===== Overlay Menu Functionality - NEW DESIGN - مع دعم الروابط =====
    // فقط على الشاشات الكبيرة (992px فما فوق) وفي صفحة index فقط
    if (window.innerWidth >= 992 && document.body.classList.contains('index-page')) {
        // ===== إضافة event listener لأيقونة البحث لفتح الـ Overlay =====
        const searchIcon = document.getElementById('searchIcon');
        if (searchIcon) {
            searchIcon.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                // إغلاق جميع القوائم المنسدلة الأصلية
                closeAllOriginalDropdowns();

                // فتح القائمة المنبثقة وعرض محتوى "Академия" كافتراضي
                const overlay = document.getElementById('menuOverlay');
                const overlayContent = document.getElementById('overlayMenuContent');
                const overlayNavItems = document.querySelectorAll('.overlay-nav-item');

                if (overlay && overlayContent) {
                    // قراءة بيانات الروابط
                    const overlayDataElement = document.getElementById('overlay-data');
                    let overlayData = {};

                    if (overlayDataElement) {
                        try {
                            overlayData = JSON.parse(overlayDataElement.textContent);
                        } catch (e) {
                            console.error('Error parsing overlay data:', e);
                        }
                    }

                    // تفعيل رابط "Академия" في الـ Overlay
                    overlayNavItems.forEach(item => {
                        item.classList.remove('active');
                        if (item.textContent.trim() === 'Академия') {
                            item.classList.add('active');
                        }
                    });

                    // توليد محتوى قائمة "Академия"
                    const content = generateMenuContent('Академия', overlayData);
                    overlayContent.innerHTML = content;
                    overlay.style.display = 'block';
                    document.body.style.overflow = 'hidden';

                    // إغلاق أي قوائم منسدلة مفتوحة
                    const overlayLanguageDropdown = document.getElementById('overlayLanguageDropdown');
                    const overlayAccountDropdown = document.getElementById('overlayAccountDropdown');
                    const overlayLanguage = document.getElementById('overlayLanguage');
                    if (overlayLanguageDropdown) overlayLanguageDropdown.classList.remove('active');
                    if (overlayAccountDropdown) overlayAccountDropdown.classList.remove('active');
                    if (overlayLanguage) overlayLanguage.classList.remove('active');
                }
            });
        }

        // قراءة بيانات الروابط من script tag
        const overlayDataElement = document.getElementById('overlay-data');
        let overlayData = {};

        if (overlayDataElement) {
            try {
                overlayData = JSON.parse(overlayDataElement.textContent);
            } catch (e) {
                console.error('Error parsing overlay data:', e);
            }
        }

        // دالة لتوليد محتوى القائمة - محدثة حسب الطلب
        function generateMenuContent(menuKey, data) {
            // بيانات الروابط كما هي (بدون عناوين)
            const menuContents = {
                'Академия': {
                    links: [
                        { text: 'Об академии', url: data.about_academy_url || '#' },
                        { text: 'Мероприятия', url: data.events_url || '#' },
                        { text: 'Общежития', url: data.under_construction_url ? data.under_construction_url.replace('Общежития', 'Общежития') : '#' },
                        { text: 'Партнеры', url: data.partners_list_url || '#' },
                        { text: 'Преподаватели и сотрудники', url: data.teachers_staff_url || '#' },
                        { text: 'Проекты', url: data.projects_list_url || '#' },
                        { text: 'СМИ', url: data.news_list_url || '#' },
                        { text: 'Сведения об образовательной деятельности', url: data.education_info_url || '#' }
                    ]
                },
                'Поступление': {
                    links: [
                        { text: 'Правила приема', url: '#' },
                        { text: 'Приемная комиссия', url: '#' },
                        { text: 'Дополнительные платформы для обучающихся', url: '#' },
                        { text: 'Сведения об образовательных программах', url: '#' },
                        { text: 'Целевое обучение', url: '#' },
                        { text: 'Библиотека и электронные ресурсы', url: '#' },
                        { text: 'Учебная документация', url: '#' }
                    ]
                },
                'Обучение': {
                    links: [
                        { text: 'Поиск заявления по СНИЛС', url: data.applicants_search_url || '#' },
                        { text: 'Общежития', url: data.under_construction_url ? data.under_construction_url.replace('Общежития', 'Общежития') : '#' },
                        { text: 'Расписание', url: data.schedule_url || '#' },
                        { text: 'Материально-техническое обеспечение', url: '#' },
                        { text: 'Услуги одного окна', url: data.single_window_url || '#' },
                        { text: 'Научно-исследовательская деятельность', url: '#' },
                        { text: 'Консультации', url: data.consultations_url || '#' }   
                    ]
                },
                'Наука': {
                    links: [
                        { text: 'Инновационные проекты', url: '#' },
                        { text: 'Конференции', url: data.research_list_url ? data.research_list_url + '?tab=conferences' : '#' },
                        { text: 'Журнал', url: data.journal_url || '#' },
                        { text: 'Центры и лаборатории', url: '#' },
                        { text: 'Конкурсы и гранты', url: '#' },
                        { text: 'Патенты', url: data.patents_list_url || '#' },
                        { text: 'Совет молодых ученых', url: data.research_list_url ? data.research_list_url + '?tab=youth-council' : '#' }
                    ]
                }
            };

            const linksArray = menuContents[menuKey]?.links;
            if (!linksArray) return '';

            // تقسيم الروابط إلى عمودين
            const half = Math.ceil(linksArray.length / 2);
            const firstColumnLinks = linksArray.slice(0, half);
            const secondColumnLinks = linksArray.slice(half);

            let html = '';

            // إنشاء العمود الأول
            html += `<div class="overlay-menu-column">`;
            html += `<div class="overlay-menu-links">`;
            firstColumnLinks.forEach(link => {
                html += `
                    <a href="${link.url}" class="overlay-menu-link" onclick="handleOverlayLinkClick(event, '${link.url}')">
                        <span class="link-dot"></span>
                        <span class="link-text">${link.text}</span>
                    </a>
                `;
            });
            html += `</div></div>`;

            // إنشاء العمود الثاني
            html += `<div class="overlay-menu-column">`;
            html += `<div class="overlay-menu-links">`;
            secondColumnLinks.forEach(link => {
                html += `
                    <a href="${link.url}" class="overlay-menu-link" onclick="handleOverlayLinkClick(event, '${link.url}')">
                        <span class="link-dot"></span>
                        <span class="link-text">${link.text}</span>
                    </a>
                `;
            });
            html += `</div></div>`;

            return html;
        }

        // الحصول على عناصر الـ Overlay الموجودة في HTML
        const overlay = document.getElementById('menuOverlay');
        const overlayContent = document.getElementById('overlayMenuContent');
        const overlayClose = document.getElementById('overlayClose');
        const navLinks = document.querySelectorAll('.nav-main-link.dropdown-toggle');
        const overlayNavItems = document.querySelectorAll('.overlay-nav-item');
        const overlaySearchInput = document.querySelector('.overlay-search-input');

        // إضافة event listeners للغة والحساب في الـ Overlay
        const overlayLanguage = document.getElementById('overlayLanguage');
        const overlayLanguageDropdown = document.getElementById('overlayLanguageDropdown');
        const overlayAccount = document.getElementById('overlayAccount');
        const overlayAccountDropdown = document.getElementById('overlayAccountDropdown');
        const overlayContacts = document.getElementById('overlayContacts');
        const overlayCoworking = document.getElementById('overlayCoworking');

        // نسخ قوائم اللغات والحساب من القائمة الأصلية إلى الـ Overlay
        function copyDropdownsToOverlay() {
            // نسخ قائمة اللغات
            const originalLanguageDropdown = document.getElementById('languageDropdown');
            if (originalLanguageDropdown && overlayLanguageDropdown) {
                overlayLanguageDropdown.innerHTML = originalLanguageDropdown.innerHTML;
            }

            // نسخ قائمة الحساب
            const originalAccountDropdown = document.getElementById('accountDropdown');
            if (originalAccountDropdown && overlayAccountDropdown) {
                overlayAccountDropdown.innerHTML = originalAccountDropdown.innerHTML;
            }
        }

        // استدعاء دالة نسخ القوائم عند تحميل الصفحة
        copyDropdownsToOverlay();

        // دالة إغلاق جميع القوائم المنسدلة الأصلية
        function closeAllOriginalDropdowns() {
            // هذه الدالة تؤثر فقط في الشاشات الكبيرة
            if (window.innerWidth >= 992) {
                document.querySelectorAll('.dropdown-menu-custom').forEach(menu => {
                    menu.style.display = 'none';
                    menu.classList.remove('show');
                });

                // إخفاء جميع قوائم Bootstrap المنسدلة
                document.querySelectorAll('.nav-item.dropdown').forEach(dropdown => {
                    const dropdownInstance = bootstrap.Dropdown.getInstance(dropdown.querySelector('.dropdown-toggle'));
                    if (dropdownInstance) {
                        dropdownInstance.hide();
                    }
                });
            }
        }

        // ===== إضافة event listeners للعناصر التفاعلية في الـ Overlay =====

        // 1. اللغة - عند النقر تظهر القائمة المنسدلة فوق الـ Overlay
        if (overlayLanguage && overlayLanguageDropdown) {
            overlayLanguage.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                // إغلاق قائمة الحساب إذا كانت مفتوحة
                if (overlayAccountDropdown && overlayAccountDropdown.classList.contains('active')) {
                    overlayAccountDropdown.classList.remove('active');
                }

                // تبديل قائمة اللغة
                overlayLanguage.classList.toggle('active');
                overlayLanguageDropdown.classList.toggle('active');
            });
        }

        // 2. الحساب - عند النقر تظهر القائمة المنسدلة فوق الـ Overlay
        if (overlayAccount && overlayAccountDropdown) {
            overlayAccount.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                // إغلاق قائمة اللغة إذا كانت مفتوحة
                if (overlayLanguageDropdown && overlayLanguageDropdown.classList.contains('active')) {
                    overlayLanguageDropdown.classList.remove('active');
                    overlayLanguage.classList.remove('active');
                }

                // تبديل قائمة الحساب
                overlayAccountDropdown.classList.toggle('active');
            });
        }

        // 3. إغلاق القوائم عند النقر خارجها في الـ Overlay
        overlay.addEventListener('click', function(e) {
            // إغلاق قائمة اللغة إذا تم النقر خارجها
            if (overlayLanguage && overlayLanguageDropdown &&
                !overlayLanguage.contains(e.target) &&
                !overlayLanguageDropdown.contains(e.target)) {
                overlayLanguageDropdown.classList.remove('active');
                overlayLanguage.classList.remove('active');
            }

            // إغلاق قائمة الحساب إذا تم النقر خارجها
            if (overlayAccount && overlayAccountDropdown &&
                !overlayAccount.contains(e.target) &&
                !overlayAccountDropdown.contains(e.target)) {
                overlayAccountDropdown.classList.remove('active');
            }
        });

        // 4. منع إغلاق القوائم عند النقر داخلها
        if (overlayLanguageDropdown) {
            overlayLanguageDropdown.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }

        if (overlayAccountDropdown) {
            overlayAccountDropdown.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }

        // 5. روابط КОНТАКТЫ и КОВОРКИНГ - افتح الصفحات الخاصة
        if (overlayContacts) {
            overlayContacts.addEventListener('click', function(e) {
                e.stopPropagation();
                window.location.href = overlayData.contacts_page_url || '#';
            });
        }

        if (overlayCoworking) {
            overlayCoworking.addEventListener('click', function(e) {
                e.stopPropagation();
                window.location.href = overlayData.coworking_home_url || '#';
            });
        }

        // ===== event listeners للروابط الرئيسية في الشريط العلوي (فقط في الشاشات الكبيرة) =====

        // إضافة event listeners لعناصر القائمة الأصلية (فقط في الشاشات الكبيرة)
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // تأكد أننا فقط في الشاشات الكبيرة
                if (window.innerWidth >= 992) {
                    e.preventDefault();
                    e.stopPropagation();

                    // إغلاق جميع القوائم المنسدلة الأصلية
                    closeAllOriginalDropdowns();

                    const linkText = this.textContent.trim();
                    const content = generateMenuContent(linkText, overlayData);

                    if (content) {
                        // تفعيل الرابط المحدد في الـ Overlay
                        overlayNavItems.forEach(item => {
                            item.classList.remove('active');
                            if (item.textContent.trim() === linkText) {
                                item.classList.add('active');
                            }
                        });

                        overlayContent.innerHTML = content;
                        overlay.style.display = 'block';
                        document.body.style.overflow = 'hidden';

                        // إغلاق أي قوائم منسدلة مفتوحة
                        if (overlayLanguageDropdown) overlayLanguageDropdown.classList.remove('active');
                        if (overlayAccountDropdown) overlayAccountDropdown.classList.remove('active');
                        if (overlayLanguage) overlayLanguage.classList.remove('active');
                    }
                }
            });
        });

        // إضافة event listeners لعناصر القائمة في الـ Overlay
        overlayNavItems.forEach(item => {
            item.addEventListener('click', function() {
                // إغلاق جميع القوائم المنسدلة الأصلية
                closeAllOriginalDropdowns();

                const menuKey = this.getAttribute('data-menu');
                const content = generateMenuContent(menuKey, overlayData);

                if (content) {
                    // تفعيل الرابط المحدد
                    overlayNavItems.forEach(item => {
                        item.classList.remove('active');
                    });
                    this.classList.add('active');

                    overlayContent.innerHTML = content;
                }
            });
        });

        // إغلاق الـ Overlay
        if (overlayClose) {
            overlayClose.addEventListener('click', function() {
                closeOverlay();
            });
        }

        // إغلاق الـ Overlay عند النقر خارج المحتوى
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                closeOverlay();
            }
        });

        // ===== إضافة نظام البحث الحي (Live Search) في Overlay =====
        // إعداد بيانات البحث
        const searchItems = [];

        // إضافة روابط من القوائم الأربعة (أكاديميا، بوستوبليني، أوبوتشيني، ناوكا)
        const menuContentsForSearch = {
            'Академия': [
                { text: 'Об академии', url: overlayData.about_academy_url },
                { text: 'Мероприятия', url: overlayData.events_url },
                { text: 'Общежития', url: overlayData.under_construction_url ? overlayData.under_construction_url.replace('Общежития', 'Общежития') : '#' },
                { text: 'Партнеры', url: overlayData.partners_list_url },
                { text: 'Преподаватели и сотрудники', url: overlayData.teachers_staff_url },
                { text: 'Проекты', url: overlayData.projects_list_url },
                { text: 'СМИ', url: overlayData.news_list_url },
                { text: 'Сведения об образовательной деятельности', url: overlayData.education_info_url }
            ],
            'Поступление': [
                { text: 'Правила приема', url: '#' },
                { text: 'Приемная комиссия', url: '#' },
                { text: 'Дополнительные платформы для обучающихся', url: '#' },
                { text: 'Сведения об образовательных программах', url: '#' },
                { text: 'Целевое обучение', url: '#' },
                { text: 'Библиотека и электронные ресурсы', url: '#' },
                { text: 'Учебная документация', url: '#' }
            ],
            'Обучение': [
                { text: 'Поиск заявления по СНИЛС', url: overlayData.applicants_search_url },
                { text: 'Общежития', url: overlayData.under_construction_url ? overlayData.under_construction_url.replace('Общежития', 'Общежития') : '#' },
                { text: 'Расписание', url: overlayData.schedule_url },
                { text: 'Материально-техническое обеспечение', url: '#' },
                { text: 'Услуги одного окна', url: overlayData.single_window_url },
                { text: 'Научно-исследовательская деятельность', url: '#' },
                { text: 'Консультации', url: '#' }
            ],
            'Наука': [
                { text: 'Инновационные проекты', url: '#' },
                { text: 'Конференции', url: overlayData.research_list_url ? overlayData.research_list_url + '?tab=conferences' : '#' },
                { text: 'Журнал', url: overlayData.journal_url },
                { text: 'Центры и лаборатории', url: '#' },
                { text: 'Конкурсы и гранты', url: '#' },
                { text: 'Патенты', url: '#' },
                { text: 'Совет молодых ученых', url: overlayData.research_list_url ? overlayData.research_list_url + '?tab=youth-council' : '#' }
            ]
        };

        // تجميع جميع العناصر في مصفوفة واحدة (بدون استثناء)
        Object.values(menuContentsForSearch).forEach(category => {
            category.forEach(item => {
                // نضيف جميع العناصر حتى لو كان الرابط '#'
                searchItems.push(item);
            });
        });

        // إضافة بعض الروابط الهامة الأخرى (مثل КОНТАКТЫ، КОВОРКИНГ)
        if (overlayData.contacts_page_url) searchItems.push({ text: 'Контакты', url: overlayData.contacts_page_url });
        if (overlayData.coworking_home_url) searchItems.push({ text: 'Коворкинг', url: overlayData.coworking_home_url });

        // إنشاء عنصر عرض النتائج
        const overlaySearchSection = document.querySelector('.overlay-search-section');
        const searchResultsContainer = document.createElement('div');
        searchResultsContainer.className = 'overlay-search-results';
        searchResultsContainer.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #ddd;
            border-radius: 0 0 8px 8px;
            max-height: 300px;
            overflow-y: auto;
            z-index: 1000;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: none;
        `;
        overlaySearchSection.style.position = 'relative';
        overlaySearchSection.appendChild(searchResultsContainer);

        // دالة تصفية وعرض النتائج
        function filterSearchResults(query) {
            if (!query.trim()) {
                searchResultsContainer.style.display = 'none';
                return;
            }

            const lowerQuery = query.toLowerCase();
            const filtered = searchItems.filter(item => 
                item.text.toLowerCase().includes(lowerQuery)
            );

            if (filtered.length === 0) {
                searchResultsContainer.innerHTML = '<div class="no-results" style="padding: 10px; color: #999;">Ничего не найдено</div>';
                searchResultsContainer.style.display = 'block';
                return;
            }

            let html = '';
            filtered.forEach(item => {
                html += `
                    <div class="search-result-item" data-url="${item.url}" style="padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #f0f0f0; transition: background 0.2s;">
                        <span style="color: #052946;">${item.text}</span>
                    </div>
                `;
            });
            searchResultsContainer.innerHTML = html;
            searchResultsContainer.style.display = 'block';

            // إضافة event listeners لنتائج البحث
            document.querySelectorAll('.search-result-item').forEach(item => {
                item.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const url = this.dataset.url;
                    if (url && url !== '#') {
                        closeOverlay();
                        setTimeout(() => window.location.href = url, 100);
                    } else {
                        // إذا كان الرابط '#' نفتح المودال
                        closeOverlay(); // نغلق الـ overlay أولاً
                        setTimeout(() => {
                            openModal(); // فتح المودال
                        }, 100);
                    }
                });

                // تأثير hover
                item.addEventListener('mouseenter', function() {
                    this.style.backgroundColor = '#f5f5f5';
                });
                item.addEventListener('mouseleave', function() {
                    this.style.backgroundColor = '';
                });
            });
        }

        // ربط الحدث بحقل الإدخال
        if (overlaySearchInput) {
            overlaySearchInput.addEventListener('input', function(e) {
                filterSearchResults(this.value);
            });

            // إغلاق النتائج عند الضغط على Escape
            overlaySearchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    searchResultsContainer.style.display = 'none';
                }
            });
        }

        // أيقونة البحث الخارجية (الجديدة) - نضيف لها نفس وظيفة البحث مع تنبيه أو تنفيذ البحث
        const overlaySearchIcon = document.getElementById('overlaySearchIcon');
        if (overlaySearchIcon && overlaySearchInput) {
            overlaySearchIcon.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                // تنفيذ نفس وظيفة الضغط على Enter
                if (overlaySearchInput.value.trim() !== '') {
                    // هنا يمكن تنفيذ البحث الفعلي، مثلاً عرض النتائج أو التوجيه إلى صفحة بحث
                    // لكن الأفضل أن نعرض النتائج الموجودة بالفعل
                    filterSearchResults(overlaySearchInput.value);
                } else {
                    // إذا كان الحقل فارغاً، يمكن وضع المؤشر فيه
                    overlaySearchInput.focus();
                }
            });
        }

        // إغلاق نتائج البحث عند النقر خارجها
        document.addEventListener('click', function(e) {
            if (!overlaySearchSection.contains(e.target)) {
                searchResultsContainer.style.display = 'none';
            }
        });

        // عند فتح الـ overlay، نقوم بإعادة تعيين البحث
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                // إعادة تعيين حقل البحث وإخفاء النتائج
                if (overlaySearchInput) overlaySearchInput.value = '';
                searchResultsContainer.style.display = 'none';
            }
        });

        // دالة إغلاق الـ Overlay
        function closeOverlay() {
            overlay.style.display = 'none';
            document.body.style.overflow = '';
            overlayContent.innerHTML = '';

            // إزالة التفعيل من جميع الروابط
            overlayNavItems.forEach(item => {
                item.classList.remove('active');
            });

            // إغلاق القوائم المنسدلة
            if (overlayLanguageDropdown) overlayLanguageDropdown.classList.remove('active');
            if (overlayAccountDropdown) overlayAccountDropdown.classList.remove('active');
            if (overlayLanguage) overlayLanguage.classList.remove('active');

            // إخفاء نتائج البحث
            if (searchResultsContainer) searchResultsContainer.style.display = 'none';
        }

        // إغلاق الـ Overlay عند الضغط على زر Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && overlay.style.display === 'block') {
                closeOverlay();
            }
        });

        // عند فتح الـ Overlay، تأكد من إغلاق جميع القوائم المنسدلة الأصلية
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                closeAllOriginalDropdowns();
            }
        });

        // دالة معالجة نقرات الروابط في الـ Overlay
        window.handleOverlayLinkClick = function(event, url) {
            event.preventDefault();
            event.stopPropagation();

            if (url && url !== '#') {
                // إغلاق الـ Overlay أولاً
                closeOverlay();

                // الانتقال إلى الصفحة بعد تأخير بسيط
                setTimeout(() => {
                    window.location.href = url;
                }, 100);
            } else {
                // إذا كان الرابط '#', نفتح المودال
                closeOverlay();
                setTimeout(() => {
                    openModal();
                }, 100);
            }
        };

        // إضافة event listener للروابط في الـ Overlay
        overlayContent.addEventListener('click', function(e) {
            const link = e.target.closest('.overlay-menu-link');
            if (link) {
                const url = link.getAttribute('href');
                if (url && url !== '#') {
                    e.preventDefault();
                    e.stopPropagation();

                    // إغلاق الـ Overlay أولاً
                    closeOverlay();

                    // الانتقال إلى الصفحة
                    setTimeout(() => {
                        window.location.href = url;
                    }, 100);
                } else {
                    e.preventDefault();
                    e.stopPropagation();
                    closeOverlay();
                    setTimeout(() => {
                        openModal();
                    }, 100);
                }
            }
        });
    }
});