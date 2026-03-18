// album_lightbox.js
document.addEventListener('DOMContentLoaded', function() {
    // إنشاء Lightbox element بالتصميم الجديد
    const lightbox = document.createElement('div');
    lightbox.id = 'lightbox';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <button class="lightbox-close" aria-label="Close">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
            <div class="lightbox-image-container">
                <img class="lightbox-image" src="" alt="">
            </div>
            <div class="lightbox-caption"></div>
            <div class="lightbox-navigation">
                <button class="lightbox-prev" aria-label="Previous">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
                <button class="lightbox-next" aria-label="Next">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
            </div>
        </div>
    `;
    document.body.appendChild(lightbox);

    const images = document.querySelectorAll('.album-image');
    const lightboxEl = document.getElementById('lightbox');
    const lightboxImg = lightboxEl.querySelector('.lightbox-image');
    const lightboxCaption = lightboxEl.querySelector('.lightbox-caption');
    const closeBtn = lightboxEl.querySelector('.lightbox-close');
    const prevBtn = lightboxEl.querySelector('.lightbox-prev');
    const nextBtn = lightboxEl.querySelector('.lightbox-next');
    
    let currentImageIndex = 0;
    let isLoading = false;

    // وظيفة لتحميل الصورة مع التأكد من أنها ليست ضخمة
    function loadImage(imageSrc, callback) {
        if (isLoading) return;
        
        isLoading = true;
        lightboxImg.classList.add('loading');
        
        const img = new Image();
        img.onload = function() {
            lightboxImg.src = imageSrc;
            lightboxImg.classList.remove('loading');
            isLoading = false;
            
            if (callback) callback();
        };
        
        img.onerror = function() {
            console.error('فشل تحميل الصورة:', imageSrc);
            lightboxImg.classList.remove('loading');
            isLoading = false;
        };
        
        img.src = imageSrc;
    }

    // فتح Lightbox عند النقر على صورة
    images.forEach((image, index) => {
        image.style.cursor = 'pointer';
        image.addEventListener('click', () => {
            currentImageIndex = index;
            openLightbox();
            updateLightbox();
        });
    });

    // أيضاً فتح Lightbox عند النقر على أيقونة التكبير
    const zoomIcons = document.querySelectorAll('.image-zoom-icon');
    zoomIcons.forEach((icon, index) => {
        icon.addEventListener('click', (e) => {
            e.stopPropagation();
            currentImageIndex = index;
            openLightbox();
            updateLightbox();
        });
    });

    // وظيفة فتح Lightbox
    function openLightbox() {
        lightboxEl.classList.add('active');
        document.body.style.overflow = 'hidden';
        document.documentElement.style.overflow = 'hidden';
    }

    // وظيفة إغلاق Lightbox
    function closeLightbox() {
        lightboxEl.classList.remove('active');
        document.body.style.overflow = 'auto';
        document.documentElement.style.overflow = 'auto';
        lightboxImg.src = '';
        lightboxCaption.innerHTML = '';
    }

    // تحديث Lightbox بالصورة الحالية
    function updateLightbox() {
        const currentImage = images[currentImageIndex];
        const imageContainer = currentImage.closest('.album-image-item');
        const caption = imageContainer ? imageContainer.querySelector('.album-image-caption') : null;
        const description = imageContainer ? imageContainer.querySelector('.album-image-description') : null;
        
        // تعيين النص البدائي
        lightboxImg.alt = currentImage.alt;
        
        let captionText = '';
        if (caption) {
            captionText += caption.textContent;
        }
        if (description) {
            captionText += captionText ? '<br>' : '';
            captionText += description.textContent;
        }
        
        lightboxCaption.innerHTML = captionText || currentImage.alt;
        
        // تحميل الصورة
        loadImage(currentImage.src, () => {
            // تحديث حالة أزرار التنقل بعد تحميل الصورة
            prevBtn.style.opacity = currentImageIndex === 0 ? '0.3' : '1';
            prevBtn.style.pointerEvents = currentImageIndex === 0 ? 'none' : 'auto';
            nextBtn.style.opacity = currentImageIndex === images.length - 1 ? '0.3' : '1';
            nextBtn.style.pointerEvents = currentImageIndex === images.length - 1 ? 'none' : 'auto';
        });
    }

    // التنقل إلى الصورة السابقة
    function prevImage() {
        if (currentImageIndex > 0 && !isLoading) {
            currentImageIndex--;
            updateLightbox();
        }
    }

    // التنقل إلى الصورة التالية
    function nextImage() {
        if (currentImageIndex < images.length - 1 && !isLoading) {
            currentImageIndex++;
            updateLightbox();
        }
    }

    // إضافة event listeners
    closeBtn.addEventListener('click', closeLightbox);
    prevBtn.addEventListener('click', prevImage);
    nextBtn.addEventListener('click', nextImage);

    // إغلاق Lightbox عند النقر خارج الصورة (على الخلفية)
    lightboxEl.addEventListener('click', (e) => {
        if (e.target === lightboxEl && !isLoading) {
            closeLightbox();
        }
    });

    // التنقل باستخدام مفاتيح لوحة المفاتيح
    document.addEventListener('keydown', (e) => {
        if (lightboxEl.classList.contains('active') && !isLoading) {
            switch(e.key) {
                case 'Escape':
                    closeLightbox();
                    break;
                case 'ArrowLeft':
                    prevImage();
                    break;
                case 'ArrowRight':
                    nextImage();
                    break;
            }
        }
    });

    // منع النقر على الروابط داخل الصور
    document.querySelectorAll('.album-image-container a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });
});