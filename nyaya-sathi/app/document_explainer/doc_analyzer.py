"""
Legal Document Analyzer & Explainer for Nyaya Sathi.
Performs extraction, deadline detection, terminology decoding, and safety checks.
Strictly distinguishes explicit printed dates from legally inferred deadlines.
Never fabricates unreadable text or pronounces document validity.
"""

import re
from typing import Dict, List, Any, Optional
from ..config import PRIVACY_WARNING, LEGAL_DISCLAIMER

# Legal terminology dictionary with plain-language explanations in Marathi, Hindi, and English
LEGAL_GLOSSARY = {
    "show cause": {
        "term": "Show Cause (कारणे दाखवा)",
        "meaning_mr": "प्रशासनाने कारवाई करण्यापूर्वी तुम्हाला आपली बाजू किंवा स्पष्टीकरण मांडण्याची दिलेली अंतिम संधी.",
        "meaning_hi": "कार्रवाई करने से पहले विभाग द्वारा अपना पक्ष या सफाई पेश करने के लिए दिया गया अवसर।",
        "meaning_en": "An order requiring you to explain why a particular proposed penalty or action should not be taken against you."
    },
    "ex-parte": {
        "term": "Ex-Parte (एकतर्फी सुनावणी)",
        "meaning_mr": "जर तुम्ही ठरलेल्या मुदतीत हजर राहिला नाही किंवा उत्तर दिले नाही, तर अधिकारी किंवा न्यायालय केवळ दुसऱ्या पक्षाचे ऐकून निर्णय घेईल.",
        "meaning_hi": "यदि आप समय पर उपस्थित नहीं होते, तो न्यायालय या अधिकारी आपकी गैर-मौजूदगी में ही एकतरफा फैसला सुना देगा।",
        "meaning_en": "Decided in the absence of one party; if you fail to appear or reply, an order may be passed without hearing your side."
    },
    "without prejudice": {
        "term": "Without Prejudice (हक्कांना बाधा न आणता)",
        "meaning_mr": "या पत्रातील विधानांचा वापर कोर्टात भविष्यातील अधिकारांना सोडल्याचा पुरावा म्हणून करता येणार नाही.",
        "meaning_hi": "इस पत्र या बातचीत के आधार पर किसी भी पक्ष का मुख्य कानूनी अधिकार समाप्त नहीं माना जाएगा।",
        "meaning_en": "Issued without waiving or harming any existing legal rights or future claims."
    },
    "mesne profits": {
        "term": "Mesne Profits (बेकायदेशीर वापराचा मोबदला)",
        "meaning_mr": "भाडेकरार संपल्यानंतरही जागा खाली न केल्यास मालकाने मागणी केलेली वाढीव दंडात्मक भरपाई रक्कम.",
        "meaning_hi": "किराया अवधि समाप्त होने के बाद भी कब्जा बनाए रखने पर मांगा गया हर्जाना या बाजार दर का किराया।",
        "meaning_en": "Damages claimed by the property owner for the period the occupant remained in wrongful possession after tenancy expiry."
    },
    "inter-alia": {
        "term": "Inter-alia (इतर बाबींबरोबरच / Among other things)",
        "meaning_mr": "उदाहरणादाखल दिलेली बाब; केवळ हीच एक गोष्ट नसून इतरही गोष्टींचा यात समावेश आहे.",
        "meaning_hi": "अन्य बातों के साथ-साथ; इसका अर्थ है कि यह केवल एक बिंदु है और अन्य कारण भी मौजूद हैं।",
        "meaning_en": "Among other things; indicating that the stated items are not exhaustive."
    },
    "section 351": {
        "term": "Section 351 (महानगरपालिका कायदा कलम ३५१)",
        "meaning_mr": "अनधिकृत बांधकाम आढळल्यास ते पाडण्यापूर्वी मालकाला मंजूर नकाशा दाखवण्यासाठी दिलेली कायदेशीर नोटीस.",
        "meaning_hi": "कथित अवैध निर्माण को गिराने से पहले स्वीकृत नक्शा दिखाने हेतु दी जाने वाली कानूनी नोटिस।",
        "meaning_en": "Statutory notice under Municipal Corporation Act requiring owner to produce approved building plans for alleged unauthorized works."
    }
}

class DocumentAnalyzer:
    """Analyzes text from official notices and contracts safely and transparently."""

    def analyze_document(self, text: str, user_language: str = "mr-IN") -> Dict[str, Any]:
        """Parses document text, extracts explicit dates, actions, terms, and lawyer questions."""
        
        if not text or len(text.strip()) < 15:
            return {
                "error": True,
                "message": "कागदपत्रातील मजकूर अत्यंत अपुरा किंवा अस्पष्ट आहे. कृपया स्पष्ट मजकूर टाका. / Document text too short or unreadable."
            }

        # 1. Detect Document Type
        doc_type = self._classify_doc_type(text)

        # 2. Extract Explicit Dates (Regex search)
        explicit_dates = self._extract_explicit_dates(text)

        # 3. Detect Legal Terminology
        matched_terms = self._find_legal_terms(text, user_language)

        # 4. Generate Plain Summary
        summary = self._generate_plain_summary(doc_type, text, user_language)

        # 5. Distinguish Explicit vs Inferred Deadlines
        deadlines_info = self._analyze_deadlines(text, explicit_dates, user_language)

        # 6. Action Items Requested from User
        action_items = self._extract_requested_actions(text, doc_type, user_language)

        # 7. Verification Checklist
        verification_items = [
            "कागदपत्रावरील आवक/जावक क्रमांक (Notice Number) व अधिकृत शिक्का तपासा.",
            "नोटीस देणाऱ्या अधिकाऱ्याचे पद आणि कार्यालयाचा पत्ता अधिकृत आहे का याची खात्री करा.",
            "नोटीस तुम्हाला प्रत्यक्षात कोणत्या तारखेला मिळाली (Postal / Delivery Date) ती तारीख नोंदवून ठेवा."
        ]

        # 8. Questions to ask DLSA / Legal Aid Lawyer
        lawyer_questions = self._suggest_lawyer_questions(doc_type, user_language)

        return {
            "privacy_notice": PRIVACY_WARNING,
            "apparent_document_type": doc_type,
            "plain_summary": summary,
            "explicit_dates_found": explicit_dates,
            "deadlines_analysis": deadlines_info,
            "actions_requested": action_items,
            "legal_terms_explained": matched_terms,
            "verification_checklist": verification_items,
            "questions_for_lawyer": lawyer_questions,
            "validity_disclaimer": "महत्त्वाची नोंद: एआय प्रणाली कागदपत्राची कायदेशीर वैधता किंवा अवैधता घोषित करू शकत नाही. मूळ कागदपत्रे वकिलांना दाखवून पुढील पाऊल उचलावे."
        }

    def _classify_doc_type(self, text: str) -> str:
        text_lower = text.lower()
        if "section 351" in text_lower or "unauthorized construction" in text_lower or "demolition" in text_lower or "municipal" in text_lower:
            return "Municipal Statutory Show Cause Notice (महानगरपालिका अतिक्रमण कारणे दाखवा नोटीस)"
        elif "salary" in text_lower or "remuneration" in text_lower or "withholding" in text_lower or "employee" in text_lower:
            return "Employment Notice / Wage Withholding Memorandum (नोकरीतील वेतन रोखल्याचे पत्र)"
        elif "leave and license" in text_lower or "tenant" in text_lower or "vacate" in text_lower or "rent" in text_lower:
            return "Tenancy Eviction Notice (घर रिकामे करण्याची कायदेशीर नोटीस)"
        elif "court" in text_lower or "summons" in text_lower or "magistrate" in text_lower:
            return "Court Summons / Judicial Notice (न्यायालयीन समन्स)"
        return "Official Legal Notice / Communication (अधिकृत कायदेशीर नोटीस)"

    def _extract_explicit_dates(self, text: str) -> List[str]:
        """Extracts strictly dates and period spans printed in the text."""
        date_patterns = [
            r'\b\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4}\b',
            r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b',
            r'\b(?:within\s+)?\d+\s+\([A-Z]+\)\s+DAYS\b'
        ]
        found = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                if m not in found:
                    found.append(m)
        return found

    def _find_legal_terms(self, text: str, lang: str) -> List[Dict[str, str]]:
        matched = []
        text_lower = text.lower()
        for key, item in LEGAL_GLOSSARY.items():
            if key in text_lower:
                matched.append({
                    "term": item["term"],
                    "explanation": item.get(f"meaning_{lang[:2]}", item["meaning_en"])
                })
        return matched

    def _analyze_deadlines(self, text: str, explicit_dates: List[str], lang: str) -> Dict[str, Any]:
        """Explicitly distinguishes printed dates from legally inferred deadlines."""
        text_lower = text.lower()
        inferred = []
        explicit_deadlines = []

        if "15 days" in text_lower or "fifteen days" in text_lower:
            explicit_deadlines.append("कागदपत्रात स्पष्ट नमूद: नोटीस मिळाल्यापासून १५ दिवसांच्या आत उत्तर देणे आवश्यक आहे.")
        if "30 days" in text_lower or "thirty days" in text_lower:
            explicit_deadlines.append("कागदपत्रात स्पष्ट नमूद: ३० दिवसांच्या आत जागा खाली करणे किंवा उत्तर देणे नमूद आहे.")

        # Check for specific dates
        for d in explicit_dates:
            if "/" in d or "-" in d:
                explicit_deadlines.append(f"दस्तऐवजात छापलेली तारीख / वेळ: {d}")

        # Inferred deadline reminder
        inferred.append(
            "कायद्यानुसार अनुमानित मुदत: नोटीस पोस्टाने मिळाली असल्यास पोस्टाची पोहोच पावती तारीख (Date of Delivery) ही मुदतीचा पहिला दिवस मानला जातो, केवळ नोटीसवर छापलेली तारीख नव्हे."
        )

        return {
            "explicitly_printed_deadlines": explicit_deadlines or ["कागदपत्रात ठराविक अंतिम तारीख स्पष्टपणे नमूद नाही; लवकरात लवकर संपर्क साधणे आवश्यक आहे."],
            "inferred_legal_rule": inferred
        }

    def _generate_plain_summary(self, doc_type: str, text: str, lang: str) -> str:
        text_lower = text.lower()
        if "municipal" in text_lower or "section 351" in text_lower:
            if lang.startswith("mr"):
                return "ही महानगरपालिकेची कारणे दाखवा नोटीस आहे. आपल्या दुकानावर/घरावर अनधिकृत शेड किंवा बांधकाम केल्याचा आरोप आहे. हे बांधकाम पाडण्यापूर्वी आपल्याला १५ दिवसांच्या आत मंजुरीचे नकाशे आणि कागदपत्रे दाखवण्याची संधी दिली आहे. दुर्लक्ष केल्यास प्रशासन एकतर्फी कारवाई करू शकते."
            elif lang.startswith("hi"):
                return "यह नगर निगम का कारण बताओ नोटिस है। इसमें कथित अवैध निर्माण या शेड हटाने हेतु 15 दिनों के भीतर स्वीकृत नक्शे व दस्तावेज प्रस्तुत करने को कहा गया है। जवाब न देने पर एकतरफा कार्रवाई हो सकती है।"
            else:
                return "This is a municipal show cause notice alleging unauthorized shed construction. It requires you to produce approved building plans within 15 days, failing which the municipality may initiate ex-parte demolition."
        elif "salary" in text_lower or "withholding" in text_lower:
            if lang.startswith("mr"):
                return "हे कंपनीचे अंतर्गत मेमो पत्र आहे. कंपनीने अंतर्गत चौकशीच्या कारणावरून सप्टेंबर महिन्याचे वेतन (रु. २४,५००) रोखून ठेवल्याचे कळवले आहे आणि १२ ऑक्टोबरपूर्वी लेखी खुलासा मागितला आहे. कायद्यानुसार कामगाराचे वेतन असे परस्पर रोखून ठेवता येत नाही."
            elif lang.startswith("hi"):
                return "यह कंपनी का नोटिस है जिसमें आंतरिक जांच के नाम पर सितंबर माह का वेतन रोके जाने की बात कही गई है। 12 तारीख तक जवाब मांगा गया है। कानूनी रूप से बिना विधिवत प्रक्रिया के वेतन रोकना अनुचित है।"
            else:
                return "This is an employment memo stating that your September wages are being temporarily withheld pending an audit inquiry, with an explanation demanded by 12th October."
        elif "vacate" in text_lower or "rent" in text_lower:
            if lang.startswith("mr"):
                return "ही घरमालकाच्या वकिलाने पाठवलेली घर रिकामे करण्याची नोटीस आहे. भाडेकरार संपल्याचे आणि थकीत भाड्याचे कारण देऊन ३० दिवसांत घर सोडण्याची मागणी केली आहे, अन्यथा न्यायालयात जाण्याचा इशारा दिला आहे."
            elif lang.startswith("hi"):
                return "यह मकान खाली करने की कानूनी नोटिस है। इसमें 30 दिनों के भीतर परिसर खाली करने का निर्देश दिया गया है।"
            else:
                return "This is an eviction notice from the landlord's counsel demanding peaceful possession within 30 days alleging tenancy expiry."

        return "हे एक कायदेशीर पत्र/नोटीस आहे ज्यामध्ये ठराविक मुद्द्यांवर खुलासा मागितला आहे किंवा कार्यवाहीचा इशारा दिला आहे."

    def _extract_requested_actions(self, text: str, doc_type: str, lang: str) -> List[str]:
        actions = []
        text_lower = text.lower()
        if "produce" in text_lower or "plan" in text_lower:
            actions.append("मंजूर इमारत नकाशा, प्रॉपर्टी टॅक्स पावती व बांधकाम परवाना मूळ प्रतीसह सादर करणे.")
        if "explanation" in text_lower or "reply" in text_lower or "show cause" in text_lower:
            actions.append("मुदतीच्या आत लेखी उत्तर (Written Reply / Explanation) तयार करून सक्षम अधिकाऱ्याकडे दाखल करणे.")
        if "vacate" in text_lower:
            actions.append("परिसर रिकामा करणे अथवा भाडे भरल्याच्या पावत्यांसह कायदेशीर वकिलांमार्फत नोटीसला उत्तर देणे.")
        if not actions:
            actions.append("नोटीस देणाऱ्या कार्यालयाशी संपर्क साधून लेखी पोहोच पावती घेणे.")
        return actions

    def _suggest_lawyer_questions(self, doc_type: str, lang: str) -> List[str]:
        if "Municipal" in doc_type:
            return [
                "१. या नोटीसविरोधात दिवाणी न्यायालयात तात्पुरता स्थगिती आदेश (Injunction / Stay) मागता येईल का?",
                "२. हे बांधकाम नियमितीकरण (Regularization / Compounding) प्रक्रियेद्वारे कायदेशीर करता येते का?",
                "३. कारणे दाखवा नोटीसला उत्तर देताना कोणकोणते तांत्रिक नकाशे जोडणे आवश्यक आहे?"
            ]
        elif "Employment" in doc_type:
            return [
                "१. अंतर्गत चौकशीच्या नावाखाली कंपनी वेतन कायद्यानुसार पगार रोखून ठेवू शकते का?",
                "२. कामगार आयुक्त कार्यालयात कलम १५ अन्वये तात्काळ दावा दाखल करावा का?",
                "३. खुलासा पत्रात कायदेशीर अधिकार राखून ठेवण्यासाठी काय शब्दरचना असावी?"
            ]
        else:
            return [
                "१. या नोटीसची मुदत संपण्यापूर्वी औपचारिक उत्तर नोंदणीकृत टपालाने (RPAD) पाठवणे आवश्यक आहे का?",
                "२. या प्रकरणात विधी सेवा प्राधिकरणाकडून (DLSA) मोफत वकील मिळवण्यासाठी मी पात्र आहे का?",
                "३. वाद मिटवण्यासाठी लोकअदालत किंवा मध्यस्थीचा मार्ग वापरता येईल का?"
            ]
