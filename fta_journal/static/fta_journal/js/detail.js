// detail.js - نسخة متوافقة مع HTMX
class PDFViewerClass {
    constructor() {
        this.modal = null;
        this.pagesContainer = null;
        this.loader = null;
        this.pageInfo = null;
        this.zoomLevelSpan = null;
        this.readButton = null;
        this.closeBtn = null;
        this.prevBtn = null;
        this.nextBtn = null;
        this.zoomInBtn = null;
        this.zoomOutBtn = null;
        this.fullscreenBtn = null;
        this.downloadBtn = null;
        this.printBtn = null;

        this.pdfDoc = null;
        this.currentPageNumber = 1;
        this.totalPages = 0;
        this.currentZoom = 1.0;
        this.zoomStep = 0.25;
        this.isLoading = false;
        this.currentRenderTask = null;
        this.pageCache = new Map();
        this.pdfUrl = null;
    }

    init() {
        // إعادة ربط العناصر بعد أي تحديث للـ DOM
        this.modal = document.getElementById('pdfViewerModal');
        this.pagesContainer = document.getElementById('pdfPagesContainer');
        this.loader = document.getElementById('pdfLoader');
        this.pageInfo = document.getElementById('pageInfo');
        this.zoomLevelSpan = document.getElementById('zoomLevel');
        this.readButton = document.querySelector('.btn-action.btn-read');
        this.closeBtn = document.getElementById('closePdfViewer');
        this.prevBtn = document.getElementById('prevPage');
        this.nextBtn = document.getElementById('nextPage');
        this.zoomInBtn = document.getElementById('zoomIn');
        this.zoomOutBtn = document.getElementById('zoomOut');
        this.fullscreenBtn = document.getElementById('fullscreenBtn');
        this.downloadBtn = document.getElementById('downloadPdf');
        this.printBtn = document.getElementById('printPdf');

        if (!this.readButton) return;

        // إزالة المستمعين السابقين لمنع التكرار (باستخدام cloneNode)
        const newReadButton = this.readButton.cloneNode(true);
        this.readButton.parentNode.replaceChild(newReadButton, this.readButton);
        this.readButton = newReadButton;

        this.readButton.addEventListener('click', this.handleReadClick.bind(this));

        if (this.closeBtn) this.closeBtn.addEventListener('click', this.close.bind(this));
        if (this.prevBtn) this.prevBtn.addEventListener('click', this.goToPrevPage.bind(this));
        if (this.nextBtn) this.nextBtn.addEventListener('click', this.goToNextPage.bind(this));
        if (this.zoomInBtn) this.zoomInBtn.addEventListener('click', this.zoomIn.bind(this));
        if (this.zoomOutBtn) this.zoomOutBtn.addEventListener('click', this.zoomOut.bind(this));
        if (this.fullscreenBtn) this.fullscreenBtn.addEventListener('click', this.toggleFullscreen.bind(this));
        if (this.downloadBtn) this.downloadBtn.addEventListener('click', this.download.bind(this));
        if (this.printBtn) this.printBtn.addEventListener('click', this.print.bind(this));

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal && this.modal.style.display === 'block') {
                this.close();
            }
        });

        if (this.modal) {
            this.modal.querySelector('.pdf-modal-container')?.addEventListener('click', (e) => e.stopPropagation());
        }

        if (this.pagesContainer) {
            this.pagesContainer.addEventListener('scroll', this.onScroll.bind(this));
        }
    }

    handleReadClick(e) {
        e.preventDefault();
        const pdfUrl = this.readButton.getAttribute('href');
        if (!pdfUrl || pdfUrl === '#') {
            alert('PDF файл не загружен');
            return;
        }
        this.pdfUrl = pdfUrl;
        this.open(pdfUrl);
    }

    async open(url) {
        this.showLoader('Загрузка документа...');
        this.modal.style.display = 'block';
        this.pagesContainer.innerHTML = '';
        this.pageCache.clear();

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Ошибка загрузки (${response.status})`);
            const blob = await response.blob();
            if (blob.size === 0) throw new Error('Файл пуст (0 байт)');

            const blobUrl = URL.createObjectURL(blob);
            const loadingTask = pdfjsLib.getDocument(blobUrl);

            this.pdfDoc = await loadingTask.promise;
            this.totalPages = this.pdfDoc.numPages;
            this.currentPageNumber = 1;
            this.currentZoom = 1.0;
            this.zoomLevelSpan.textContent = '100%';

            await this.renderPage(1);

            this.hideLoader();
            this.updatePageInfo();
            this.enableControls();
        } catch (error) {
            this.hideLoader();
            this.showError('Ошибка загрузки PDF: ' + error.message);
            console.error(error);
        }
    }

    async renderPage(pageNumber, zoom = this.currentZoom) {
        if (!this.pdfDoc) return;

        if (this.currentRenderTask) {
            this.currentRenderTask.cancel();
            this.currentRenderTask = null;
        }

        const cached = this.pageCache.get(pageNumber);
        if (cached && cached.zoom === zoom) {
            this.setCanvasToContainer(cached.canvas);
            return;
        }

        this.isLoading = true;
        this.disableControls();

        try {
            const page = await this.pdfDoc.getPage(pageNumber);
            const viewport = page.getViewport({ scale: zoom });

            const canvas = document.createElement('canvas');
            canvas.className = 'pdf-page-canvas';
            canvas.width = viewport.width;
            canvas.height = viewport.height;

            const context = canvas.getContext('2d');
            const renderTask = page.render({
                canvasContext: context,
                viewport: viewport
            });

            this.currentRenderTask = renderTask;

            await renderTask.promise;

            this.pageCache.clear();
            this.pageCache.set(pageNumber, { canvas, zoom });

            this.setCanvasToContainer(canvas);

            this.isLoading = false;
            this.currentRenderTask = null;
            this.enableControls();
        } catch (error) {
            if (error.name !== 'RenderingCancelledException') {
                this.showError(`Ошибка рендеринга страницы ${pageNumber}`);
                console.error(error);
            }
            this.isLoading = false;
            this.currentRenderTask = null;
            this.enableControls();
        }
    }

    setCanvasToContainer(canvas) {
        this.pagesContainer.innerHTML = '';
        this.pagesContainer.appendChild(canvas);
    }

    goToPrevPage() {
        if (this.currentPageNumber > 1 && !this.isLoading) {
            this.currentPageNumber--;
            this.renderPage(this.currentPageNumber);
            this.updatePageInfo();
        }
    }

    goToNextPage() {
        if (this.currentPageNumber < this.totalPages && !this.isLoading) {
            this.currentPageNumber++;
            this.renderPage(this.currentPageNumber);
            this.updatePageInfo();
        }
    }

    zoomIn() {
        if (this.currentZoom < 3.0 && !this.isLoading) {
            this.currentZoom += this.zoomStep;
            this.zoomLevelSpan.textContent = Math.round(this.currentZoom * 100) + '%';
            this.renderPage(this.currentPageNumber, this.currentZoom);
        }
    }

    zoomOut() {
        if (this.currentZoom > 0.5 && !this.isLoading) {
            this.currentZoom -= this.zoomStep;
            this.zoomLevelSpan.textContent = Math.round(this.currentZoom * 100) + '%';
            this.renderPage(this.currentPageNumber, this.currentZoom);
        }
    }

    updatePageInfo() {
        if (this.totalPages) {
            this.pageInfo.textContent = `${this.currentPageNumber} / ${this.totalPages}`;
        }
    }

    onScroll() {
        // ليس ضرورياً
    }

    toggleFullscreen() {
        const container = this.modal.querySelector('.pdf-modal-container');
        if (!document.fullscreenElement) {
            container.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    download() {
        if (this.pdfUrl) {
            const a = document.createElement('a');
            a.href = this.pdfUrl;
            a.download = '';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }

    print() {
        if (this.pdfUrl) {
            window.open(this.pdfUrl, '_blank');
        }
    }

    close() {
        this.modal.style.display = 'none';
        if (this.pdfDoc) {
            if (this.pdfDoc.destroy) this.pdfDoc.destroy();
            this.pdfDoc = null;
        }
        if (this.currentRenderTask) {
            this.currentRenderTask.cancel();
            this.currentRenderTask = null;
        }
        this.pageCache.clear();
        this.pagesContainer.innerHTML = '';
        this.pdfUrl = null;
        this.totalPages = 0;
        this.currentPageNumber = 1;
        this.currentZoom = 1.0;
        this.zoomLevelSpan.textContent = '100%';
        this.pageInfo.textContent = '1 / 1';
        this.hideLoader();
        this.enableControls();
    }

    showLoader(message) {
        this.loader.style.display = 'block';
        this.loader.textContent = message;
    }

    hideLoader() {
        this.loader.style.display = 'none';
    }

    showError(message) {
        this.pagesContainer.innerHTML = `<div class="pdf-error">${message}</div>`;
    }

    disableControls() {
        [this.prevBtn, this.nextBtn, this.zoomInBtn, this.zoomOutBtn, this.fullscreenBtn, this.downloadBtn, this.printBtn].forEach(btn => {
            if (btn) btn.disabled = true;
        });
    }

    enableControls() {
        [this.prevBtn, this.nextBtn, this.zoomInBtn, this.zoomOutBtn, this.fullscreenBtn, this.downloadBtn, this.printBtn].forEach(btn => {
            if (btn) btn.disabled = false;
        });
        if (this.currentPageNumber === 1) this.prevBtn.disabled = true;
        if (this.currentPageNumber === this.totalPages) this.nextBtn.disabled = true;
    }
}

// إنشاء كائن عام وإعادة تهيئته عند الحاجة
let pdfViewerInstance = null;

function initPdfViewer() {
    if (!pdfViewerInstance) {
        pdfViewerInstance = new PDFViewerClass();
    }
    pdfViewerInstance.init();
}

// تهيئة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', initPdfViewer);

// إعادة تهيئة بعد تحديث HTMX
document.addEventListener('htmx:afterSwap', function(evt) {
    if (evt.detail.target && evt.detail.target.id === 'journal-content') {
        initPdfViewer();
    }
});