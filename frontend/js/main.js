// frontend/js/main.js
/**
 * Main JavaScript file for SecureLearn Cyber Lab
 * Common utilities and functions
 */

// API Base URL
const API_BASE_URL = '/api';

/**
 * Make API request
 */
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const responseData = await response.json();
        
        if (!response.ok) {
            throw new Error(responseData.error || 'Request failed');
        }
        
        return responseData;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background-color: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 9999;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

/**
 * Get risk color
 */
function getRiskColor(riskLevel) {
    const colors = {
        'LOW': '#10b981',
        'MEDIUM': '#f59e0b',
        'HIGH': '#ef4444'
    };
    return colors[riskLevel] || '#64748b';
}

/**
 * Sanitize HTML to prevent XSS
 */
function sanitizeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/**
 * Copy to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success');
    } catch (error) {
        console.error('Copy failed:', error);
        showNotification('Failed to copy', 'error');
    }
}

/**
 * Log simulation event
 */
async function logSimulationEvent(eventType, eventData = {}, riskLevel = 'UNKNOWN') {
    try {
        await apiRequest('/simulation-event', 'POST', {
            event_type: eventType,
            ...eventData,
            risk_level: riskLevel,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        console.error('Failed to log event:', error);
    }
}

/**
 * Smooth scroll to element
 */
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Initialize tooltips (if needed)
 */
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = element.dataset.tooltip;
            tooltip.style.cssText = `
                position: absolute;
                background-color: #1e293b;
                color: white;
                padding: 0.5rem;
                border-radius: 0.25rem;
                font-size: 0.875rem;
                z-index: 1000;
                pointer-events: none;
            `;
            document.body.appendChild(tooltip);
            
            const rect = element.getBoundingClientRect();
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 5}px`;
            tooltip.style.left = `${rect.left + (rect.width - tooltip.offsetWidth) / 2}px`;
            
            element._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', (e) => {
            if (element._tooltip) {
                document.body.removeChild(element._tooltip);
                element._tooltip = null;
            }
        });
    });
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initTooltips();
    
    // Add animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});