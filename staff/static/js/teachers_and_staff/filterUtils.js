// static/js/teachers_and_staff/filterUtils.js
// ============================================

export function applyFilter(filterValue) {
    const teacherCards = document.querySelectorAll('.teacher-card');
    const councilCards = document.querySelectorAll('.council-card');
    const staffCards = document.querySelectorAll('.staff-card');
    const departmentSections = document.querySelectorAll('.department-section');
    
    if (filterValue === 'all') {
        // إظهار جميع العناصر
        teacherCards.forEach(card => card.style.display = 'block');
        councilCards.forEach(card => card.style.display = 'block');
        staffCards.forEach(card => card.style.display = 'block');
        departmentSections.forEach(section => section.style.display = 'block');
    } else {
        const departmentId = filterValue.replace('department-', '');
        
        // إخفاء جميع الأقسام أولاً
        departmentSections.forEach(section => {
            section.style.display = 'none';
        });
        
        // فلترة البطاقات وإظهار الأقسام التي تحتوي على بطاقات معروضة
        const allCards = [...teacherCards, ...councilCards, ...staffCards];
        allCards.forEach(card => {
            const departments = card.getAttribute('data-department');
            if (departments && departments.split(',').includes(departmentId)) {
                card.style.display = 'block';
                const departmentSection = card.closest('.department-section');
                if (departmentSection) {
                    departmentSection.style.display = 'block';
                }
            } else {
                card.style.display = 'none';
            }
        });
    }
}