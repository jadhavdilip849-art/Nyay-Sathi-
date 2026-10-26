/**
 * Nyaya Sathi - Interactive Hackathon Demonstration Runner
 * Executes DEMO A, DEMO B, and DEMO C with a single click.
 */

function runDemo(demoType) {
  fetch('/api/demo/scenarios')
    .then(res => res.json())
    .then(data => {
      const scenarios = data.scenarios;
      if (demoType === 'demo_a') {
        executeDemoA(scenarios.demo_a);
      } else if (demoType === 'demo_b') {
        executeDemoB(scenarios.demo_b);
      } else if (demoType === 'demo_c') {
        executeDemoC(scenarios.demo_c);
      }
    });
}

function executeDemoA(demoData) {
  // Switch to Rights / Talk tab
  window.switchTab('rights-tab');
  window.setLanguage('mr-IN');

  const inputEl = document.getElementById('chat-query-input');
  inputEl.value = demoData.user_speech_input;

  // Highlight status
  const micStatus = document.getElementById('mic-status');
  if (micStatus) micStatus.innerText = `🎙️ [DEMO A] वापरकर्ता बोलत आहे: "${demoData.user_speech_input}"`;

  // Submit query
  setTimeout(() => {
    submitQuery();

    // Auto-populate complaint draft with Demo A factual details
    setTimeout(() => {
      const f = demoData.facts;
      document.getElementById('comp-name').value = f.complainant_name;
      document.getElementById('comp-address').value = f.complainant_address;
      document.getElementById('comp-phone').value = f.complainant_phone;
      document.getElementById('comp-opp-name').value = f.opposite_party_name;
      document.getElementById('comp-opp-address').value = f.opposite_party_address;
      document.getElementById('comp-dates').value = f.dates_involved;
      document.getElementById('comp-facts').value = f.factual_summary;
      document.getElementById('comp-prior-action').value = f.prior_action_taken;
      document.getElementById('comp-relief').value = f.requested_relief;
      document.getElementById('comp-type').value = f.matter_type;
    }, 1200);
  }, 400);
}

function executeDemoB(demoData) {
  // Switch to Document Explainer tab
  window.switchTab('document-tab');
  window.setLanguage('mr-IN');

  const docInput = document.getElementById('doc-text-input');
  docInput.value = demoData.sample_doc.raw_text;

  const selectEl = document.getElementById('sample-doc-select');
  if (selectEl) selectEl.value = demoData.document_id;

  // Trigger analysis
  setTimeout(() => {
    analyzeDocument();
  }, 300);
}

function executeDemoC(demoData) {
  // Switch to Legal Aid tab
  window.switchTab('legalaid-tab');
  window.setLanguage('mr-IN');

  const check = demoData.eligibility_check;
  document.getElementById('aid-category').value = check.category;
  document.getElementById('aid-state').value = check.state;
  document.getElementById('aid-district').value = check.district;

  // Check eligibility and fetch district authority
  setTimeout(() => {
    checkEligibility();
    searchDistrictAuthority();
  }, 300);
}
