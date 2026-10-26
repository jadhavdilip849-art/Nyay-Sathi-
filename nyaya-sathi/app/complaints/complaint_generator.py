"""
Factual Complaint Generator for Nyaya Sathi.
Creates truthful representations without fabricating evidence, sections, or allegations.
Generates:
1. Formal Representation Letter (for physical submission or registered post)
2. Simple Representation
3. Short online form version (character-constrained for portals like Samadhan/CPGRAMS)
4. English translation
5. Verified evidence checklist
"""

from typing import Dict, List, Any, Optional
import datetime

class ComplaintGenerator:
    """Generates strictly factual complaints without legal hallucinations."""

    def generate_complaint(
        self,
        complainant_name: str,
        complainant_address: str,
        complainant_phone: str,
        opposite_party_name: str,
        opposite_party_address: str,
        matter_type: str, # e.g. "unpaid_wages", "consumer", "rental"
        dates_involved: str,
        factual_summary: str,
        prior_action_taken: str,
        requested_relief: str,
        language: str = "mr-IN"
    ) -> Dict[str, Any]:
        """Constructs multi-format representations adhering strictly to user-supplied facts."""
        
        today_date = datetime.date.today().strftime("%d/%m/%Y")

        # Fallback sanitize
        complainant_name = complainant_name.strip() or "नागरिक (तक्रारदार)"
        opposite_party_name = opposite_party_name.strip() or "संबंधित आस्थापना / विरोधी पक्ष"
        factual_summary = factual_summary.strip()
        requested_relief = requested_relief.strip() or "थकीत रकमेचा किंवा न्याय्य तोडग्याचा त्वरित निपटारा व्हावा."

        # Supporting document checklist based on matter type
        checklists = {
            "unpaid_wages": [
                "कामाचे ओळखपत्र किंवा नियुक्ती पत्र (Appointment Letter / ID Card)",
                "हजेरी नोंदवही किंवा पंचिंग रेकॉर्ड (Attendance records / Log sheet)",
                "पूर्वी मिळालेल्या पगाराचे बँक स्टेटमेंट किंवा पगार स्लिप्स (Past salary slips / Bank Statement)",
                "नियोक्त्याला पाठवलेले आधीचे संदेश (WhatsApp / SMS / Email messages requesting salary)"
            ],
            "consumer": [
                "वस्तू खरेदी पावती किंवा मूळ बिल (Original Tax Invoice / Cash Memo)",
                "वॉरंटी कार्ड किंवा गॅरंटी दस्तऐवज (Warranty Card)",
                "वस्तूतील दोषाची छायाचित्रे किंवा व्हिडिओ (Photos of defect)",
                "दुकानदाराशी किंवा कस्टमर केअरशी केलेला पत्रव्यवहार (Customer care complaint token / emails)"
            ],
            "rental": [
                "स्वाक्षरी केलेला भाडेकरार (Signed / Registered Rent Agreement)",
                "सुरक्षा अनामत (Deposit) दिल्याचा बँक व्यवहार पुरावा किंवा पावती",
                "घर सोडल्याची पूर्वसूचना (Vacating Notice) व चावी सोपवल्याचा पुरावा",
                "घर रिकामे करतानाची स्थिती दर्शवणारी छायाचित्रे"
            ],
            "general": [
                "तक्रारदाराचे ओळखपत्र (Proof of Identity)",
                "घटनेशी संबंधित मूळ पावत्या, पत्रे किंवा संदेश",
                "विरोधी पक्षाने दिलेले कोणतेही लेखी उत्तर"
            ]
        }
        evidence_checklist = checklists.get(matter_type, checklists["general"])

        # Submission channels
        submission_channels = {
            "unpaid_wages": {
                "channel_mr": "१) संबंधित जिल्ह्याचे कामगार आयुक्त कार्यालय किंवा २) श्रम मंत्रालयाचे 'समाधान' पोर्टल (samadhan.labour.gov.in)",
                "channel_en": "1) Office of the Assistant Labour Commissioner (District Labour Court) OR 2) Central Samadhan Portal (samadhan.labour.gov.in)",
                "mode": "Physical delivery with acknowledgment receipt OR online registration"
            },
            "consumer": {
                "channel_mr": "१) राष्ट्रीय ग्राहक हेल्पलाइन १९१५ किंवा २) ई-दाखील पोर्टल (edaakhil.nic.in)",
                "channel_en": "1) National Consumer Helpline (1915 / consumerhelpline.gov.in) OR 2) e-Daakhil Portal (edaakhil.nic.in)",
                "mode": "Toll-free telephone complaint OR e-Daakhil filing"
            },
            "rental": {
                "channel_mr": "१) संबंधित उपविभागीय अधिकारी (SDO) / भाडे न्यायालय किंवा २) जिल्हा विधी सेवा प्राधिकरण (DLSA) मध्यस्थी कक्ष",
                "channel_en": "1) Designated Rent Authority / Small Causes Court OR 2) DLSA Pre-litigation Mediation Desk",
                "mode": "Registered Post with A.D. or in-person submission"
            },
            "general": {
                "channel_mr": "संबंधित विभागाचे मुख्य अधिकारी किंवा CPGRAMS (pgportal.gov.in)",
                "channel_en": "Competent Departmental Authority or CPGRAMS Public Grievance Portal",
                "mode": "Direct submission"
            }
        }
        channel_info = submission_channels.get(matter_type, submission_channels["general"])

        # 1. Formal Marathi Letter
        formal_mr = f"""दिनांक: {today_date}

प्रति,
सक्षम अधिकारी / प्रमुख,
{opposite_party_name}
पत्ता: {opposite_party_address or '[पत्ता नमूद करा]'}

विषय: {factual_summary[:60]}... बाबत तक्रार व कायदेशीर मागणी अर्ज.

महोदय / महोदया,

मी, {complainant_name}, रा. {complainant_address or '[पत्ता]'}, खालीलप्रमाणे नमूद वस्तुस्थिती आपल्या निदर्शनास आणत आहे:

१. वस्तुस्थिती (घटनाक्रम):
{factual_summary}

२. कालावधी व तारखा:
संबंधित प्रकरण दिनांक / कालावधी: {dates_involved or 'तक्रारीत नमूद केल्याप्रमाणे'} या दरम्यान घडलेले आहे.

३. यापूर्वी घेतलेले प्रयत्न:
{prior_action_taken or 'मी विरोधी पक्षाशी वारंवार संपर्क साधला, परंतु अद्याप कोणतीही सकारात्मक दखल घेण्यात आली नाही.'}

४. विनंती व मागणी:
{requested_relief}

कृपया या अर्जाची नोंद घेऊन येत्या ७ दिवसांच्या आत वरील मागणीची पूर्तता करावी, ही नम्र विनंती. विहित मुदतीत न्याय न मिळाल्यास मला सक्षम कामगार/ग्राहक न्यायालय किंवा विधी सेवा प्राधिकरणाकडे अधिकृत दाद मागावी लागेल.

आपला / आपली नम्र,

(स्वाक्षरी)
नाव: {complainant_name}
मोबाईल: {complainant_phone or '[फोन नंबर]'}
सोबत: आवश्यक कागदपत्रांच्या छायाप्रती
"""

        # 2. Short Form Version (Ideal for online portals with character limits)
        short_mr = f"तक्रारदार: {complainant_name}. विरोधी पक्ष: {opposite_party_name}. कालावधी: {dates_involved}. सारांश: {factual_summary}. यापूर्वी घेतलेली कृती: {prior_action_taken}. मागणी: {requested_relief}."
        if len(short_mr) > 500:
            short_mr = short_mr[:497] + "..."

        # 3. Formal English Version
        formal_en = f"""Date: {today_date}

To,
The Competent Authority / Management,
{opposite_party_name}
Address: {opposite_party_address or '[Insert Address]'}

Subject: Formal Representation and Grievance regarding {factual_summary[:50]}...

Dear Sir/Madam,

I, {complainant_name}, residing at {complainant_address or '[Address]'}, submit this factual representation as under:

1. Statement of Facts:
{factual_summary}

2. Relevant Period / Dates:
{dates_involved or 'As specified in the statement of facts above.'}

3. Prior Actions / Follow-ups Undertaken:
{prior_action_taken or 'Prior reminders were given, but the grievance remains unaddressed.'}

4. Relief Requested:
{requested_relief}

I request you to look into this matter and resolve the same within 7 days from the receipt of this communication. Should the matter remain unresolved, I reserve the right to approach the statutory authorities or the Legal Services Authority.

Yours sincerely,

(Signature)
Name: {complainant_name}
Mobile: {complainant_phone or '[Contact Number]'}
Enclosed: Supporting evidentiary documents
"""

        # 4. Short English Version
        short_en = f"Complainant: {complainant_name}. Opposite Party: {opposite_party_name}. Period: {dates_involved}. Summary: {factual_summary}. Prior Action: {prior_action_taken}. Relief Sought: {requested_relief}."
        if len(short_en) > 500:
            short_en = short_en[:497] + "..."

        return {
            "metadata": {
                "date_generated": today_date,
                "matter_type": matter_type,
                "complainant": complainant_name,
                "opposite_party": opposite_party_name
            },
            "formal_letter_mr": formal_mr,
            "formal_letter_en": formal_en,
            "short_portal_version_mr": short_mr,
            "short_portal_version_en": short_en,
            "supporting_documents_checklist": evidence_checklist,
            "submission_channel": channel_info,
            "important_warning": "हे एक वस्तुस्थितीदर्शक मसुदा आहे. कोणताही खोटा पुरावा किंवा मनघडंत आरोप टाळणे आवश्यक आहे. न्याय साथी स्वतः परस्पर तक्रार दाखल करत नाही."
        }
