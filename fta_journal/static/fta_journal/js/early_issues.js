document.addEventListener('DOMContentLoaded', function() {
    const filterToggle = document.getElementById('filterToggle');
    const filterDropdown = document.getElementById('filterDropdown');

    if (filterToggle && filterDropdown) {
        filterToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            filterDropdown.classList.toggle('show');
        });

        document.querySelectorAll('.filter-option').forEach(option => {
            option.addEventListener('click', function(e) {
                e.stopPropagation();
                const period = this.dataset.period;
                const urlParams = new URLSearchParams(window.location.search);
                
                if (period === 'all') {
                    urlParams.delete('period');
                } else {
                    urlParams.set('period', period);
                }
                // الحفاظ على التبويب والصفحة
                urlParams.set('tab', 'journal');
                urlParams.set('journal_page', 'early');
                
                window.location.search = urlParams.toString();
            });
        });

        document.addEventListener('click', function(e) {
            if (!filterToggle.contains(e.target) && !filterDropdown.contains(e.target)) {
                filterDropdown.classList.remove('show');
            }
        });
    }
});