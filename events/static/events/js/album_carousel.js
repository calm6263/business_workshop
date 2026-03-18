 
// events/static/events/js/album_carousel.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize carousel only if elements exist on page
    const carouselTrack = document.getElementById('carouselTrack');
    if (!carouselTrack) {
        console.log('Carousel track not found');
        return;
    }
    
    console.log('Initializing carousel...');
    
    const slides = Array.from(carouselTrack.querySelectorAll('.carousel-slide'));
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const thumbnails = document.querySelectorAll('.thumbnail');
    const indicators = document.querySelectorAll('.carousel-indicator');
    const carouselCounter = document.getElementById('carouselCounter');
    
    console.log('Found elements:', {
        slides: slides.length,
        prevButton: !!prevButton,
        nextButton: !!nextButton,
        thumbnails: thumbnails.length,
        indicators: indicators.length,
        counter: !!carouselCounter
    });
    
    let currentIndex = 0;
    const totalSlides = slides.length;
    
    // Update carousel counter
    function updateCounter() {
        if (carouselCounter) {
            carouselCounter.textContent = `${currentIndex + 1} / ${totalSlides}`;
        }
    }
    
    // Initialize carousel
    function updateCarousel() {
        // Move track
        carouselTrack.style.transform = `translateX(-${currentIndex * 100}%)`;
        
        // Update active states
        slides.forEach((slide, index) => {
            slide.classList.toggle('active', index === currentIndex);
        });
        
        // Update thumbnails
        if (thumbnails && thumbnails.length) {
            thumbnails.forEach((thumb, index) => {
                thumb.classList.toggle('active', index === currentIndex);
            });
        }
        
        // Update indicators
        if (indicators && indicators.length) {
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentIndex);
            });
        }
        
        // Update counter
        updateCounter();
        
        console.log('Carousel updated to slide:', currentIndex + 1);
    }
    
    // Navigation functions
    function goToSlide(index) {
        currentIndex = index;
        if (currentIndex < 0) currentIndex = totalSlides - 1;
        if (currentIndex >= totalSlides) currentIndex = 0;
        updateCarousel();
    }
    
    function nextSlide() {
        goToSlide(currentIndex + 1);
    }
    
    function prevSlide() {
        goToSlide(currentIndex - 1);
    }
    
    // Event listeners for buttons
    if (prevButton) {
        prevButton.addEventListener('click', function(e) {
            console.log('Previous button clicked');
            e.preventDefault();
            e.stopPropagation();
            prevSlide();
        });
    } else {
        console.error('Previous button not found!');
    }
    
    if (nextButton) {
        nextButton.addEventListener('click', function(e) {
            console.log('Next button clicked');
            e.preventDefault();
            e.stopPropagation();
            nextSlide();
        });
    } else {
        console.error('Next button not found!');
    }
    
    // Thumbnail clicks
    if (thumbnails && thumbnails.length) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', () => {
                const index = parseInt(thumb.getAttribute('data-index'));
                console.log('Thumbnail clicked, index:', index);
                goToSlide(index);
            });
        });
    }
    
    // Indicator clicks
    if (indicators && indicators.length) {
        indicators.forEach(indicator => {
            indicator.addEventListener('click', () => {
                const index = parseInt(indicator.getAttribute('data-index'));
                console.log('Indicator clicked, index:', index);
                goToSlide(index);
            });
        });
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') prevSlide();
        if (e.key === 'ArrowRight') nextSlide();
        if (e.key === 'Home') goToSlide(0);
        if (e.key === 'End') goToSlide(totalSlides - 1);
    });
    
    // Touch/swipe support
    let startX = 0;
    let endX = 0;
    let isDragging = false;
    
    if (carouselTrack) {
        carouselTrack.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isDragging = true;
        });
        
        carouselTrack.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            endX = e.touches[0].clientX;
        });
        
        carouselTrack.addEventListener('touchend', () => {
            if (!isDragging) return;
            
            const diffX = startX - endX;
            const threshold = 50;
            
            if (Math.abs(diffX) > threshold) {
                if (diffX > 0) {
                    nextSlide(); // Swipe left
                } else {
                    prevSlide(); // Swipe right
                }
            }
            
            isDragging = false;
        });
        
        // Mouse drag support
        carouselTrack.addEventListener('mousedown', (e) => {
            startX = e.clientX;
            isDragging = true;
        });
        
        carouselTrack.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            endX = e.clientX;
        });
        
        carouselTrack.addEventListener('mouseup', () => {
            if (!isDragging) return;
            
            const diffX = startX - endX;
            const threshold = 100;
            
            if (Math.abs(diffX) > threshold) {
                if (diffX > 0) {
                    nextSlide(); // Drag left
                } else {
                    prevSlide(); // Drag right
                }
            }
            
            isDragging = false;
        });
        
        carouselTrack.addEventListener('mouseleave', () => {
            isDragging = false;
        });
    }
    
    // Initialize
    updateCarousel();
    updateCounter();
    
    console.log('✅ Album carousel initialized successfully');
});
 