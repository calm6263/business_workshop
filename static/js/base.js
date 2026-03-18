// ===== إدارة القوائم المنسدلة الأساسية =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('بدء تهيئة القوائم المنسدلة...');
    
    // ===== 1. قائمة اللغات =====
    const flagContainer = document.getElementById('flagContainer');
    const languageDropdown = document.getElementById('languageDropdown');
    
    if (flagContainer && languageDropdown) {
        console.log('تهيئة قائمة اللغات...');
        
        // النقر على علم/نص اللغة
        flagContainer.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // إغلاق قائمة الحساب إذا كانت مفتوحة
            const accountDropdown = document.getElementById('accountDropdown');
            if (accountDropdown && accountDropdown.classList.contains('active')) {
                accountDropdown.classList.remove('active');
            }
            
            // تبديل قائمة اللغة
            languageDropdown.classList.toggle('active');
            flagContainer.classList.toggle('active');
        });
        
        // إغلاق عند النقر خارجها
        document.addEventListener('click', function(e) {
            if (!flagContainer.contains(e.target) && !languageDropdown.contains(e.target)) {
                languageDropdown.classList.remove('active');
                flagContainer.classList.remove('active');
            }
        });
        
        // منع إغلاق عند النقر داخل القائمة
        languageDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // ===== 2. قائمة الحساب =====
    const accountBtn = document.getElementById('accountBtn');
    const accountDropdown = document.getElementById('accountDropdown');
    
    if (accountBtn && accountDropdown) {
        console.log('تهيئة قائمة الحساب...');
        
        // النقر على أيقونة الحساب
        accountBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // إغلاق قائمة اللغة إذا كانت مفتوحة
            const languageDropdown = document.getElementById('languageDropdown');
            const flagContainer = document.getElementById('flagContainer');
            if (languageDropdown && languageDropdown.classList.contains('active')) {
                languageDropdown.classList.remove('active');
            }
            if (flagContainer && flagContainer.classList.contains('active')) {
                flagContainer.classList.remove('active');
            }
            
            // تبديل قائمة الحساب
            accountDropdown.classList.toggle('active');
        });
        
        // إغلاق عند النقر خارجها
        document.addEventListener('click', function(e) {
            if (!accountBtn.contains(e.target) && !accountDropdown.contains(e.target)) {
                accountDropdown.classList.remove('active');
            }
        });
        
        // منع إغلاق عند النقر داخل القائمة
        accountDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // ===== 3. البحث - النسخة المحسنة =====
    const searchIcon = document.getElementById('searchIcon');
    const searchBox = document.getElementById('searchBox');
    
    if (searchIcon && searchBox) {
        console.log('تهيئة مربع البحث...');
        
        // التحقق مما إذا كنا في صفحة index وفي الشاشات الكبيرة
        const isIndexPage = document.body.classList.contains('index-page');
        const isLargeScreen = window.innerWidth >= 992;
        
        if (isIndexPage && isLargeScreen) {
            // في صفحة index للشاشات الكبيرة: إخفاء مربع البحث التلقائي
            searchBox.style.display = 'none';
            // السلوك الخاص للبحث في index.js (Overlay menu)
        } else {
            // في باقي الصفحات أو الشاشات الصغيرة: سلوك مبسط للنقر فقط
            searchIcon.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // تبديل حالة مربع البحث
                const isActive = searchBox.classList.contains('active');
                
                if (isActive) {
                    // إذا كان مفتوحاً، نغلقه
                    searchBox.classList.remove('active');
                } else {
                    // إذا كان مغلقاً، نفتحه ونركز على حقل الإدخال
                    searchBox.classList.add('active');
                    
                    // التركيز على حقل الإدخال بعد تأخير بسيط
                    setTimeout(() => {
                        const searchInput = searchBox.querySelector('.search-input');
                        if (searchInput) {
                            searchInput.focus();
                        }
                    }, 100);
                }
            });
            
            // إغلاق عند النقر خارج مربع البحث
            document.addEventListener('click', function(e) {
                if (!searchIcon.contains(e.target) && !searchBox.contains(e.target)) {
                    searchBox.classList.remove('active');
                }
            });
            
            // إغلاق عند الضغط على زر Escape
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && searchBox.classList.contains('active')) {
                    searchBox.classList.remove('active');
                }
            });
            
            // منع إغلاق مربع البحث عند النقر داخله
            searchBox.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    }
    
    // ===== 4. القوائم المنسدلة الرئيسية (للجوال فقط) =====
    function handleMobileDropdowns() {
        const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
        
        dropdownToggles.forEach(toggle => {
            // إزالة الأحداث السابقة لمنع التكرار
            const newToggle = toggle.cloneNode(true);
            toggle.parentNode.replaceChild(newToggle, toggle);
            
            // إضافة حدث النقر
            newToggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // إغلاق قوائم اللغات والحساب
                closeLanguageAndAccount();
                
                const dropdownMenu = this.nextElementSibling;
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
                
                // تبديل القائمة الحالية
                if (!isShowing) {
                    dropdownMenu.classList.add('show');
                    dropdownMenu.style.display = 'block';
                } else {
                    dropdownMenu.classList.remove('show');
                    dropdownMenu.style.display = 'none';
                }
            });
        });
        
        // إغلاق جميع القوائم عند النقر خارجها (للجوال)
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown-toggle') && !e.target.closest('.dropdown-menu-custom')) {
                closeAllDropdowns();
            }
        });
        
        // إغلاق عند التمرير (للجوال)
        window.addEventListener('scroll', function() {
            closeAllDropdowns();
        });
    }
    
    // ===== 5. القوائم المنسدلة الرئيسية (للسطح المكتب) =====
    function handleDesktopDropdowns() {
        // نستخدم Bootstrap للسطح المكتب، لكن نضيف بعض التحسينات
        
        // إغلاق القوائم عند النقر خارجها
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.nav-item.dropdown')) {
                // إغلاق قوائم Bootstrap يدوياً إذا لزم الأمر
                document.querySelectorAll('.dropdown-menu-custom.show').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
    }
    
    // ===== 6. وظائف مساعدة =====
    function closeAllDropdowns() {
        // إغلاق جميع القوائم المنسدلة
        document.querySelectorAll('.dropdown-menu-custom').forEach(menu => {
            menu.classList.remove('show');
            menu.style.display = 'none';
        });
        
        // إغلاق قوائم اللغات والحساب
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

// ===== تهيئة متأخرة للتأكد من تحميل جميع العناصر =====
setTimeout(function() {
    console.log('تهيئة متأخرة...');
    
    // إعادة ربط الأحداث للقوائم الرئيسية
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        // التأكد من أن لديهم أحداث النقر
        if (!toggle.hasAttribute('data-click-initialized')) {
            toggle.setAttribute('data-click-initialized', 'true');
            
            toggle.addEventListener('click', function(e) {
                // فقط للجوال
                if (window.innerWidth <= 992) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const dropdownMenu = this.nextElementSibling;
                    if (dropdownMenu) {
                        const isShowing = dropdownMenu.classList.contains('show');
                        
                        if (!isShowing) {
                            dropdownMenu.classList.add('show');
                            dropdownMenu.style.display = 'block';
                        } else {
                            dropdownMenu.classList.remove('show');
                            dropdownMenu.style.display = 'none';
                        }
                    }
                }
            });
        }
    });
}, 1000);