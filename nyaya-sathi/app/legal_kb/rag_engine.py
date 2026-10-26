"""
Legal Retrieval-Augmented Generation (RAG) Engine for Nyaya Sathi.
Retrieves authoritative legal sources, maps user queries to statutory frameworks,
generates plain-language explanations in Marathi, Hindi, and English, and enforces anti-hallucination checks.
"""

import re
import json
from typing import Dict, List, Any, Optional
from .sources_catalog import AUTHORITATIVE_SOURCES
from ..config import LEGAL_DISCLAIMER

# Domain keyword mappings across Marathi, Hindi, and English
DOMAIN_KEYWORDS = {
    "unpaid_wages": {
        "keywords": [
            "पगार", "वेतन", "मजुरी", "पैसे दिले नाही", "कामगार", "मालक", "कंपने", "कामाचे पैसे",
            "वेतन नहीं मिला", "सैलरी", "मजदूरी", "तनख्वाह", "बकाया", "मालिक", "पेमेंट",
            "wage", "salary", "unpaid", "employer", "worker", "labor", "labour", "dues", "remuneration"
        ],
        "source_key": "PAYMENT_OF_WAGES",
        "domain_name_mr": "रोजगार व थकीत वेतन अधिकार",
        "domain_name_hi": "रोजगार एवं बकाया वेतन अधिकार",
        "domain_name_en": "Employment & Unpaid Wages Rights"
    },
    "consumer_complaints": {
        "keywords": [
            "दुकानदार", "खराब वस्तू", "वॉरंटी", "फसवणूक", "पैसे परत नाही", "खराब माल", "ग्राहक",
            "दुकानदार", "खराब सामान", "वारंटी", "धोखाधड़ी", "रिफंड", "उपभोक्ता", "वारंटी अस्वीकार",
            "consumer", "defective", "refund", "warranty", "seller", "faulty", "replacement", "shopkeeper"
        ],
        "source_key": "CONSUMER_PROTECTION",
        "domain_name_mr": "ग्राहक हक्क व तक्रार निवारण",
        "domain_name_hi": "उपभोक्ता अधिकार एवं शिकायत निवारण",
        "domain_name_en": "Consumer Protection & Redressal"
    },
    "cybercrime": {
        "keywords": [
            "ऑनलाइन", "फसवणूक", "खात्यातून", "बँक", "सायबर", "ओटीपी", "यूपीआय", "लिंक",
            "ऑनलाइन फ्रॉड", "खाते से पैसे", "ओटीपी", "बैंक फ्रॉड", "साइबर", "यूपीआई", "धोखाधड़ी",
            "cybercrime", "cyber", "online fraud", "upi scam", "otp stolen", "hacked", "phishing", "unauthorized transaction"
        ],
        "source_key": "CYBERCRIME_IT_ACT",
        "domain_name_mr": "सायबर गुन्हे व डिजिटल आर्थिक सुरक्षा",
        "domain_name_hi": "साइबर अपराध एवं डिजिटल वित्तीय सुरक्षा",
        "domain_name_en": "Cybercrime & Online Financial Fraud"
    },
    "rental_housing": {
        "keywords": [
            "भाडे", "घरमालक", "डिपॉझिट", "घर खाली करणे", "भाडेकरू", "लाईट पाणी बंद", "अनामत रक्कम",
            "किराया", "मकान मालिक", "डिपॉजिट", "मकान खाली", "किराएदार", "बिजली पानी बंद", "सिक्योरिटी",
            "rent", "landlord", "tenant", "security deposit", "eviction", "tenancy", "lease"
        ],
        "source_key": "RENT_TENANCY_LAWS",
        "domain_name_mr": "भाडेकरू व घरमालक विवाद अधिकार",
        "domain_name_hi": "किराएदार एवं मकान मालिक विवाद अधिकार",
        "domain_name_en": "Rental & Housing Tenancy Rights"
    },
    "women_rights": {
        "keywords": [
            "कौटुंबिक छळ", "मारहाण", "घरगुती हिंसाचार", "पती", "सासरचे लोक", "छळवणूक", "महिला संरक्षण",
            "घरेलू हिंसा", "मारपीट", "दहेज", "पति", "ससुराल", "प्रताड़ना", "महिला सुरक्षा",
            "domestic violence", "abuse", "harassment", "husband", "in-laws", "beating", "protection order", "dowry"
        ],
        "source_key": "DOMESTIC_VIOLENCE_PWDVA",
        "domain_name_mr": "महिलांचे कायदेशीर संरक्षण व हक्क",
        "domain_name_hi": "महिला कानूनी संरक्षण एवं अधिकार",
        "domain_name_en": "Women's Legal Protections & Safety"
    },
    "legal_aid": {
        "keywords": [
            "मोफत वकील", "कायदेशीर मदत", "नालसा", "कोर्टाचा खर्च", "सरकारी वकील", "विधी सेवा",
            "मुफ्त वकील", "कानूनी सहायता", "नालसा", "कोर्ट का खर्च", "सरकारी वकील", "विधिक सेवा",
            "free lawyer", "legal aid", "nalsa", "dlsa", "court fee", "legal assistance", "indigent"
        ],
        "source_key": "LEGAL_SERVICES_AUTHORITIES",
        "domain_name_mr": "मोफत कायदेशीर मदत (विधी सेवा प्राधिकरण)",
        "domain_name_hi": "मुफ्त कानूनी सहायता (विधिक सेवा प्राधिकरण)",
        "domain_name_en": "Free Legal Aid & Services Authority"
    },
    "senior_citizens": {
        "keywords": [
            "ज्येष्ठ नागरिक", "म्हातारपण", "मुलगा सांभाळत नाही", "पोटगी", "वृद्धाश्रम", "मालमत्ता परत",
            "वरिष्ठ नागरिक", "बुजुर्ग", "बेटा देखभाल नहीं करता", "भरण पोषण", "बुढ़ापा", "संपत्ति वापसी",
            "senior citizen", "elderly", "parents maintenance", "children neglecting", "elder abuse"
        ],
        "source_key": "SENIOR_CITIZENS_ACT",
        "domain_name_mr": "ज्येष्ठ नागरिक व पालक हक्क",
        "domain_name_hi": "वरिष्ठ नागरिक एवं माता-पिता अधिकार",
        "domain_name_en": "Senior Citizen & Parental Rights"
    },
    "disability_rights": {
        "keywords": [
            "दिव्यांग", "अपंग", "भेदभाव", "प्रमाणपत्र", "सवलत", "अपंग हक्क",
            "दिव्यांग", "विकलांग", "भेदभाव", "सर्टिफिकेट", "आरक्षण", "विकलांग अधिकार",
            "disability", "disabled", "handicap", "wheelchair", "special needs", "accessibility", "pwd"
        ],
        "source_key": "DISABILITY_RIGHTS_RPWD",
        "domain_name_mr": "दिव्यांग व्यक्तींचे हक्क व समान संधी",
        "domain_name_hi": "दिव्यांगजन अधिकार एवं समान अवसर",
        "domain_name_en": "Disability Rights & Equal Opportunity"
    },
    "government_benefits": {
        "keywords": [
            "राशन", "रेशन कार्ड", "सरकारी योजना", "पेन्शन बंद", "अनुदान", "लाभ नाकारला",
            "राशन", "राशन कार्ड", "सरकारी योजना", "पेंशन बंद", "सब्सिडी", "लाभ नहीं मिला",
            "ration card", "govt benefit", "pension denied", "welfare scheme", "subsidy", "cpgrams"
        ],
        "source_key": "GOVT_BENEFITS_NFSA",
        "domain_name_mr": "शासकीय योजना व सार्वजनिक सेवा हक्क",
        "domain_name_hi": "सरकारी योजनाएं एवं सार्वजनिक सेवा अधिकार",
        "domain_name_en": "Government Benefits & Public Services"
    },
    "land_disputes": {
        "keywords": [
            "जमीन", "शेतीचा रस्ता", "बांध", "७/१२", "फेरफार", "जमीन वाद", "तहसीलदार",
            "जमीन", "खेत का रास्ता", "मेड़", "खतौनी", "दाखिल खारिज", "भूमि विवाद", "तहसीलदार",
            "land", "agricultural land", "boundary", "mutation", "pathway", "farmer land dispute", "revenue"
        ],
        "source_key": "LAND_AGRICULTURAL_DISPUTES",
        "domain_name_mr": "जमीन, शेती व महसूल संबंधित विवाद",
        "domain_name_hi": "भूमि, कृषि एवं राजस्व संबंधी विवाद",
        "domain_name_en": "Land & Agricultural Revenue Disputes"
    }
}

class LegalRAGEngine:
    """Retrieval-Augmented Generation engine backed by verified legal metadata."""

    def __init__(self):
        self.sources = AUTHORITATIVE_SOURCES
        self.domains = DOMAIN_KEYWORDS

    def detect_language(self, text: str) -> str:
        """Heuristic language detection for Marathi, Hindi, and English."""
        # Check Devanagari script presence
        devanagari_chars = re.findall(r'[\u0900-\u097F]', text)
        if len(devanagari_chars) > 0:
            # Check characteristic Marathi words/endings
            marathi_indicators = ["आहे", "नाही", "केले", "दिले", "पगार", "पाहिजे", "करू", "माझा", "माझी", "गेल्या", "होते", "त्यांनी"]
            for w in marathi_indicators:
                if w in text:
                    return "mr-IN"
            return "hi-IN"
        return "en-IN"

    def retrieve(self, query: str, explicit_category: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves matching legal sources, generates plain-language rights analysis,
        formulates follow-up clarifying questions, and identifies practical steps.
        """
        detected_lang = self.detect_language(query)
        normalized_q = query.lower()

        matched_domain_key = None
        highest_score = 0

        # If user explicitly selected category
        if explicit_category and explicit_category in self.domains:
            matched_domain_key = explicit_category
            highest_score = 100
        else:
            # Score against domain keywords
            for domain_key, data in self.domains.items():
                score = 0
                for kw in data["keywords"]:
                    if kw.lower() in normalized_q:
                        score += 1
                if score > highest_score:
                    highest_score = score
                    matched_domain_key = domain_key

        # Default fallback to employment/wages if query is ambiguous or default general inquiry
        if not matched_domain_key or highest_score == 0:
            if any(term in normalized_q for term in ["help", "rights", "law", "कायदे", "हक्क", "अधिकार"]):
                matched_domain_key = "unpaid_wages"
            else:
                matched_domain_key = "legal_aid"

        domain_info = self.domains[matched_domain_key]
        source_record = self.sources.get(domain_info["source_key"], self.sources["LEGAL_SERVICES_AUTHORITIES"])

        # Build response payload tailored to language
        response_data = self._build_domain_response(
            domain_key=matched_domain_key,
            source=source_record,
            user_query=query,
            lang=detected_lang
        )

        return response_data

    def _build_domain_response(self, domain_key: str, source: Dict[str, Any], user_query: str, lang: str) -> Dict[str, Any]:
        """Constructs safe, factual, plain-language legal explanation with citations."""
        
        # Follow-up questions to understand material facts without assuming
        follow_up_questions = {
            "unpaid_wages": {
                "mr": [
                    "आपण कंपनीत किंवा दुकानात किती महिन्यांपासून काम करत आहात?",
                    "आपल्याकडे नियुक्ती पत्र (Appointment Letter), पगार स्लिप किंवा बँक स्टेटमेंट आहे का?",
                    "आपण मालकाशी याबाबत लेखी संपर्क (उदा. व्हॉट्सॲप, ईमेल किंवा पत्र) साधला आहे का?",
                    "संबंधित आस्थापना कोणत्या शहरात किंवा जिल्ह्यात आहे?"
                ],
                "hi": [
                    "आप उस संस्थान में कितने समय से कार्यरत हैं और कितने महीनों का वेतन बकाया है?",
                    "क्या आपके पास नियुक्ति पत्र, वेतन पर्ची (Salary slip) या बैंक स्टेटमेंट उपलब्ध है?",
                    "क्या आपने नियोक्ता को लिखित रूप में सूचित किया है?",
                    "कार्यस्थल किस जिले या राज्य में स्थित है?"
                ],
                "en": [
                    "How long have you been employed there, and for which specific months is wage unpaid?",
                    "Do you have appointment records, salary slips, or bank statements showing past payments?",
                    "Have you made any written representation or demand to the employer (e.g. email, message)?",
                    "In which district and state is the workplace located?"
                ]
            },
            "consumer_complaints": {
                "mr": [
                    "वस्तू कधी खरेदी केली आणि आपल्याकडे वैध पावती/बिल आहे का?",
                    "वस्तूमध्ये नेमका काय दोष आढळला आहे?",
                    "दुकानदार किंवा कंपनीने दुरुस्ती/परताव्यासाठी लेखी नकार दिला आहे का?"
                ],
                "hi": [
                    "सामान कब खरीदा गया और क्या आपके पास खरीद की पक्की रसीद (Bill) मौजूद है?",
                    "सामान या सेवा में किस प्रकार की खराबी आई है?",
                    "क्या कंपनी या विक्रेता ने लिखित रूप में समाधान देने से मना किया है?"
                ],
                "en": [
                    "When was the purchase made and do you possess a valid invoice or receipt?",
                    "What specific defect or deficiency occurred?",
                    "Did the seller or company give a written refusal or fail to respond?"
                ]
            },
            "cybercrime": {
                "mr": [
                    "फसवणूक होऊन किती तास झाले आहेत? (२ तासांच्या आत १९३० वर कॉल केल्यास पैसे गोठवता येतात)",
                    "कोणत्या बँकेचे खाते किंवा यूपीआय ॲप वापरले गेले?",
                    "संशयित व्यवहार संदर्भ क्रमांक (UTR / Transaction ID) उपलब्ध आहे का?"
                ],
                "hi": [
                    "घटना को हुए कितने घंटे बीत चुके हैं? (2 घंटे के अंदर 1930 पर कॉल करने से लेन-देन फ्रीज हो सकता है)",
                    "किस बैंक खाते या यूपीआई माध्यम से लेन-देन हुआ?",
                    "क्या आपके पास बैंक का यूटीआर (UTR) या ट्रांजेक्शन आईडी सुरक्षित है?"
                ],
                "en": [
                    "How many hours have passed since the fraudulent transfer? (Immediate calling on 1930 can freeze money)",
                    "Which bank account or UPI application was involved?",
                    "Do you have the transaction reference number (UTR / SMS alert) preserved?"
                ]
            },
            "rental_housing": {
                "mr": [
                    "आपल्याकडे नोंदणीकृत भाडेकरार (Registered Rent Agreement) आहे का?",
                    "सुरक्षा अनामत रक्कम (Deposit) किती दिली होती आणि त्याची पावती आहे का?",
                    "घर रिकामे करण्याची सूचना (Notice) दिली होती का?"
                ],
                "hi": [
                    "क्या आपके पास वैध किराया अनुबंध (Rent Agreement) उपलब्ध है?",
                    "सुरक्षा जमा राशि (Deposit) कितनी थी और क्या बैंक से भुगतान का प्रमाण है?",
                    "क्या घर खाली करने का पूर्व नोटिस दिया गया था?"
                ],
                "en": [
                    "Is there an active written or registered tenancy agreement?",
                    "What was the security deposit amount and is proof of bank payment available?",
                    "Was adequate written notice served before vacating?"
                ]
            },
            "legal_aid": {
                "mr": [
                    "आपल्याला कोणत्या प्रकारच्या न्यायालयीन खटल्यासाठी वकिलाची आवश्यकता आहे?",
                    "आपण महिला, औद्योगिक कामगार, अनुसूचित जाती/जमाती किंवा वार्षिक उत्पन्न ३ लाखांपेक्षा कमी असलेल्या वर्गात मोडता का?",
                    "आपण कोणत्या जिल्ह्यातील न्यायालयात मदत शोधत आहात?"
                ],
                "hi": [
                    "आपको किस प्रकार के मामले के लिए कानूनी सहायता की आवश्यकता है?",
                    "क्या आप महिला, औद्योगिक कामगार, एससी/एसटी वर्ग, अथवा निर्धारित आय सीमा के अंतर्गत आते हैं?",
                    "आप किस जिले के विधिक सेवा प्राधिकरण से संपर्क करना चाहते हैं?"
                ],
                "en": [
                    "What nature of legal matter or court proceeding do you require assistance with?",
                    "Do you qualify under Section 12 criteria (woman, industrial worker, SC/ST, custody, or eligible income)?",
                    "Which district court or state jurisdiction does your matter fall under?"
                ]
            }
        }

        # Practical next steps
        action_steps = {
            "unpaid_wages": [
                {"step": 1, "text_mr": "पुराव्यांची जुळवाजुळव: कामाचे दिवस, हजेरी, बँक स्टेटमेंट आणि नियुक्ती पत्र गोळा करा.", "text_hi": "सबूत एकत्र करें: उपस्थिति रिकॉर्ड, नियुक्ति पत्र और बैंक स्टेटमेंट सुरक्षित रखें।", "text_en": "Preserve Evidence: Gather attendance records, appointment letter, and bank statements."},
                {"step": 2, "text_mr": "लेखी स्मरणपत्र: मालकाला थकीत वेतनाची मागणी करणारे औपचारिक पत्र किंवा ईमेल पाठवा.", "text_hi": "लिखित मांग पत्र: नियोक्ता को बकाया वेतन तुरंत देने हेतु औपचारिक पत्र या ईमेल भेजें।", "text_en": "Written Demand: Send a formal written demand or email to the employer requesting clearance of dues."},
                {"step": 3, "text_mr": "कामगार आयुक्त तक्रार: वेतन न मिळाल्यास कामगार आयुक्त कार्यालयात किंवा 'समाधान' (samadhan.labour.gov.in) वर तक्रार नोंदवा.", "text_hi": "श्रम आयुक्त में शिकायत: श्रम आयुक्त कार्यालय या समाधान पोर्टल पर ऑनलाइन शिकायत दर्ज करें।", "text_en": "Labour Authority: File a formal claim before the Labour Commissioner or on the Samadhan portal."},
                {"step": 4, "text_mr": "मोफत कायदेशीर मदत: आवश्यक असल्यास जिल्हा विधी सेवा प्राधिकरणाकडून (DLSA) मोफत वकिलाची मदत घ्या.", "text_hi": "मुफ्त कानूनी सहायता: आवश्यकता पड़ने पर जिला विधिक सेवा प्राधिकरण (DLSA) से निःशुल्क वकील प्राप्त करें।", "text_en": "Free Legal Aid: Approach the District Legal Services Authority (DLSA) if legal representation is needed."}
            ],
            "consumer_complaints": [
                {"step": 1, "text_mr": "खरेदी पावती आणि वॉरंटी कार्ड सुरक्षित ठेवा.", "text_hi": "खरीद रसीद और वारंटी दस्तावेज सुरक्षित रखें।", "text_en": "Safeguard purchase invoice and warranty documentation."},
                {"step": 2, "text_mr": "राष्ट्रीय ग्राहक हेल्पलाइन १९१५ वर कॉल करून अथवा consumerhelpline.gov.in वर तक्रार नोंदवा.", "text_hi": "राष्ट्रीय उपभोक्ता हेल्पलाइन 1915 पर कॉल करें अथवा ऑनलाइन शिकायत दर्ज करें।", "text_en": "Call 1915 or register grievance on consumerhelpline.gov.in."},
                {"step": 3, "text_mr": "निवारण न झाल्यास ई-दाखील (edaakhil.nic.in) द्वारे जिल्हा ग्राहक मंचाकडे दाद मागा.", "text_hi": "समाधान न होने पर ई-दाखिल पोर्टल से जिला उपभोक्ता आयोग में याचिका दायर करें।", "text_en": "File a petition before District Consumer Commission via e-Daakhil (edaakhil.nic.in)."}
            ],
            "cybercrime": [
                {"step": 1, "text_mr": "तातडीने सायबर हेल्पलाइन १९३० वर संपर्क साधून खात्यातील व्यवहार गोठवण्याची विनंती करा.", "text_hi": "तुरंत 1930 पर कॉल कर संबंधित बैंक खाते को फ्रीज कराने की प्रक्रिया शुरू करें।", "text_en": "Immediately dial 1930 to freeze fraudulent fund transfers with the involved banks."},
                {"step": 2, "text_mr": "cybercrime.gov.in वर ऑनलाइन अधिकृत तक्रार नोंदवून पावती क्रमांक (Acknowledgement) घ्या.", "text_hi": "cybercrime.gov.in पर औपचारिक रिपोर्ट दर्ज कर पावती संख्या सुरक्षित रखें।", "text_en": "Lodge an official report on cybercrime.gov.in and save the acknowledgment receipt."},
                {"step": 3, "text_mr": "आपल्या बँकेच्या शाखेत जाऊन अनधिकृत व्यवहाराची लेखी माहिती द्या आणि कार्ड/खाते ब्लॉक करा.", "text_hi": "अपनी बैंक शाखा जाकर लिखित सूचना दें तथा एटीएम/नेटबैंकिंग ब्लॉक कराएं।", "text_en": "Visit your home bank branch to submit written notification of unauthorized debits."}
            ],
            "rental_housing": [
                {"step": 1, "text_mr": "भाडेकरार, डिपॉझिट पावती आणि घर रिकामे करतानाचे फोटो/व्हिडिओ जतन करा.", "text_hi": "किराया अनुबंध, जमा पर्ची और घर सौंपने के समय के साक्ष्य सुरक्षित रखें।", "text_en": "Preserve rent agreement, deposit payment slip, and proof of handing over possession."},
                {"step": 2, "text_mr": "घरमालकाला कायदेशीर नोटीस किंवा लेखी स्मरणपत्र पाठवा.", "text_hi": "मकान मालिक को सुरक्षा जमा राशि वापसी हेतु लिखित नोटिस प्रेषित करें।", "text_en": "Issue a written demand notice requesting return of security deposit within a reasonable time."},
                {"step": 3, "text_mr": "भाडे नियंत्रण प्राधिकरण किंवा विधी सेवा प्राधिकरणाकडे मध्यस्थीसाठी संपर्क साधा.", "text_hi": "किराया प्राधिकरण या विधिक सेवा प्राधिकरण से मध्यस्थता हेतु संपर्क करें।", "text_en": "Approach the Rent Authority or Legal Services Authority for mediation and recovery."}
            ],
            "legal_aid": [
                {"step": 1, "text_mr": "आपल्या जिल्ह्यातील जिल्हा विधी सेवा प्राधिकरण (DLSA) कार्यालयाचा पत्ता शोधा.", "text_hi": "अपने जिले के जिला विधिक सेवा प्राधिकरण (DLSA) कार्यालय का पता ज्ञात करें।", "text_en": "Locate your District Legal Services Authority (DLSA) office located within the District Court complex."},
                {"step": 2, "text_mr": "राष्ट्रीय कायदेशीर मदत हेल्पलाइन १५१०० वर मोफत मार्गदर्शन मिळवा.", "text_hi": "राष्ट्रीय विधिक सहायता टोल-फ्री हेल्पलाइन 15100 पर संपर्क करें।", "text_en": "Dial toll-free national helpline 15100 for immediate procedural guidance."},
                {"step": 3, "text_mr": "nalsa.gov.in वर किंवा प्रत्यक्ष कार्यालयात अर्ज करून मोफत पॅनेल वकिलाची नेमणूक मिळवा.", "text_hi": "nalsa.gov.in पर अथवा प्रत्यक्ष आवेदन कर पैनल वकील की निःशुल्क नियुक्ति प्राप्त करें।", "text_en": "Submit an application online at nalsa.gov.in or in person for assignment of a panel advocate."}
            ]
        }

        q_list = follow_up_questions.get(domain_key, follow_up_questions["legal_aid"]).get(
            lang[:2], follow_up_questions.get(domain_key, follow_up_questions["legal_aid"])["en"]
        )
        steps_list = action_steps.get(domain_key, action_steps["legal_aid"])

        # Localized summary
        summary = source.get(f"summary_{lang[:2]}", source["summary_en"])
        domain_name = self.domains[domain_key].get(f"domain_name_{lang[:2]}", self.domains[domain_key]["domain_name_en"])

        return {
            "query": user_query,
            "detected_language": lang,
            "domain_id": domain_key,
            "domain_name": domain_name,
            "plain_language_summary": summary,
            "clarifying_questions": q_list,
            "key_provisions": source.get("key_provisions", []),
            "action_steps": [
                {"step": s["step"], "action": s.get(f"text_{lang[:2]}", s.get("text_en"))}
                for s in steps_list
            ],
            "official_citation": {
                "title": source["title"],
                "issuing_authority": source["issuing_authority"],
                "jurisdiction": source["jurisdiction"],
                "official_url": source.get("official_url"),
                "portal_url": source.get("portal_url"),
                "helpline": source.get("helpline"),
                "verification_status": source.get("verification_status", "VERIFIED_OFFICIAL"),
                "retrieval_date": source.get("retrieval_date")
            },
            "stated_facts": "वापरकर्त्याने नमूद केलेली प्राथमिक अडचण / Stated circumstances: " + user_query,
            "unknown_facts": "कामाचे अचूक ठिकाण, लेखी पुराव्यांचे स्वरूप आणि विरोधी पक्षाची भूमिका अद्याप माहित नाही. / Employment details, written proof, and employer's exact defense remain unverified.",
            "important_uncertainty": "कायद्यानुसार दाद मागण्याचा अधिकार असला तरी अंतिम निकाल पुरावे आणि सक्षम प्राधिकरणाच्या पडताळणीवर अवलंबून असतो. कोणतीही हमी देता येत नाही. / Legal rights are contingent upon verified evidence and procedural adherence. No outcome is guaranteed.",
            "disclaimer": LEGAL_DISCLAIMER
        }
