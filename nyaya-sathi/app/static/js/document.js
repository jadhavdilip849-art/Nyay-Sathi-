/**
 * Nyaya Sathi - Explain My Document Logic
 */

function loadSampleNotices() {
  const selectEl = document.getElementById('sample-doc-select');
  if (!selectEl) return;

  fetch('/api/document/samples')
    .then(res => res.json())
    .then(data => {
      const samples = data.samples || [];
      selectEl.innerHTML = '<option value="">-- किंवा नमुना नोटीस निवडा (Select Sample Notice) --</option>' +
        samples.map(s => `<option value="${s.id}">${s.title}</option>`).join('');
    })
    .catch(err => console.error("Error loading sample notices:", err));
}

function onSampleDocSelected() {
  const selectEl = document.getElementById('sample-doc-select');
  const sampleId = selectEl.value;
  if (!sampleId) return;

  fetch('/api/document/samples')
    .then(res => res.json())
    .then(data => {
      const matched = data.samples.find(s => s.id === sampleId);
      if (matched) {
        document.getElementById('doc-text-input').value = matched.raw_text;
      }
    });
}

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    const textContent = e.target.result;
    document.getElementById('doc-text-input').value = textContent;
  };

  // If text file
  if (file.type.includes("text") || file.name.endsWith(".txt") || file.name.endsWith(".csv")) {
    reader.readAsText(file);
  } else {
    // For images/PDFs in prototype, simulate OCR extraction notice
    document.getElementById('doc-text-input').value = 
      `[दस्तऐवज अपलोड: ${file.name}]\nMUNICIPAL CORPORATION OF GREATER MUMBAI / PUNE MUNICIPAL CORPORATION\nNOTICE UNDER SECTION 351 OF THE MUNICIPAL CORPORATION ACT\nNotice No: MC/ENC/2026/8942\nDate of Notice: 15/10/2026\nTo, Occupier / Owner of Shop No. 4, Shivaji Market, Pune.\nSUBJECT: SHOW CAUSE NOTICE UNDER SECTION 351 FOR ALLEGED UNAUTHORIZED SHED EXTENSION\nCalled upon to SHOW CAUSE in writing within 15 (FIFTEEN) DAYS as to why the unauthorized construction should not be demolished. Required to produce original building plans on or before 30/10/2026. Failing which matter will be decided EX-PARTE.`;
  }
}

function analyzeDocument() {
  const text = document.getElementById('doc-text-input').value.trim();
  const resultContainer = document.getElementById('doc-analysis-result');
  if (!text) {
    alert("कृपया दस्तऐवजाचा मजकूर टाका किंवा फाइल अपलोड करा.");
    return;
  }

  resultContainer.innerHTML = `
    <div class="result-card" style="text-align: center; padding: 2rem;">
      <div style="font-size: 2rem;">📄</div>
      <p>कागदपत्राचे विश्लेषण, तारखा आणि कायदेशीर अटी तपासत आहे...</p>
    </div>
  `;

  fetch('/api/document/explain', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: text,
      language: window.currentLang || 'mr-IN'
    })
  })
  .then(res => res.json())
  .then(data => {
    renderDocAnalysis(data);
  })
  .catch(err => {
    resultContainer.innerHTML = `<div class="result-card" style="color: var(--danger);">त्रुटी: ${err.message}</div>`;
  });
}

function renderDocAnalysis(data) {
  const container = document.getElementById('doc-analysis-result');
  if (!container) return;

  const terms = data.legal_terms_explained || [];
  const actions = data.actions_requested || [];
  const deadlines = data.deadlines_analysis || {};
  const lawyerQuestions = data.questions_for_lawyer || [];

  container.innerHTML = `
    <div class="result-card">
      <div class="result-header">
        <div>
          <span class="badge-official">📑 कागदपत्र विश्लेषण / Document Explainer</span>
          <h2 style="font-size: 1.25rem; color: var(--primary); margin-top: 0.35rem;">
            ${data.apparent_document_type || 'अधिकृत नोटीस'}
          </h2>
        </div>
        <button class="btn-speaker" onclick="window.voiceAssistant.speak('${escapeQuotes(data.plain_summary)}')">
          🔊 सारांश ऐका / Listen Summary
        </button>
      </div>

      <div style="font-size: 1.05rem; line-height: 1.6; margin-bottom: 1.25rem;">
        <strong>१. सोप्या भाषेतील सारांश (Plain Summary):</strong><br>
        ${data.plain_summary}
      </div>

      <div style="background: #fefce8; border-left: 4px solid #eab308; padding: 1rem; border-radius: 4px; margin-bottom: 1.25rem;">
        <div style="font-weight: bold; color: #854d0e; margin-bottom: 0.35rem;">
          ⏰ महत्त्वाच्या तारखा व मुदत विश्लेषण (Explicit vs Inferred Deadlines):
        </div>
        <div>
          <strong>दस्तऐवजात स्पष्ट छापलेली मुदत:</strong>
          <ul style="padding-left: 1.2rem; margin: 0.25rem 0;">
            ${(deadlines.explicitly_printed_deadlines || []).map(d => `<li>${d}</li>`).join('')}
          </ul>
        </div>
        <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #713f12;">
          <strong>कायदेशीर नियम:</strong> ${(deadlines.inferred_legal_rule || []).join(' ')}
        </div>
      </div>

      <div class="section-title">⚡ आपल्याकडून अपेक्षित कृती (Requested Actions):</div>
      <ul class="steps-list">
        ${actions.map(a => `<li>${a}</li>`).join('')}
      </ul>

      <div class="section-title">📖 कठीण कायदेशीर शब्दांचे सोपे अर्थ (Legal Glossary):</div>
      <div style="display: grid; gap: 0.5rem; margin-top: 0.5rem;">
        ${terms.map(t => `
          <div style="background: #f1f5f9; padding: 0.65rem 0.9rem; border-radius: 6px;">
            <strong style="color: var(--primary);">${t.term}:</strong> ${t.explanation}
          </div>
        `).join('')}
      </div>

      <div class="section-title" style="margin-top: 1.25rem;">❓ सरकारी किंवा मोफत वकिलांना विचारण्यासाठी महत्त्वाचे प्रश्न:</div>
      <ul class="questions-list">
        ${lawyerQuestions.map(q => `<li>${q}</li>`).join('')}
      </ul>

      <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border-color); font-size: 0.8rem; color: var(--text-muted);">
        <strong>गोपनीयता व कायदेशीर सूचना:</strong> ${data.validity_disclaimer}
      </div>
    </div>
  `;
}
