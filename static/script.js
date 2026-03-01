// =====================================================
// LegalAI — Search Page JavaScript
// =====================================================

const API_URL = '/api';

const searchBtn = document.getElementById('searchBtn');
const caseStudyInput = document.getElementById('caseStudy');
const resultsSection = document.getElementById('resultsSection');
const resultsContainer = document.getElementById('resultsContainer');
const loadingIndicator = document.getElementById('loadingIndicator');
const summarySection = document.getElementById('summarySection');
const summaryBox = document.getElementById('summaryBox');
const aiAnalysisSection = document.getElementById('aiAnalysisSection');
const aiAnalysisContainer = document.getElementById('aiAnalysisContainer');
const entitiesSection = document.getElementById('entitiesSection');
const entitiesContainer = document.getElementById('entitiesContainer');

// Search for similar cases
searchBtn.addEventListener('click', async () => {
    const caseStudy = caseStudyInput.value.trim();

    if (!caseStudy) {
        showToast('Please enter a case study description', 'error');
        return;
    }

    try {
        showLoading('Analyzing your case with AI...');
        resultsSection.style.display = 'none';
        aiAnalysisSection.style.display = 'none';
        summarySection.style.display = 'none';
        entitiesSection.style.display = 'none';
        searchBtn.disabled = true;

        const response = await fetch(`${API_URL}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ case_study: caseStudy })
        });

        const data = await response.json();

        if (response.ok) {
            displayEntities(data.entities);
            displaySummary(data.summarized_input);
            displayAIAnalysis(data.ai_analysis);
            displayResults(data.results);
        } else {
            showToast(data.error || 'Failed to search cases', 'error');
        }
    } catch (error) {
        showToast('Connection error: ' + error.message, 'error');
    } finally {
        hideLoading();
        searchBtn.disabled = false;
    }
});

// Display NER entities
function displayEntities(entityData) {
    if (!entityData || !entityData.success || entityData.total_entities === 0) {
        entitiesSection.style.display = 'none';
        return;
    }

    const entities = entityData.entities;
    let html = '';

    const categoryConfig = {
        persons: { class: 'person', icon: '👤' },
        courts: { class: 'court', icon: '🏛️' },
        laws: { class: 'law', icon: '📜' },
        sections: { class: 'section', icon: '§' },
        dates: { class: 'date', icon: '📅' },
        locations: { class: 'location', icon: '📍' },
        monetary: { class: 'money', icon: '💰' },
        organizations: { class: 'court', icon: '🏢' },
        legal_roles: { class: 'law', icon: '⚖' }
    };

    for (const [category, items] of Object.entries(entities)) {
        const config = categoryConfig[category] || { class: 'law', icon: '•' };
        items.forEach(item => {
            html += `<span class="entity-tag ${config.class}">${config.icon} ${item.text}</span>`;
        });
    }

    if (html) {
        entitiesContainer.innerHTML = html;
        entitiesSection.style.display = 'block';
    }
}

// Display summary
function displaySummary(summarizedText) {
    if (summarizedText && summarizedText.trim()) {
        summaryBox.textContent = summarizedText;
        summarySection.style.display = 'block';
    } else {
        summarySection.style.display = 'none';
    }
}

// Display AI Analysis
function displayAIAnalysis(aiData) {
    if (!aiData || !aiData.available) {
        aiAnalysisSection.style.display = 'none';
        return;
    }

    const analysis = aiData.analysis;
    let html = '';

    // Verdict Prediction
    if (analysis.verdict_prediction) {
        const verdict = analysis.verdict_prediction.toLowerCase();
        const verdictClass = verdict === 'win' ? 'verdict-win' : verdict === 'loss' ? 'verdict-loss' : 'verdict-draw';
        const confidence = analysis.confidence_level || 'medium';

        html += `
            <div class="ai-verdict-box ${verdictClass}">
                <div class="verdict-header">
                    <h3>📊 Predicted Verdict</h3>
                    <span class="confidence-badge confidence-${confidence}">${confidence.toUpperCase()} CONFIDENCE</span>
                </div>
                <div class="verdict-result">
                    ${analysis.verdict_prediction.toUpperCase()}
                </div>
                ${analysis.win_probability_plaintiff !== undefined ? `
                    <div class="probability-bars">
                        <div class="prob-bar">
                            <label>Plaintiff Win Probability:</label>
                            <div class="prob-fill" style="width: ${analysis.win_probability_plaintiff}%">
                                ${analysis.win_probability_plaintiff}%
                            </div>
                        </div>
                        <div class="prob-bar">
                            <label>Defendant Win Probability:</label>
                            <div class="prob-fill" style="width: ${analysis.win_probability_defendant}%">
                                ${analysis.win_probability_defendant}%
                            </div>
                        </div>
                    </div>
                ` : ''}
                ${aiData.provider ? `<div style="text-align: right; margin-top: 0.75rem; font-size: 0.7rem; color: var(--text-muted);">via ${aiData.provider}</div>` : ''}
            </div>
        `;
    }

    // Analysis Details
    html += '<div class="ai-analysis-details">';

    if (analysis.legal_issues && Array.isArray(analysis.legal_issues)) {
        html += `<div class="analysis-card"><h4>🔍 Key Legal Issues</h4><ul>${analysis.legal_issues.map(i => `<li>${i}</li>`).join('')}</ul></div>`;
    }
    if (analysis.applicable_laws && Array.isArray(analysis.applicable_laws)) {
        html += `<div class="analysis-card"><h4>⚖️ Applicable Laws</h4><ul>${analysis.applicable_laws.map(l => `<li>${l}</li>`).join('')}</ul></div>`;
    }
    if (analysis.plaintiff_strengths && Array.isArray(analysis.plaintiff_strengths)) {
        html += `<div class="analysis-card"><h4>💪 Plaintiff Strengths</h4><ul>${analysis.plaintiff_strengths.map(s => `<li>${s}</li>`).join('')}</ul></div>`;
    }
    if (analysis.plaintiff_weaknesses && Array.isArray(analysis.plaintiff_weaknesses)) {
        html += `<div class="analysis-card"><h4>⚠️ Plaintiff Weaknesses</h4><ul>${analysis.plaintiff_weaknesses.map(w => `<li>${w}</li>`).join('')}</ul></div>`;
    }
    if (analysis.defendant_strengths && Array.isArray(analysis.defendant_strengths)) {
        html += `<div class="analysis-card"><h4>🛡️ Defendant Strengths</h4><ul>${analysis.defendant_strengths.map(s => `<li>${s}</li>`).join('')}</ul></div>`;
    }
    if (analysis.defendant_weaknesses && Array.isArray(analysis.defendant_weaknesses)) {
        html += `<div class="analysis-card"><h4>⚡ Defendant Weaknesses</h4><ul>${analysis.defendant_weaknesses.map(w => `<li>${w}</li>`).join('')}</ul></div>`;
    }
    if (analysis.reasoning) {
        html += `<div class="analysis-card"><h4>🧠 Detailed Reasoning</h4><p>${analysis.reasoning}</p></div>`;
    }
    if (analysis.recommended_legal_strategy) {
        html += `<div class="analysis-card strategy-card"><h4>📋 Recommended Strategy</h4><p>${analysis.recommended_legal_strategy}</p></div>`;
    }

    html += '</div>';

    aiAnalysisContainer.innerHTML = html;
    aiAnalysisSection.style.display = 'block';
}

// Display search results
function displayResults(results) {
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="result-card"><p style="color: var(--text-muted);">No similar cases found.</p></div>';
    } else {
        results.forEach((result, index) => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.innerHTML = `
                <div class="result-header">
                    <div class="case-name">${index + 1}. ${result.case_name}</div>
                    <div class="similarity-score">${result.similarity_score}% Match</div>
                </div>
                <div class="result-footer">
                    <span class="filename">${result.filename}</span>
                    <button class="btn-open-pdf" onclick="openPDF('${result.filename}')">📄 Open PDF</button>
                </div>
            `;
            resultsContainer.appendChild(card);
        });
    }

    resultsSection.style.display = 'block';
}

// Open PDF
function openPDF(filename) {
    window.open(`/pdf/${encodeURIComponent(filename)}`, '_blank');
}

// Loading states
function showLoading(message) {
    loadingIndicator.querySelector('p').textContent = message || 'Processing...';
    loadingIndicator.style.display = 'block';
}

function hideLoading() {
    loadingIndicator.style.display = 'none';
}

// Toast notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3500);
}
