// research/static/research/js/youthCouncilDetail.js
import { showLoading, hideLoading, createElement } from './utils.js';

// دالة تحميل التفاصيل (تم تصديرها للاستخدام الخارجي)
export async function loadYouthCouncilDetail(memberId, section) {
    try {
        showLoading();

        // إخفاء الفلتر
        const filterSection = document.querySelector('#youth-council-content .filters-section');
        if (filterSection) filterSection.style.display = 'none';

        const cards = section.querySelectorAll('.council-card');
        const title = section.querySelector('.department-title-wrapper');
        cards.forEach(c => c.style.display = 'none');
        if (title) title.style.display = 'none';

        const oldDetail = section.querySelector('.member-detail-inline');
        if (oldDetail) oldDetail.remove();

        const detailContainer = createElement('div', 'member-detail-inline');
        detailContainer.innerHTML = `<div class="detail-loading"><div class="spinner"></div><p>Загрузка...</p></div>`;
        section.insertBefore(detailContainer, section.firstChild);

        const response = await fetch(`/research/youth-council/${memberId}/detail/`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        if (!response.ok) throw new Error('Network error');
        const html = await response.text();
        detailContainer.innerHTML = html;

        const shareBtn = detailContainer.querySelector('.share-contact-btn');
        if (shareBtn) {
            shareBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const shareUrl = window.location.href;
                const memberName = detailContainer.querySelector('.member-detail-name')?.textContent || 'Член совета';
                openSharePopup(shareUrl, memberName);
            });
        }

        const backBtn = createElement('button', 'back-to-cards-btn', `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 12H4M4 12L10 18M4 12L10 6" stroke="#052946" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Назад
        `);
        backBtn.onclick = (e) => {
            e.preventDefault();
            showCardsView(section);
        };
        detailContainer.insertBefore(backBtn, detailContainer.firstChild);

        // تحديث URL مع معامل member و sectionId
        window.history.pushState(
            { memberId: memberId, sectionId: section.id },
            '',
            `?tab=youth-council&member=${memberId}`
        );

    } catch (error) {
        console.error(error);
        alert('Ошибка загрузки');
        showCardsView(section);
    } finally {
        hideLoading();
    }
}

// دالة العودة لعرض البطاقات (تم تصديرها)
export function showCardsView(section) {
    const detail = section.querySelector('.member-detail-inline');
    if (detail) detail.remove();

    // إظهار الفلتر مرة أخرى
    const filterSection = document.querySelector('#youth-council-content .filters-section');
    if (filterSection) filterSection.style.display = '';

    const cards = section.querySelectorAll('.council-card');
    const title = section.querySelector('.department-title-wrapper');
    cards.forEach(c => c.style.display = 'block');
    if (title) title.style.display = 'flex';

    // إزالة member من URL مع الحفاظ على tab
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.delete('member');
    urlParams.set('tab', 'youth-council');
    const newUrl = window.location.pathname + '?' + urlParams.toString();
    window.history.pushState({}, '', newUrl);
}

export function setupYouthCouncilCardEvents() {
    const cards = document.querySelectorAll('.view-youth-council-detail');
    cards.forEach(card => {
        card.addEventListener('click', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            const memberId = this.getAttribute('data-member-id');
            const cardElement = this.closest('.council-card');
            const departmentSection = cardElement.closest('.department-section');
            await loadYouthCouncilDetail(memberId, departmentSection);
        });
    });
}

function openSharePopup(url, title) {
    if (navigator.share) {
        navigator.share({ title: title, url: url }).catch(() => {});
    } else {
        alert('Скопируйте ссылку: ' + url);
    }
}