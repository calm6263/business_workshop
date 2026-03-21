// dashboards/static/dashboards/js/sidebar_scroll.js
document.addEventListener('DOMContentLoaded', function() {
    const sidebarNav = document.querySelector('.sidebar-nav');
    if (!sidebarNav) return;

    // استعادة موضع التمرير المحفوظ
    const savedScrollTop = localStorage.getItem('sidebar_scroll_top');
    if (savedScrollTop !== null) {
        sidebarNav.scrollTop = parseInt(savedScrollTop, 10);
    }

    // حفظ موضع التمرير عند النقر على أي رابط داخل الشريط الجانبي
    const sidebarLinks = sidebarNav.querySelectorAll('a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            localStorage.setItem('sidebar_scroll_top', sidebarNav.scrollTop);
        });
    });

    // (اختياري) حفظ الموضع عند مغادرة الصفحة كإجراء احتياطي
    window.addEventListener('beforeunload', function() {
        localStorage.setItem('sidebar_scroll_top', sidebarNav.scrollTop);
    });
});