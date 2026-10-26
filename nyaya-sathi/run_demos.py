"""
Automated Hackathon Demonstration Script for Nyaya Sathi.
Simulates and displays the complete end-to-end user journeys for:
- DEMO A: Unpaid Wages (in Marathi) with Plain Explanation & Complaint Drafting
- DEMO B: Understanding a Government Notice with Explicit Deadlines & Glossary
- DEMO C: Finding Free Legal Aid under Section 12 with Pune DLSA Verification
"""

import sys
import os
import json
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.legal_kb.rag_engine import LegalRAGEngine
from app.complaints.complaint_generator import ComplaintGenerator
from app.document_explainer.doc_analyzer import DocumentAnalyzer
from app.document_explainer.sample_notices import SAMPLE_NOTICES
from app.legal_aid.legal_aid_service import LegalAidService

def print_separator(title=""):
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)

def run_demo_a():
    print_separator("DEMO A: UNPAID WAGES (मराठी कामगार - थकीत वेतन)")
    print("👤 USER: रुपेश तुकाराम पाटील (कारखाना कामगार / Assembly Operator, भोसरी MIDC)")
    user_input = "मी गेल्या दोन महिन्यांपासून एका कारखान्यात काम करत आहे, पण मालकाने अजूनही माझा पगार दिलेला नाही. मी काय करू शकतो?"
    print(f"🎙️ VOICE INPUT (Marathi): \"{user_input}\"")

    rag = LegalRAGEngine()
    result = rag.retrieve(user_input)

    print("\n[१] न्याय साथी कायदेशीर माहिती विश्लेषण:")
    print(f"• ओळखलेला विषय: {result['domain_name']}")
    print(f"• सोप्या भाषेत स्पष्टीकरण: {result['plain_language_summary']}")
    print(f"• अधिकृत कायदा व तरतूद: {result['official_citation']['title']}")
    print(f"• तक्रार निवारण पोर्टल: {result['official_citation']['portal_url']}")

    print("\n[२] विचारलेले पूरक प्रश्न (Clarifying Questions):")
    for idx, q in enumerate(result['clarifying_questions'][:3], 1):
        print(f"  {idx}. {q}")

    print("\n[३] सुचवलेली पुढील पावले (Action Steps):")
    for step in result['action_steps']:
        print(f"  पायरी {step['step']}: {step['action']}")

    # Generate Complaint
    comp_gen = ComplaintGenerator()
    draft = comp_gen.generate_complaint(
        complainant_name="रुपेश तुकाराम पाटील",
        complainant_address="घर क्र. १२, भोसरी एमआयडीसी, पुणे - ४११०२६",
        complainant_phone="९८२२००११२२",
        opposite_party_name="सनशाईन मॅन्युफॅक्चरिंग प्रा. लि.",
        opposite_party_address="प्लॉट क्र. ५२, सेक्टर बी, एमआयडीसी भोसरी, पुणे",
        matter_type="unpaid_wages",
        dates_involved="१ ऑगस्ट २०२६ ते ३० सप्टेंबर २०२६",
        factual_summary="मी असेंब्ली विभागात काम करतो. ऑगस्ट व सप्टेंबर २०२६ या दोन महिन्यांचे एकूण ४५,००० रुपये वेतन थकीत आहे.",
        prior_action_taken="सुपरवायझर आणि एचआर यांना तोंडी विनंती केली, पण दखल घेतली नाही.",
        requested_relief="थकीत ४५,००० रुपये तात्काळ बँक खात्यात जमा करावेत.",
        language="mr-IN"
    )

    print("\n[४] तयार झालेला तक्रार मसुदा (Complaint Representation):")
    print(draft['short_portal_version_mr'])
    print("\n[५] जोडायच्या पुराव्यांची यादी (Checklist):")
    for doc in draft['supporting_documents_checklist']:
        print(f"  ☑️ {doc}")
    print(f"• अधिकृत सादर करण्याचा मार्ग: {draft['submission_channel']['channel_mr']}")

def run_demo_b():
    print_separator("DEMO B: UNDERSTANDING A GOVERNMENT NOTICE (कागदपत्र स्पष्टीकरण)")
    print("👤 USER: दुकानदार / नागरिक, पुणे")
    sample = SAMPLE_NOTICES["MUNICIPAL_SHOW_CAUSE"]
    print(f"📄 UPLOADED DOCUMENT: {sample['title']}")

    analyzer = DocumentAnalyzer()
    analysis = analyzer.analyze_document(sample['raw_text'], user_language="mr-IN")

    print("\n[१] दस्तऐवजाचा प्रकार व सोपा सारांश:")
    print(f"• प्रकार: {analysis['apparent_document_type']}")
    print(f"• सारांश: {analysis['plain_summary']}")

    print("\n[२] मुदतीचे विश्लेषण (Explicit vs Inferred Deadlines):")
    print("• कागदपत्रात स्पष्ट छापलेली मुदत:")
    for d in analysis['deadlines_analysis']['explicitly_printed_deadlines']:
        print(f"  - {d}")
    print("• कायदेशीर नियम:")
    for rule in analysis['deadlines_analysis']['inferred_legal_rule']:
        print(f"  - {rule}")

    print("\n[३] कठीण कायदेशीर शब्दांचे सोपे अर्थ (Legal Glossary):")
    for t in analysis['legal_terms_explained']:
        print(f"• {t['term']}: {t['explanation']}")

    print("\n[४] विधी सेवा वकिलांना विचारण्यासाठी महत्त्वाचे प्रश्न:")
    for q in analysis['questions_for_lawyer']:
        print(f"  {q}")

def run_demo_c():
    print_separator("DEMO C: FINDING FREE LEGAL AID (मोफत विधी सेवा - कलम १२)")
    print("👤 USER: सुनीता कांबळे (गृहिणी, पुणे जिल्हा)")
    print("📌 चौकशी: न्यायालयात कौटुंबिक किंवा मालमत्ता वाद सुरू असून खासगी वकील परवडत नाही.")

    service = LegalAidService()
    eligibility = service.evaluate_eligibility(category="woman", state="Maharashtra")

    print("\n[१] विधी सेवा प्राधिकरण कायदा, १९८७ अंतर्गत पात्रता तपासणी:")
    print(f"• पात्रता स्थिती: {'पात्र (Eligible)' if eligibility['is_eligible'] else 'अपात्र'}")
    print(f"• लागू कायदेशीर कलम: {eligibility['statutory_clause']}")
    print(f"• कारण: {eligibility['explanation']}")

    print("\n[२] कायद्यानुसार मिळणारे मोफत हक्क:")
    for ent in eligibility['free_entitlements']:
        print(f"  🎁 {ent}")

    contacts = service.get_contacts(state="Maharashtra", district="pune")
    dlsa = contacts['district_authority']
    print("\n[३] पुणे जिल्हा विधी सेवा प्राधिकरण (DLSA) अधिकृत संपर्क:")
    print(f"• कार्यालय: {dlsa['name']}")
    print(f"• पत्ता: {dlsa['address']}")
    print(f"• फोन: {dlsa['phone']}")
    print(f"• कामकाज वेळ: {dlsa.get('working_hours', '१०:३० ते ५:३०')}")
    print(f"• राष्ट्रीय टोल-फ्री हेल्पलाइन: {contacts['emergency_legal_helpline']} (15100)")

if __name__ == "__main__":
    print("======================================================================")
    print("          NYAYA SATHI - LIVE HACKATHON DEMONSTRATION RUNNER           ")
    print("======================================================================")
    run_demo_a()
    run_demo_b()
    run_demo_c()
    print_separator("ALL 3 HACKATHON DEMONSTRATIONS EXECUTED SUCCESSFULLY")
