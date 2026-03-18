// research/static/research/js/conferenceDetail.js
import { showLoading, hideLoading, createElement } from './utils.js';

// ==================== دوال المشاركة ====================
function closeShareModal() {
    const modal = document.getElementById('conferenceShareModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

window.openConferenceShareModal = function() {
    const modal = document.getElementById('conferenceShareModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
};

// ربط أحداث المشاركة عند تحميل الصفحة (مرة واحدة)
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('conferenceShareModal');
    if (modal) {
        const closeBtn = modal.querySelector('.share-modal-close');
        if (closeBtn) closeBtn.addEventListener('click', closeShareModal);
        
        modal.addEventListener('click', function(e) {
            if (e.target === modal) closeShareModal();
        });

        // معالجة خيارات المشاركة
        modal.querySelectorAll('.share-modal-item').forEach(item => {
            item.addEventListener('click', function(e) {
                const shareType = this.dataset.share;
                const url = window.location.href;
                const title = document.querySelector('.event-short-description')?.textContent || 'Конференция';
                
                if (shareType === 'telegram') {
                    window.open(`https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`, '_blank');
                } else if (shareType === 'vkontakte') {
                    window.open(`https://vk.com/share.php?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`, '_blank');
                } else if (shareType === 'twitter') {
                    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`, '_blank');
                } else if (shareType === 'copy') {
                    navigator.clipboard.writeText(url).then(() => {
                        alert('Ссылка скопирована!');
                    }).catch(() => {
                        alert('Не удалось скопировать ссылку');
                    });
                }
                closeShareModal();
            });
        });
    }
});

// ==================== دوال تحميل التفاصيل ====================

/**
 * تحميل تفاصيل المؤتمر عبر AJAX وعرضها داخل تبويب المؤتمرات
 * @param {string|number} conferenceId - معرف المؤتمر
 */
export async function loadConferenceDetail(conferenceId) {
    try {
        showLoading();

        const contentDiv = document.getElementById('conferences-content');
        if (!contentDiv) return;

        // إخفاء عناصر القائمة
        const filterSection = contentDiv.querySelector('.filters-section');
        const grid = contentDiv.querySelector('.research-grid');
        const brochureWrapper = contentDiv.querySelector('.brochure-download-wrapper');
        if (filterSection) filterSection.style.display = 'none';
        if (grid) grid.style.display = 'none';
        if (brochureWrapper) brochureWrapper.style.display = 'none';

        // إزالة أي تفاصيل سابقة
        const oldDetail = contentDiv.querySelector('.conference-detail-inline');
        if (oldDetail) oldDetail.remove();

        // إنشاء حاوية التفاصيل مع مؤشر تحميل
        const detailContainer = createElement('div', 'conference-detail-inline');
        detailContainer.innerHTML = `<div class="detail-loading"><div class="spinner"></div><p>Загрузка...</p></div>`;
        contentDiv.appendChild(detailContainer);

        // جلب التفاصيل
        const response = await fetch(`/research/conferences/${conferenceId}/`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        if (!response.ok) throw new Error('Network error');
        const html = await response.text();
        detailContainer.innerHTML = html;

        // إعادة ربط الأزرار داخل التفاصيل
        attachDetailHandlers(detailContainer);

        // ربط زر العودة
        const backBtn = detailContainer.querySelector('#back-to-conferences-list');
        if (backBtn) {
            backBtn.addEventListener('click', (e) => {
                e.preventDefault();
                showConferencesList();
            });
        }

        // تحديث URL مع الحفاظ على التبويب
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('tab', 'conferences');
        urlParams.set('conference', conferenceId);
        window.history.pushState(
            { conferenceId, tab: 'conferences' },
            '',
            window.location.pathname + '?' + urlParams.toString()
        );

    } catch (error) {
        console.error('Error loading conference detail:', error);
        alert('Ошибка загрузки. Пожалуйста, попробуйте позже.');
        showConferencesList();
    } finally {
        hideLoading();
    }
}

/**
 * العودة إلى عرض قائمة المؤتمرات
 */
export function showConferencesList() {
    const contentDiv = document.getElementById('conferences-content');
    if (!contentDiv) return;

    // إزالة حاوية التفاصيل
    const detail = contentDiv.querySelector('.conference-detail-inline');
    if (detail) detail.remove();

    // إظهار عناصر القائمة
    const filterSection = contentDiv.querySelector('.filters-section');
    const grid = contentDiv.querySelector('.research-grid');
    const brochureWrapper = contentDiv.querySelector('.brochure-download-wrapper');
    if (filterSection) filterSection.style.display = '';
    if (grid) grid.style.display = '';
    if (brochureWrapper) brochureWrapper.style.display = '';

    // تحديث URL - إزالة معامل conference
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.delete('conference');
    urlParams.set('tab', 'conferences');
    window.history.pushState({}, '', window.location.pathname + '?' + urlParams.toString());
}

/**
 * ربط الأحداث للأزرار داخل التفاصيل (مشاركة، تسجيل)
 * @param {HTMLElement} container - العنصر الذي يحتوي على التفاصيل
 */
function attachDetailHandlers(container) {
    // زر المشاركة
    const shareBtn = container.querySelector('.share-contact-btn');
    if (shareBtn) {
        shareBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.openConferenceShareModal();  // فتح مودال المشاركة الخاص بالمؤتمرات
        });
    }

    // زر التسجيل
    const registerBtn = container.querySelector('.btn-register-detail');
    if (registerBtn && !registerBtn.disabled && window.openConferenceRegistrationModalList) {
        registerBtn.addEventListener('click', () => {
            const confId = registerBtn.getAttribute('data-conference-id');
            if (confId) window.openConferenceRegistrationModalList(confId);
        });
    }
}

/**
 * إعداد روابط البطاقات في تبويب المؤتمرات
 */
export function setupConferenceCards() {
    const cards = document.querySelectorAll('#conferences-content .conference-card');
    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            // تجاهل النقر على زر التسجيل نفسه
            if (e.target.closest('.register-conference-btn')) return;

            const conferenceId = this.getAttribute('data-conference-id');
            if (conferenceId) {
                loadConferenceDetail(conferenceId);
            }
        });
        card.style.cursor = 'pointer';
    });
}