// research/static/research/js/research_conference_list.js
import { setupConferenceCards, loadConferenceDetail, showConferencesList } from './conferenceDetail.js';

(function() {
    // ---------- Helper: get CSRF token ----------
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

    // ---------- التسجيل ----------
    const modal = document.getElementById('conferenceRegistrationModalList');
    const guestModal = document.getElementById('conferenceRegistrationModalGuestList');
    const closeBtns = document.querySelectorAll('.modal-close-btn');
    const overlays = document.querySelectorAll('.modal-overlay');
    const userAuth = document.getElementById('userAuthenticated')?.value === 'true';

    // دالة فتح مودال التسجيل (تُستخدم من الأزرار)
    window.openConferenceRegistrationModalList = function(conferenceId) {
        if (userAuth) {
            if (modal) {
                document.getElementById('modalConferenceIdList').value = conferenceId;
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        } else {
            if (guestModal) {
                guestModal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }
    };

    function closeAllModals() {
        [modal, guestModal].forEach(m => {
            if (m) m.classList.remove('active');
        });
        document.body.style.overflow = '';
    }

    closeBtns.forEach(btn => btn.addEventListener('click', closeAllModals));
    overlays.forEach(overlay => overlay.addEventListener('click', closeAllModals));
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && (modal?.classList.contains('active') || guestModal?.classList.contains('active'))) {
            closeAllModals();
        }
    });

    // أزرار التسجيل في البطاقات
    const registerBtns = document.querySelectorAll('.register-conference-btn');
    registerBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // منع تفعيل النقر على البطاقة
            const conferenceId = this.getAttribute('data-conference-id');
            window.openConferenceRegistrationModalList(conferenceId);
        });
    });

    // إعداد بطاقات المؤتمرات للتحميل الديناميكي
    setupConferenceCards();

    // إرسال النموذج
    const form = document.getElementById('conferenceRegistrationFormList');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const conferenceId = document.getElementById('modalConferenceIdList').value;
            const fullName = document.getElementById('modalFullNameList').value;
            const phone = document.getElementById('modalPhoneList').value;
            const email = document.getElementById('modalEmailList').value;
            const agree = document.getElementById('modalRegistrationAgreeList').checked;

            if (!fullName || !phone || !email) {
                alert('Пожалуйста, заполните все поля');
                return;
            }
            if (!agree) {
                alert('Пожалуйста, согласитесь с условиями');
                return;
            }

            fetch(`/research/conferences/${conferenceId}/register/`, {
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
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showSuccessMessage(data.message);
                    form.reset();
                    closeAllModals();
                } else {
                    alert(data.error);
                }
            })
            .catch(err => {
                console.error(err);
                alert('Ошибка соединения с сервером');
            });
        });
    }

    function showSuccessMessage(message) {
        const template = document.getElementById('success-message-template-list');
        const content = template.content.cloneNode(true);
        content.querySelector('.success-message').textContent = message;
        const overlay = content.querySelector('.success-modal-overlay');
        const closeBtn = content.querySelector('.success-close-btn');
        closeBtn.addEventListener('click', () => overlay.remove());
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
        document.body.appendChild(content);
    }

    // التحقق من وجود معامل conference في URL عند التحميل
    const urlParams = new URLSearchParams(window.location.search);
    const conferenceId = urlParams.get('conference');
    if (conferenceId && urlParams.get('tab') === 'conferences') {
        loadConferenceDetail(conferenceId);
    }
})();