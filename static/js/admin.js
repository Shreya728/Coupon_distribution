document.addEventListener('DOMContentLoaded', function() {
    // Flash message auto-hide
    const flashMessages = document.querySelectorAll('.flash-message');
    
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 500);
            });
        }, 3000);
    }
    
    // Confirm coupon deactivation
    const deactivateButtons = document.querySelectorAll('.btn-danger');
    
    deactivateButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to deactivate this coupon?')) {
                e.preventDefault();
            }
        });
    });
    
    // Add form validation
    const addCouponForm = document.querySelector('.add-coupon-form');
    
    if (addCouponForm) {
        addCouponForm.addEventListener('submit', function(e) {
            const codeInput = document.getElementById('code');
            const code = codeInput.value.trim();
            
            if (code === '') {
                e.preventDefault();
                alert('Please enter a coupon code');
                codeInput.focus();
            }
        });
    }
});
