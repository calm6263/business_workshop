// static/js/teachers_and_staff/memberDetail.js
import { showLoading, hideLoading, createElement } from './utils.js';
import { applyFilter } from './filterUtils.js';
import { getCurrentFilter } from './filters.js';
import { openSharePopup } from './share.js';

let currentMemberSection = null;
let currentMemberId = null;

export function setupMemberCardEvents() {
    const memberCards = document.querySelectorAll('.view-member-detail');
    
    memberCards.forEach(card => {
        card.addEventListener('click', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const memberId = this.getAttribute('data-member-id');
            const cardElement = this.closest('.teacher-card, .council-card, .staff-card');
            
            // تحديد نوع العضو بناءً على class البطاقة
            let memberType = 'teacher';
            if (cardElement.classList.contains('council-card')) {
                memberType = 'council';
            } else if (cardElement.classList.contains('staff-card')) {
                memberType = 'staff';
            }
            
            currentMemberSection = cardElement.closest('.department-section');
            currentMemberId = memberId;
            
            await loadMemberDetailInPlace(memberId, memberType);
        });
    });
}

export async function loadMemberDetailInPlace(memberId, memberType) {
    try {
        showLoading();
        
        // إخفاء الفلتر
        document.body.classList.add('detail-view-active');
        
        if (!currentMemberSection) {
            throw new Error('No current member section found');
        }
        
        // إخفاء جميع البطاقات في القسم الحالي
        const allCards = currentMemberSection.querySelectorAll('.teacher-card, .council-card, .staff-card');
        const departmentTitle = currentMemberSection.querySelector('.department-title-wrapper');
        
        allCards.forEach(card => card.style.display = 'none');
        if (departmentTitle) departmentTitle.style.display = 'none';
        
        // إزالة أي حاوية تفاصيل قديمة
        const existingDetailContainer = currentMemberSection.querySelector('.member-detail-inline');
        if (existingDetailContainer) existingDetailContainer.remove();
        
        // إنشاء حاوية جديدة
        const detailContainer = createElement('div', 'member-detail-inline');
        detailContainer.innerHTML = `<div class="detail-loading"><div class="spinner"></div><p>Загрузка профиля...</p></div>`;
        currentMemberSection.insertBefore(detailContainer, currentMemberSection.firstChild);
        
        const response = await fetch(`/staff/member/${memberId}/detail/?type=${memberType}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        
        if (!response.ok) throw new Error('Network response was not ok');
        
        const html = await response.text();
        detailContainer.innerHTML = html;
        
        // ربط زر المشاركة (باستخدام الكلاس الجديد)
        const shareButton = detailContainer.querySelector('.share-contact-btn');
        if (shareButton) {
            shareButton.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                // استخدام الرابط الحالي للصفحة (مع query parameter member)
                const shareUrl = window.location.href;
                const memberName = detailContainer.querySelector('.member-detail-name')?.textContent || 'Преподаватель';
                openSharePopup(shareUrl, memberName);
            });
        }
        
        // إضافة زر الرجوع بتصميم محسّن
        const backButton = createElement('button', 'back-to-cards-btn', `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 12H4M4 12L10 18M4 12L10 6" stroke="#052946" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Назад
        `);
        backButton.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            showCardsView();
        };
        detailContainer.insertBefore(backButton, detailContainer.firstChild);
        
        // تحديث تاريخ المتصفح
        window.history.pushState(
            { memberId: memberId, section: currentMemberSection.id },
            '',
            `?member=${memberId}`
        );
        
    } catch (error) {
        console.error('Error loading member details:', error);
        alert('Ошибка загрузки данных. Пожалуйста, попробуйте еще раз.');
        showCardsView();
    } finally {
        hideLoading();
    }
}

export function showCardsView() {
    // إظهار الفلتر مرة أخرى
    document.body.classList.remove('detail-view-active');
    
    if (currentMemberSection) {
        const detailContainer = currentMemberSection.querySelector('.member-detail-inline');
        const allCards = currentMemberSection.querySelectorAll('.teacher-card, .council-card, .staff-card');
        const departmentTitle = currentMemberSection.querySelector('.department-title-wrapper');
        
        if (detailContainer) {
            detailContainer.remove();
            
            allCards.forEach(card => card.style.display = 'block');
            if (departmentTitle) departmentTitle.style.display = 'flex';
            
            // إعادة تطبيق الفلتر إذا كان نشطًا
            const currentFilter = getCurrentFilter();
            if (currentFilter) applyFilter(currentFilter);
            
            window.history.replaceState({}, '', window.location.pathname);
            currentMemberId = null;
        }
    }
}

export function getCurrentMemberId() {
    return currentMemberId;
}