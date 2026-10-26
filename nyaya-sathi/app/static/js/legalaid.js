/**
 * Nyaya Sathi - Find Free Legal Help Module
 * Statutory Eligibility (Section 12) & Official DLSA / SLSA Directory
 */

function checkEligibility() {
  const category = document.getElementById('aid-category').value;
  const state = document.getElementById('aid-state').value;
  const incomeStr = document.getElementById('aid-income').value;
  const income = incomeStr ? parseFloat(incomeStr) : null;

  const resultContainer = document.getElementById('eligibility-result');
  resultContainer.innerHTML = '<p>पात्रता निकष तपासत आहे...</p>';

  fetch('/api/legalaid/eligibility', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      category: category,
      state: state,
      annual_income: income
    })
  })
  .then(res => res.json())
  .then(data => {
    const isEligible = data.is_eligible;
    const badgeClass = isEligible ? 'badge-official' : 'badge-emergency';
    const statusText = isEligible 
      ? '✓ आपण मोफत कायदेशीर सेवेसाठी पात्र आहात (Eligible for Free Legal Aid)'
      : '⚠️ नियमित उत्पन्न निकषानुसार थेट पात्र नाही (Check specific exemptions)';

    resultContainer.innerHTML = `
      <div style="background: ${isEligible ? '#f0fdf4' : '#fff7ed'}; border: 1px solid ${isEligible ? '#86efac' : '#fed7aa'}; border-radius: 8px; padding: 1.25rem; margin-top: 1rem;">
        <span class="${badgeClass}" style="margin-bottom: 0.5rem;">${statusText}</span>
        <div style="font-size: 1rem; margin-top: 0.5rem; font-weight: 600; color: var(--primary);">
          कायदेशीर तरतूद: ${data.act_name} - ${data.statutory_clause}
        </div>
        <p style="font-size: 0.95rem; margin-top: 0.35rem; color: #334155;">
          ${data.explanation}
        </p>

        <div style="margin-top: 1rem;">
          <strong>🎁 आपल्याला मोफत काय मिळणार (Entitlements):</strong>
          <ul style="padding-left: 1.2rem; margin-top: 0.35rem; font-size: 0.9rem;">
            ${(data.free_entitlements || []).map(e => `<li>${e}</li>`).join('')}
          </ul>
        </div>

        <div style="margin-top: 0.75rem;">
          <strong>📄 आवश्यक कागदपत्रे:</strong>
          <ul style="padding-left: 1.2rem; margin-top: 0.35rem; font-size: 0.9rem;">
            ${(data.documents_required || []).map(d => `<li>${d}</li>`).join('')}
          </ul>
        </div>

        <div style="margin-top: 0.75rem;">
          <strong>🚀 अर्ज कसा करावा:</strong>
          <ol style="padding-left: 1.2rem; margin-top: 0.35rem; font-size: 0.9rem;">
            ${(data.how_to_apply || []).map(h => `<li>${h}</li>`).join('')}
          </ol>
        </div>
      </div>
    `;
  })
  .catch(err => {
    resultContainer.innerHTML = `<p style="color: var(--danger);">तपासणीत त्रुटी: ${err.message}</p>`;
  });
}

function searchDistrictAuthority() {
  const state = document.getElementById('aid-state').value;
  const district = document.getElementById('aid-district').value;
  const resultContainer = document.getElementById('district-contact-result');

  resultContainer.innerHTML = '<p>अधिकृत संपर्क माहिती शोधत आहे...</p>';

  fetch(`/api/legalaid/directory?state=${encodeURIComponent(state)}&district=${encodeURIComponent(district)}`)
    .then(res => res.json())
    .then(data => {
      const national = data.national || {};
      const stateAuth = data.state_authority || {};
      const dlsa = data.district_authority || {};

      resultContainer.innerHTML = `
        <div style="display: grid; gap: 1rem; margin-top: 1rem;">
          <!-- DLSA Card -->
          <div style="background: #ffffff; border: 2px solid var(--accent); border-radius: 8px; padding: 1.25rem; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.8rem; font-weight: bold; color: var(--accent); text-transform: uppercase;">आपल्या जिल्ह्यातील अधिकृत कार्यालय</div>
            <h3 style="font-size: 1.15rem; color: var(--primary); margin: 0.25rem 0;">${dlsa.name || 'जिल्हा विधी सेवा प्राधिकरण (DLSA)'}</h3>
            <p style="font-size: 0.9rem; color: #475569; margin: 0.35rem 0;"><strong>पत्ता:</strong> ${dlsa.address || 'जिल्हा न्यायालय परिसर'}</p>
            <p style="font-size: 0.9rem; color: #475569;"><strong>दूरध्वनी:</strong> <span style="font-weight: bold; color: var(--primary);">${dlsa.phone || 'उपलब्ध नाही'}</span></p>
            ${dlsa.email ? `<p style="font-size: 0.9rem; color: #475569;"><strong>ईमेल:</strong> ${dlsa.email}</p>` : ''}
            ${dlsa.working_hours ? `<p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">कामकाजाची वेळ: ${dlsa.working_hours}</p>` : ''}
          </div>

          <!-- National Helpline Card -->
          <div style="background: #f8fafc; border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem;">
            <div style="font-weight: bold; color: var(--primary);">📞 राष्ट्रीय विधी सेवा टोल-फ्री हेल्पलाइन:</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: var(--accent); margin: 0.25rem 0;">१५१०० (15100)</div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">देशभरातून २४ तास मोफत उपलब्ध. थेट सरकारी विधी अधिकाऱ्यांशी संवाद.</p>
            <p style="font-size: 0.85rem; margin-top: 0.35rem;">
              <strong>अधिकृत राष्ट्रीय पोर्टल:</strong> <a href="${national.portal || 'https://nalsa.gov.in'}" target="_blank" class="citation-link">${national.portal || 'nalsa.gov.in'}</a>
            </p>
          </div>
        </div>
      `;
    })
    .catch(err => {
      resultContainer.innerHTML = `<p style="color: var(--danger);">माहिती मिळवण्यात अडचण: ${err.message}</p>`;
    });
}
