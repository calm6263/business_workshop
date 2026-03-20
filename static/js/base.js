// ===== إدارة القوائم المنسدلة الأساسية =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('بدء تهيئة القوائم المنسدلة...');
    
    // ===== 1. قائمة اللغات =====
    const flagContainer = document.getElementById('flagContainer');
    const languageDropdown = document.getElementById('languageDropdown');
    
    if (flagContainer && languageDropdown) {
        console.log('تهيئة قائمة اللغات...');
        
        flagContainer.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const accountDropdown = document.getElementById('accountDropdown');
            if (accountDropdown && accountDropdown.classList.contains('active')) {
                accountDropdown.classList.remove('active');
            }
            
            languageDropdown.classList.toggle('active');
            flagContainer.classList.toggle('active');
        });
        
        document.addEventListener('click', function(e) {
            if (!flagContainer.contains(e.target) && !languageDropdown.contains(e.target)) {
                languageDropdown.classList.remove('active');
                flagContainer.classList.remove('active');
            }
        });
        
        languageDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // ===== 2. قائمة الحساب =====
    const accountBtn = document.getElementById('accountBtn');
    const accountDropdown = document.getElementById('accountDropdown');
    
    if (accountBtn && accountDropdown) {
        console.log('تهيئة قائمة الحساب...');
        
        accountBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const languageDropdown = document.getElementById('languageDropdown');
            const flagContainer = document.getElementById('flagContainer');
            if (languageDropdown && languageDropdown.classList.contains('active')) {
                languageDropdown.classList.remove('active');
            }
            if (flagContainer && flagContainer.classList.contains('active')) {
                flagContainer.classList.remove('active');
            }
            
            accountDropdown.classList.toggle('active');
        });
        
        document.addEventListener('click', function(e) {
            if (!accountBtn.contains(e.target) && !accountDropdown.contains(e.target)) {
                accountDropdown.classList.remove('active');
            }
        });
        
        accountDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // ===== 3. البحث - النسخة المحسنة =====
    const searchIcon = document.getElementById('searchIcon');
    const searchBox = document.getElementById('searchBox');
    
    if (searchIcon && searchBox) {
        console.log('تهيئة مربع البحث...');
        
        const isIndexPage = document.body.classList.contains('index-page');
        const isLargeScreen = window.innerWidth >= 992;
        
        if (isIndexPage && isLargeScreen) {
            searchBox.style.display = 'none';
        } else {
            searchIcon.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const isActive = searchBox.classList.contains('active');
                if (isActive) {
                    searchBox.classList.remove('active');
                } else {
                    searchBox.classList.add('active');
                    setTimeout(() => {
                        const searchInput = searchBox.querySelector('.search-input');
                        if (searchInput) searchInput.focus();
                    }, 100);
                }
            });
            
            document.addEventListener('click', function(e) {
                if (!searchIcon.contains(e.target) && !searchBox.contains(e.target)) {
                    searchBox.classList.remove('active');
                }
            });
            
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && searchBox.classList.contains('active')) {
                    searchBox.classList.remove('active');
                }
            });
            
            searchBox.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    }
    
    // ===== 4. القوائم المنسدلة الرئيسية (للجوال فقط) - باستخدام تفويض الأحداث =====
    function handleMobileDropdowns() {
        // إزالة سمة data-bs-toggle لمنع Bootstrap من التداخل
        const toggles = document.querySelectorAll('.dropdown-toggle');
        toggles.forEach(toggle => {
            if (window.innerWidth <= 992) {
                toggle.removeAttribute('data-bs-toggle');
                toggle.setAttribute('data-mobile-toggle', 'true');
            } else {
                if (toggle.getAttribute('data-mobile-toggle') === 'true') {
                    toggle.removeAttribute('data-mobile-toggle');
                    toggle.setAttribute('data-bs-toggle', 'dropdown');
                }
            }
        });
        
        // إزالة المستمع القديم إن وجد
        document.removeEventListener('click', mobileDropdownHandler);
        // إضافة مستمع جديد باستخدام تفويض الأحداث
        document.addEventListener('click', mobileDropdownHandler);
    }
    
    function mobileDropdownHandler(e) {
        // نعمل فقط على الشاشات الصغيرة
        if (window.innerWidth > 992) return;
        
        const toggle = e.target.closest('.dropdown-toggle');
        if (!toggle) return;
        
        e.preventDefault();
        e.stopPropagation();
        
        // إغلاق قوائم اللغات والحساب
        closeLanguageAndAccount();
        
        const dropdownMenu = toggle.nextElementSibling;
        if (!dropdownMenu) return;
        
        const isShowing = dropdownMenu.classList.contains('show') || 
                         dropdownMenu.style.display === 'block';
        
        // إغلاق جميع القوائم الأخرى
        document.querySelectorAll('.dropdown-menu-custom').forEach(menu => {
            if (menu !== dropdownMenu) {
                menu.classList.remove('show');
                menu.style.display = 'none';
            }
        });
        
        if (!isShowing) {
            dropdownMenu.classList.add('show');
            dropdownMenu.style.display = 'block';
        } else {
            dropdownMenu.classList.remove('show');
            dropdownMenu.style.display = 'none';
        }
    }
    
    // ===== 5. القوائم المنسدلة الرئيسية (للسطح المكتب) =====
    function handleDesktopDropdowns() {
        // استعادة سمة data-bs-toggle للعناصر التي أزيلت منها
        const toggles = document.querySelectorAll('.dropdown-toggle');
        toggles.forEach(toggle => {
            if (toggle.getAttribute('data-mobile-toggle') === 'true') {
                toggle.removeAttribute('data-mobile-toggle');
                toggle.setAttribute('data-bs-toggle', 'dropdown');
            }
        });
        
        // إزالة مستمع الجوال إن كان موجوداً
        document.removeEventListener('click', mobileDropdownHandler);
        
        // السماح لـ Bootstrap بالعمل
        // (لا حاجة لتدخل يدوي)
    }
    
    // ===== 6. وظائف مساعدة =====
    function closeAllDropdowns() {
        document.querySelectorAll('.dropdown-menu-custom').forEach(menu => {
            menu.classList.remove('show');
            menu.style.display = 'none';
        });
        closeLanguageAndAccount();
    }
    
    function closeLanguageAndAccount() {
        const languageDropdown = document.getElementById('languageDropdown');
        const flagContainer = document.getElementById('flagContainer');
        const accountDropdown = document.getElementById('accountDropdown');
        
        if (languageDropdown) languageDropdown.classList.remove('active');
        if (flagContainer) flagContainer.classList.remove('active');
        if (accountDropdown) accountDropdown.classList.remove('active');
    }
    
    // ===== 7. التهيئة حسب حجم الشاشة =====
    function initializeBasedOnScreenSize() {
        if (window.innerWidth <= 992) {
            console.log('تهيئة وضع الجوال...');
            handleMobileDropdowns();
        } else {
            console.log('تهيئة وضع سطح المكتب...');
            handleDesktopDropdowns();
        }
    }
    
    // جعل الدالة عامة لتستدعي من خارج الملف
    window.reinitMobileDropdowns = function() {
        if (window.innerWidth <= 992) {
            console.log('إعادة تهيئة القوائم المنسدلة للجوال...');
            handleMobileDropdowns();
        }
    };
    
    // التهيئة الأولية
    initializeBasedOnScreenSize();
    
    // إعادة التهيئة عند تغيير حجم النافذة
    window.addEventListener('resize', function() {
        console.log('تغيير حجم الشاشة، إعادة التهيئة...');
        closeAllDropdowns();
        initializeBasedOnScreenSize();
    });
    
    // ===== 8. بطاقات الخدمات =====
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            if (url && url !== '#') {
                window.location.href = url;
            }
        });
        card.style.cursor = 'pointer';
    });
    
    // ===== 9. الروابط المعطلة =====
    const disabledLinks = document.querySelectorAll('.disabled-link, .account-option.disabled');
    disabledLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            alert('Эта функция временно недоступна');
        });
        link.style.cursor = 'not-allowed';
    });
    
    // ===== 10. تأكيد تسجيل الخروج =====
    const logoutLinks = document.querySelectorAll('a[href*="logout"]');
    logoutLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите выйти?')) {
                e.preventDefault();
            }
        });
    });
    
    console.log('تهيئة القوائم المنسدلة مكتملة');
});