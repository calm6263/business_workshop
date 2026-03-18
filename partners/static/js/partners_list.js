// Accordion functionality (إذا كان موجوداً في الصفحة)
function toggleAccordion(element) {
    const content = element.nextElementSibling;
    const isActive = element.classList.contains('active');
    
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.classList.remove('active');
    });
    document.querySelectorAll('.accordion-content').forEach(content => {
        content.classList.remove('active');
    });
    
    if (!isActive) {
        element.classList.add('active');
        content.classList.add('active');
    }
}

// Modal functions
function openApplicationModal() {
    document.getElementById('partnershipModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeApplicationModal() {
    document.getElementById('partnershipModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    resetApplicationForm();
}

function resetApplicationForm() {
    const form = document.querySelector('.application-form-compact');
    if (form) {
        form.reset();
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('partnershipModal');
    if (event.target === modal) {
        closeApplicationModal();
    }
}

// Auto-close alerts after 8 seconds (for error messages, and hiding success messages after modal appears)
document.addEventListener('DOMContentLoaded', function() {
    // Auto-close any alert (like error) after 8 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-success)'); // exclude success because we'll handle separately
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 8000);

    // Show success modal if a success message exists and contains a request number
    const successAlert = document.querySelector('.alert-success');
    if (successAlert) {
        const requestNumberSpan = successAlert.querySelector('.request-number');
        if (requestNumberSpan) {
            const requestNumber = requestNumberSpan.textContent.trim();
            const displaySpan = document.getElementById('requestNumberDisplay');
            if (displaySpan) {
                displaySpan.textContent = requestNumber;
                
                // Initialize and show Bootstrap modal
                const successModal = new bootstrap.Modal(document.getElementById('successModal'));
                successModal.show();
                
                // Hide the original alert (optional, but good)
                successAlert.style.display = 'none';
            }
        }
    }
});