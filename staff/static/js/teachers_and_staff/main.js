// static/js/teachers_and_staff/main.js
// =====================================

import { setupFilters, resetFilter } from './filters.js';
import { setupTabs, switchToTab } from './tabs.js';
import { setupMemberCardEvents, showCardsView } from './memberDetail.js';
import { setupBrowserHistory, setupUrlHandling } from './history.js';

// دالة متطورة لعرض السطر الأول أو جزء مناسب من نص المنصب
function truncatePositionToFirstLine() {
    const positionElements = document.querySelectorAll(
        '.teacher-card-position, .council-card-position, .staff-card-position'
    );
    
    positionElements.forEach(el => {
        const fullText = el.innerText || el.textContent;
        let trimmed = fullText;
        let modified = false;

        // 1. إذا كان النص يحتوي على أسطر جديدة (\n) نأخذ أول سطر
        if (fullText.includes('\n')) {
            trimmed = fullText.split('\n')[0].trim();
            modified = true;
        }
        // 2. إذا لم توجد أسطر جديدة، نتحقق من وجود وسوم <br> في الـ HTML
        else if (el.innerHTML.includes('<br>')) {
            // نقسم على <br> ونأخذ أول جزء مع إزالة أي وسوم HTML منه
            const firstPart = el.innerHTML.split('<br>')[0];
            // إزالة الوسوم للحصول على النص الصافي
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = firstPart;
            trimmed = tempDiv.innerText.trim();
            modified = true;
        }
        // 3. إذا كان النص طويلاً جداً (أكثر من 100 حرف) نقتطعه مع إضافة علامة القطع
        else if (fullText.length > 70) {
            trimmed = fullText.substring(0, 70).trim() + '...';
            modified = true;
        }

        // إذا تغير النص نقوم بتحديثه
        if (modified && trimmed !== fullText) {
            el.innerText = trimmed;
        }
    });
}

export function initializeAllComponents() {
    setupTabs();
    setupFilters();
    setupMemberCardEvents();
    setupBrowserHistory();
}

// تنفيذ الدوال عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    initializeAllComponents();
    setupUrlHandling();
    truncatePositionToFirstLine(); // عرض السطر الأول أو جزء مناسب من المنصب
});

// عند تحميل محتوى غير متزامن (مثل العودة من صفحة التفاصيل)
document.addEventListener('ajaxContentLoaded', function() {
    truncatePositionToFirstLine();
});

// عند تغيير حجم الشاشة (للتأكد من عدم تغير السلوك بسبب الـ responsive)
window.addEventListener('resize', function() {
    truncatePositionToFirstLine();
});

// إنشاء حدث مخصص لتحميل محتوى AJAX
const originalFetch = window.fetch;
window.fetch = async function(...args) {
    const response = await originalFetch(...args);
    if (args[0].includes('/staff/member/') && args[0].includes('/detail/')) {
        setTimeout(() => {
            document.dispatchEvent(new Event('ajaxContentLoaded'));
        }, 50);
    }
    return response;
};