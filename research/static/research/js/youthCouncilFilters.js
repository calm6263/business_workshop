// research/static/research/js/youthCouncilFilters.js

/**
 * إعداد فلتر قسم "Молодежный ученый совет"
 * يقوم بتصفية البطاقات حسب القسم المختار دون إعادة تحميل الصفحة
 */
export function setupYouthCouncilFilters() {
    const filterTrigger = document.querySelector('#youth-council-content .filter-trigger');
    const filterDropdown = document.querySelector('#youth-council-content .filter-dropdown');
    const filterOptions = document.querySelectorAll('#youth-council-content .filter-option');
    const filterArrow = filterTrigger?.querySelector('.filter-arrow');

    if (!filterTrigger || !filterDropdown) return;

    // فتح/إغلاق القائمة عند النقر على الزناد
    filterTrigger.addEventListener('click', (e) => {
        e.stopPropagation();
        filterDropdown.classList.toggle('show');
        filterTrigger.classList.toggle('active');
        if (filterArrow) filterArrow.classList.toggle('open');
    });

    // معالجة اختيار خيار من القائمة
    filterOptions.forEach(opt => {
        opt.addEventListener('click', () => {
            const filterValue = opt.dataset.filter;
            selectYouthCouncilFilter(filterValue);
            filterDropdown.classList.remove('show');
            filterTrigger.classList.remove('active');
            if (filterArrow) filterArrow.classList.remove('open');
        });
    });

    // إغلاق القائمة عند النقر خارجها
    document.addEventListener('click', (e) => {
        if (!filterTrigger.contains(e.target) && !filterDropdown.contains(e.target)) {
            filterDropdown.classList.remove('show');
            filterTrigger.classList.remove('active');
            if (filterArrow) filterArrow.classList.remove('open');
        }
    });
}

/**
 * تطبيق التصفية بناءً على القيمة المختارة
 * @param {string} filterValue - قيمة الفلتر (مثل 'all' أو 'department-1')
 */
function selectYouthCouncilFilter(filterValue) {
    const cards = document.querySelectorAll('#youth-council-content .council-card');
    const sections = document.querySelectorAll('#youth-council-content .department-section');
    const filterLabel = document.querySelector('#youth-council-content .filter-label');
    const activeOption = document.querySelector(`#youth-council-content .filter-option[data-filter="${filterValue}"]`);

    if (activeOption) {
        filterLabel.textContent = activeOption.querySelector('.option-text').textContent;
        document.querySelectorAll('#youth-council-content .filter-option').forEach(opt => opt.classList.remove('active'));
        activeOption.classList.add('active');
    }

    if (filterValue === 'all') {
        // إظهار كل الأقسام والبطاقات
        cards.forEach(c => c.style.display = 'block');
        sections.forEach(s => s.style.display = 'block');
    } else {
        // إخفاء كل الأقسام أولاً
        sections.forEach(s => s.style.display = 'none');
        // إظهار البطاقات التي تنتمي للقسم المختار، وإظهار القسم الذي توجد به
        cards.forEach(c => {
            const depts = c.dataset.department?.split(',') || [];
            if (depts.includes(filterValue.replace('department-', ''))) {
                c.style.display = 'block';
                const section = c.closest('.department-section');
                if (section) section.style.display = 'block';
            } else {
                c.style.display = 'none';
            }
        });
    }
}