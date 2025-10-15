// APAAR Verification Form Handler
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('verifyForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const resultBox = document.getElementById('resultBox');
    const resultTitle = document.getElementById('resultTitle');
    const resultContent = document.getElementById('resultContent');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get CSRF token
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Get form data
        const formData = {
            apaar_id: document.getElementById('apaar_id').value.trim(),
            name: document.getElementById('name').value.trim(),
            income: parseInt(document.getElementById('income').value),
            education_level: document.getElementById('education_level').value,
            location: document.getElementById('location').value.trim()
        };

        // Validate form
        if (!formData.apaar_id || !formData.name || !formData.income || 
            !formData.education_level || !formData.location) {
            alert('Please fill in all required fields');
            return;
        }

        // Show loading state
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        resultBox.style.display = 'none';

        try {
            // Send POST request to API
            const response = await fetch('/api/verify-apaar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            // Hide loading state
            submitBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';

            // Display results
            resultBox.style.display = 'block';

            if (response.ok && data.status === 'success') {
                resultBox.className = 'result-box success';
                resultTitle.textContent = '✅ Verification Successful';
                resultContent.innerHTML = `
                    <p><strong>Message:</strong> ${data.message}</p>
                    <p><strong>Trust Score:</strong> ${data.trust_score}/100</p>
                    <p><strong>Status:</strong> <span class="status-badge status-${data.status_flag}">${data.status_flag}</span></p>
                    ${data.trust_score >= 60 
                        ? '<p class="success-msg">✅ You are eligible for verification</p>' 
                        : '<p class="warning-msg">⚠️ Your verification requires manual review</p>'}
                    <p style="margin-top: 1rem;">
                        <a href="/dashboard/" class="btn-primary">Go to Dashboard</a>
                    </p>
                `;
            } else {
                resultBox.className = 'result-box error';
                resultTitle.textContent = '❌ Verification Failed';
                resultContent.innerHTML = `
                    <p><strong>Error:</strong> ${data.message || 'Unable to verify APAAR ID'}</p>
                    <p>Please check your APAAR ID and try again.</p>
                    <p><strong>Demo IDs:</strong> Use <code>APAAR123</code> or <code>VALID123</code></p>
                `;
            }

            // Scroll to result
            resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (error) {
            console.error('Error:', error);
            
            // Hide loading state
            submitBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';

            // Display error
            resultBox.style.display = 'block';
            resultBox.className = 'result-box error';
            resultTitle.textContent = '❌ Network Error';
            resultContent.innerHTML = `
                <p>Unable to connect to the server. Please check your internet connection and try again.</p>
                <p><strong>Error:</strong> ${error.message}</p>
            `;
        }
    });
});

// Future integration placeholders:

// TODO: Integrate with real OTP service (Twilio/AWS SNS)
// function sendRealOTP(phoneNumber) {
//     // Implementation for sending real OTP via SMS gateway
// }

// TODO: Integrate with DigiLocker API for document verification
// async function verifyWithDigiLocker(apaarId) {
//     // Implementation for DigiLocker integration
//     // Fetch documents from DigiLocker using APAAR ID
// }

// TODO: Integrate with ML model for trust scoring
// async function calculateAITrustScore(userData) {
//     // Send user data to ML model endpoint
//     // Receive sophisticated trust score based on multiple factors
// }

// TODO: Integrate with blockchain for immutable record storage
// async function storeOnBlockchain(verificationRecord) {
//     // Store verification hash on blockchain
//     // Return transaction hash
// }
