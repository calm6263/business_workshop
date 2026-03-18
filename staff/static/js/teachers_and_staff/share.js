// static/js/teachers_and_staff/share.js
// ======================================

/**
 * فتح نافذة المشاركة المنبثقة
 * @param {string} url - الرابط المراد مشاركته (افتراضي: الرابط الحالي)
 * @param {string} title - عنوان الصفحة (اختياري)
 */
export function openSharePopup(url = window.location.href, title = document.title) {
    // إزالة أي نافذة مشاركة مفتوحة سابقاً
    const existingPopup = document.querySelector('.share-popup');
    if (existingPopup) existingPopup.remove();

    // إنشاء عناصر النافذة
    const popup = document.createElement('div');
    popup.className = 'share-popup';
    popup.setAttribute('role', 'dialog');
    popup.setAttribute('aria-label', 'Поделиться');

    const popupContent = document.createElement('div');
    popupContent.className = 'share-popup-content';

    // عنوان النافذة
    const header = document.createElement('div');
    header.className = 'share-popup-header';
    header.innerHTML = '<h3>Поделиться</h3><button class="share-popup-close" aria-label="Закрыть">&times;</button>';
    popupContent.appendChild(header);

    // قائمة خيارات المشاركة
    const options = document.createElement('div');
    options.className = 'share-options';

    // إضافة خيارات وسائل التواصل
    const shareItems = [
        { name: 'Facebook', icon: 'facebook', url: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}` },
        { name: 'Twitter', icon: 'twitter', url: `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}` },
        { name: 'Telegram', icon: 'telegram', url: `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}` },
        { name: 'WhatsApp', icon: 'whatsapp', url: `https://api.whatsapp.com/send?text=${encodeURIComponent(title + ' ' + url)}` },
        { name: 'Копировать ссылку', icon: 'copy', action: 'copy' }
    ];

    shareItems.forEach(item => {
        const btn = document.createElement('button');
        btn.className = 'share-option';
        btn.setAttribute('data-share', item.name);

        // أيقونة باستخدام رموز تعبيرية (يمكن استبدالها بـ SVG لاحقاً)
        const iconSpan = document.createElement('span');
        iconSpan.className = `share-icon share-icon-${item.icon}`;
        switch (item.icon) {
            case 'facebook': iconSpan.textContent = '📘'; break;
            case 'twitter': iconSpan.textContent = '🐦'; break;
            case 'telegram': iconSpan.textContent = '📲'; break;
            case 'whatsapp': iconSpan.textContent = '💬'; break;
            case 'copy': iconSpan.textContent = '📋'; break;
            default: iconSpan.textContent = '🔗';
        }
        btn.appendChild(iconSpan);

        const textSpan = document.createElement('span');
        textSpan.textContent = item.name;
        btn.appendChild(textSpan);

        if (item.url) {
            btn.addEventListener('click', () => {
                window.open(item.url, '_blank', 'width=600,height=400');
                popup.remove();
            });
        } else if (item.action === 'copy') {
            btn.addEventListener('click', () => {
                navigator.clipboard.writeText(url).then(() => {
                    // إظهار رسالة نجاح قصيرة
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '<span>✓ Скопировано!</span>';
                    setTimeout(() => {
                        btn.innerHTML = originalText;
                        popup.remove();
                    }, 1500);
                }).catch(() => {
                    alert('Не удалось скопировать ссылку');
                });
            });
        }

        options.appendChild(btn);
    });

    popupContent.appendChild(options);
    popup.appendChild(popupContent);
    document.body.appendChild(popup);

    // إغلاق النافذة عند النقر على الزر X أو خارجها
    const closeBtn = popup.querySelector('.share-popup-close');
    closeBtn.addEventListener('click', () => popup.remove());

    popup.addEventListener('click', (e) => {
        if (e.target === popup) popup.remove();
    });

    // منع التمرير خلف النافذة
    document.body.style.overflow = 'hidden';
    
    // استعادة التمرير عند الإغلاق
    const observer = new MutationObserver(() => {
        if (!document.body.contains(popup)) {
            document.body.style.overflow = '';
            observer.disconnect();
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
}