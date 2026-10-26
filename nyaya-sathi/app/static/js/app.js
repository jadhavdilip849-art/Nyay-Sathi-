/**
 * Nyaya Sathi - Core Application Orchestrator
 * Manages tabs, multilingual strings, and accessibility preferences.
 */

window.currentLang = 'mr-IN'; // Default to Marathi per prompt guidance (Marathi + Hindi first)
window.currentFontSize = 16;

const UI_TRANSLATIONS = {
  "mr-IN": {
    "tagline": "आपले हक्क जाणून घ्या. कायदा समजून घ्या. पुढचे पाऊल उचला.",
    "tab_rights": "⚖️ हक्क जाणून घ्या",
    "tab_document": "📄 कागदपत्र स्पष्टीकरण",
    "tab_complaint": "✍️ तक्रार मसुदा",
    "tab_legalaid": "🏛️ मोफत विधी सेवा",
    "tab_demos": "🚀 थेट प्रात्यक्षिक (Demos)",
    "hero_title": "आपल्या हक्कांचे संरक्षण, आपल्या मातृभाषेत",
    "hero_sub": "कोणत्याही गुंतागुंतीच्या कायदेशीर शब्दांशिवाय आपले हक्क, सरकारी योजना आणि मोफत कायदेशीर मदत मिळवा.",
    "input_placeholder": "उदा. माझ्या मालकाने दोन महिने पगार दिला नाही, मी काय करू?",
    "btn_ask": "विचारा / शोध घ्या",
    "categories_title": "प्रमुख कायदेशीर समस्या निवडा:"
  },
  "hi-IN": {
    "tagline": "अपने अधिकार जानें। कानून को समझें। अगला कदम उठाएं।",
    "tab_rights": "⚖️ अधिकार समझें",
    "tab_document": "📄 दस्तावेज स्पष्टीकरण",
    "tab_complaint": "✍️ शिकायत प्रारूप",
    "tab_legalaid": "🏛️ मुफ्त विधिक सहायता",
    "tab_demos": "🚀 लाइव डेमो (Demos)",
    "hero_title": "अपने अधिकारों की सुरक्षा, अपनी भाषा में",
    "hero_sub": "बिना किसी कानूनी जटिलता के अपने अधिकार, सरकारी शिकायत तंत्र और मुफ्त कानूनी मदद प्राप्त करें।",
    "input_placeholder": "उदा. मेरे नियोक्ता ने दो महीने से वेतन नहीं दिया है, मैं क्या करूँ?",
    "btn_ask": "पूछें / खोजें",
    "categories_title": "प्रमुख कानूनी श्रेणियां चुनें:"
  },
  "en-IN": {
    "tagline": "Know Your Rights. Understand the Law. Take the Next Step.",
    "tab_rights": "⚖️ Understand My Rights",
    "tab_document": "📄 Explain My Document",
    "tab_complaint": "✍️ Write a Complaint",
    "tab_legalaid": "🏛️ Find Legal Help",
    "tab_demos": "🚀 Live Demos",
    "hero_title": "Know Your Rights in Your Language",
    "hero_sub": "Get plain-language legal clarity, factual complaint drafting, and verified legal aid without technical legal jargon.",
    "input_placeholder": "e.g. My employer has not paid my wages for two months, what can I do?",
    "btn_ask": "Ask Nyaya Sathi",
    "categories_title": "Select a Legal Category:"
  }
};

function switchTab(tabId) {
  // Update nav tabs
  document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.classList.remove('active');
  });
  const activeTabBtn = document.querySelector(`[data-tab="${tabId}"]`);
  if (activeTabBtn) activeTabBtn.classList.add('active');

  // Update tab content
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.remove('active');
  });
  const targetContent = document.getElementById(tabId);
  if (targetContent) targetContent.classList.add('active');

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function setLanguage(langCode) {
  window.currentLang = langCode;
  const select = document.getElementById('language-select');
  if (select) select.value = langCode;

  if (window.voiceAssistant) {
    window.voiceAssistant.setLanguage(langCode);
  }

  // Update UI strings
  const t = UI_TRANSLATIONS[langCode] || UI_TRANSLATIONS["en-IN"];
  const elTagline = document.getElementById('ui-tagline');
  if (elTagline) elTagline.innerText = t.tagline;

  const elHeroTitle = document.getElementById('ui-hero-title');
  if (elHeroTitle) elHeroTitle.innerText = t.hero_title;

  const elHeroSub = document.getElementById('ui-hero-sub');
  if (elHeroSub) elHeroSub.innerText = t.hero_sub;

  const elInput = document.getElementById('chat-query-input');
  if (elInput) elInput.placeholder = t.input_placeholder;

  const elBtnAsk = document.getElementById('ui-btn-ask');
  if (elBtnAsk) elBtnAsk.innerText = t.btn_ask;

  const elCatTitle = document.getElementById('ui-categories-title');
  if (elCatTitle) elCatTitle.innerText = t.categories_title;

  // Refresh categories in new language
  if (typeof loadCategories === 'function') {
    loadCategories();
  }
}

function toggleContrast() {
  document.body.classList.toggle('high-contrast');
}

function adjustFontSize(delta) {
  window.currentFontSize = Math.min(22, Math.max(13, window.currentFontSize + delta));
  document.documentElement.style.setProperty('--font-base-size', `${window.currentFontSize}px`);
}

document.addEventListener('DOMContentLoaded', () => {
  // Setup tabs
  document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-tab');
      switchTab(target);
    });
  });

  // Setup language selector
  const langSelect = document.getElementById('language-select');
  if (langSelect) {
    langSelect.addEventListener('change', (e) => {
      setLanguage(e.target.value);
    });
  }

  // Setup mic button
  const micBtn = document.getElementById('mic-btn');
  if (micBtn && window.voiceAssistant) {
    micBtn.addEventListener('click', () => {
      window.voiceAssistant.toggleRecording();
    });
  }

  // Setup enter key on query input
  const queryInput = document.getElementById('chat-query-input');
  if (queryInput) {
    queryInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        submitQuery();
      }
    });
  }

  // Initial loads
  setLanguage(window.currentLang);
  if (typeof loadSampleNotices === 'function') {
    loadSampleNotices();
  }
});

window.switchTab = switchTab;
window.setLanguage = setLanguage;
