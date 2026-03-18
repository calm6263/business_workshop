// about_academy/js/about_academy.js

document.addEventListener('DOMContentLoaded', function() {
    // Full width adjustment for hero section
    function setFullWidth() {
        const heroSection = document.querySelector('.academy-hero-fullwidth');
        const backgroundContainer = document.querySelector('.hero-background-container');
        const backgroundImage = document.querySelector('.hero-background-image');

        if (heroSection) {
            heroSection.style.width = '100vw';
            heroSection.style.marginLeft = 'calc(-50vw + 50%)';
            heroSection.style.marginRight = 'calc(-50vw + 50%)';
            heroSection.style.left = '0';
            heroSection.style.right = '0';
        }

        if (backgroundContainer) {
            backgroundContainer.style.width = '100vw';
            backgroundContainer.style.maxWidth = 'none';
        }

        if (backgroundImage) {
            backgroundImage.style.width = '100vw';
            backgroundImage.style.maxWidth = 'none';
            backgroundImage.style.minWidth = '100vw';
        }
    }

    setFullWidth();
    window.addEventListener('resize', setFullWidth);

    // Tabs functionality
    const navTabsHero = document.querySelectorAll('.nav-tab-hero');
    const aboutSection = document.getElementById('about');
    const leadershipDynamic = document.getElementById('leadership-dynamic-content');
    let teamDynamic = document.getElementById('team-dynamic-content');
    const downloadSection = document.getElementById('downloadable-section');

    function toggleDownloadButton(show) {
        if (downloadSection) {
            downloadSection.style.display = show ? 'block' : 'none';
        }
    }

    if (!teamDynamic) {
        teamDynamic = document.createElement('div');
        teamDynamic.id = 'team-dynamic-content';
        teamDynamic.className = 'team-dynamic-content';
        teamDynamic.style.display = 'none';
        const mainContent = document.querySelector('.academy-main-content');
        if (mainContent) {
            mainContent.appendChild(teamDynamic);
        } else {
            document.body.appendChild(teamDynamic);
        }
    }

    window.carouselInitialized = false;

    function scrollToMainContent() {
        const mainContent = document.querySelector('.academy-main-content');
        if (mainContent) {
            window.scrollTo({
                top: mainContent.offsetTop,
                behavior: 'smooth'
            });
        }
    }

    // ========== Team Member Detail Functions ==========
    function attachTeamCardEvents() {
        const teamCards = document.querySelectorAll('#team-dynamic-content .view-member-detail');
        teamCards.forEach(card => {
            card.addEventListener('click', async function(e) {
                e.preventDefault();
                e.stopPropagation();

                const memberId = this.getAttribute('data-member-id');
                await loadTeamMemberDetail(memberId);
            });
        });
    }

    async function loadTeamMemberDetail(memberId) {
        const teamContainer = document.getElementById('team-dynamic-content');
        if (!teamContainer) return;

        teamContainer.innerHTML = '<div class="detail-loading"><div class="spinner"></div><p>Загрузка профиля...</p></div>';

        try {
            const response = await fetch(`/about-academy/team-member/${memberId}/detail/`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });

            if (!response.ok) throw new Error('Network error');

            const html = await response.text();
            teamContainer.innerHTML = html;

            // ربط حدث زر العودة الموجود في القالب
            const backButton = teamContainer.querySelector('.back-to-cards-btn');
            if (backButton) {
                backButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    showTeamListView();
                });
            }

            // ربط حدث زر المشاركة
            const shareBtn = teamContainer.querySelector('.share-contact-btn');
            if (shareBtn) {
                shareBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    const url = window.location.href;
                    navigator.clipboard.writeText(url).then(() => {
                        alert('Ссылка скопирована в буфер обмена');
                    }).catch(() => {
                        alert('Не удалось скопировать ссылку');
                    });
                });
            }

            // Update URL
            const url = new URL(window.location);
            url.searchParams.set('team_member', memberId);
            window.history.pushState({ teamMemberId: memberId }, '', url);

        } catch (error) {
            console.error('Error loading team member detail:', error);
            teamContainer.innerHTML = '<p class="text-danger">Ошибка загрузки данных.</p>';
            setTimeout(showTeamListView, 2000);
        }
    }

    function showTeamListView() {
        const teamContainer = document.getElementById('team-dynamic-content');
        if (!teamContainer) return;

        teamContainer.innerHTML = '<div class="detail-loading"><div class="spinner"></div><p>Загрузка списка...</p></div>';

        fetch('/about-academy/team-partial/')
            .then(response => response.text())
            .then(html => {
                teamContainer.innerHTML = html;
                attachTeamCardEvents();
                initTeamFilters();
                const url = new URL(window.location);
                url.searchParams.delete('team_member');
                window.history.replaceState({}, '', url);
            })
            .catch(err => {
                console.error('Error reloading team list:', err);
                teamContainer.innerHTML = '<p class="text-danger">Ошибка загрузки списка.</p>';
            });
    }

    // ========== Leadership Functions ==========
    function showAbout() {
        aboutSection.style.display = 'block';
        leadershipDynamic.style.display = 'none';
        teamDynamic.style.display = 'none';
        toggleDownloadButton(true);

        if (!window.carouselInitialized) {
            initVideoCarousel();
            window.carouselInitialized = true;
        }

        scrollToMainContent();
    }

    function showLeadership() {
        aboutSection.style.display = 'none';
        teamDynamic.style.display = 'none';
        leadershipDynamic.style.display = 'block';
        toggleDownloadButton(false);

        if (!leadershipDynamic.innerHTML.trim()) {
            fetch('/about-academy/leadership-detail/')
                .then(response => response.text())
                .then(html => {
                    leadershipDynamic.innerHTML = html;
                    const shareBtn = leadershipDynamic.querySelector('.share-contact-btn');
                    if (shareBtn) {
                        shareBtn.addEventListener('click', function(e) {
                            e.preventDefault();
                            e.stopPropagation();
                            const url = window.location.href;
                            navigator.clipboard.writeText(url).then(() => {
                                alert('Ссылка скопирована в буфер обмена');
                            }).catch(() => {
                                alert('Не удалось скопировать ссылку');
                            });
                        });
                    }
                    scrollToMainContent();
                })
                .catch(err => console.error('Error loading leadership data:', err));
        } else {
            scrollToMainContent();
        }
    }

    function showTeam() {
        aboutSection.style.display = 'none';
        leadershipDynamic.style.display = 'none';
        teamDynamic.style.display = 'block';
        toggleDownloadButton(false);

        if (!teamDynamic.innerHTML.trim()) {
            fetch('/about-academy/team-partial/')
                .then(response => response.text())
                .then(html => {
                    teamDynamic.innerHTML = html;
                    attachTeamCardEvents();
                    initTeamFilters();
                    scrollToMainContent();
                })
                .catch(err => console.error('Error loading team data:', err));
        } else {
            attachTeamCardEvents();
            scrollToMainContent();
        }
    }

    // ========== Team Filters (copied from original) ==========
    function initTeamFilters() {
        const filterTrigger = document.querySelector('#team-filters .filter-trigger');
        const filterDropdown = document.querySelector('#team-filters .filter-dropdown');
        const filterOptions = document.querySelectorAll('#team-filters .filter-option');
        const filterLabel = document.querySelector('#team-filters .filter-label');
        const filterArrow = document.querySelector('#team-filters .filter-arrow');

        if (!filterTrigger) return;

        filterTrigger.addEventListener('click', function(e) {
            e.stopPropagation();
            filterTrigger.classList.toggle('active');
            filterDropdown.classList.toggle('show');
            filterArrow.classList.toggle('open');
        });

        filterOptions.forEach(opt => {
            opt.addEventListener('click', function() {
                const filterValue = this.getAttribute('data-filter');
                filterLabel.textContent = this.querySelector('.option-text').textContent;
                filterOptions.forEach(o => o.classList.remove('active'));
                this.classList.add('active');
                filterTrigger.classList.remove('active');
                filterDropdown.classList.remove('show');
                filterArrow.classList.remove('open');
                applyTeamFilter(filterValue);
            });
        });

        document.addEventListener('click', function(e) {
            if (!filterTrigger.contains(e.target) && !filterDropdown.contains(e.target)) {
                filterTrigger.classList.remove('active');
                filterDropdown.classList.remove('show');
                filterArrow.classList.remove('open');
            }
        });
    }

    function applyTeamFilter(filterValue) {
        const departmentSections = document.querySelectorAll('.department-section');
        if (filterValue === 'all') {
            departmentSections.forEach(section => section.style.display = 'block');
        } else {
            departmentSections.forEach(section => {
                if (section.id === filterValue) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
        }
    }

    // ========== Attach Tab Handlers ==========
    navTabsHero.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();

            navTabsHero.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            const targetId = this.getAttribute('href').substring(1); // about, leadership, team

            if (targetId === 'about') {
                showAbout();
            } else if (targetId === 'leadership') {
                showLeadership();
            } else if (targetId === 'team') {
                showTeam();
            }
        });
    });

    // Activate first tab
    const firstTab = document.querySelector('.nav-tab-hero[href="#about"]');
    if (firstTab) {
        firstTab.classList.add('active');
        showAbout();
    } else {
        showAbout();
    }

    // ========== Video Carousel ==========
    function initVideoCarousel() {
        const carousel = document.querySelector('.leader-videos-carousel');
        if (!carousel) return;

        const slidesContainer = carousel.querySelector('.carousel-slides');
        const slides = carousel.querySelectorAll('.carousel-slide');
        const prevBtn = carousel.querySelector('.carousel-prev');
        const nextBtn = carousel.querySelector('.carousel-next');
        const dotsContainer = carousel.querySelector('.carousel-dots');

        if (!slides.length) return;

        let currentIndex = 0;

        dotsContainer.innerHTML = '';

        slides.forEach((_, idx) => {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (idx === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToSlide(idx));
            dotsContainer.appendChild(dot);
        });

        const dots = dotsContainer.querySelectorAll('.dot');

        function hideVideo(slide) {
            const video = slide.querySelector('video');
            if (video) {
                video.style.opacity = '0';
                video.style.transition = 'opacity 0.2s';
            }
        }

        function showVideo(slide) {
            const video = slide.querySelector('video');
            if (video) {
                video.style.opacity = '1';
                video.controls = false;
                requestAnimationFrame(() => {
                    video.controls = true;
                });
            }
        }

        function goToSlide(index) {
            if (index < 0) index = slides.length - 1;
            if (index >= slides.length) index = 0;

            hideVideo(slides[currentIndex]);

            currentIndex = index;
            slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
            dots.forEach((dot, i) => dot.classList.toggle('active', i === currentIndex));
        }

        slidesContainer.addEventListener('transitionend', function() {
            showVideo(slides[currentIndex]);
        });

        setTimeout(() => {
            showVideo(slides[0]);
        }, 200);

        prevBtn.addEventListener('click', () => goToSlide(currentIndex - 1));
        nextBtn.addEventListener('click', () => goToSlide(currentIndex + 1));

        document.addEventListener('keydown', (e) => {
            if (carousel.closest('.content-section')?.style.display !== 'none') {
                if (e.key === 'ArrowLeft') goToSlide(currentIndex - 1);
                if (e.key === 'ArrowRight') goToSlide(currentIndex + 1);
            }
        });
    }

    // ========== History Handling (back/forward) ==========
    window.addEventListener('popstate', function(event) {
        const urlParams = new URLSearchParams(window.location.search);
        const memberId = urlParams.get('team_member');
        if (memberId) {
            loadTeamMemberDetail(memberId);
        } else {
            // If no member param, ensure we show the team list if team tab is active
            if (teamDynamic && teamDynamic.style.display === 'block') {
                showTeamListView();
            }
        }
    });

    // Initial event attachment if team is visible on load
    if (teamDynamic && teamDynamic.style.display !== 'none') {
        attachTeamCardEvents();
    }
});