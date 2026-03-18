// research/static/research/js/research_tabs.js

document.addEventListener('DOMContentLoaded', function() {
    // ========== إدارة تبويبات الهيرو مع تحديث URL ==========
    const tabs = document.querySelectorAll('.nav-tab-hero');
    const contents = {
        'research': document.getElementById('research-content'),
        'conferences': document.getElementById('conferences-content'),
        'youth-council': document.getElementById('youth-council-content')
    };

    // دالة لتفعيل التبويب وتحديث URL مع الحفاظ على المعاملات الأخرى
    function activateTab(targetId, updateUrl = true) {
        // إزالة active من جميع التبويبات
        tabs.forEach(tab => tab.classList.remove('active'));
        // إخفاء جميع المحتويات
        Object.values(contents).forEach(content => {
            if (content) content.style.display = 'none';
        });

        // تفعيل التبويب المطلوب
        const activeTab = document.querySelector(`.nav-tab-hero[href="#${targetId}"]`);
        if (activeTab) activeTab.classList.add('active');

        // إظهار المحتوى المناسب
        if (contents[targetId]) {
            contents[targetId].style.display = 'block';
        }

        // تحديث URL
        if (updateUrl) {
            const urlParams = new URLSearchParams(window.location.search);
            urlParams.set('tab', targetId);

            // حذف المعاملات الخاصة بالتبويبات الأخرى
            if (targetId !== 'conferences') {
                urlParams.delete('conference');
            }
            if (targetId !== 'youth-council') {
                urlParams.delete('member');
            }

            const newUrl = window.location.pathname + '?' + urlParams.toString();
            window.history.pushState({}, '', newUrl);
        }

        // إذا كان التبويب هو conferences، تحقق من وجود معامل conference لتحميل التفاصيل
        if (targetId === 'conferences') {
            const urlParams = new URLSearchParams(window.location.search);
            const confId = urlParams.get('conference');
            if (confId) {
                import('./conferenceDetail.js').then(module => {
                    module.loadConferenceDetail(confId);
                });
            } else {
                // تأكد من عرض القائمة (إزالة أي تفاصيل قد تكون ظاهرة)
                import('./conferenceDetail.js').then(module => {
                    module.showConferencesList();
                });
            }
        }

        // تمرير سلس إلى المحتوى (اختياري)
        const mainContent = document.querySelector('.research-main-content');
        if (mainContent) {
            window.scrollTo({
                top: mainContent.offsetTop - 50,
                behavior: 'smooth'
            });
        }
    }

    // ربط الأحداث بالتبويبات
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href').substring(1); // يزيل #
            activateTab(target);
        });
    });

    // قراءة التبويب من URL عند التحميل
    const urlParams = new URLSearchParams(window.location.search);
    const tabFromUrl = urlParams.get('tab');
    if (tabFromUrl && contents[tabFromUrl]) {
        activateTab(tabFromUrl, false); // لا تحدث URL مرة أخرى
    } else {
        // تفعيل التبويب الأول افتراضياً
        activateTab('research', false);
    }

    // ========== إدارة القوائم المنسدلة للفلاتر (مع تجاهل فلتر youth-council) ==========
    function setupFilterDropdowns() {
        const allFilters = document.querySelectorAll('.main-filter');
        // استبعاد الفلاتر الموجودة داخل قسم youth-council لأنها تدار بواسطة youthCouncilFilters.js
        const filterContainers = Array.from(allFilters).filter(el => !el.closest('#youth-council-content'));

        // إغلاق جميع القوائم
        function closeAllDropdowns() {
            filterContainers.forEach(container => {
                const trigger = container.querySelector('.filter-trigger');
                const dropdown = container.querySelector('.filter-dropdown');
                const arrow = container.querySelector('.filter-arrow');
                if (trigger) trigger.classList.remove('active');
                if (dropdown) dropdown.classList.remove('show');
                if (arrow) arrow.classList.remove('open');
            });
        }

        filterContainers.forEach(container => {
            const trigger = container.querySelector('.filter-trigger');
            const dropdown = container.querySelector('.filter-dropdown');
            const arrow = container.querySelector('.filter-arrow');
            const options = container.querySelectorAll('.filter-option');

            if (!trigger || !dropdown) return;

            // فتح/غلق القائمة عند النقر على الزناد
            trigger.addEventListener('click', function(e) {
                e.stopPropagation();
                const isOpen = dropdown.classList.contains('show');

                closeAllDropdowns(); // إغلاق الباقي

                if (!isOpen) {
                    trigger.classList.add('active');
                    dropdown.classList.add('show');
                    if (arrow) arrow.classList.add('open');
                }
            });

            // معالجة اختيار الخيارات
            options.forEach(option => {
                option.addEventListener('click', function(e) {
                    e.stopPropagation();

                    // تجاهل الخيارات الموجودة داخل youth-ccontent (تتم معالجتها بواسطة youthCouncilFilters.js)
                    if (this.closest('#youth-council-content')) {
                        return;
                    }

                    // تحديد نوع الفلتر بناءً على data attribute
                    const type = this.dataset.filterType;
                    const sort = this.dataset.filterSort;
                    const period = this.dataset.filterPeriod;
                    const confType = this.dataset.filterConferenceType;
                    const confSort = this.dataset.filterConferenceSort;
                    const confPeriod = this.dataset.filterConferencePeriod;

                    // بناء URL جديد مع الحفاظ على المعاملات الأخرى
                    const urlParams = new URLSearchParams(window.location.search);

                    if (type !== undefined) {
                        if (type) urlParams.set('type', type);
                        else urlParams.delete('type');
                    }
                    if (sort !== undefined) {
                        if (sort) urlParams.set('sort', sort);
                        else urlParams.delete('sort');
                    }
                    if (period !== undefined) {
                        if (period && period !== 'all') urlParams.set('period', period);
                        else urlParams.delete('period');
                    }
                    if (confType !== undefined) {
                        if (confType) urlParams.set('conference_type', confType);
                        else urlParams.delete('conference_type');
                    }
                    if (confSort !== undefined) {
                        if (confSort) urlParams.set('conference_sort', confSort);
                        else urlParams.delete('conference_sort');
                    }
                    if (confPeriod !== undefined) {
                        if (confPeriod) urlParams.set('conference_period', confPeriod);
                        else urlParams.delete('conference_period');
                    }

                    // الحفاظ على التبويب النشط
                    const activeTab = getActiveTab();
                    urlParams.set('tab', activeTab);

                    const newUrl = window.location.pathname + '?' + urlParams.toString();
                    window.location.href = newUrl; // إعادة تحميل الصفحة بالمعاملات الجديدة
                });
            });
        });

        // إغلاق القوائم عند النقر خارج أي منها
        document.addEventListener('click', closeAllDropdowns);

        // منع الإغلاق عند النقر داخل القائمة
        document.querySelectorAll('.filter-dropdown').forEach(d => {
            d.addEventListener('click', e => e.stopPropagation());
        });
    }

    // دالة للحصول على التبويب النشط حاليًا (للاستخدام في الفلاتر)
    function getActiveTab() {
        for (let id in contents) {
            if (contents[id] && contents[id].style.display !== 'none') {
                return id;
            }
        }
        return 'research';
    }

    setupFilterDropdowns();

    // ضبط عرض الهيرو عند التحميل وتغيير الحجم
    function setFullWidth() {
        const heroSection = document.querySelector('.research-hero-fullwidth');
        if (heroSection) {
            heroSection.style.width = '100vw';
            heroSection.style.marginLeft = 'calc(-50vw + 50%)';
            heroSection.style.marginRight = 'calc(-50vw + 50%)';
        }
    }
    setFullWidth();
    window.addEventListener('resize', setFullWidth);
});