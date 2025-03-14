document.addEventListener('DOMContentLoaded', function() {
    const claimButton = document.getElementById('claim-coupon');
    const couponResult = document.getElementById('coupon-result');
    const claimContainer = document.getElementById('claim-container');
    const couponCode = document.getElementById('coupon-code');
    const copyButton = document.getElementById('copy-coupon');
    const errorMessage = document.getElementById('error-message');
    
    // Claim coupon button click handler
    claimButton.addEventListener('click', function() {
        // Disable button to prevent multiple clicks
        claimButton.disabled = true;
        claimButton.textContent = 'Processing...';
        
        // Make API request to claim a coupon
        fetch('/claim_coupon', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show the coupon code
                couponCode.textContent = data.coupon_code;
                couponResult.classList.remove('hidden');
                claimContainer.classList.add('hidden');
                errorMessage.classList.add('hidden');
            } else {
                // Show error message
                errorMessage.textContent = data.message;
                errorMessage.classList.remove('hidden');
                // Re-enable the button
                claimButton.disabled = false;
                claimButton.textContent = 'Claim Your Coupon';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = 'An error occurred. Please try again later.';
            errorMessage.classList.remove('hidden');
            // Re-enable the button
            claimButton.disabled = false;
            claimButton.textContent = 'Claim Your Coupon';
        });
    });
    
    // Copy coupon code button
    copyButton.addEventListener('click', function() {
        const code = couponCode.textContent;
        
        // Use the Clipboard API if available
        if (navigator.clipboard) {
            navigator.clipboard.writeText(code)
                .then(() => {
                    copyButton.textContent = 'Copied!';
                    setTimeout(() => {
                        copyButton.textContent = 'Copy Code';
                    }, 2000);
                })
                .catch(err => {
                    console.error('Could not copy text: ', err);
                    fallbackCopyTextToClipboard(code);
                });
        } else {
            fallbackCopyTextToClipboard(code);
        }
    });
    
    // Fallback copy method for older browsers
    function fallbackCopyTextToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        
        // Make the textarea out of viewport
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            if (successful) {
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy Code';
                }, 2000);
            } else {
                copyButton.textContent = 'Failed to copy';
            }
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
            copyButton.textContent = 'Failed to copy';
        }
        
        document.body.removeChild(textArea);
    }
});
