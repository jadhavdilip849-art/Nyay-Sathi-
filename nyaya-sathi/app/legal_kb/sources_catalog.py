"""
Authoritative Legal Sources Catalog for Nyaya Sathi.
Contains verified statutory sources, official portals, helplines, and government authorities.
Every source has strict metadata: title, authority, jurisdiction, source_url, verified date, and provisions.
"""

AUTHORITATIVE_SOURCES = {
    "PAYMENT_OF_WAGES": {
        "id": "PAYMENT_OF_WAGES",
        "title": "Payment of Wages Act, 1936 & Code on Wages, 2019",
        "issuing_authority": "Ministry of Labour & Employment, Government of India",
        "jurisdiction": "Central / State (India)",
        "official_url": "https://www.indiacode.nic.in/handle/123456789/2387",
        "portal_url": "https://samadhan.labour.gov.in",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["unpaid_wages", "employment", "labor"],
        "key_provisions": [
            "Section 5: Wages must be paid before expiry of 7th day (less than 1000 workers) or 10th day (other establishments) after the wage period.",
            "Section 15: Application for claims arising out of deductions from wages or delay in payment of wages before the appointed Authority.",
            "Section 15(2): Limitation period of 12 months (or 3 years under Code on Wages) from the date on which wage was due.",
            "Section 33C(2) Industrial Disputes Act: Workman can apply to Labour Court for recovery of money due from employer."
        ],
        "summary_mr": "कामगारांना वेळेवर वेतन मिळण्याचा कायदेशीर अधिकार आहे. वेतन थकवल्यास कामगार आयुक्त किंवा 'समाधान' पोर्टलवर दाद मागता येते.",
        "summary_hi": "मजदूरों और कर्मचारियों को समय पर वेतन पाने का कानूनी अधिकार है। वेतन न मिलने पर श्रम आयुक्त या समाधान पोर्टल पर शिकायत की जा सकती है।",
        "summary_en": "Workers have a statutory right to timely wage payment. In case of non-payment, claims can be filed before the Labour Commissioner or Samadhan Portal."
    },
    "CONSUMER_PROTECTION": {
        "id": "CONSUMER_PROTECTION",
        "title": "Consumer Protection Act, 2019 (Act No. 35 of 2019)",
        "issuing_authority": "Department of Consumer Affairs, Ministry of Consumer Affairs, Food and Public Distribution",
        "jurisdiction": "All India",
        "official_url": "https://www.indiacode.nic.in/handle/123456789/15256",
        "portal_url": "https://consumerhelpline.gov.in",
        "e_daakhil_url": "https://edaakhil.nic.in",
        "helpline": "1915 (National Consumer Helpline)",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["consumer_complaints", "defective_goods", "unfair_trade"],
        "key_provisions": [
            "Section 2(7): Definition of consumer - covers online and offline transactions.",
            "Section 35: Manner in which complaint shall be made to District Commission (claims up to Rs. 50 Lakhs).",
            "Section 38: Procedure on admission of complaint; District Commission can order refund, replacement, or compensation.",
            "Section 69: Limitation period is 2 years from date on which cause of action arose."
        ],
        "summary_mr": "खराब वस्तू किंवा सेवेतील त्रुटीविरोधात ग्राहक १९१५ हेल्पलाइन किंवा ई-दाखील पोर्टलद्वारे ग्राहक मंचात तक्रार करू शकतात.",
        "summary_hi": "खराब सामान या अनुचित सेवा मिलने पर उपभोक्ता 1915 राष्ट्रीय उपभोक्ता हेल्पलाइन या ई-दाखिल पोर्टल पर शिकायत दर्ज कर सकते हैं।",
        "summary_en": "Consumers can file complaints for defective goods or deficient services via the 1915 helpline or the e-Daakhil portal."
    },
    "CYBERCRIME_IT_ACT": {
        "id": "CYBERCRIME_IT_ACT",
        "title": "Information Technology Act, 2000 (as amended) & I4C Citizen Financial Cyber Fraud Reporting",
        "issuing_authority": "Ministry of Home Affairs & Ministry of Electronics and Information Technology",
        "jurisdiction": "All India",
        "official_url": "https://www.indiacode.nic.in/handle/123456789/13116",
        "portal_url": "https://cybercrime.gov.in",
        "helpline": "1930 (Citizen Financial Cyber Fraud Reporting System)",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["cybercrime", "online_fraud", "upi_scam"],
        "key_provisions": [
            "Section 43A & 66C: Identity theft and fraudulent use of password/electronic signature.",
            "Section 66D: Cheating by personation by using computer resource.",
            "Golden Hour Reporting: Call 1930 immediately within 2 hours of unauthorized financial transactions to freeze beneficiary bank accounts."
        ],
        "summary_mr": "ऑनलाइन आर्थिक फसवणूक किंवा सायबर गुन्ह्याची तक्रार तातडीने १९३० क्रमांकावर किंवा cybercrime.gov.in वर करावी.",
        "summary_hi": "ऑनलाइन वित्तीय धोखाधड़ी या साइबर अपराध होने पर तुरंत 1930 हेल्पलाइन पर कॉल करें या cybercrime.gov.in पर रिपोर्ट करें।",
        "summary_en": "Report financial cyber frauds immediately by calling 1930 or lodging an incident on cybercrime.gov.in."
    },
    "LEGAL_SERVICES_AUTHORITIES": {
        "id": "LEGAL_SERVICES_AUTHORITIES",
        "title": "Legal Services Authorities Act, 1987 (Act No. 39 of 1987)",
        "issuing_authority": "National Legal Services Authority (NALSA) & Supreme Court of India",
        "jurisdiction": "All India (NALSA / SLSA / DLSA / TLSC)",
        "official_url": "https://nalsa.gov.in/acts-rules/the-legal-services-authorities-act-1987",
        "portal_url": "https://nalsa.gov.in",
        "helpline": "15100 (NALSA Toll-Free National Legal Aid Helpline)",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["legal_aid", "free_lawyer", "nalsa", "dlsa"],
        "key_provisions": [
            "Section 12: Criteria for giving legal services to eligible persons (women, children, SC/ST, industrial workmen, disabled, custody, low income).",
            "Section 13: Entitlement to legal services - if prima facie case exists.",
            "Free services include court fees, process fees, advocate fees, paper book preparation, and certified copies."
        ],
        "summary_mr": "पात्र नागरिकांना (महिला, कामगार, दुर्बल घटक) मोफत सरकारी वकील आणि कायदेशीर मदत NALSA आणि DLSA द्वारे विनामूल्य दिली जाते.",
        "summary_hi": "योग्य नागरिकों (महिलाओं, कामगारों, कमजोर वर्गों) को नालसा और डीएलएसए के माध्यम से मुफ्त सरकारी वकील और कानूनी सहायता मिलती है।",
        "summary_en": "Eligible citizens receive free legal representation and court fee waivers through NALSA and District Legal Services Authorities (DLSA)."
    },
    "DOMESTIC_VIOLENCE_PWDVA": {
        "id": "DOMESTIC_VIOLENCE_PWDVA",
        "title": "Protection of Women from Domestic Violence Act, 2005 (PWDVA)",
        "issuing_authority": "Ministry of Women and Child Development",
        "jurisdiction": "All India",
        "official_url": "https://www.indiacode.nic.in/handle/123456789/2021",
        "helpline": "181 (Women Helpline) / 112 (National Emergency)",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["women_rights", "domestic_violence", "family_disputes"],
        "key_provisions": [
            "Section 3: Broad definition of domestic violence (physical, emotional, sexual, verbal, and economic abuse).",
            "Section 12: Application to Magistrate for protection orders, residence orders, monetary relief, and custody orders.",
            "Section 18 & 19: Protection orders prohibiting respondent from committing violence; Right to reside in shared household.",
            "Section 9 & 10: Role of Protection Officers and Service Providers / Sakhi One Stop Centres."
        ],
        "summary_mr": "कौटुंबिक हिंसाचाराविरोधात महिलांना संरक्षण, राहण्याचा हक्क आणि आर्थिक मदत मिळण्याचा हक्क आहे. १८१ हेल्पलाइन किंवा संरक्षण अधिकाऱ्यांकडे मदत मिळते.",
        "summary_hi": "घरेलू हिंसा के खिलाफ महिलाओं को संरक्षण आदेश, साझा घर में रहने का अधिकार और 181 महिला हेल्पलाइन से त्वरित सहायता मिलती है।",
        "summary_en": "Women facing domestic abuse can obtain protection orders, residence orders, and emergency shelter through Protection Officers and Helpline 181."
    },
    "RENT_TENANCY_LAWS": {
        "id": "RENT_TENANCY_LAWS",
        "title": "Model Tenancy Act & State Rent Control Acts (e.g., Maharashtra Rent Control Act, 1999)",
        "issuing_authority": "Ministry of Housing and Urban Affairs & Respective State Governments",
        "jurisdiction": "State-specific (e.g. Maharashtra, Delhi, Karnataka)",
        "official_url": "https://mohua.gov.in/upload/uploadfiles/files/Model_Tenancy_Act_English.pdf",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["rental_housing", "deposit_refund", "eviction"],
        "key_provisions": [
            "Security Deposit Cap: Typically capped at 2 months' rent for residential premises under Model Tenancy Act.",
            "Deposit Refund: Landlord must refund deposit upon tenant vacating after deducting lawful dues.",
            "Unlawful Eviction: Landlord cannot cut essential services (water, electricity) or evict without due process under Rent Control Act.",
            "Grievance forum: Competent Authority / Rent Authority / Rent Tribunal or Small Causes Court."
        ],
        "summary_mr": "घरमालक बेकायदेशीरपणे वीज-पाणी तोडू शकत नाही आणि डिपॉझिट अडवून ठेवू शकत नाही. वाद असल्यास भाडे प्राधिकरणाकडे दाद मागता येते.",
        "summary_hi": "मकान मालिक बिना कानूनी प्रक्रिया के किराएदार को बेदखल नहीं कर सकता और न ही आवश्यक सेवाएं काट सकता है। सुरक्षा जमा राशि वापस पाने का अधिकार है।",
        "summary_en": "Landlords cannot unlawfully withhold security deposits or cut essential utilities. Disputes are resolved before Rent Authorities or Courts."
    },
    "SENIOR_CITIZENS_ACT": {
        "id": "SENIOR_CITIZENS_ACT",
        "title": "Maintenance and Welfare of Parents and Senior Citizens Act, 2007",
        "issuing_authority": "Ministry of Social Justice and Empowerment",
        "jurisdiction": "All India",
        "official_url": "https://www.indiacode.nic.in/handle/123456789/2027",
        "helpline": "14567 (Elder Line National Helpline)",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["senior_citizens", "elder_care", "maintenance"],
        "key_provisions": [
            "Section 4 & 5: Right of senior citizens and parents to claim maintenance from adult children or legal heirs.",
            "Section 7: Maintenance Tribunal presided over by Sub-Divisional Officer (SDO).",
            "Section 23: Transfer of property by senior citizen can be declared void if conditions of basic amenities are breached."
        ],
        "summary_mr": "ज्येष्ठ नागरिकांना मुलांकडून पोटगी मिळण्याचा आणि फसवणुकीने घेतलेली संपत्ती परत मिळवण्याचा अधिकार आहे. हेल्पलाइन १४५६७ उपलब्ध आहे.",
        "summary_hi": "वरिष्ठ नागरिकों को भरण-पोषण पाने और बुनियादी जरूरतों की अनदेखी पर संपत्ति हस्तांतरण रद्द कराने का कानूनी अधिकार है। हेल्पलाइन 14567।",
        "summary_en": "Senior citizens have a legal right to claim maintenance from adult heirs and revoke property transfers if neglected (Helpline 14567)."
    },
    "DISABILITY_RIGHTS_RPWD": {
        "id": "DISABILITY_RIGHTS_RPWD",
        "title": "Rights of Persons with Disabilities Act, 2016 (RPwD Act)",
        "issuing_authority": "Department of Empowerment of Persons with Disabilities, Ministry of Social Justice and Empowerment",
        "jurisdiction": "All India",
        "official_url": "https://www.indiacode.nic.in/handle/123456789/2237",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["disability_rights", "accessibility", "reservation"],
        "key_provisions": [
            "Section 3: Equality and non-discrimination for persons with disabilities.",
            "Section 20 & 21: Non-discrimination in government and private employment; reasonable accommodation.",
            "Section 75 & 80: State Commissioner for Persons with Disabilities has power to investigate deprivation of rights."
        ],
        "summary_mr": "दिव्यांग व्यक्तींशी कोणताही भेदभाव करण्यास सक्त मनाई आहे. नोकरी व शिक्षणात समान संधी आणि तक्रारीसाठी दिव्यांग आयुक्तांचे कार्यालय आहे.",
        "summary_hi": "दिव्यांग व्यक्तियों के साथ किसी भी प्रकार का भेदभाव गैरकानूनी है। समान अवसर और अधिकारों की रक्षा के लिए दिव्यांग आयुक्त नियुक्त हैं।",
        "summary_en": "Guarantees equality, non-discrimination, and reasonable accommodation for persons with disabilities before the Disability Commissioner."
    },
    "GOVT_BENEFITS_NFSA": {
        "id": "GOVT_BENEFITS_NFSA",
        "title": "National Food Security Act, 2013 & Central Grievance Redressal (CPGRAMS)",
        "issuing_authority": "Ministry of Consumer Affairs, Food & Public Distribution and DARPG",
        "jurisdiction": "All India",
        "official_url": "https://www.indiacode.nic.in/handle/123456789/2123",
        "portal_url": "https://pgportal.gov.in",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["government_benefits", "ration_card", "welfare_schemes"],
        "key_provisions": [
            "Section 14 & 15: District Grievance Redressal Officer (DGRO) for redressing ration and food security complaints.",
            "CPGRAMS Portal (pgportal.gov.in): Centralized public grievance redress and monitoring system for central and state schemes.",
            "Right to reasons in writing for denial of eligible scheme benefits."
        ],
        "summary_mr": "राशन किंवा सरकारी योजनेचा लाभ नाकारल्यास जिल्हा तक्रार निवारण अधिकारी किंवा CPGRAMS (pgportal.gov.in) वर ऑनलाइन तक्रार करता येते.",
        "summary_hi": "राशन या सरकारी योजना से वंचित किए जाने पर जिला शिकायत निवारण अधिकारी या CPGRAMS पोर्टल पर ऑनलाइन शिकायत दर्ज की जा सकती है।",
        "summary_en": "Denial of ration or welfare benefits can be escalated to the District Grievance Redressal Officer (DGRO) or via CPGRAMS (pgportal.gov.in)."
    },
    "LAND_AGRICULTURAL_DISPUTES": {
        "id": "LAND_AGRICULTURAL_DISPUTES",
        "title": "State Land Revenue Codes (e.g. Maharashtra Land Revenue Code, 1966) & Specific Relief Act",
        "issuing_authority": "State Revenue Departments & High Courts",
        "jurisdiction": "State-specific (e.g. Maharashtra, Uttar Pradesh, Punjab, Bihar)",
        "official_url": "https://www.indiacode.nic.in/handle/123456789/1583",
        "portal_url": "https://bhulekh.gov.in",
        "verification_status": "VERIFIED_OFFICIAL",
        "retrieval_date": "2026-10-26",
        "categories": ["land_disputes", "farmer_rights", "property_boundary"],
        "key_provisions": [
            "Demarcation & Boundary Disputes: Tahsildar / Taluk Executive Magistrate has jurisdiction under Land Revenue Code.",
            "Record of Rights (7/12 Extract / Khatauni): Mutation entries under Revenue Authority with appeal to Sub-Divisional Officer (SDO).",
            "Title & Possession Disputes: Civil Court has exclusive jurisdiction for permanent injunction or declaration of ownership under Specific Relief Act.",
            "Mamlatdar's Courts Act (in Maharashtra/Gujarat): Summary proceedings for removal of obstruction to agricultural way/road."
        ],
        "summary_mr": "जमीन मोजणी किंवा शेतीचा रस्ता अडवल्यास तहसीलदार किंवा मामलेदार न्यायालयात अर्ज करता येतो. मालकी हक्काच्या वादासाठी दिवाणी न्यायालय असते.",
        "summary_hi": "जमीन सीमांकन या रास्ते के विवाद में तहसीलदार या राजस्व अधिकारी के पास आवेदन किया जाता है। मालिकाना हक के लिए दीवानी अदालत में जाना होता है।",
        "summary_en": "Boundary and agricultural pathway disputes are handled by the Tahsildar/Revenue Court; ownership and title disputes require Civil Court."
    }
}
