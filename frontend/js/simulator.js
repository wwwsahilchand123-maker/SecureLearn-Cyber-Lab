// frontend/js/simulator.js
/**
 * Phishing Simulation functionality
 */

// Simulation templates
const SIMULATIONS = {
    banking: {
        title: 'SecureBank Online',
        url: 'http://securebank-verify.tk/login',
        logo: '🏦',
        description: 'Suspicious banking login page',
        html: `
            <div style="max-width: 400px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">🏦</div>
                <h2 style="text-align: center; color: #1e40af; margin-bottom: 0.5rem;">SecureBank Online</h2>
                <div style="background: #fee2e2; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 4px solid #ef4444;">
                    <strong>⚠️ Security Alert:</strong> Your account has been locked due to suspicious activity. Login immediately to verify your identity.
                </div>
                <form id="phishingForm" onsubmit="handlePhishingSubmit(event, 'banking')">
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Account Number:</label>
                        <input type="text" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 0.5rem;">
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Password:</label>
                        <input type="password" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 0.5rem;">
                    </div>
                    <button type="submit" style="width: 100%; padding: 1rem; background: #ef4444; color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer;">
                        Login Now
                    </button>
                </form>
                <div style="margin-top: 1rem; text-align: center; font-size: 0.75rem; color: #64748b;">
                    URL: http://securebank-verify.tk/login
                </div>
            </div>
        `,
        indicators: [
            'Suspicious domain (securebank-verify.tk)',
            'Creates urgency with "account locked" message',
            'Unusual TLD (.tk is often used in phishing)',
            'Missing HTTPS encryption',
            'Generic design with minimal branding',
            'Threatening language'
        ]
    },
    social: {
        title: 'SocialConnect',
        url: 'http://socialconnect-security.xyz/verify',
        logo: '📱',
        description: 'Fake social media verification',
        html: `
            <div style="max-width: 400px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">📱</div>
                <h2 style="text-align: center; color: #3b82f6; margin-bottom: 0.5rem;">SocialConnect</h2>
                <div style="background: #fef3c7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 4px solid #f59e0b;">
                    <strong>⚠️ Action Required:</strong> We've detected a login from an unknown device. Verify your account within 24 hours to avoid suspension.
                </div>
                <form id="phishingForm" onsubmit="handlePhishingSubmit(event, 'social')">
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Email or Username:</label>
                        <input type="text" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 0.5rem;">
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Password:</label>
                        <input type="password" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 0.5rem;">
                    </div>
                    <button type="submit" style="width: 100%; padding: 1rem; background: #3b82f6; color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer;">
                        Verify Account
                    </button>
                </form>
                <div style="margin-top: 1rem; text-align: center; font-size: 0.75rem; color: #64748b;">
                    URL: http://socialconnect-security.xyz/verify
                </div>
            </div>
        `,
        indicators: [
            'Suspicious domain (socialconnect-security.xyz)',
            'Unusual TLD (.xyz)',
            'Missing HTTPS',
            'Creates urgency (24 hours)',
            'Threatens account suspension',
            'Generic branding'
        ]
    },
    email: {
        title: 'CloudMail',
        url: 'http://cloudmail-verify.ml/signin',
        logo: '📧',
        description: 'Suspicious email service login',
        html: `
            <div style="max-width: 400px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">📧</div>
                <h2 style="text-align: center; color: #10b981; margin-bottom: 0.5rem;">CloudMail</h2>
                <div style="background: #fee2e2; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 4px solid #ef4444;">
                    <strong>⚠️ Storage Full:</strong> Your mailbox is 99% full. Verify your account to increase storage or lose old emails permanently.
                </div>
                <form id="phishingForm" onsubmit="handlePhishingSubmit(event, 'email')">
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Email Address:</label>
                        <input type="email" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 0.5rem;">
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Password:</label>
                        <input type="password" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 0.5rem;">
                    </div>
                    <button type="submit" style="width: 100%; padding: 1rem; background: #10b981; color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer;">
                        Verify & Upgrade
                    </button>
                </form>
                <div style="margin-top: 1rem; text-align: center; font-size: 0.75rem; color: #64748b;">
                    URL: http://cloudmail-verify.ml/signin
                </div>
            </div>
        `,
        indicators: [
            'Suspicious domain (cloudmail-verify.ml)',
            'Free TLD (.ml) often used in scams',
            'No HTTPS encryption',
            'Creates false urgency about storage',
            'Threatens data loss',
            'Poor domain structure'
        ]
    },
    shopping: {
        title: 'ShopFast',
        url: 'http://shopfast-account.gq/update',
        logo: '🛒',
        description: 'E-commerce account verification scam',
        html: `
            <div style="max-width: 400px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">🛒</div>
                <h2 style="text-align: center; color: #f59e0b; margin-bottom: 0.5rem;">ShopFast</h2>
                <div style="background: #fef3c7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 4px solid #f59e0b;">
                    <strong>🎁 Congratulations!</strong> You've won a $500 gift card! Login to claim your prize before it expires in 2 hours.
                </div>
                <form id="phishingForm" onsubmit="handlePhishingSubmit(event, 'shopping')">
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Email or Phone:</label>
                        <input type="text" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 0.5rem;">
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Password:</label>
                        <input type="password" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 0.5rem;">
                    </div>
                    <button type="submit" style="width: 100%; padding: 1rem; background: #f59e0b; color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer;">
                        Claim Prize Now!
                    </button>
                </form>
                <div style="margin-top: 1rem; text-align: center; font-size: 0.75rem; color: #64748b;">
                    URL: http://shopfast-account.gq/update
                </div>
            </div>
        `,
        indicators: [
            'Suspicious domain (shopfast-account.gq)',
            'Free TLD (.gq)',
            'No HTTPS',
            'Too good to be true (free $500)',
            'Creates extreme urgency (2 hours)',
            'Unsolicited prize notification'
        ]
    }
};

/**
 * Start simulation
 */
function startSimulation(type) {
    const simulation = SIMULATIONS[type];
    if (!simulation) return;
    
    // Log event
    logSimulationEvent('simulation_started', {
        page: 'simulator',
        simulation_type: type,
        interaction: 'simulation_opened'
    }, 'MEDIUM');
    
    // Hide selection, show simulation
    const simulationContainer = document.getElementById('simulationContainer');
    const simulationContent = document.getElementById('simulationContent');
    
    if (simulationContainer && simulationContent) {
        simulationContent.innerHTML = simulation.html;
        simulationContainer.style.display = 'block';
        simulationContainer.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Handle phishing form submission (SAFE - NO DATA STORED)
 */
function handlePhishingSubmit(event, type) {
    event.preventDefault();
    
    // IMPORTANT: DO NOT collect or store any form data
    // Immediately show warning
    
    const simulation = SIMULATIONS[type];
    
    // Log that user interacted (but no credentials)
    logSimulationEvent('phishing_interaction', {
        page: 'simulator',
        simulation_type: type,
        interaction: 'form_submitted'
    }, 'HIGH');
    
    // Show warning modal
    showPhishingWarning(simulation);
    
    return false;
}

/**
 * Show phishing warning
 */
function showPhishingWarning(simulation) {
    const modal = document.getElementById('warningModal');
    const warningIndicators = document.getElementById('warningIndicators');
    const warningEducation = document.getElementById('warningEducation');
    
    if (modal && warningIndicators && warningEducation) {
        // Populate indicators
        warningIndicators.innerHTML = `
            <div style="background: #fef2f2; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
                <h3 style="color: #ef4444; margin-bottom: 0.5rem;">🚩 Red Flags Detected:</h3>
                <ul style="margin-left: 1.5rem;">
                    ${simulation.indicators.map(ind => `<li>${sanitizeHTML(ind)}</li>`).join('')}
                </ul>
            </div>
        `;
        
        // Education content
        warningEducation.innerHTML = `
            <div style="background: #eff6ff; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
                <h3 style="color: #2563eb; margin-bottom: 0.5rem;">📚 What You Should Know:</h3>
                <ul style="margin-left: 1.5rem;">
                    <li><strong>Never</strong> enter real credentials on suspicious sites</li>
                    <li>Always verify URLs carefully before logging in</li>
                    <li>Legitimate companies won't threaten account closure via email</li>
                    <li>Be skeptical of urgency and "act now" messages</li>
                    <li>When in doubt, contact the company directly through official channels</li>
                </ul>
            </div>
        `;
        
        modal.style.display = 'flex';
    }
}

/**
 * Close warning modal
 */
function closeWarningModal() {
    const modal = document.getElementById('warningModal');
    if (modal) {
        modal.style.display = 'none';
    }
    
    // End simulation
    endSimulation();
}

/**
 * Show detailed analysis
 */
function showDetailedAnalysis() {
    closeWarningModal();
    window.location.href = 'resources.html';
}

/**
 * End simulation
 */
function endSimulation() {
    const simulationContainer = document.getElementById('simulationContainer');
    if (simulationContainer) {
        simulationContainer.style.display = 'none';
    }
    
    // Scroll back to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}