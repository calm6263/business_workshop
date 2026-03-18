// research/static/research/js/youthCouncilMain.js
import { setupYouthCouncilCardEvents, loadYouthCouncilDetail } from './youthCouncilDetail.js';
import { setupYouthCouncilFilters } from './youthCouncilFilters.js';

document.addEventListener('DOMContentLoaded', () => {
    setupYouthCouncilCardEvents();
    setupYouthCouncilFilters();

    // التحقق من وجود member في URL لتحميل التفاصيل تلقائياً
    const urlParams = new URLSearchParams(window.location.search);
    const memberId = urlParams.get('member');
    if (memberId) {
        const section = document.querySelector('#youth-council-content .department-section');
        if (section) {
            loadYouthCouncilDetail(memberId, section);
        }
    }
});

// الاستماع لتغييرات history (الأزرار الخلفية/الأمامية)
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.memberId && event.state.sectionId) {
        const section = document.getElementById(event.state.sectionId);
        if (section) {
            loadYouthCouncilDetail(event.state.memberId, section);
        }
    } else {
        // إذا لم تكن هناك حالة، نعود إلى عرض البطاقات
        const section = document.querySelector('#youth-council-content .department-section');
        if (section) {
            // استدعاء showCardsView مباشرةً (يجب استيراده)
            import('./youthCouncilDetail.js').then(module => {
                module.showCardsView(section);
            });
        }
    }
});