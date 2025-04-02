// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.classList.add('fade');
            setTimeout(function() {
                message.remove();
            }, 150);
        }, 5000);
    });
});

// Password confirmation validation
const registerForm = document.querySelector('form[action*="register"]');
if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        
        if (password !== confirmPassword) {
            e.preventDefault();
            alert('Passwords do not match!');
        }
    });
}

// Image preview for recipe form
const imageUrlInput = document.getElementById('image_url');
if (imageUrlInput) {
    imageUrlInput.addEventListener('input', function() {
        const preview = document.createElement('img');
        preview.src = this.value;
        preview.style.maxWidth = '200px';
        preview.style.marginTop = '10px';
        
        const previewContainer = this.parentElement.querySelector('.image-preview');
        if (previewContainer) {
            previewContainer.innerHTML = '';
        } else {
            const container = document.createElement('div');
            container.className = 'image-preview';
            this.parentElement.appendChild(container);
        }
        
        if (this.value) {
            previewContainer.appendChild(preview);
        }
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}); 