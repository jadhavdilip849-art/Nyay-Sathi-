/**
 * Nyaya Sathi - Help Me Write a Complaint Module
 */

function generateComplaintDraft() {
  const complainantName = document.getElementById('comp-name').value;
  const complainantAddress = document.getElementById('comp-address').value;
  const complainantPhone = document.getElementById('comp-phone').value;
  const oppositeName = document.getElementById('comp-opp-name').value;
  const oppositeAddress = document.getElementById('comp-opp-address').value;
  const matterType = document.getElementById('comp-type').value;
  const dates = document.getElementById('comp-dates').value;
  const facts = document.getElementById('comp-facts').value;
  const priorAction = document.getElementById('comp-prior-action').value;
  const relief = document.getElementById('comp-relief').value;

  if (!facts.trim()) {
    alert("कृपया काय घडले ते थोडक्यात नमूद करा. / Please enter facts of what happened.");
    return;
  }

  const container = document.getElementById('complaint-result-container');
  container.innerHTML = `
    <div class="result-card" style="text-align: center; padding: 2rem;">
      <div style="font-size: 2rem;">✍️</div>
      <p>वस्तुस्थितीदर्शक तक्रार मसुदा, ऑनलाइन फॉर्म आवृत्ती आणि कागदपत्र यादी तयार करत आहे...</p>
    </div>
  `;

  fetch('/api/complaint/draft', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      complainant_name: complainantName,
      complainant_address: complainantAddress,
      complainant_phone: complainantPhone,
      opposite_party_name: oppositeName,
      opposite_party_address: oppositeAddress,
      matter_type: matterType,
      dates_involved: dates,
      factual_summary: facts,
      prior_action_taken: priorAction,
      requested_relief: relief,
      language: window.currentLang || 'mr-IN'
    })
  })
  .then(res => res.json())
  .then(data => {
    renderComplaintOutput(data);
  })
  .catch(err => {
    container.innerHTML = `<div class="result-card" style="color: var(--danger);">मसुदा तयार करताना त्रुटी: ${err.message}</div>`;
  });
}

function renderComplaintOutput(data) {
  const container = document.getElementById('complaint-result-container');
  if (!container) return;

  const checklist = data.supporting_documents_checklist || [];
  const channel = data.submission_channel || {};

  container.innerHTML = `
    <div class="result-card">
      <div class="result-header">
        <div>
          <span class="badge-official">✓ वस्तुस्थितीदर्शक मसुदा / Factual Representation</span>
          <h2 style="font-size: 1.25rem; color: var(--primary); margin-top: 0.35rem;">
            तक्रार अर्ज व पुरावे तपासणी यादी
          </h2>
        </div>
      </div>

      <div style="margin-bottom: 1.5rem;">
        <div style="display: flex; gap: 0.5rem; margin-bottom: 0.75rem;">
          <button class="btn-secondary" style="border-bottom: 2px solid var(--accent);" id="tab-btn-formal" onclick="switchDraftVersion('formal')">
            📄 औपचारिक अर्ज (मराठी पत्र)
          </button>
          <button class="btn-secondary" id="tab-btn-short" onclick="switchDraftVersion('short')">
            💻 ऑनलाइन पोर्टल संक्षिप्त आवृत्ती (Short Form)
          </button>
          <button class="btn-secondary" id="tab-btn-en" onclick="switchDraftVersion('en')">
            🌐 English Representation
          </button>
        </div>

        <div id="draft-box-formal">
          <textarea id="complaint-text-formal" style="width: 100%; height: 260px; font-family: monospace; font-size: 0.9rem; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 6px;">${data.formal_letter_mr}</textarea>
        </div>

        <div id="draft-box-short" style="display: none;">
          <textarea id="complaint-text-short" style="width: 100%; height: 160px; font-family: monospace; font-size: 0.9rem; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 6px;">${data.short_portal_version_mr}</textarea>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">(समाधान किंवा CPGRAMS ऑनलाइन पोर्टलवरील ५०० अक्षरांच्या मर्यादेसाठी आदर्श)</p>
        </div>

        <div id="draft-box-en" style="display: none;">
          <textarea id="complaint-text-en" style="width: 100%; height: 260px; font-family: monospace; font-size: 0.9rem; padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 6px;">${data.formal_letter_en}</textarea>
        </div>

        <div style="margin-top: 0.75rem; display: flex; gap: 0.75rem;">
          <button class="btn-primary" onclick="copyCurrentDraft()">
            📋 मजकूर कॉपी करा / Copy Draft
          </button>
          <button class="btn-secondary" onclick="downloadDraft()">
            💾 फाइल डाउनलोड करा / Download
          </button>
        </div>
      </div>

      <div class="section-title">📎 तक्रारीसोबत जोडावयाची आवश्यक कागदपत्रे (Checklist):</div>
      <ul class="steps-list">
        ${checklist.map(item => `<li>☑️ ${item}</li>`).join('')}
      </ul>

      <div class="section-title" style="margin-top: 1.25rem;">📮 तक्रार कुठे सादर करावी (Verified Submission Channel):</div>
      <div style="background: #f8fafc; border: 1px solid var(--border-color); padding: 0.9rem; border-radius: 6px; font-size: 0.92rem;">
        <div><strong>अधिकृत मार्ग:</strong> ${channel.channel_mr || channel.channel_en}</div>
        <div style="margin-top: 0.35rem;"><strong>पद्धत:</strong> ${channel.mode}</div>
      </div>

      <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border-color); font-size: 0.8rem; color: var(--text-muted);">
        <strong>कायदेशीर सुरक्षितता:</strong> ${data.important_warning}
      </div>
    </div>
  `;
}

function switchDraftVersion(version) {
  const formalBox = document.getElementById('draft-box-formal');
  const shortBox = document.getElementById('draft-box-short');
  const enBox = document.getElementById('draft-box-en');
  
  formalBox.style.display = (version === 'formal') ? 'block' : 'none';
  shortBox.style.display = (version === 'short') ? 'block' : 'none';
  enBox.style.display = (version === 'en') ? 'block' : 'none';

  window.currentDraftTab = version;
}

function copyCurrentDraft() {
  const tab = window.currentDraftTab || 'formal';
  let textareaId = 'complaint-text-formal';
  if (tab === 'short') textareaId = 'complaint-text-short';
  if (tab === 'en') textareaId = 'complaint-text-en';

  const text = document.getElementById(textareaId).value;
  navigator.clipboard.writeText(text)
    .then(() => alert("मजकूर क्लिपबोर्डवर कॉपी झाला! / Draft copied successfully!"))
    .catch(() => alert("मजकूर कॉपी करता आला नाही."));
}

function downloadDraft() {
  const tab = window.currentDraftTab || 'formal';
  let textareaId = 'complaint-text-formal';
  if (tab === 'short') textareaId = 'complaint-text-short';
  if (tab === 'en') textareaId = 'complaint-text-en';

  const text = document.getElementById(textareaId).value;
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Nyaya_Sathi_Complaint_${new Date().toISOString().slice(0,10)}.txt`;
  a.click();
}
