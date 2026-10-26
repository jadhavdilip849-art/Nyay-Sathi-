"""
Legal Aid Service for Nyaya Sathi.
Implements statutory eligibility evaluation under Section 12 of the Legal Services Authorities Act, 1987,
and provides verified contact directories for NALSA, SLSAs, and DLSAs.
"""

from typing import Dict, List, Any, Optional

STATE_INCOME_LIMITS = {
    "Maharashtra": 300000,
    "Delhi": 400000,
    "Karnataka": 300000,
    "Uttar Pradesh": 300000,
    "Tamil Nadu": 300000,
    "General / Other States": 300000
}

LEGAL_AID_DIRECTORY = {
    "NALSA": {
        "name": "National Legal Services Authority (NALSA)",
        "level": "National",
        "address": "12/11 Jam Nagar House, Shahjahan Road, New Delhi - 110011",
        "helpline": "15100 (Toll-Free 24x7 National Legal Aid Helpline)",
        "phone": "011-23382778",
        "email": "nalsa-dla@nic.in",
        "portal": "https://nalsa.gov.in",
        "services": [
            "Assignment of Free Panel Lawyer",
            "Payment of Court & Process Fees",
            "Preparation of Legal Briefs and Paper-books",
            "National Lok Adalat Settlement"
        ]
    },
    "Maharashtra": {
        "slsa": {
            "name": "Maharashtra State Legal Services Authority (MSLSA)",
            "address": "105, High Court P.W.D. Building, Fort, Mumbai - 400032",
            "phone": "022-22691395 / 022-22673962",
            "email": "mslsa-bhc@nic.in",
            "portal": "https://legalservices.maharashtra.gov.in"
        },
        "districts": {
            "pune": {
                "name": "District Legal Services Authority (DLSA), Pune",
                "district": "Pune",
                "address": "Ground Floor, New Building, District and Sessions Court, Shivajinagar, Pune - 411005",
                "phone": "020-25537550",
                "email": "dlsa.pune@maharashtra.gov.in",
                "working_hours": "10:30 AM to 5:30 PM (Monday to Saturday, except 2nd/4th Saturdays)"
            },
            "mumbai": {
                "name": "District Legal Services Authority (DLSA), Mumbai City",
                "district": "Mumbai City",
                "address": "City Civil & Sessions Court, Old Secretariat Building, Fort, Mumbai - 400032",
                "phone": "022-22676644",
                "email": "dlsa.mumbaicity@maharashtra.gov.in"
            },
            "mumbai_suburban": {
                "name": "District Legal Services Authority (DLSA), Mumbai Suburban",
                "district": "Mumbai Suburban",
                "address": "District Court Complex, Station Road, Bandra (East), Mumbai - 400051",
                "phone": "022-26556100",
                "email": "dlsa.mumbaisuburban@maharashtra.gov.in"
            },
            "nagpur": {
                "name": "District Legal Services Authority (DLSA), Nagpur",
                "district": "Nagpur",
                "address": "District Court Building, Civil Lines, Nagpur - 440001",
                "phone": "0712-2565152",
                "email": "dlsa.nagpur@maharashtra.gov.in"
            },
            "nashik": {
                "name": "District Legal Services Authority (DLSA), Nashik",
                "district": "Nashik",
                "address": "District Court Campus, Old Agra Road, Nashik - 422002",
                "phone": "0253-2578500",
                "email": "dlsa.nashik@maharashtra.gov.in"
            },
            "chhatrapati_sambhajinagar": {
                "name": "District Legal Services Authority (DLSA), Chhatrapati Sambhajinagar",
                "district": "Chhatrapati Sambhajinagar (Aurangabad)",
                "address": "District Court Premises, Adalat Road, Chhatrapati Sambhajinagar - 431005",
                "phone": "0240-2334810",
                "email": "dlsa.aurangabad@maharashtra.gov.in"
            }
        }
    },
    "Delhi": {
        "slsa": {
            "name": "Delhi State Legal Services Authority (DSLSA)",
            "address": "Central Office, Patiala House Courts, New Delhi - 110001",
            "phone": "011-23384781",
            "helpline": "1516 (24x7 Delhi Toll-Free Helpline)",
            "email": "dslsa-phc@nic.in",
            "portal": "https://dslsa.org"
        },
        "districts": {
            "central_delhi": {
                "name": "DLSA Central Delhi",
                "district": "Central Delhi",
                "address": "Tis Hazari Courts Complex, Delhi - 110054",
                "phone": "011-23968052"
            },
            "new_delhi": {
                "name": "DLSA New Delhi",
                "district": "New Delhi",
                "address": "Patiala House Courts, New Delhi - 110001",
                "phone": "011-23072352"
            },
            "south_delhi": {
                "name": "DLSA South Delhi",
                "district": "South Delhi",
                "address": "Saket Courts Complex, New Delhi - 110017",
                "phone": "011-29562205"
            }
        }
    },
    "Karnataka": {
        "slsa": {
            "name": "Karnataka State Legal Services Authority (KSLSA)",
            "address": "Nyaya Degula, 1st Floor, Siddaiah Road, Bangalore - 560027",
            "phone": "080-22111725",
            "email": "kslsa.kar@nic.in",
            "portal": "https://kslsa.kar.nic.in"
        },
        "districts": {
            "bangalore_urban": {
                "name": "DLSA Bengaluru Urban",
                "district": "Bengaluru Urban",
                "address": "City Civil Court Complex, KG Road, Bengaluru - 560009",
                "phone": "080-22210080"
            }
        }
    },
    "Uttar Pradesh": {
        "slsa": {
            "name": "Uttar Pradesh State Legal Services Authority (UPSLSA)",
            "address": "3rd Floor, Jawahar Bhawan Annexe, Lucknow - 226001",
            "phone": "0522-2287972",
            "email": "upslsa@nic.in",
            "portal": "https://upslsa.up.gov.in"
        },
        "districts": {
            "lucknow": {
                "name": "DLSA Lucknow",
                "district": "Lucknow",
                "address": "District Court Building, Qaiserbagh, Lucknow - 226001",
                "phone": "0522-2616422"
            }
        }
    }
}

class LegalAidService:
    """Service to evaluate statutory legal aid qualification and retrieve official DLSA/SLSA details."""

    def evaluate_eligibility(
        self,
        category: str,
        annual_income: Optional[float] = None,
        state: str = "Maharashtra"
    ) -> Dict[str, Any]:
        """
        Evaluates eligibility under Section 12 of Legal Services Authorities Act, 1987.
        Categories: woman, child, sc_st, industrial_workman, disabled, custody, disaster_victim, low_income
        """
        statutory_provisions = {
            "woman": ("Section 12(c)", "Women are automatically eligible for free legal aid regardless of income limit in most states."),
            "child": ("Section 12(c)", "Children below 18 years are automatically eligible for free legal representation."),
            "sc_st": ("Section 12(a)", "Members of Scheduled Castes (SC) or Scheduled Tribes (ST) are eligible under statute."),
            "industrial_workman": ("Section 12(e)", "Industrial workmen / laborers are entitled to free legal aid for employment and civil matters."),
            "disabled": ("Section 12(d)", "Persons with disabilities under the RPwD Act are eligible under Section 12(d)."),
            "custody": ("Section 12(g)", "Persons in judicial or police custody or in protective homes qualify automatically."),
            "disaster_victim": ("Section 12(b)", "Victims of mass disaster, caste atrocity, flood, earthquake or industrial accident qualify."),
            "low_income": ("Section 12(h)", f"Citizens whose annual family income is below Rs. {STATE_INCOME_LIMITS.get(state, 300000):,} are eligible.")
        }

        limit = STATE_INCOME_LIMITS.get(state, 300000)
        is_eligible = False
        reasons = []
        clause = "Section 12"

        if category in ["woman", "child", "sc_st", "industrial_workman", "disabled", "custody", "disaster_victim"]:
            is_eligible = True
            sec, desc = statutory_provisions[category]
            clause = sec
            reasons.append(desc)
        elif category == "low_income" or (annual_income is not None):
            clause = "Section 12(h)"
            if annual_income is not None and annual_income <= limit:
                is_eligible = True
                reasons.append(f"वार्षिक उत्पन्न रु. {annual_income:,.0f} हे {state} मधील कायदेशीर मर्यादा रु. {limit:,} पेक्षा कमी असल्याने आपण विधी सेवा प्राधिकरण कायद्याच्या कलम १२(h) नुसार पात्र आहात.")
            elif annual_income is not None:
                is_eligible = False
                reasons.append(f"वार्षिक उत्पन्न रु. {annual_income:,.0f} हे विहित उत्पन्न मर्यादा रु. {limit:,} पेक्षा जास्त असल्यास नियमित उत्पन्नाच्या निकषावर मदत मिळत नाही; मात्र महिला, कामगार, दिव्यांग किंवा एससी/एसटी प्रवर्गात असल्यास उत्पन्न विचारात घेतले जात नाही.")
            else:
                is_eligible = True
                reasons.append(f"कुटुंबाचे वार्षिक उत्पन्न रु. {limit:,} च्या आत असल्यास आपण पात्र ठरता.")

        return {
            "is_eligible": is_eligible,
            "statutory_clause": clause,
            "act_name": "Legal Services Authorities Act, 1987",
            "state": state,
            "income_threshold": limit,
            "explanation": " ".join(reasons),
            "free_entitlements": [
                "मोफत न्यायालयीन फी व अर्ज फी (Exemption from Court Fees)",
                "मोफत अधिकृत पॅनेल वकील (Free Assigned Panel Advocate)",
                "खटल्याच्या कागदपत्रांचे व पुराव्यांचे मोफत टंकलेखन व छायाप्रती (Drafting & Typing expenses)",
                "प्रमाणित प्रती मोफत मिळणे (Free Certified Copies of orders)"
            ],
            "documents_required": [
                "ओळख पुरावा (आधार / मतदार ओळखपत्र / रेशन कार्ड)",
                "उत्पन्नाचा दाखला (केवळ उत्पन्न निकषावर अर्ज करत असल्यास, महिला किंवा कामगारांना सक्ती नाही)",
                "खटल्याशी संबंधित प्राथमिक कागदपत्रे किंवा नोटीस"
            ],
            "how_to_apply": [
                "पायरी १: राष्ट्रीय हेल्पलाइन १५१०० वर मोफत कॉल करा किंवा nalsa.gov.in वर ऑनलाइन अर्ज भरा.",
                "पायरी २: आपल्या तालुका किंवा जिल्हा न्यायालयातील DLSA कार्यालयात प्रत्यक्ष भेट द्या.",
                "पायरी ३: अर्ज सादर केल्यावर सचिव (जिल्हा न्यायाधीश दर्जाचे अधिकारी) कागदपत्रांची पडताळणी करून वकील नेमून देतात."
            ]
        }

    def get_contacts(self, state: str = "Maharashtra", district: Optional[str] = None) -> Dict[str, Any]:
        """Retrieves official contacts for the requested state and district."""
        state_data = LEGAL_AID_DIRECTORY.get(state, LEGAL_AID_DIRECTORY["Maharashtra"])
        nalsa = LEGAL_AID_DIRECTORY["NALSA"]
        
        district_key = (district or "pune").lower().replace(" ", "_")
        district_data = None
        
        if "districts" in state_data:
            district_data = state_data["districts"].get(district_key)
            if not district_data:
                # Default to first district available in that state
                first_key = list(state_data["districts"].keys())[0]
                district_data = state_data["districts"][first_key]

        return {
            "national": nalsa,
            "state_authority": state_data.get("slsa"),
            "district_authority": district_data,
            "emergency_legal_helpline": "15100",
            "online_portal": "https://nalsa.gov.in"
        }
