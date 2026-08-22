// frontend/js/analyzer.js
/**
 * URL Analyzer functionality
 */

// Analyze URL function
async function analyzeUrl(url) {
    if (!url) {
        url = document.getElementById('urlInput').value.trim();
    } else {
        document.getElementById('urlInput').value = url;
    }
    
    if (!url) {
        showNotification('Please enter a URL', 'error');
        return;
    }
    
    // Show loading state
    const analyzeButton = document.getElementById('analyzeButtonText');
    const loadingButton = document.getElementById('analyzeButtonLoading');
    
    if (analyzeButton && loadingButton) {
        analyzeButton.style.display = 'none';
        loadingButton.style.display = 'inline';
    }
    
    try {
        // Call API
        const response = await apiRequest('/analyze-url', 'POST', { url });
        
        if (response.success) {
            displayUrlResults(response.result);
            
            // Log event
            await logSimulationEvent('url_analysis', {
                page: 'url-analyzer',
                interaction: 'analysis_completed'
            }, response.result.risk_level);
            
            showNotification('Analysis complete!', 'success');
        } else {
            showNotification(response.error || 'Analysis failed', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        // Reset button state
        if (analyzeButton && loadingButton) {
            analyzeButton.style.display = 'inline';
            loadingButton.style.display = 'none';
        }
    }
}

/**
 * Display URL analysis results
 */
function displayUrlResults(result) {
    // Show results section
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Display risk score
    const scoreNumber = document.getElementById('scoreNumber');
    const scoreCircle = document.getElementById('scoreCircle');
    const riskLevel = document.getElementById('riskLevel');
    
    if (scoreNumber && scoreCircle && riskLevel) {
        scoreNumber.textContent = result.risk_score;
        riskLevel.textContent = result.risk_level;
        
        // Color code based on risk
        scoreCircle.className = 'score-circle';
        if (result.risk_level === 'HIGH') {
            scoreCircle.classList.add('risk-high');
        } else if (result.risk_level === 'MEDIUM') {
            scoreCircle.classList.add('risk-medium');
        } else {
            scoreCircle.classList.add('risk-low');
        }
    }
    
    // Display analyzed URL
    const analyzedUrl = document.getElementById('analyzedUrl');
    if (analyzedUrl) {
        analyzedUrl.textContent = result.url;
    }
    
    // Display ML prediction
    const mlPrediction = document.getElementById('mlPrediction');
    const mlConfidence = document.getElementById('mlConfidence');
    
    if (mlPrediction && mlConfidence) {
        mlPrediction.textContent = result.ml_prediction.toUpperCase();
        mlPrediction.style.color = result.ml_prediction === 'phishing' ? '#ef4444' : '#10b981';
        mlConfidence.textContent = (result.ml_confidence * 100).toFixed(2) + '%';
    }
    
    // Display indicators
    const indicatorsList = document.getElementById('indicatorsList');
    if (indicatorsList) {
        if (result.indicators && result.indicators.length > 0) {
            indicatorsList.innerHTML = '<ul class="indicators-list">' +
                result.indicators.map(ind => `<li>⚠️ ${sanitizeHTML(ind)}</li>`).join('') +
                '</ul>';
        } else {
            indicatorsList.innerHTML = '<p class="success-message">✅ No major phishing indicators detected</p>';
        }
    }
    
    // Display features
    const featuresList = document.getElementById('featuresList');
    if (featuresList && result.features) {
        const featuresHTML = Object.entries(result.features)
            .filter(([key, value]) => typeof value === 'number' || typeof value === 'boolean')
            .map(([key, value]) => `
                <div class="feature-badge">
                    <strong>${formatFeatureName(key)}</strong>
                    <span>${formatFeatureValue(value)}</span>
                </div>
            `).join('');
        featuresList.innerHTML = featuresHTML;
    }
    
    // Display recommendation
    const recommendationText = document.getElementById('recommendationText');
    const recommendationCard = document.getElementById('recommendationCard');
    
    if (recommendationText && recommendationCard) {
        recommendationText.textContent = result.recommendation;
        
        recommendationCard.className = 'card recommendation-card';
        if (result.risk_level === 'HIGH') {
            recommendationCard.classList.add('risk-high');
        } else if (result.risk_level === 'MEDIUM') {
            recommendationCard.classList.add('risk-medium');
        } else {
            recommendationCard.classList.add('risk-low');
        }
    }
    
    // Display ML explanation
    const explanationContent = document.getElementById('explanationContent');
    if (explanationContent && result.ml_explanation) {
        const topFeatures = Object.entries(result.ml_explanation)
            .slice(0, 10)
            .map(([feature, data]) => `
                <div class="explanation-item" style="margin-bottom: 1rem; padding: 0.75rem; background-color: #f8fafc; border-radius: 0.5rem;">
                    <strong>${formatFeatureName(feature)}</strong><br>
                    Value: ${data.value}, Importance: ${(data.importance * 100).toFixed(2)}%
                </div>
            `).join('');
        
        explanationContent.innerHTML = `
            <h3>Top Contributing Features:</h3>
            ${topFeatures}
        `;
    }
}

/**
 * Format feature name for display
 */
function formatFeatureName(name) {
    return name
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
}

/**
 * Format feature value for display
 */
function formatFeatureValue(value) {
    if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No';
    }
    if (typeof value === 'number') {
        return value % 1 === 0 ? value : value.toFixed(2);
    }
    return value;
}

// Add event listener for form submission
if (document.getElementById('urlAnalysisForm')) {
    document.getElementById('urlAnalysisForm').addEventListener('submit', (e) => {
        e.preventDefault();
        analyzeUrl();
    });
}