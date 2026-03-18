// static/js/teachers_and_staff/tabs.js
// =====================================

import { smoothScrollTo } from './utils.js';

let activeTab = 'teachers-section';

export function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    // إخفاء جميع المحتويات وإظهار الأول فقط
    tabPanes.forEach(pane => {
        pane.classList.remove('active');
    });
    
    // إظهار المحتوى الأول فقط
    const firstTab = document.querySelector('.tab-button[data-target="teachers-section"]');
    const firstPane = document.querySelector('#teachers-section');
    if (firstTab && firstPane) {
        firstTab.classList.add('active');
        firstPane.classList.add('active');
        activeTab = 'teachers-section';
    }
    
    // إضافة مستمعي الأحداث لأزرار التبويب
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('active')) return;
            
            const targetId = this.getAttribute('data-target');
            const targetPane = document.getElementById(targetId);
            
            if (!targetPane) return;
            
            // إزالة النشاط من جميع الأزرار
            tabButtons.forEach(btn => {
                btn.classList.remove('active');
            });
            
            // إخفاء جميع المحتويات
            tabPanes.forEach(pane => {
                pane.classList.remove('active');
            });
            
            // إضافة النشاط للزر المحدد والمحتوى المقابل
            this.classList.add('active');
            targetPane.classList.add('active');
            activeTab = targetId;
            
            // التمرير السلس إلى القسم
            setTimeout(() => {
                smoothScrollTo(targetPane, 100);
            }, 100);
        });
    });
}

export function getActiveTab() {
    return activeTab;
}

export function switchToTab(tabId) {
    const tabButton = document.querySelector(`.tab-button[data-target="${tabId}"]`);
    if (tabButton) {
        tabButton.click();
    }
}