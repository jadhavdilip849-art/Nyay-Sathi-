/**
 * Nyaya Sathi - Understand My Rights Feature Logic
 */

function loadCategories() {
  const container = document.getElementById('categories-container');
  if (!container) return;

  fetch('/api/rights/categories')
    .then(res => res.json())
    .then(data => {
      const categories = data.categories || [];
      const lang = window.currentLang || 'mr-IN';
      const langPrefix = lang.slice(0, 2);

      const iconMap = {
        "unpaid_wages": "💼",
        "consumer_complaints": "🛍️",
        "cybercrime": "🛡️",
        "rental_housing": "🏠",
        "women_rights": "👩",
        "legal_aid": "⚖️",
        "senior_citizens": "👴",
        "disability_rights": "♿",
        "government_benefits": "📜",
        "land_disputes": "🌾"
      };

      container.innerHTML = categories.map(cat => {
        const name = cat[`name_${langPrefix}`] || cat.name_en;
        const icon = iconMap[cat.id] || "⚖️";
        return `
          <div class="category-card" onclick="selectCategory('${cat.id}')">
            <div class="cat-header">
              <span class="cat-icon">${icon}</span>
              <div class="cat-title">${name}</div>
            </div>
            <div class="cat-desc">${langPrefix === 'mr' ? 'कायदेशीर हक्क आणि पुढील पावले जाणून घ्या' : (langPrefix === 'hi' ? 'कानूनी अधिकार और प्रक्रिया समझें' : 'Understand rights and procedures')}</div>
          </div>
        `;
      }).join('');
    })
    .catch(err => console.error("Error loading categories:", err));
}

function selectCategory(categoryId) {
  const inputEl = document.getElementById('chat-query-input');
  if (categoryId === 'unpaid_wages') {
    inputEl.value = (window.currentLang === 'hi-IN') 
      ? "मेरे नियोक्ता ने दो महीने से वेतन नहीं दिया है। मुझे क्या करना चाहिए?" 
      : (window.currentLang === 'en-IN' ? "My employer has not paid my wages for two months. What can I do?" : "माझ्या मालकाने दोन महिन्यांपासून पगार दिलेला नाही. मी काय करू शकतो?");
  } else if (categoryId === 'consumer_complaints') {
    inputEl.value = (window.currentLang === 'hi-IN')
      ? "दुकानदार ने खराब सामान दिया और वारंटी से मना कर रहा है।"
      : (window.currentLang === 'en-IN' ? "Shopkeeper sold defective item and refuses warranty refund." : "दुकानदाराने खराब वस्तू दिली असून वॉरंटी नाकारत आहे.");
  } else if (categoryId === 'cybercrime') {
    inputEl.value = (window.currentLang === 'hi-IN')
      ? "मेरे बैंक खाते से ऑनलाइन धोखाधड़ी में पैसे कट गए हैं।"
      : (window.currentLang === 'en-IN' ? "Money debited through online banking fraud." : "माझ्या बँक खात्यातून ऑनलाइन फसवणुकीद्वारे पैसे गेले आहेत.");
  } else if (categoryId === 'legal_aid') {
    inputEl.value = (window.currentLang === 'hi-IN')
      ? "मुझे अदालत के मामले में मुफ्त सरकारी वकील की सहायता चाहिए।"
      : (window.currentLang === 'en-IN' ? "I need free legal representation in court." : "मला कोर्टाच्या कामासाठी मोफत सरकारी वकील कसा मिळेल?");
  } else if (categoryId === 'rental_housing') {
    inputEl.value = (window.currentLang === 'hi-IN')
      ? "घर खाली करने पर मकान मालिक मेरी सुरक्षा राशि नहीं लौटा रहा।"
      : (window.currentLang === 'en-IN' ? "Landlord refuses to return security deposit upon vacating." : "घर सोडल्यावर घरमालक डिपॉझिट परत करत नाही.");
  } else {
    inputEl.value = `हक्क आणि कायदा: ${categoryId}`;
  }

  submitQuery();
}

function submitQuery() {
  const inputEl = document.getElementById('chat-query-input');
  const query = inputEl ? inputEl.value.trim() : '';
  if (!query) return;

  const resultContainer = document.getElementById('query-result-container');
  if (!resultContainer) return;

  resultContainer.innerHTML = `
    <div class="result-card" style="text-align: center; padding: 2.5rem;">
      <div style="font-size: 2rem; margin-bottom: 0.5rem;">⏳</div>
      <p style="font-weight: 600;">कायदेशीर माहिती व अधिकृत स्रोत शोधत आहे... / Retrieving verified legal information...</p>
    </div>
  `;

  fetch('/api/rights/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: query,
      language: window.currentLang || 'mr-IN'
    })
  })
  .then(res => res.json())
  .then(data => {
    renderQueryResult(data);
  })
  .catch(err => {
    resultContainer.innerHTML = `<div class="result-card" style="color: var(--danger);">माहिती मिळवताना अडचण आली: ${err.message}</div>`;
  });
}

function renderQueryResult(data) {
  const container = document.getElementById('query-result-container');
  if (!container) return;

  // Emergency Safety Banner if triggered
  let safetyHtml = '';
  if (data.safety && data.safety.is_emergency) {
    safetyHtml = `
      <div class="badge-emergency">
        ⚠️ तातडीची सूचना / Emergency Alert: ${data.safety.escalation_message || 'कृपया तातडीने ११२ किंवा १८१ वर संपर्क साधा!'}
      </div>
    `;
  }

  const citation = data.official_citation || {};
  const steps = data.action_steps || [];
  const questions = data.clarifying_questions || [];

  container.innerHTML = `
    <div class="result-card">
      ${safetyHtml}
      
      <div class="result-header">
        <div>
          <span class="badge-official">✓ अधिकृत कायदेशीर माहिती / Verified Official Source</span>
          <h2 style="font-size: 1.3rem; color: var(--primary); margin-top: 0.5rem;">${data.domain_name || 'कायदेशीर माहिती'}</h2>
        </div>
        <button class="btn-speaker" onclick="window.voiceAssistant.speak('${escapeQuotes(data.plain_language_summary)}')">
          🔊 ऐका / Listen
        </button>
      </div>

      <div style="font-size: 1.05rem; line-height: 1.6; margin-bottom: 1.25rem;">
        <strong>सोप्या भाषेत स्पष्टीकरण:</strong><br>
        ${data.plain_language_summary}
      </div>

      <div class="citation-box">
        <div style="font-weight: bold; margin-bottom: 0.25rem;">📜 अधिकृत संदर्भ / Official Statutory Authority:</div>
        <div><strong>कायदा:</strong> ${citation.title || 'N/A'}</div>
        <div><strong>प्राधिकरण:</strong> ${citation.issuing_authority || 'N/A'}</div>
        ${citation.official_url ? `<div><strong>अधिकृत पोर्टल:</strong> <a href="${citation.official_url}" target="_blank" class="citation-link">${citation.official_url}</a></div>` : ''}
        ${citation.helpline ? `<div><strong>टोल-फ्री हेल्पलाइन:</strong> <span style="font-weight: bold; color: var(--accent);">${citation.helpline}</span></div>` : ''}
      </div>

      <div class="section-title">🔍 पुढील वस्तुस्थिती समजून घेण्यासाठी महत्त्वाचे प्रश्न:</div>
      <ul class="questions-list">
        ${questions.map(q => `<li>${q}</li>`).join('')}
      </ul>

      <div class="section-title">🗺️ आपल्यासाठी सुचवलेली पुढील पावले (Action Plan):</div>
      <ol class="steps-list">
        ${steps.map(s => `<li>${s.action}</li>`).join('')}
      </ol>

      <div style="margin-top: 1.5rem; display: flex; gap: 0.75rem; flex-wrap: wrap;">
        <button class="btn-primary" onclick="openComplaintWithContext('${escapeQuotes(data.query)}')">
          ✍️ ही तक्रार तयार करा / Help Me Draft Complaint
        </button>
        <button class="btn-secondary" onclick="openLegalAidWithContext()">
          🏛️ मोफत विधी सेवा शोधा / Find Free Legal Aid
        </button>
      </div>

      <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border-color); font-size: 0.8rem; color: var(--text-muted);">
        <strong>अस्वीकरण:</strong> ${data.disclaimer}
      </div>
    </div>
  `;
}

function escapeQuotes(str) {
  if (!str) return '';
  return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

function openComplaintWithContext(query) {
  window.switchTab('complaint-tab');
  const factInput = document.getElementById('comp-facts');
  if (factInput && !factInput.value) {
    factInput.value = query;
  }
}

function openLegalAidWithContext() {
  window.switchTab('legalaid-tab');
}
