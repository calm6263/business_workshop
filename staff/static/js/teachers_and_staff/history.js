// static/js/teachers_and_staff/history.js
// ========================================

import { loadMemberDetailInPlace, getCurrentMemberId } from './memberDetail.js';
import { showCardsView } from './memberDetail.js';

export function setupBrowserHistory() {
    window.addEventListener('popstate', function(event) {
        const urlParams = new URLSearchParams(window.location.search);
        const memberId = urlParams.get('member');
        
        if (memberId && event.state && event.state.memberId) {
            if (!document.querySelector('.member-detail-inline')) {
                const card = document.querySelector(`[data-member-id="${memberId}"]`);
                if (card) {
                    const cardElement = card.closest('.teacher-card, .council-card, .staff-card');
                    currentMemberSection = cardElement.closest('.department-section');
                    loadMemberDetailInPlace(memberId);
                }
            }
        } else {
            showCardsView();
        }
    });
}

export function setupUrlHandling() {
    const urlParams = new URLSearchParams(window.location.search);
    const memberId = urlParams.get('member');
    if (memberId) {
        setTimeout(() => {
            const card = document.querySelector(`[data-member-id="${memberId}"]`);
            if (card) {
                const cardElement = card.closest('.teacher-card, .council-card, .staff-card');
                currentMemberSection = cardElement.closest('.department-section');
                loadMemberDetailInPlace(memberId);
            }
        }, 500);
    }
}