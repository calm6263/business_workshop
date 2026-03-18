// patents/static/patents/js/patents.js

document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('patentsCarousel');
    const captionElement = document.getElementById('patentCaption');
    
    if (!carousel || !captionElement) return;

    // دالة لتحديث النص بناءً على السلايد النشط
    function updateCaption() {
        const activeItem = carousel.querySelector('.carousel-item.active');
        if (activeItem) {
            // استخدام textContent بدلاً من innerHTML لمنع XSS
            captionElement.textContent = activeItem.dataset.caption || 'Патент на изобретение';
        }
    }

    // تحديث النص عند التبديل بين السلايدات
    carousel.addEventListener('slid.bs.carousel', updateCaption);

    // تحديث النص عند التحميل الأول
    updateCaption();
});