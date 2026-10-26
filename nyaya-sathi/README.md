# Nyaya Sathi (न्याय साथी)

### *"Know Your Rights. Understand the Law. Take the Next Step."*
### *"आपले हक्क जाणून घ्या. कायदा समजून घ्या. पुढचे पाऊल उचला."*

Nyaya Sathi is an AI-powered, multilingual legal information and assistance platform built for ordinary citizens in India. It enables rural workers, women, tenants, senior citizens, farmers, and first-time smartphone users to articulate their grievances in their own mother tongue (starting with Marathi and Hindi), understand relevant legal protections in plain language, discover official legal aid, and draft factual complaints without encountering impenetrable legal jargon.

---

## 🏛️ Core Features

1. **Multilingual Voice Assistant (`Talk to Nyaya Sathi`)**
   - Natural speech interaction in **Marathi (मराठी)**, **Hindi (हिन्दी)**, and **English (India)**.
   - Dual-engine speech architecture: Real **Sarvam AI APIs** (`Saaras:v4` STT, `Bulbul:v1` TTS, `Mayura` Translation) with automatic, resilient fallback to **Browser Web Speech API** and local linguistic engines.
   - Live transcription confirmation, editable query input, and clear audio playback.

2. **Understand My Rights (`हक्क जाणून घ्या`)**
   - Retrieval-Augmented Generation (RAG) backed by verified statutory frameworks across 10+ civic categories:
     - Unpaid wages & employment disputes
     - Consumer protection & defective goods
     - Online financial cybercrime & UPI frauds (1930 Helpline)
     - Tenancy & security deposit disputes
     - Domestic violence & women's protections (PWDVA, Sakhi 181)
     - Senior citizen maintenance & property rights (14567 Helpline)
     - Disability rights (RPwD Act)
     - Denial of ration & government benefits (CPGRAMS / NFSA)
     - Land boundary and agricultural pathway disputes
   - Distinguishes **what the user stated**, **what remains unknown**, **what the statute establishes**, and **what uncertain factors exist**.

3. **Explain My Document (`कागदपत्र स्पष्टीकरण`)**
   - Parses official notices, municipal demolition warnings (Section 351), employment withholding memorandums, and tenancy eviction notices.
   - **Strictly distinguishes explicit printed deadlines** from **legally inferred rules** (e.g. date of registered post delivery).
   - Plain-language legal glossary: decodes *Show Cause*, *Ex-Parte*, *Without Prejudice*, *Mesne Profits*, *Inter-alia*, etc.
   - Prepares specific questions for users to ask a Legal Aid or DLSA advocate.

4. **Help Me Write a Complaint (`तक्रार मसुदा`)**
   - Interactive guided interview collecting only factual essentials (dates, facts, prior action, relief requested).
   - Generates three ready-to-use formats:
     1. **Formal Representation Letter** (for registered post with A.D. or in-person submission).
     2. **Short Online Form Version** (under 500 characters, formatted for CPGRAMS or Samadhan).
     3. **English Translation**.
   - Generates a verified supporting evidence checklist and official submission channel details.
   - **Anti-fabrication safeguard**: Never hallucinates penal sections, allegations, or fake dates.

5. **Find Free Legal Help (`मोफत विधी सेवा`)**
   - Statutory eligibility calculator under **Section 12 of the Legal Services Authorities Act, 1987**:
     - Women and children (automatic Sec 12(c))
     - Industrial workmen (Sec 12(e))
     - SC / ST community members (Sec 12(a))
     - Persons with disabilities (Sec 12(d))
     - Annual income thresholds by state (e.g. Rs. 3,00,000 for Maharashtra)
   - Official verified contact directory for **NALSA (Helpline 15100)**, **MSLSA (Mumbai)**, and **DLSAs** (Pune, Mumbai Suburban, Nagpur, Delhi Central, etc.).

6. **Legal Safety, Ethics & Emergency Escalations**
   - Clear identification as an AI information tool (not a lawyer or court).
   - Real-time emergency detection: keywords trigger immediate hotlines for **112 (National Emergency)**, **181 (Women in Distress)**, and **1930 (Financial Cyber Fraud)**.
   - Privacy shield: detects and warns against entering Aadhaar numbers, OTPs, or passwords.

---

## 🏗️ Architecture & Project Structure

```
nyaya-sathi/
├── app/
│   ├── __init__.py
│   ├── server.py              # Multi-threaded HTTP REST and Static Server (Python 3.12 stdlib)
│   ├── config.py              # Environment variables, Sarvam models, and legal disclaimers
│   ├── legal_kb/              # Verified Authoritative Legal Knowledge Base & RAG Index
│   │   ├── rag_engine.py      # Keyword and metadata retrieval engine
│   │   └── sources_catalog.py # Indiacode.nic.in, NALSA, Samadhan, NCH 1915 metadata
│   ├── legal_aid/             # Legal Services Authorities Directory & Section 12 Engine
│   │   └── legal_aid_service.py # Statutory qualification and DLSA contact locator
│   ├── authorities/           # Authority & Grievance Routing Engine
│   │   └── authority_service.py # Recommends Labour Commissioner, e-Daakhil, I4C 1930, etc.
│   ├── complaints/            # Factual Complaint Drafting Module
│   │   └── complaint_generator.py # Generates formal, short, and English representations
│   ├── document_explainer/    # Notice & Legal Document Explainer
│   │   ├── doc_analyzer.py    # Deadline extraction, glossary decoding, and lawyer questions
│   │   └── sample_notices.py  # Realistic municipal show cause, wage withholding, & eviction notices
│   ├── voice/                 # Voice & Sarvam AI Integration Layer
│   │   └── sarvam_client.py   # Sarvam Saaras STT, Bulbul TTS, Mayura Translate + Fallbacks
│   ├── guardrails/            # Legal Safety & Ethics Safeguards
│   │   └── safety_checker.py  # Emergency triggers (112/181/1930), Aadhaar leak warnings
│   └── static/                # Mobile-First Civic Web Interface
│       ├── index.html         # Accessible Single Page Application
│       ├── css/style.css      # High-contrast mode, accessible typography, mobile layout
│       └── js/
│           ├── app.js         # Tab switching and multilingual dictionary
│           ├── voice_assistant.js # Mic controls and Web Speech synthesis
│           ├── rights.js      # Understand My Rights UI
│           ├── document.js    # Document Explainer UI
│           ├── complaint.js   # Complaint Drafting Wizard
│           ├── legalaid.js    # Legal Aid & Section 12 UI
│           └── demos.js       # 1-Click Interactive Hackathon Scenarios
├── tests/
│   ├── test_rag_engine.py     # Tests for legal retrieval and Marathi/Hindi queries
│   ├── test_legal_aid.py      # Tests for Section 12 criteria and DLSA directory
│   ├── test_complaint.py      # Tests for factual complaints without hallucinations
│   ├── test_doc_explainer.py  # Tests for explicit dates vs inferred deadlines
│   ├── test_guardrails.py     # Tests for emergency triggers and Aadhaar alerts
│   ├── test_sarvam_client.py  # Tests for Sarvam client fallback behavior
│   ├── test_mock_server_handlers.py # In-memory HTTP REST and static serving tests
│   └── run_all_tests.py       # Master test runner (100% passing)
├── run.py                     # Web application entry point
├── run_demos.py               # Automated console demo runner (Demos A, B, and C)
├── .env.example               # Configuration template
├── requirements.txt           # Listed dependencies
└── README.md                  # Complete documentation
```

---

## ⚡ Zero-Dependency Execution

The core runtime is built using the **Python 3.12 Standard Library** (`http.server.ThreadingHTTPServer`, `urllib`, `json`, `sqlite3`, `unittest`).
**It requires 0 external pip packages to run or test.**

---

## 🚀 Installation & Running

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari on desktop or Android/iOS).

### 2. Run the Application
Open a terminal in the project directory and run:

```bash
# Start the Nyaya Sathi server on http://127.0.0.1:8080
python run.py
```

To bind to a specific host or port:
```bash
python run.py --host 0.0.0.0 --port 8080
```

Open your browser and navigate to:
```
http://127.0.0.1:8080
```

---

## 🧪 Running the Test Suite

Execute the unified test runner:
```bash
python tests/run_all_tests.py
```

### Test Results:
```
Total Tests Run: 29
Errors: 0, Failures: 0
ALL NYAYA SATHI CORE TESTS PASSED SUCCESSFULLY! (100%)
```

---

## 🎬 3 Hackathon Demonstrations

Nyaya Sathi includes a dedicated **"🚀 थेट प्रात्यक्षिक (Live Demos)"** tab in the web UI, as well as an automated command-line runner:

```bash
python run_demos.py
```

### DEMO A: Unpaid Wages in Marathi (रुपेश पाटील, भोसरी MIDC)
- **Input**: *"मी गेल्या दोन महिन्यांपासून एका कारखान्यात काम करत आहे, पण मालकाने अजूनही माझा पगार दिलेला नाही. मी काय करू शकतो?"*
- **Assistant Output**: Identifies Payment of Wages Act & Code on Wages, details the Office of Labour Commissioner & Samadhan Portal, asks 4 clarifying questions, and drafts a formal representation letter and a short 500-character portal submission.

### DEMO B: Understanding a Municipal Notice (कलम ३५१ कारणे दाखवा नोटीस)
- **Input**: Show Cause Notice from Municipal Corporation alleging unauthorized shed construction.
- **Assistant Output**: Detects explicit 15-day deadline (until 30/10/2026), decodes *Show Cause* and *Ex-Parte*, lists 3 strategic questions to ask a DLSA advocate, and emphasizes postal delivery date rules.

### DEMO C: Finding Free Legal Aid under Section 12 (सुनीता कांबळे, पुणे)
- **Input**: Woman resident of Pune seeking court assistance.
- **Assistant Output**: Verifies statutory qualification under Section 12(c) (automatic entitlement for women), explains free lawyer and court fee waiver entitlements, and provides verified address & phone number for the **Pune DLSA at Shivajinagar District Court** and NALSA Helpline **15100**.

---

## 🛡️ Authoritative Legal Sources Catalog

Every substantive legal explanation references verified official portals:
1. **India Code (Official Legislation)**: [indiacode.nic.in](https://www.indiacode.nic.in)
2. **National Legal Services Authority (NALSA)**: [nalsa.gov.in](https://nalsa.gov.in) (Toll-free: `15100`)
3. **Ministry of Labour & Employment (Samadhan Portal)**: [samadhan.labour.gov.in](https://samadhan.labour.gov.in)
4. **National Consumer Helpline (NCH)**: [consumerhelpline.gov.in](https://consumerhelpline.gov.in) (Toll-free: `1915`)
5. **e-Daakhil Consumer Court Filing**: [edaakhil.nic.in](https://edaakhil.nic.in)
6. **National Cyber Crime Reporting Portal**: [cybercrime.gov.in](https://cybercrime.gov.in) (Helpline: `1930`)
7. **Sakhi One Stop Centre & Women Helpline**: [wcd.nic.in](https://wcd.nic.in) (Helpline: `181`)
8. **National Emergency Response Support System**: Helpline `112`

---

## 🔒 Known Limitations & Production Roadmap

1. **OCR on Scanned Handwritten Notices**: Prototype currently performs reliable text parsing and rule extraction on typed notices and sample public documents. Handwritten regional script OCR requires integrating specialized document intelligence pipelines.
2. **Direct Court Filing Integration**: For ethical and legal reasons, Nyaya Sathi does not auto-submit complaints to courts without human review and official authorization; it prepares the verified representation for citizen review.
3. **Language Expansion**: Currently fully implemented for Marathi, Hindi, and English; designed modularly so Tamil, Telugu, Bengali, and Gujarati can be added by declaring domain vocabulary dictionaries.

---
*Nyaya Sathi Prototype — Built for civic-tech empowerment and access to justice in India.*
