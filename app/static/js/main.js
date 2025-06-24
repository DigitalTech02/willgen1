// Main JavaScript for WillGen

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Loading button states
    const loadingButtons = document.querySelectorAll('.btn[data-loading-text]');
    loadingButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            const loadingText = this.getAttribute('data-loading-text');
            
            this.innerHTML = loadingText;
            this.classList.add('loading');
            this.disabled = true;
            
            // Reset after 3 seconds (adjust as needed)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.classList.remove('loading');
                this.disabled = false;
            }, 3000);
        });
    });
});

// Utility functions
const WillGen = {
    // Show loading state on button
    showLoading: function(button, text = 'Loading...') {
        const originalText = button.innerHTML;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = text;
        button.classList.add('loading');
        button.disabled = true;
    },

    // Hide loading state on button
    hideLoading: function(button) {
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
            button.removeAttribute('data-original-text');
        }
        button.classList.remove('loading');
        button.disabled = false;
    },

    // Show toast notification
    showToast: function(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer();
        
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert" id="${toastId}">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    },

    // Create toast container if it doesn't exist
    createToastContainer: function() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
        return container;
    },

    // Confirm dialog
    confirm: function(message, callback) {
        if (window.confirm(message)) {
            callback();
        }
    },

    // Format date
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Validate email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    // Debounce function
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },

    // Auto-save functionality
    autoSave: function(formId, saveUrl, interval = 30000) {
        const form = document.getElementById(formId);
        if (!form) return;

        const saveData = this.debounce(function() {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            fetch(saveUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    WillGen.showToast('Draft saved automatically', 'success');
                }
            })
            .catch(error => {
                console.error('Auto-save error:', error);
            });
        }, 2000);

        // Save on form changes
        form.addEventListener('input', saveData);
        form.addEventListener('change', saveData);

        // Periodic save
        setInterval(saveData, interval);
    }
};

// Make WillGen available globally
window.WillGen = WillGen;
