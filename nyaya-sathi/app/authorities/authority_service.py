"""
Authority Recommendation and Grievance Routing Engine for Nyaya Sathi.
Maps user legal grievances to the exact statutory authority, filing portal, and physical desk.
"""

from typing import Dict, List, Any, Optional

AUTHORITY_MAP = {
    "unpaid_wages": {
        "primary_authority": {
            "name": "कार्यालय कामगार आयुक्त / Office of the Labour Commissioner",
            "jurisdiction_type": "State / Central Labour Department",
            "filing_mode": "Online & Physical",
            "official_portal": "https://samadhan.labour.gov.in",
            "portal_name": "SAMADHAN Portal (Ministry of Labour & Employment)",
            "statutory_role": "Authority appointed under Section 15 of Payment of Wages Act / Section 33C of Industrial Disputes Act.",
            "reason": "कामगारांचे थकीत वेतन वसूल करण्याचे आणि नियोक्त्यावर कायदेशीर कारवाई करण्याचे अधिकार कामगार आयुक्तांना आहेत.",
            "reason_en": "The Labour Commissioner is the statutory authority empowered to hear wage claims and order recovery with compensation.",
            "contact_guide": "आपल्या जिल्ह्यातील जिल्हाधिकारी कार्यालय किंवा कामगार भवन (Labour Court) येथे प्रत्यक्ष अर्ज करता येतो."
        },
        "alternative_authority": {
            "name": "जिल्हा विधी सेवा प्राधिकरण (DLSA) - कामगार सहायता कक्ष",
            "jurisdiction_type": "District Court Campus",
            "filing_mode": "Physical Walk-in & Helpline 15100",
            "reason": "आर्थिक परिस्थितीमुळे खासगी वकील ठेवणे शक्य नसल्यास विधी सेवा प्राधिकरणामार्फत विनामूल्य मध्यस्थी व वकील मिळतो."
        }
    },
    "consumer_complaints": {
        "primary_authority": {
            "name": "राष्ट्रीय ग्राहक हेल्पलाइन / National Consumer Helpline (NCH)",
            "jurisdiction_type": "Central Department of Consumer Affairs",
            "filing_mode": "Toll-Free Phone (1915), SMS, WhatsApp & Web Portal",
            "official_portal": "https://consumerhelpline.gov.in",
            "portal_name": "National Consumer Helpline (NCH)",
            "statutory_role": "First-tier alternative consumer dispute redressal mechanism.",
            "reason": "न्यायालयात जाण्यापूर्वी १९१५ वर कॉल करून किंवा पोर्टलवर तक्रार नोंदवून ९०% पेक्षा जास्त प्रकरणांचे जलद निवारण होते.",
            "reason_en": "Provides an immediate, no-cost conciliation route between consumers and registered companies.",
            "contact_guide": "सकाळी ८ ते रात्री ८ दरम्यान थेट १९१५ डायल करा किंवा ८१३० ० ० ९८०० वर व्हॉट्सॲप करा."
        },
        "alternative_authority": {
            "name": "जिल्हा ग्राहक वाद निवारण आयोग (District Consumer Commission) via e-Daakhil",
            "jurisdiction_type": "Quasi-Judicial Commission",
            "filing_mode": "Online e-Daakhil Portal & District Court",
            "official_portal": "https://edaakhil.nic.in",
            "statutory_role": "Adjudicates claims up to Rs. 50 Lakhs under Section 35 of Consumer Protection Act, 2019.",
            "reason": "कंपनीने दाद न दिल्यास नुकसानभरपाईसह रक्कमेचा परतावा मिळवण्यासाठी ग्राहक न्यायालयात याचिका दाखल करता येते."
        }
    },
    "cybercrime": {
        "primary_authority": {
            "name": "नागरिक वित्तीय सायबर फसवणूक निवारण प्रणाली (Helpline 1930)",
            "jurisdiction_type": "Indian Cybercrime Coordination Centre (I4C), MHA",
            "filing_mode": "Toll-Free Helpline 1930",
            "official_portal": "https://cybercrime.gov.in",
            "portal_name": "National Cyber Crime Reporting Portal",
            "statutory_role": "Interbanks real-time lien/freeze system for fraudulent transactions.",
            "reason": "पैसे खात्यातून कापल्यापासून पहिल्या २ तासांत १९३० वर तक्रार केल्यास गुन्हेगाराच्या खात्यातील रक्कम तातडीने गोठवली जाते.",
            "reason_en": "Immediate reporting to 1930 triggers real-time bank account freezing across all scheduled banks.",
            "contact_guide": "कोणताही विलंब न करता १९३० वर फोन लावा. व्यवहार संदर्भ क्रमांक (UTR) जवळ ठेवा."
        },
        "alternative_authority": {
            "name": "स्थानिक सायबर पोलीस ठाणे / Local Cyber Police Station",
            "jurisdiction_type": "District Police Commissionerate",
            "filing_mode": "Physical FIR & Formal Investigation",
            "reason": "मोठ्या रकमेच्या किंवा ब्लॅकमेलिंगच्या प्रकरणात अधिकृत एफआयआर नोंदवून चौकशी करण्यासाठी."
        }
    },
    "women_rights": {
        "primary_authority": {
            "name": "महिला संरक्षण अधिकारी (Protection Officer) व सखी वन स्टॉप सेंटर",
            "jurisdiction_type": "District Women & Child Development Department",
            "filing_mode": "Helpline 181, 112 & Walk-in",
            "official_portal": "https://wcd.nic.in",
            "portal_name": "Sakhi One Stop Centre Scheme",
            "statutory_role": "Statutory Protection Officer under Section 9 of PWDVA, 2005.",
            "reason": "कौटुंबिक हिंसाचारापासून तातडीचे संरक्षण, वैद्यकीय मदत, तात्पुरता निवारा आणि दंडाधिकाऱ्यांसमोर अर्ज भरून देणे.",
            "reason_en": "Statutorily appointed officers responsible for filing Domestic Incident Reports (DIR) and providing safe shelter.",
            "contact_guide": "१८१ महिला हेल्पलाइनवर २४ तास कॉल करा किंवा स्थानिक जिल्हा सामान्य रुग्णालयातील सखी केंद्राला भेट द्या."
        },
        "alternative_authority": {
            "name": "प्रथम वर्ग न्यायदंडाधिकारी न्यायालय (JMFC Court)",
            "jurisdiction_type": "Judicial Magistrate",
            "filing_mode": "Formal Court Petition under Section 12 PWDVA",
            "reason": "सामायिक घरात राहण्याचा आदेश (Residence Order) व आर्थिक पोटगी आदेश मिळवण्यासाठी."
        }
    },
    "rental_housing": {
        "primary_authority": {
            "name": "सक्षम प्राधिकारी / भाडे न्यायालय (Rent Authority / Rent Court)",
            "jurisdiction_type": "Sub-Divisional / Municipal Rent Authority",
            "filing_mode": "Physical Petition",
            "statutory_role": "Authority established under State Rent Control Act / Model Tenancy Act.",
            "reason": "घरमालक-भाडेकरू यांच्यातील सुरक्षा अनामत परत न करणे किंवा बेकायदेशीरपणे बाहेर काढण्याच्या वादांचा निवाडा करणे.",
            "reason_en": "Designated forum for tenancy agreements, deposit disputes, and unlawful utility cutoffs."
        },
        "alternative_authority": {
            "name": "दिवाणी न्यायालय किंवा लोकअदालत (Lok Adalat)",
            "jurisdiction_type": "Civil Court / DLSA Alternative Dispute Resolution",
            "filing_mode": "Pre-litigation Mediation via DLSA",
            "reason": "कोर्ट कचेरीचा खर्च टाळून मोफत सामंजस्यपूर्ण तोडगा काढण्यासाठी."
        }
    },
    "government_benefits": {
        "primary_authority": {
            "name": "जिल्हा तक्रार निवारण अधिकारी (DGRO) / CPGRAMS",
            "jurisdiction_type": "District Administration / DARPG Central Portal",
            "filing_mode": "Online Portal (pgportal.gov.in)",
            "official_portal": "https://pgportal.gov.in",
            "portal_name": "CPGRAMS Central Public Grievance Portal",
            "statutory_role": "Statutory redressal officer under National Food Security Act / Central Grievance Rules.",
            "reason": "राशन कार्ड, पेन्शन किंवा सरकारी अनुदानात होणारा भ्रष्टाचार व दिरंगाईविरोधात थेट मंत्रालयात नोंद होणारी तक्रार.",
            "reason_en": "Direct online escalation system monitored by Central and State department secretaries."
        }
    }
}

class AuthorityRecommendationService:
    """Matches user issues to the appropriate official authority and filing mechanism."""

    def recommend_authority(
        self,
        domain_key: str,
        state: str = "Maharashtra",
        dispute_amount: Optional[float] = None
    ) -> Dict[str, Any]:
        """Provides reasoned authority recommendations with links and submission instructions."""
        route = AUTHORITY_MAP.get(domain_key, AUTHORITY_MAP["unpaid_wages"])
        
        clarifying_factors = []
        if dispute_amount is not None:
            if domain_key == "consumer_complaints":
                if dispute_amount <= 5000000:
                    clarifying_factors.append(f"दावा रक्कम रु. {dispute_amount:,.0f} असल्याने जिल्हा ग्राहक आयोगाची मर्यादा (५० लाखांपर्यंत) लागू होते.")
                else:
                    clarifying_factors.append(f"दावा रक्कम ५० लाखांपेक्षा जास्त असल्यास राज्य ग्राहक आयोगाकडे जावे लागते.")

        return {
            "domain": domain_key,
            "state": state,
            "primary_authority": route["primary_authority"],
            "alternative_authority": route.get("alternative_authority"),
            "clarifying_factors": clarifying_factors,
            "important_rule": "न्याय साथी थेट तक्रार दाखल करत नाही. वरील अधिकृत पोर्टलवर किंवा प्रत्यक्ष जाऊन आपण तक्रार सादर करू शकता."
        }
