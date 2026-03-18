// dashboards/static/dashboards/js/notifications.js

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

function loadNotifications() {
    if (!window.NOTIFICATIONS_URLS || !window.NOTIFICATIONS_URLS.unread) {
        console.error('NOTIFICATIONS_URLS غير معرفة');
        return;
    }

    fetch(window.NOTIFICATIONS_URLS.unread)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const badge = document.getElementById('notificationsBadge');
            if (badge) {
                if (data.unread_count > 0) {
                    badge.textContent = data.unread_count;
                    badge.style.display = 'inline';
                } else {
                    badge.style.display = 'none';
                }
            }

            const list = document.getElementById('notificationsList');
            if (!list) return;
            
            list.innerHTML = '';
            if (data.notifications.length === 0) {
                list.innerHTML = '<div class="notification-item empty">Нет новых уведомлений</div>';
            } else {
                data.notifications.forEach(n => {
                    const item = document.createElement('div');
                    item.className = 'notification-item' + (n.read ? '' : ' unread');
                    item.dataset.id = n.id;
                    
                    let contentHtml = '';
                    if (n.link) {
                        contentHtml = `<a href="${n.link}" class="notification-link">${n.message}</a>`;
                    } else {
                        contentHtml = `<p>${n.message}</p>`;
                    }
                    
                    item.innerHTML = `
                        <div class="notification-content">
                            ${contentHtml}
                            <small>${n.created_at}</small>
                        </div>
                        <button class="mark-read" data-id="${n.id}">✓ Прочитано</button>
                    `;
                    list.appendChild(item);
                });

                document.querySelectorAll('.mark-read').forEach(btn => {
                    btn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        const id = this.dataset.id;
                        if (!window.NOTIFICATIONS_URLS.mark_read) return;
                        const url = window.NOTIFICATIONS_URLS.mark_read.replace('0', id);
                        fetch(url, {
                            method: 'POST',
                            headers: {'X-CSRFToken': getCookie('csrftoken')}
                        }).then(response => {
                            if (response.ok) loadNotifications();
                        }).catch(err => console.error('خطأ في تعيين كمقروء:', err));
                    });
                });
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки уведомлений:', error);
            const list = document.getElementById('notificationsList');
            if (list) {
                list.innerHTML = '<div class="notification-item error">فشل تحميل الإشعارات. حاول مرة أخرى.</div>';
            }
        });
}

document.addEventListener('DOMContentLoaded', function() {
    loadNotifications();
    setInterval(loadNotifications, 30000);

    const toggle = document.getElementById('notificationsToggle');
    const menu = document.getElementById('notificationsMenu');

    if (toggle && menu) {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            menu.classList.toggle('show');
            if (menu.classList.contains('show')) {
                loadNotifications();
            }
        });

        document.addEventListener('click', function(e) {
            if (!menu.contains(e.target) && !toggle.contains(e.target)) {
                menu.classList.remove('show');
            }
        });
    }

    const markAllBtn = document.getElementById('markAllRead');
    if (markAllBtn && window.NOTIFICATIONS_URLS && window.NOTIFICATIONS_URLS.mark_all_read) {
        markAllBtn.addEventListener('click', function() {
            fetch(window.NOTIFICATIONS_URLS.mark_all_read, {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')}
            }).then(response => {
                if (response.ok) {
                    loadNotifications();
                    if (menu) menu.classList.remove('show');
                }
            }).catch(err => console.error('خطأ في تعيين الكل مقروء:', err));
        });
    }
});