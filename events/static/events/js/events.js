// events/static/events/js/events.js
// COMPLETE REFACTORED VERSION – مع تطبيق التوصيات الأمنية
// ========== GLOBAL HELPER FUNCTIONS ==========
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
window.getCookie = getCookie;

// ========== HIGHLIGHT SEARCH RESULTS ==========
function highlightSearchResults() {
    const searchInput = document.getElementById('searchInput');
    const searchQuery = searchInput ? searchInput.value : '';
    if (searchQuery && searchQuery.length > 0) {
        const eventCards = document.querySelectorAll('.event-card');
        eventCards.forEach(card => {
            const text = card.textContent.toLowerCase();
            if (text.includes(searchQuery.toLowerCase())) {
                card.classList.add('highlight');
            }
        });
    }
}

// ========== SHARE FUNCTIONALITY ==========
function getShareData() {
    const eventTitle = document.querySelector('.event-short-description')?.textContent.trim() || 'Мероприятие';
    const eventDate = document.getElementById('detail-date')?.textContent.trim() || '';
    const location = document.getElementById('detail-location')?.textContent.trim() || 'Уточняется';
    const eventUrl = window.location.href;

    const shareText = `${eventTitle}\nДата: ${eventDate}\nМесто: ${location}\nПодробнее: ${eventUrl}`;

    return {
        title: eventTitle,
        text: shareText,
        url: eventUrl
    };
}

function openShareModal(shareData) {
    const modal = document.getElementById('shareModal');
    if (!modal) return;

    const encodedText = encodeURIComponent(shareData.text);
    const encodedUrl = encodeURIComponent(shareData.url);

    document.getElementById('share-telegram')?.setAttribute('href', `https://t.me/share/url?url=${encodedUrl}&text=${encodedText}`);
    document.getElementById('share-whatsapp')?.setAttribute('href', `https://wa.me/?text=${encodedText}`);
    document.getElementById('share-vk')?.setAttribute('href', `https://vk.com/share.php?url=${encodedUrl}&title=${encodeURIComponent(shareData.title)}&comment=${encodedText}`);
    document.getElementById('share-twitter')?.setAttribute('href', `https://twitter.com/intent/tweet?text=${encodedText}`);

    const copyBtn = document.getElementById('share-copy-link');
    if (copyBtn) {
        const newCopyBtn = copyBtn.cloneNode(true);
        copyBtn.parentNode.replaceChild(newCopyBtn, copyBtn);
        newCopyBtn.addEventListener('click', function(e) {
            e.preventDefault();
            navigator.clipboard.writeText(shareData.url).then(() => {
                const notification = document.createElement('div');
                notification.className = 'copy-notification';
                notification.textContent = '✅ Ссылка скопирована';
                document.body.appendChild(notification);
                setTimeout(() => notification.remove(), 2000);
            }).catch(() => {
                alert('Не удалось скопировать ссылку');
            });
        });
    }

    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeShareModal() {
    const modal = document.getElementById('shareModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

function initShareModalListeners() {
    const modal = document.getElementById('shareModal');
    if (!modal) return;

    modal.addEventListener('click', function(e) {
        if (e.target === modal) closeShareModal();
    });

    const closeBtn = document.getElementById('shareModalClose');
    if (closeBtn) closeBtn.addEventListener('click', closeShareModal);

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            closeShareModal();
        }
    });
}

function attachShareHandler(eventId) {
    const shareBtn = document.querySelector('.share-contact-btn');
    if (!shareBtn) return;

    const newShareBtn = shareBtn.cloneNode(true);
    shareBtn.parentNode.replaceChild(newShareBtn, shareBtn);

    newShareBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        const shareData = getShareData();
        const isMobileScreen = window.matchMedia('(max-width: 768px)').matches;
        const isWebShareSupported = navigator.share && isMobileScreen;

        if (isWebShareSupported) {
            navigator.share({
                title: shareData.title,
                text: shareData.text,
                url: shareData.url
            }).catch(err => {
                if (err.name !== 'AbortError') {
                    console.warn('Web Share API failed, opening modal:', err);
                    openShareModal(shareData);
                }
            });
        } else {
            openShareModal(shareData);
        }
    });
}

// ========== LOAD EVENT DETAIL ==========
function loadEventDetail(eventId) {
    showLoadingIndicator();

    const searchSection = document.querySelector('.search-container-section');
    if (searchSection) searchSection.style.display = 'none';

    const filterContainer = document.querySelector('.container-custom > .filter-header-content')?.parentElement;
    if (filterContainer) filterContainer.style.display = 'none';

    fetch(`/events/api/${eventId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const event = data.event;

                document.getElementById('events-list-container').style.display = 'none';
                const detailContainer = document.getElementById('event-detail-container');
                detailContainer.style.display = 'block';

                const template = document.getElementById('event-detail-template');
                const content = template.content.cloneNode(true);

                // ===== ЗАПОЛНЕНИЕ ДАННЫМИ =====
                const img = content.querySelector('#detail-event-image');
                img.src = event.image_url;
                img.alt = event.title;

                const shortDescTop = content.querySelector('#detail-short-description-top');
                if (shortDescTop) shortDescTop.textContent = event.short_description || '';

                content.querySelector('#detail-organizers').textContent = event.organizers || 'Не указано';
                content.querySelector('#detail-price').textContent = event.price_display;
                content.querySelector('#detail-date').textContent = event.date;

                const timeElement = content.querySelector('#detail-time');
                if (event.time && timeElement) {
                    timeElement.textContent = ' ' + event.time;
                    timeElement.style.display = 'inline';
                } else if (timeElement) {
                    timeElement.style.display = 'none';
                }

                content.querySelector('#detail-location').textContent = event.location || 'Уточняется';

                const mapLink = content.querySelector('#show-on-map-link');
                if (mapLink) {
                    const location = event.location || '';
                    if (location && location !== 'Уточняется') {
                        const mapUrl = `https://yandex.ru/maps/?text=${encodeURIComponent(location)}`;
                        mapLink.href = mapUrl;
                        mapLink.style.display = 'inline-flex';
                    } else {
                        mapLink.style.display = 'none';
                    }
                }

                content.querySelector('#detail-contact-person').textContent = event.contact_person || 'Не указано';
                content.querySelector('#detail-contact-phone').textContent = event.contact_phone || 'Не указано';
                content.querySelector('#detail-contact-email').textContent = event.contact_email || 'Не указано';

                // ========== معالجة الوصف التفصيلي مع حماية XSS ==========
                const detailedDesc = content.querySelector('#detail-detailed-description');
                const placeholder = content.querySelector('#detail-description-placeholder');
                if (event.detailed_description) {
                    // استخدام DOMPurify لتنقية HTML إذا كان متاحاً
                    if (typeof DOMPurify !== 'undefined') {
                        detailedDesc.innerHTML = DOMPurify.sanitize(event.detailed_description);
                    } else {
                        // إذا لم يكن DOMPurify متاحاً، نستخدم textContent لمنع XSS
                        detailedDesc.textContent = event.detailed_description;
                    }
                    detailedDesc.style.display = 'block';
                    if (placeholder) placeholder.style.display = 'none';
                } else {
                    detailedDesc.style.display = 'none';
                    if (placeholder) {
                        placeholder.textContent = 'Нет подробного описания';
                        placeholder.style.display = 'block';
                    }
                }

                // زر التسجيل
                const buttonContainer = content.querySelector('#detail-register-button-container');
                if (event.can_register) {
                    const registerBtn = document.createElement('button');
                    registerBtn.className = 'btn-register-detail';
                    registerBtn.setAttribute('data-event-id', event.id);
                    registerBtn.textContent = 'Зарегистрироваться';
                    buttonContainer.appendChild(registerBtn);
                } else {
                    const disabledBtn = document.createElement('button');
                    disabledBtn.className = 'btn-register-detail registration-ended';
                    disabledBtn.disabled = true;
                    disabledBtn.textContent = 'Регистрация закрыта';
                    buttonContainer.appendChild(disabledBtn);
                }

                // فيديو
                const videoSection = content.querySelector('#detail-video-section');
                const videoSource = content.querySelector('#detail-video-player source');
                const videoTitle = content.querySelector('#detail-video-title');

                if (event.video_url) {
                    videoSource.src = event.video_url;
                    videoSource.parentElement.load();
                    if (videoTitle) videoTitle.textContent = event.video_title || 'Как дойти?';
                    videoSection.style.display = 'block';
                } else {
                    videoSection.style.display = 'none';
                }

                detailContainer.innerHTML = '';
                detailContainer.appendChild(content);

                addBackButton();
                setupEventDetailEventHandlers(eventId);
                detailContainer.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('Ошибка загрузки данных мероприятия');
                hideLoadingIndicator();
            }
        })
        .catch(error => {
            console.error('Error loading event detail:', error);
            alert('Ошибка загрузки данных мероприятия');
            hideLoadingIndicator();
        });
}

function addBackButton() {
    const backButton = document.getElementById('back-to-events');
    if (backButton) {
        backButton.addEventListener('click', function() {
            document.getElementById('event-detail-container').style.display = 'none';
            document.getElementById('events-list-container').style.display = 'block';

            const searchSection = document.querySelector('.search-container-section');
            if (searchSection) searchSection.style.display = 'block';

            const filterContainer = document.querySelector('.container-custom > .filter-header-content')?.parentElement;
            if (filterContainer) filterContainer.style.display = 'block';

            document.getElementById('events-list-container').scrollIntoView({ behavior: 'smooth' });
        });
    }
}

function setupEventDetailEventHandlers(eventId) {
    const registerButton = document.querySelector('.btn-register-detail');
    if (registerButton) {
        registerButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const eventId = this.getAttribute('data-event-id');
            if (eventId && typeof window.openEventRegistrationModal === 'function') {
                window.openEventRegistrationModal(eventId);
            }
        });
    }
    attachShareHandler(eventId);
}

function showLoadingIndicator() {}
function hideLoadingIndicator() {}

// ========== SEARCH FUNCTIONALITY ==========
function initializeSearch() {
    console.log('🔍 Инициализация функции поиска...');
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const searchForm = document.getElementById('eventSearchForm');
    
    if (!searchInput || !searchForm) {
        console.error('❌ Элементы поиска не найдены!');
        return;
    }
    
    console.log('✅ Элементы поиска найдены');
    
    setTimeout(() => {
        if (window.location.hash !== '#gallery') {
            searchInput.focus();
        }
    }, 300);
    
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', function() {
            searchInput.value = '';
            searchForm.submit();
        });
    }
    
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function() {
            if (searchInput.value.length > 2 || searchInput.value.length === 0) {
                searchForm.submit();
            }
        }, 500);
    });
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchForm.submit();
        }
    });
    
    console.log('✅ Функция поиска успешно инициализирована');
}

// ========== HERO NAVIGATION ==========
function initializeHeroNavigation() {
    console.log('🎨 Инициализация навигации Hero...');
    const heroNavLinks = document.querySelectorAll('.hero-nav-link');
    
    heroNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            heroNavLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            const contentType = this.getAttribute('data-content');
            switchContent(contentType);
        });
    });
    
    console.log('✅ Навигация Hero успешно инициализирована');
}

function switchContent(contentType) {
    const eventsContent = document.getElementById('events-content');
    const galleryContent = document.getElementById('gallery-content');
    const searchSection = document.querySelector('.search-container-section');
    const heroTitle = document.getElementById('dynamic-hero-title');
    const heroSubtitle = document.getElementById('dynamic-hero-subtitle');
    
    if (contentType === 'events') {
        if (eventsContent) eventsContent.classList.add('active');
        if (galleryContent) galleryContent.classList.remove('active');
        if (searchSection) searchSection.style.display = 'block';
        if (heroTitle) heroTitle.textContent = 'Мероприятия';
        if (heroSubtitle) {
            heroSubtitle.textContent = 'Присоединяйтесь к нашим событиям и развивайтесь вместе с нами';
            heroSubtitle.style.display = 'block';
        }
        window.history.pushState({content: 'events'}, '', '#events');
    } else if (contentType === 'gallery') {
        if (galleryContent) galleryContent.classList.add('active');
        if (eventsContent) eventsContent.classList.remove('active');
        if (searchSection) searchSection.style.display = 'none';
        if (heroTitle) heroTitle.textContent = 'Фотогалерея';
        if (heroSubtitle) {
            heroSubtitle.textContent = 'Воспоминания о наших мероприятиях в фотографиях';
            heroSubtitle.style.display = 'block';
        }
        window.history.pushState({content: 'gallery'}, '', '#gallery');
        if (galleryContent.innerHTML === '') {
            loadGalleryContent();
        }
    }
}

function loadGalleryContent() {
    fetch('/events/gallery/')
        .then(response => response.text())
        .then(html => {
            const galleryContent = document.getElementById('gallery-content');
            if (galleryContent) {
                galleryContent.innerHTML = html;
                initializeGalleryEvents();
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки контента галереи:', error);
        });
}

function initializeGalleryEvents() {
    const gallerySearchInput = document.querySelector('#gallery-content .search-input-field');
    if (gallerySearchInput) {
        let searchTimeout;
        gallerySearchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length > 2 || this.value.length === 0) {
                    window.location.href = `/events/gallery/?q=${encodeURIComponent(this.value)}`;
                }
            }, 500);
        });
    }
    
    document.querySelectorAll('#gallery-content a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ========== REGISTRATION MODAL ==========
function initializeRegistrationModal() {
    console.log('🎫 Инициализация модального окна регистрации...');
    
    const registrationModal = document.getElementById('registrationModal');
    const guestRegistrationModal = document.getElementById('registrationModalGuest');
    const closeModalBtns = document.querySelectorAll('.modal-close-btn');
    const modalOverlays = document.querySelectorAll('.modal-overlay');
    const registrationFormEvents = document.getElementById('registrationFormEvents');
    
    window.openEventRegistrationModal = function(eventId) {
        const userAuthenticated = document.getElementById('userAuthenticated');
        const isAuthenticated = userAuthenticated ? userAuthenticated.value === 'true' : false;

        if (isAuthenticated) {
            const userType = document.getElementById('userType')?.value || '';
            const allowedTypes = ['regular', 'student', 'company'];

            if (allowedTypes.includes(userType)) {
                if (registrationModal) {
                    const modalEventId = document.getElementById('modalEventId');
                    if (modalEventId) modalEventId.value = eventId;
                    registrationModal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                    console.log('✅ Открыто обычное окно регистрации для события ID:', eventId);
                }
            } else {
                alert('Регистрация на мероприятие доступна только для обычных пользователей, студентов и компаний.');
            }
        } else {
            if (guestRegistrationModal) {
                guestRegistrationModal.classList.add('active');
                document.body.style.overflow = 'hidden';
                console.log('✅ Открыто окно регистрации для гостя');
            }
        }
    };
    
    function closeRegistrationModal() {
        const modals = document.querySelectorAll('.registration-modal.active');
        modals.forEach(modal => {
            modal.classList.remove('active');
        });
        document.body.style.overflow = '';
        console.log('✅ Закрыты все окна регистрации');
    }
    
    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', closeRegistrationModal);
    });
    
    modalOverlays.forEach(overlay => {
        overlay.addEventListener('click', closeRegistrationModal);
    });
    
    document.addEventListener('keydown', function(e) {
        const activeModals = document.querySelectorAll('.registration-modal.active');
        if (e.key === 'Escape' && activeModals.length > 0) {
            closeRegistrationModal();
        }
    });
    
    if (registrationFormEvents) {
        registrationFormEvents.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const eventId = document.getElementById('modalEventId').value;
            const fullName = document.getElementById('modalFullName').value;
            const phone = document.getElementById('modalPhone').value;
            const email = document.getElementById('modalEmail').value;
            const agree = document.getElementById('modalRegistrationAgree').checked;
            
            if (!fullName || !phone || !email) {
                alert('Пожалуйста, заполните все обязательные поля');
                return;
            }
            if (!agree) {
                alert('Пожалуйста, согласитесь с условиями');
                return;
            }
            if (!eventId) {
                alert('Не удалось определить мероприятие для регистрации');
                return;
            }
            
            console.log(`📝 Отправка регистрации для мероприятия ID: ${eventId}`);
            
            fetch(`/events/${eventId}/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    full_name: fullName,
                    phone: phone,
                    email: email,
                    agreement: agree
                })
            })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    showSuccessMessage(data.message, data.registration_number);
                    registrationFormEvents.reset();
                    closeRegistrationModal();
                } else {
                    // يمكن أن يكون الخطأ كائن errors أو نص
                    if (typeof data.error === 'object') {
                        // عرض أول خطأ
                        const firstError = Object.values(data.error)[0];
                        alert(firstError);
                    } else {
                        alert(data.error || 'Произошла ошибка при регистрации');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка подключения к серверу. Пожалуйста, попробуйте позже.');
            });
        });
    }
    
    function showSuccessMessage(message, registrationNumber) {
        const template = document.getElementById('success-message-template');
        const content = template.content.cloneNode(true);
        
        content.querySelector('.success-message').textContent = message;
        
        const overlay = content.querySelector('.success-modal-overlay');
        const closeBtn = content.querySelector('.success-close-btn');
        
        closeBtn.addEventListener('click', function() {
            document.body.removeChild(overlay);
        });
        
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                document.body.removeChild(overlay);
            }
        });
        
        document.body.appendChild(content);
    }
    
    console.log('✅ Модальное окно регистрации успешно инициализировано');
}

// ========== DROPDOWN FILTER ==========
function initializeDropdownFilter() {
    const dropdownBtn = document.querySelector('.filter-dropdown-btn');
    const dropdownContent = document.querySelector('.filter-dropdown-content');
    const filterOptions = document.querySelectorAll('.filter-option');
    const eventSections = document.querySelectorAll('.event-section');
    
    const defaultOption = document.querySelector('.filter-option[data-type="all"]');
    if (defaultOption) {
        defaultOption.classList.add('active');
        defaultOption.querySelector('.filter-checkbox').classList.add('checked');
    }
    
    const allEventsSection = document.getElementById('all-events');
    if (allEventsSection) {
        allEventsSection.classList.add('active');
    }
    
    if (dropdownBtn && dropdownContent) {
        dropdownBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdownContent.classList.toggle('show');
            dropdownBtn.classList.toggle('active');
        });
        
        document.addEventListener('click', function(e) {
            if (!dropdownBtn.contains(e.target) && !dropdownContent.contains(e.target)) {
                dropdownContent.classList.remove('show');
                dropdownBtn.classList.remove('active');
            }
        });
    }
    
    filterOptions.forEach(btn => {
        btn.addEventListener('click', function() {
            const eventType = this.getAttribute('data-type');
            const filterText = this.querySelector('.filter-text').textContent;
            
            filterOptions.forEach(b => {
                b.classList.remove('active');
                b.querySelector('.filter-checkbox').classList.remove('checked');
            });
            this.classList.add('active');
            this.querySelector('.filter-checkbox').classList.add('checked');
            
            if (dropdownBtn) {
                dropdownBtn.querySelector('span').textContent = filterText;
            }
            
            if (dropdownContent) {
                dropdownContent.classList.remove('show');
                dropdownBtn.classList.remove('active');
            }
            
            eventSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === `${eventType}-events`) {
                    section.classList.add('active');
                }
            });
        });
    });
}

// ========== NEWSLETTER ==========
function initializeNewsletter() {
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('#newsletterEmail').value;
            const agree = this.querySelector('#newsletterAgreeCheck').checked;
            
            if (!email) {
                alert('Пожалуйста, введите электронную почту');
                return;
            }
            if (!agree) {
                alert('Пожалуйста, согласитесь с условиями');
                return;
            }
            
            fetch('/events/newsletter/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ email: email, agreement: agree })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNewsletterSuccess();
                } else {
                    if (typeof data.error === 'object') {
                        const firstError = Object.values(data.error)[0];
                        alert(firstError);
                    } else {
                        alert(data.error);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка. Пожалуйста, попробуйте позже.');
            });
        });
    }
}

function showNewsletterSuccess() {
    const newsletterCard = document.querySelector('.newsletter-card');
    if (!newsletterCard) return;

    const imageInput = document.getElementById('newsletterSuccessImage');
    const imageUrl = imageInput ? imageInput.value : '';

    // إنشاء العناصر باستخدام createElement بدلاً من innerHTML
    const successDiv = document.createElement('div');
    successDiv.className = 'newsletter-success';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'success-content';
    
    const title = document.createElement('h3');
    title.className = 'success-title';
    title.textContent = 'Вы подписаны на новости!';
    
    const subtitle = document.createElement('p');
    subtitle.className = 'success-subtitle';
    subtitle.textContent = 'Теперь вы будете в курсе всех новостей Академии';
    
    contentDiv.appendChild(title);
    contentDiv.appendChild(subtitle);
    successDiv.appendChild(contentDiv);

    if (imageUrl) {
        const imageDiv = document.createElement('div');
        imageDiv.className = 'success-image';
        const img = document.createElement('img');
        img.src = imageUrl;
        img.alt = '';
        imageDiv.appendChild(img);
        successDiv.appendChild(imageDiv);
    }

    newsletterCard.innerHTML = '';
    newsletterCard.appendChild(successDiv);
}

// ========== SMOOTH SCROLL ==========
function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ========== CARD CLICK HANDLER ==========
function initializeCardClick() {
    document.addEventListener('click', function(e) {
        const eventCard = e.target.closest('.event-card');
        if (eventCard && !e.target.closest('.event-card-register-btn')) {
            e.preventDefault();
            const eventId = eventCard.getAttribute('data-event-id');
            if (eventId) {
                loadEventDetail(eventId);
            }
        }
    });

    document.addEventListener('click', function(e) {
        const registerBtn = e.target.closest('.event-card-register-btn');
        if (registerBtn) {
            e.stopPropagation();
            if (!registerBtn.classList.contains('registration-ended') && !registerBtn.disabled) {
                e.preventDefault();
                const eventId = registerBtn.getAttribute('data-event-id');
                if (eventId && typeof window.openEventRegistrationModal === 'function') {
                    window.openEventRegistrationModal(eventId);
                }
            }
        }
    });
}

// ========== DOCUMENT READY ==========
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ events.js успешно загружен');
    
    initShareModalListeners();
    initializeDropdownFilter();
    initializeNewsletter();
    initializeSearch();
    initializeHeroNavigation();
    initializeRegistrationModal();
    initializeSmoothScroll();
    initializeCardClick();
    
    highlightSearchResults();
});

window.addEventListener('popstate', function(event) {
    const hash = window.location.hash;
    if (hash === '#gallery') {
        switchContent('gallery');
    } else {
        switchContent('events');
    }
});