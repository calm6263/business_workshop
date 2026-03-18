// static/js/teachers_and_staff/utils.js
// =====================================

// دوال التحكم بالتحميل
export function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

export function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        setTimeout(() => {
            overlay.style.display = 'none';
        }, 300);
    }
}

// التمرير السلس
export function smoothScrollTo(element, offset = 100) {
    const elementPosition = element.offsetTop;
    const offsetPosition = elementPosition - offset;
    
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

// التحقق من طلب AJAX
export function isAjaxRequest(headers) {
    return headers.get('X-Requested-With') === 'XMLHttpRequest';
}

// إنشاء عناصر DOM
export function createElement(tag, className, innerHTML = '') {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (innerHTML) element.innerHTML = innerHTML;
    return element;
}

// التأخير
export function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}