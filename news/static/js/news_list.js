// news_list.js
document.addEventListener('DOMContentLoaded', function() {
    // فلترة الأخبار حسب الوقت (الموجود سابقاً)
    const filterItems = document.querySelectorAll('.filter-item');
    
    filterItems.forEach(item => {
        item.addEventListener('click', function() {
            filterItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            const filterType = this.getAttribute('data-filter');
            const newsItems = document.querySelectorAll('.news-item');
            const currentDate = new Date();
            
            newsItems.forEach(newsItem => {
                const itemDate = new Date(newsItem.getAttribute('data-date'));
                
                switch(filterType) {
                    case 'past':
                        newsItem.style.display = itemDate < currentDate ? 'block' : 'none';
                        break;
                    case 'present':
                        const currentMonth = currentDate.getMonth();
                        const currentYear = currentDate.getFullYear();
                        newsItem.style.display = (itemDate.getMonth() === currentMonth && itemDate.getFullYear() === currentYear) ? 'block' : 'none';
                        break;
                    case 'future':
                        newsItem.style.display = itemDate > currentDate ? 'block' : 'none';
                        break;
                    default:
                        newsItem.style.display = 'block';
                }
            });
        });
    });

    // كود الفلاتر الجديدة (التصنيف والترتيب)
    const filterSections = document.querySelectorAll('.news-filters-section .main-filter');
    
    function closeAllDropdowns() {
        filterSections.forEach(container => {
            const trigger = container.querySelector('.filter-trigger');
            const dropdown = container.querySelector('.filter-dropdown');
            const arrow = container.querySelector('.filter-arrow');
            if (trigger) trigger.classList.remove('active');
            if (dropdown) dropdown.classList.remove('show');
            if (arrow) arrow.classList.remove('open');
        });
    }

    filterSections.forEach(container => {
        const trigger = container.querySelector('.filter-trigger');
        const dropdown = container.querySelector('.filter-dropdown');
        const arrow = container.querySelector('.filter-arrow');
        const options = container.querySelectorAll('.filter-option');

        if (!trigger || !dropdown) return;

        trigger.addEventListener('click', function(e) {
            e.stopPropagation();
            const isOpen = dropdown.classList.contains('show');
            closeAllDropdowns();
            if (!isOpen) {
                trigger.classList.add('active');
                dropdown.classList.add('show');
                if (arrow) arrow.classList.add('open');
            }
        });

        options.forEach(option => {
            option.addEventListener('click', function(e) {
                e.stopPropagation();

                const category = this.dataset.filterCategory;
                const sort = this.dataset.filterSort;

                const urlParams = new URLSearchParams(window.location.search);
                const currentTab = urlParams.get('tab') || 'news';

                if (category !== undefined) {
                    if (category) urlParams.set('category', category);
                    else urlParams.delete('category');
                }
                if (sort !== undefined) {
                    if (sort && sort !== 'newest') urlParams.set('sort', sort);
                    else urlParams.delete('sort');
                }

                // الحفاظ على التبويب الحالي
                urlParams.set('tab', currentTab);

                window.location.href = window.location.pathname + '?' + urlParams.toString();
            });
        });
    });

    document.addEventListener('click', closeAllDropdowns);
    document.querySelectorAll('.news-filters-section .filter-dropdown').forEach(d => {
        d.addEventListener('click', e => e.stopPropagation());
    });

    // معالجة نموذج البحث
    const searchForm = document.getElementById('newsSearchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchInput = this.querySelector('.news-search-input');
            const query = searchInput.value.trim();
            const urlParams = new URLSearchParams(window.location.search);
            const currentTab = urlParams.get('tab') || 'news';
            
            if (query) {
                urlParams.set('q', query);
            } else {
                urlParams.delete('q');
            }
            
            urlParams.delete('page');
            urlParams.set('tab', currentTab);
            
            window.location.href = window.location.pathname + '?' + urlParams.toString();
        });
    }

    console.log('News list page loaded with tabs and filtering');
});