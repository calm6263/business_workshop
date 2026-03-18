// research/static/research/js/utils.js
export function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.style.display = 'flex';
}

export function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        setTimeout(() => overlay.style.display = 'none', 300);
    }
}

export function createElement(tag, className, innerHTML = '') {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (innerHTML) el.innerHTML = innerHTML;
    return el;
}