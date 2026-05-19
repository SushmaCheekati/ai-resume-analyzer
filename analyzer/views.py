from random import random

from django.shortcuts import render

from .forms import ResumeForm
import PyPDF2
import docx2txt
<<<<<<< HEAD
import pdfplumber
import docx
=======
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Resume
import re
<<<<<<< HEAD
#import spacy
import json
=======
import spacy
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from xhtml2pdf import pisa

<<<<<<< HEAD
import google.generativeai as genai
=======
from openai import OpenAI
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
from dotenv import load_dotenv
import os
from django.shortcuts import render, redirect
import re
from django.contrib import messages
<<<<<<< HEAD
import logging

logger = logging.getLogger(__name__)

load_dotenv()
# Also search in the analyzer directory
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Configure Gemini API safely
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    genai.configure(api_key=gemini_key)
else:
    logger.warning("GEMINI_API_KEY environment variable is not set.")


#nlp = spacy.load("en_core_web_sm")
=======

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

nlp = spacy.load("en_core_web_sm")
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487

# Skills list
skills = {
    "python": 15,
    "django": 20,
    "java": 10,
    "sql": 10,
    "html": 5,
    "css": 5,
    "javascript": 10,
    "machine learning": 25
}

def generate_interview_questions(career):

    if career == "Machine Learning Engineer":

        return [

            "What is supervised learning?",

            "Explain overfitting in machine learning.",

            "What is the difference between TensorFlow and PyTorch?",

            "Explain classification and regression."

        ]

    elif career == "Frontend Developer":

        return [

            "What is the difference between HTML and HTML5?",

            "Explain CSS Flexbox.",

            "What is JavaScript DOM?",

            "Difference between inline and block elements."

        ]

    else:

        return [

            "Explain OOP concepts.",

            "What is SQL JOIN?",

            "Difference between list and tuple in Python?",

            "What is Django framework?"

        ]

# Home Page View
@login_required
def upload_resume(request):

    if request.method == 'POST':

        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():

            resume = form.save(commit=False)

            resume.user = request.user

            resume.save()

            file_path = resume.resume_file.path
<<<<<<< HEAD
            print(f"\n=========================================\n[DEBUG] 1. STARTING UPLOAD ROUTE\n[DEBUG] File Path: {file_path}")

            extracted_text = extract_resume_text(file_path)
            print(f"[DEBUG] 2. EXTRACTED TEXT LENGTH: {len(extracted_text)}")
            if len(extracted_text) < 100:
                print(f"[DEBUG] WARNING: Extracted text is unusually short: {extracted_text}")

            print("[DEBUG] 3. CALLING analyze_resume()...")
            result = analyze_resume(extracted_text)
            print(f"[DEBUG] 8. RETURNED FROM analyze_resume(). Final career: {result['career']}")
=======

            extracted_text = extract_resume_text(file_path)

            result = analyze_resume(extracted_text)
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487

            info = extract_information(extracted_text)

            resume.score = result['score']
<<<<<<< HEAD
            resume.career = result['career']
            resume.found_skills = ",".join(result['found_skills'])
            resume.missing_skills = ",".join(result['missing_skills'])
            resume.recommendations = " | ".join(result['recommendations'])
            resume.improvements = " | ".join(result['improvements'])
            
            # Save our new granular parsing & AI feedback fields
            resume.email = info.get('email', '') or ''
            resume.phone = info.get('phone', '') or ''
            resume.education = "\n".join(info.get('education', [])) if isinstance(info.get('education'), list) else (info.get('education', '') or '')
            resume.experience = "\n".join(info.get('experience', [])) if isinstance(info.get('experience'), list) else (info.get('experience', '') or '')
            resume.projects = "\n".join(info.get('projects', [])) if isinstance(info.get('projects'), list) else (info.get('projects', '') or '')
            resume.certifications = "\n".join(info.get('certifications', [])) if isinstance(info.get('certifications'), list) else (info.get('certifications', '') or '')
            resume.interview_questions = result.get('interview_questions', '') or ''
            resume.ai_feedback = result.get('ai_feedback', '') or ''
=======

            resume.career = result['career']

            resume.found_skills = ",".join(
                result['found_skills']
            )

            resume.missing_skills = ",".join(
                result['missing_skills']
            )

            resume.recommendations = " | ".join(
                result['recommendations']
            )

            resume.improvements = " | ".join(
                result['improvements']
            )
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487

            resume.save()

            return render(request, 'success.html', {

                'result': result,

                'info': info,

                'resume': resume

            })

    else:
        form = ResumeForm()

    return render(request, 'upload.html', {'form': form})


# Function to extract text from resume
def extract_resume_text(file_path):
<<<<<<< HEAD
    text = ""
    
    # For PDF files
    if file_path.endswith('.pdf'):
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}. Falling back to PyPDF2.")
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
            except Exception as pe:
                logger.error(f"Fallback PyPDF2 extraction also failed: {pe}")
                
    # For DOCX files
    elif file_path.endswith('.docx'):
        try:
            doc_obj = docx.Document(file_path)
            full_text = []
            for para in doc_obj.paragraphs:
                full_text.append(para.text)
            text = '\n'.join(full_text)
        except Exception as e:
            logger.error(f"python-docx extraction failed: {e}. Falling back to docx2txt.")
            try:
                text = docx2txt.process(file_path)
            except Exception as de:
                logger.error(f"Fallback docx2txt extraction also failed: {de}")
                
    return text

# NLP Information Extraction (Local Offline Fallback Parser)
def extract_information(text):
    #doc = nlp(text)
    
    # 1. Name Extraction (using Spacy NER with first-line fallback)
    name = None
    #for ent in doc.ents:
        #if ent.label_ == "PERSON" and len(ent.text.strip()) > 2 and "\n" not in ent.text:
           # name = ent.text.strip()
            #break
            
    if not name:
        # Fallback to the first non-empty line of text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines[:5]:
            # Avoid picking lines that look like email/phone or section headers
            if "@" not in line and not re.search(r'\d', line) and len(line) < 50:
                name = line
                break
        if not name:
            name = "Resume Candidate"

    # 2. Email Extraction
    email = None
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    if email_match:
        email = email_match.group(0).strip()

    # 3. Phone Number Extraction
    phone = None
    phone_match = re.search(r'\+?\d[\d\s\-().]{6,16}\d', text)
    if phone_match:
        phone = phone_match.group(0).strip()

    # 4. Education Extraction
    education_degrees = [
        "B.E", "B.Tech", "M.Tech", "B.S", "M.S", "B.C.A", "M.C.A", "MBA", "Ph.D", 
        "Bachelor", "Master", "Computer Science", "Engineering", "University", "College"
    ]
    education = []
    lines = text.split('\n')
    for line in lines:
        for deg in education_degrees:
            if re.search(r'\b' + re.escape(deg) + r'\b', line, re.IGNORECASE):
                cleaned_line = line.strip()
                if cleaned_line and cleaned_line not in education and len(cleaned_line) < 150:
                    education.append(cleaned_line)
                break
                
    # 5. Experience Extraction
    exp_keywords = ["Developer", "Engineer", "Analyst", "Internship", "Manager", "Consultant", "Specialist", "Lead", "Designer", "Architect"]
    experience = []
    for line in lines:
        for keyword in exp_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', line, re.IGNORECASE):
                cleaned_line = line.strip()
                if cleaned_line and cleaned_line not in experience and len(cleaned_line) < 150:
                    experience.append(cleaned_line)
                break

    # 6. Projects Extraction
    proj_keywords = ["Project", "Github", "Repository", "Application", "Implementation", "System", "Tool"]
    projects = []
    for line in lines:
        for keyword in proj_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', line, re.IGNORECASE):
                cleaned_line = line.strip()
                if cleaned_line and cleaned_line not in projects and len(cleaned_line) < 150:
                    projects.append(cleaned_line)
                break

    # 7. Certifications Extraction
    cert_keywords = ["Certified", "AWS", "Google", "Microsoft", "Oracle", "Scrum", "Certification", "License", "Credential"]
    certifications = []
    for line in lines:
        for keyword in cert_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', line, re.IGNORECASE):
                cleaned_line = line.strip()
                if cleaned_line and cleaned_line not in certifications and len(cleaned_line) < 150:
                    certifications.append(cleaned_line)
                break

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'education': education[:4] if education else ["Not detected"],
        'experience': experience[:4] if experience else ["Not detected"],
        'projects': projects[:4] if projects else ["Not detected"],
        'certifications': certifications[:3] if certifications else ["Not detected"]
=======

    text = ""

    # For PDF files
    if file_path.endswith('.pdf'):

        with open(file_path, 'rb') as file:

            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

    # For DOCX files
    elif file_path.endswith('.docx'):

        text = docx2txt.process(file_path)

    return text
# NLP Information Extraction
def extract_information(text):

    doc = nlp(text)

    # Email Extraction
    email = None

    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)

    if email_match:
        email = email_match.group(0)

    # Phone Number Extraction
    phone = None

    phone_match = re.search(r'\+?\d[\d -]{8,12}\d', text)

    if phone_match:
        phone = phone_match.group(0)

    # Education Extraction
    education_keywords = [
        "B.E",
        "B.Tech",
        "M.Tech",
        "Bachelor",
        "Master",
        "Computer Science",
        "Engineering"
    ]

    education = []

    for word in education_keywords:

        if word.lower() in text.lower():

            education.append(word)

    return {
        'email': email,
        'phone': phone,
        'education': education
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
    }

def generate_interview_questions(found_skills):

    questions = []

    skill_questions = {

        "python": [
            "What are Python decorators?",
            "Difference between list and tuple in Python?"
        ],

        "django": [
            "What is Django ORM?",
            "Explain Django MVT architecture."
        ],

        "html": [
            "What is semantic HTML?",
            "Difference between div and span?"
        ],

        "css": [
            "What is Flexbox in CSS?",
            "Difference between relative and absolute positioning?"
        ],

        "javascript": [
            "What is DOM in JavaScript?",
            "Difference between let and var?"
        ],

        "machine learning": [
            "What is overfitting?",
            "Explain supervised learning."
        ],

        "sql": [
            "What is SQL JOIN?",
            "Difference between DELETE and DROP?"
        ]
    }

    for skill in found_skills:

        if skill in skill_questions:

            questions.extend(
                skill_questions[skill]
            )

    return questions[:6]

<<<<<<< HEAD
# Weighted Career Paths & Skills Categorization Dictionary
SKILL_CATEGORIES_DICT = {
    "Programming Languages": ["python", "javascript", "typescript", "java", "c++", "c#", "ruby", "go", "rust", "php", "swift", "kotlin", "scala", "r", "html", "css", "sql", "bash", "shell"],
    "Frameworks": ["django", "flask", "react", "angular", "vue", "node", "express", "spring boot", "laravel", "net", "asp.net", "fastapi", "next.js", "bootstrap", "tailwind"],
    "Databases": ["mysql", "postgresql", "sqlite", "mongodb", "redis", "oracle", "sql server", "firebase", "dynamodb", "neo4j", "cassandra", "mariadb"],
    "Cloud/DevOps": ["aws", "azure", "gcp", "heroku", "netlify", "vercel", "linux", "nginx", "jenkins", "kubernetes", "terraform", "ansible", "ci/cd", "devops", "docker"],
    "Security": ["kali linux", "wireshark", "owasp", "penetration testing", "siem", "burp suite", "nmap", "metasploit", "cryptography", "cissp", "ceh", "cybersecurity"],
    "AI/ML": ["tensorflow", "pytorch", "scikit-learn", "numpy", "pandas", "keras", "spacy", "opencv", "machine learning", "deep learning", "nlp", "llm", "gemini", "openai", "data science"],
    "Tools": ["git", "github", "gitlab", "npm", "yarn", "webpack", "babel", "vite", "pip", "maven", "gradle", "jira", "confluence", "figma", "postman"],
    "Soft Skills": ["communication", "leadership", "teamwork", "problem solving", "time management", "critical thinking", "agile", "scrum", "collaboration", "management"]
}

def analyze_resume(text):
    print("\n[DEBUG] 4. ENTERED analyze_resume()")
    gemini_key = os.getenv("GEMINI_API_KEY")
    print(f"[DEBUG] API Key present? {'YES' if gemini_key else 'NO'}")
    text_lower = text.lower()
    
    if gemini_key:
        try:
            print("[DEBUG] 5. ENTERING GEMINI PIPELINE...")
            model = genai.GenerativeModel('gemini-2.5-flash')

            prompt = f"""
            You are an expert AI Resume Analyzer and Career Coach.
            Analyze the following resume text. Evaluate its quality, completeness, and structure, and perform advanced skill extraction.
            The system must intelligently adapt to the domain (e.g., Cybersecurity, AI/ML, Frontend, Backend, Data Analyst, Full Stack, Cloud/DevOps).
            
            Resume Text:
            {text}
            
            Return a STRICT JSON object matching exactly this schema:
            {{
                "candidate_name": "",
                "career_domain": "",
                "recommended_roles": [],
                "skills": {{
                    "programming_languages": [],
                    "frameworks": [],
                    "databases": [],
                    "cloud_devops": [],
                    "security": [],
                    "ai_ml": [],
                    "tools": [],
                    "soft_skills": []
                }},
                "missing_skills": [],
                "ats_score_breakdown": {{
                    "skills": 0,
                    "projects": 0,
                    "experience": 0,
                    "formatting": 0,
                    "certifications": 0
                }},
                "learning_recommendations": [],
                "resume_improvements": [],
                "interview_questions": {{
                    "beginner": [],
                    "intermediate": [],
                    "advanced": []
                }},
                "career_summary": ""
            }}
            
            Rules:
            1. "recommended_roles" must contain specific, realistic roles (e.g., "Security Engineer" not "Software Developer" if it's a security resume).
            2. "learning_recommendations" must suggest what to learn.
            3. "resume_improvements" must suggest how to improve the resume format/writing. NEVER duplicate learning recommendations here.
            4. "interview_questions" must contain exactly 3 beginner, 3 intermediate, and 3 advanced questions that are highly realistic and company-grade based on the domain. Avoid repetitive patterns like "Tell me about your experience...".
            5. "ats_score_breakdown" values should sum up to a realistic score out of 100 based on the resume quality.
            """
            
            print("[DEBUG] 6. GENERATE_CONTENT CALLED")

            response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
                        
            resp_text = response.text.strip()
            print(f"[DEBUG] 7. GEMINI RAW RESPONSE:\n{resp_text}\n")
            
            # Clean markdown code block formatting if present
            if resp_text.startswith("```json"):
                resp_text = resp_text[7:]
            if resp_text.endswith("```"):
                resp_text = resp_text[:-3]
            resp_text = resp_text.strip()
            
            data = json.loads(resp_text)
            print(f"[DEBUG] JSON PARSED SUCCESSFULLY: {data.get('career_domain')}")
            
            # Flatten skills to lowercase strings for DB storage and category matching
            flat_skills = []
            if "skills" in data and isinstance(data["skills"], dict):
                for k, v in data["skills"].items():
                    if isinstance(v, list):
                        for item in v:
                            cleaned = str(item).strip().lower()
                            if cleaned and cleaned not in flat_skills:
                                flat_skills.append(cleaned)
            
            rec_roles = data.get("recommended_roles", [])
            if rec_roles:
                primary_career = str(rec_roles[0])[:95]
                secondary_career = str(rec_roles[1])[:95] if len(rec_roles) > 1 else ""
                career_str = f"{primary_career} | {secondary_career}" if secondary_career else primary_career
            else:
                career_str = str(data.get("career_domain", "Software Developer"))[:95]
                
            q_dict = data.get("interview_questions", {})
            q_list = []
            if isinstance(q_dict, dict):
                for level in ["beginner", "intermediate", "advanced"]:
                    if level in q_dict and isinstance(q_dict[level], list):
                        q_list.append(f"--- {level.upper()} ---")
                        for idx, q in enumerate(q_dict[level]):
                            q_list.append(f"{idx+1}. {q}")
            interview_questions = "\n".join(q_list)
            
            # Robust ATS score sum — handles int AND float values from Gemini
            ats_breakdown = data.get("ats_score_breakdown", {})
            if isinstance(ats_breakdown, dict) and ats_breakdown:
                try:
                    total_score = int(sum(float(v) for v in ats_breakdown.values()))
                except Exception:
                    total_score = 70
                    ats_breakdown = {"skills": 20, "projects": 20, "experience": 15, "formatting": 10, "certifications": 5}
            else:
                total_score = 70
                ats_breakdown = {"skills": 20, "projects": 20, "experience": 15, "formatting": 10, "certifications": 5}
                
            total_score = max(min(total_score, 100), 10)
            
            ai_feedback = data.get("career_summary", "")
            ai_feedback += f"\n<ATS_BREAKDOWN>{json.dumps(ats_breakdown)}</ATS_BREAKDOWN>"
            
            return {
                'score': total_score,
                'career': career_str,
                'found_skills': flat_skills,
                'missing_skills': data.get("missing_skills", []),
                'recommendations': data.get("learning_recommendations", []),
                'improvements': data.get("resume_improvements", []),
                'interview_questions': interview_questions,
                'questions': interview_questions,
                'ai_feedback': ai_feedback
            }
        except Exception as e:
            print(f"\n[DEBUG] GEMINI ERROR CAUGHT: {e}\n")
            logger.error(f"Gemini API call failed or returned invalid JSON: {e}. Running local fallback parser.")
            
    print("\n[DEBUG] EXECUTING OFFLINE FALLBACK PARSER...")
    # LOCAL OFFLINE FALLBACK PARSER
    found_skills = []
    for category, skill_list in SKILL_CATEGORIES_DICT.items():
        for skill in skill_list:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                if skill not in found_skills:
                    found_skills.append(skill)
                    
    skill_score = min(len(found_skills) * 4, 40)
    completeness = 10 if "project" in text_lower else 0
    presence = 10 if "github" in text_lower else 0
    formatting = 10 if "certificat" in text_lower else 0
    experience = 10 if "experience" in text_lower else 0
    score = skill_score + completeness + presence + formatting + experience
    score = max(min(score, 98), 35)
    
    primary = "Software Developer"
    if "security" in text_lower or "kali" in text_lower or "owasp" in text_lower:
        primary = "Security Engineer"
    elif "react" in text_lower or "css" in text_lower:
        primary = "Frontend Developer"
    elif "django" in text_lower or "flask" in text_lower:
        primary = "Backend Developer"
    elif "tensorflow" in text_lower or "machine learning" in text_lower:
        primary = "AI/ML Engineer"
    elif "pandas" in text_lower or "sql" in text_lower:
        primary = "Data Analyst"
    elif "docker" in text_lower or "kubernetes" in text_lower:
        primary = "DevOps Engineer"
        
    ai_feedback = f"Analyzed using offline fallback. Recognized {len(found_skills)} skills. Update to Gemini for advanced analysis."
    ats_breakdown = {"skills": skill_score, "projects": completeness, "experience": experience, "formatting": formatting, "certifications": 5}
    ai_feedback += f"\n<ATS_BREAKDOWN>{json.dumps(ats_breakdown)}</ATS_BREAKDOWN>"
    
    fallback_questions = f"--- BEGINNER ---\n1. Explain a core concept of {primary}.\n2. How do you handle errors in your code?\n3. Describe your typical development workflow.\n--- INTERMEDIATE ---\n1. How would you optimize a slow application in your domain?\n2. Describe a challenging bug you fixed and how you approached it.\n3. How do you manage data persistence and state in your projects?\n--- ADVANCED ---\n1. Architect a scalable system for millions of concurrent users in the {primary} domain.\n2. How would you secure a distributed application against the most common attack vectors?\n3. Discuss tradeoffs you made in a recent project's architecture design."
    return {
        'score': score,
        'career': primary[:95],
        'found_skills': found_skills,
        'missing_skills': ["Advanced " + primary + " Skills", "Docker", "Cloud APIs"],
        'recommendations': ["Learn advanced " + primary + " patterns and best practices", "Study system design and distributed architecture", "Practice problem-solving on LeetCode or similar platforms"],
        'improvements': ["Quantify every bullet point with exact metrics (e.g. 'improved speed by 40%')", "Add live GitHub repo links for all projects", "Fix resume formatting for ATS scanners: avoid tables and graphics"],
        'interview_questions': fallback_questions,
        'questions': fallback_questions,
        'ai_feedback': ai_feedback
=======
# Advanced ATS Resume Analysis
def analyze_resume(text):

    text = text.lower()

    found_skills = []

    score = 0

    # Skill Scoring
    for skill, weight in skills.items():

        if skill in text:

            found_skills.append(skill)

            score += weight

    # Education Score
    education_keywords = [
        "b.tech",
        "b.e",
        "m.tech",
        "computer science",
        "engineering"
    ]

    education_found = False

    for edu in education_keywords:

        if edu in text:

            education_found = True

            score += 10

            break

    # Experience Score
    experience_keywords = [
        "internship",
        "experience",
        "project",
        "developer"
    ]

    experience_found = False

    for exp in experience_keywords:

        if exp in text:

            experience_found = True

            score += 10

            break

    # Resume Quality Score
    if len(text) > 1000:

        score += 10

    # Limit score to 97

    if score > 97:

        score = 97

    # Missing Skills
    missing_skills = list(
        set(skills.keys()) - set(found_skills)
    )

    # Learning Recommendations
    recommendations = []

    if "python" not in found_skills:

        recommendations.append(
            "Learn Python programming fundamentals"
        )

    if "django" not in found_skills:

        recommendations.append(
            "Build backend projects using Django"
        )

    if "sql" not in found_skills:

        recommendations.append(
            "Practice SQL queries and database concepts"
        )

    if "machine learning" not in found_skills:

        recommendations.append(
            "Learn Machine Learning with TensorFlow and Scikit-learn"
        )

    if "javascript" not in found_skills:

        recommendations.append(
            "Improve frontend skills using JavaScript"
        )

    # Career Recommendation
    if "machine learning" in found_skills:

        career = "Machine Learning Engineer"

    elif (
        "django" in found_skills and
        "python" in found_skills
    ):

        career = "Backend Developer"

    elif (
        "html" in found_skills and
        "css" in found_skills and
        "javascript" in found_skills and
        "python" not in found_skills
    ):

        career = "Frontend Developer"

    elif (
        "java" in found_skills and
        "sql" in found_skills
    ):

        career = "Software Developer"

    else:

        career = "Software Developer"

    # Resume Improvement Suggestions
    improvements = []

    if len(found_skills) < 5:

        improvements.append(
            "Add more technical skills to improve ATS score"
        )

    if not education_found:

        improvements.append(
            "Add education details clearly"
        )

    if not experience_found:

        improvements.append(
            "Include internships or project experience"
        )

    if len(text) < 700:

        improvements.append(
            "Resume content is too short. Add more details"
        )
    if "github" not in text:

        improvements.append(
            "Add GitHub profile link"
        )

    if "linkedin" not in text:

        improvements.append(
            "Add LinkedIn profile link"
        )

    if "certification" not in text:

        improvements.append(
            "Add certifications to strengthen your resume"
        )
    questions = generate_interview_questions(found_skills)

    questions = generate_ai_questions(found_skills)
    ai_feedback = generate_ai_feedback(text)

    return {
        'score': score,

        'found_skills': found_skills,

        'missing_skills': missing_skills,

        'career': career,

        'education_found': education_found,

        'experience_found': experience_found,

        'recommendations': recommendations,

        'improvements': improvements,

        'interview_questions': questions,

        'questions': questions,

        'ai_feedback': ai_feedback,
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
    }

# Register View
def register_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')

        # Check existing username

        if User.objects.filter(username=username).exists():

            return render(request, 'register.html', {

                'error': 'Username already exists'

            })

        # Check existing email

        if User.objects.filter(email=email).exists():

            return render(request, 'register.html', {

                'error': 'Email already exists'

            })
# Password validation
# Password length

        if len(password) < 8:

            return render(request, 'register.html', {

                'error': 'Password must contain at least 8 characters'

            })

# Capital letter check

        if not re.search(r'[A-Z]', password):

            return render(request, 'register.html', {

                'error': 'Password must contain at least one capital letter'

            })

# Special character check

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):

            return render(request, 'register.html', {

                'error': 'Password must contain at least one special character'

        })

         # Create user

        user = User.objects.create_user(

            username=username,
            email=email,
            password=password
        )
        messages.success(request, 'Registration successful. Please login.')
        return redirect('/login/')

    return render(request, 'register.html')

from django.contrib.auth import logout

def logout_user(request):

    logout(request)

    messages.success(request, 'Logged out successfully.')

    return redirect('/login/')

# Login View
def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(request, 'Login successful.')

            return redirect('/')

        else:

            messages.error(request, 'Invalid username or password.')

            return render(request, 'login.html')

    return render(request, 'login.html')

# Dashboard View
@login_required
<<<<<<< HEAD
def download_report(request, id=None):
    from django.shortcuts import get_object_or_404
    
    if id:
        resume = get_object_or_404(Resume, id=id, user=request.user)
    else:
        resumes = Resume.objects.filter(
            user=request.user
        ).order_by('-uploaded_at')

        if not resumes.exists():
            return HttpResponse("No resume found to download report.")
        resume = resumes.first()

    result = {
        'score': resume.score,
        'career': resume.career,
        'found_skills': [s.strip() for s in resume.found_skills.split(',') if s.strip()],
        'missing_skills': [s.strip() for s in resume.missing_skills.split(',') if s.strip()],
        'recommendations': [r.strip() for r in resume.recommendations.split('|') if r.strip()],
        'improvements': [i.strip() for i in resume.improvements.split('|') if i.strip()],
        'education_found': bool(resume.education),
        'experience_found': bool(resume.experience),
        'questions': resume.interview_questions or "Customized interview questions not available.",
        'ai_feedback': resume.ai_feedback or "AI feedback not available."
    }

    info = {
        'name': resume.name,
        'email': resume.email or "Not detected",
        'phone': resume.phone or "Not detected",
        'education': [e.strip() for e in resume.education.split('\n') if e.strip()] if resume.education else ["Not detected"],
        'experience': [ex.strip() for ex in resume.experience.split('\n') if ex.strip()] if resume.experience else ["Not detected"],
        'projects': [p.strip() for p in resume.projects.split('\n') if p.strip()] if resume.projects else ["Not detected"],
        'certifications': [c.strip() for c in resume.certifications.split('\n') if c.strip()] if resume.certifications else ["Not detected"]
    }

    template = get_template('report_pdf.html')
    html = template.render({
        'result': result,
        'info': info,
        'resume': resume
    })

    response = HttpResponse(content_type='application/pdf')
    filename = f"resume_analysis_{resume.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
=======
def download_report(request):

    resumes = Resume.objects.filter(
        user=request.user
    ).order_by('-uploaded_at')

    if not resumes.exists():

        return HttpResponse("No resume found")

    resume = resumes.first()

    result = {

        'score': resume.score,

        'career': resume.career,

        'found_skills': [
            'python',
            'django',
            'html',
            'css',
            'javascript'
        ],

        'missing_skills': [],

        'recommendations': [
            "Improve ATS keywords",
            "Add more projects",
            "Add certifications"
        ],

        'improvements': [
            "Use better formatting",
            "Add measurable achievements",
            "Optimize for ATS systems"
        ],

        'education_found': True,

        'experience_found': True
    }

    info = {

        'email': 'example@gmail.com',

        'phone': '+91 XXXXX XXXXX',

        'education': ['Bachelor of Engineering']
    }

    template = get_template(
        'success.html'
    )

    html = template.render({

        'result': result,

        'info': info,

        'pdf': True
    })

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename="resume_report.pdf"'
    )
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:
<<<<<<< HEAD
        return HttpResponse('Error generating PDF report')
=======

        return HttpResponse(
            'Error generating PDF'
        )
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487

    return response

@login_required
def dashboard(request):
<<<<<<< HEAD
=======

>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
    resumes = Resume.objects.filter(
        user=request.user
    ).order_by('-uploaded_at')

    latest_resume = resumes.first()
<<<<<<< HEAD
    total_resumes = resumes.count()

    skill_labels = ["Detected Skills", "Missing Skills"]
    skill_counts = [0, 0]

    ats_breakdown_labels = ["Skills", "Projects", "Experience", "Formatting", "Certifications"]
    ats_breakdown_values = [0, 0, 0, 0, 0]

    category_labels = ["Security", "Programming", "AI/ML", "Frontend", "Backend", "Cloud/DevOps", "Databases", "Tools"]
    category_values = [0] * len(category_labels)

    dashboard_category_map = {
        "Security": ["kali linux", "wireshark", "owasp", "penetration testing", "siem", "burp suite", "nmap", "metasploit", "cryptography", "cissp", "ceh", "cybersecurity", "security"],
        "Programming": ["python", "javascript", "typescript", "java", "c++", "c#", "ruby", "go", "rust", "php", "swift", "kotlin", "scala", "r", "html", "css", "sql", "bash", "shell"],
        "AI/ML": ["tensorflow", "pytorch", "scikit-learn", "numpy", "pandas", "keras", "spacy", "opencv", "machine learning", "deep learning", "nlp", "llm", "gemini", "openai", "data science", "ai"],
        "Frontend": ["html", "css", "javascript", "typescript", "react", "angular", "vue", "bootstrap", "tailwind", "sass", "less", "next.js", "vite", "webpack", "babel", "dom"],
        "Backend": ["django", "flask", "node", "express", "spring boot", "laravel", "asp.net", "net", "fastapi", "graphql", "rest", "api", "java", "python", "c#", "php"],
        "Cloud/DevOps": ["aws", "azure", "gcp", "heroku", "netlify", "vercel", "linux", "nginx", "jenkins", "kubernetes", "terraform", "ansible", "ci/cd", "devops", "docker", "container"],
        "Databases": ["mysql", "postgresql", "sqlite", "mongodb", "redis", "oracle", "sql server", "firebase", "dynamodb", "neo4j", "cassandra", "mariadb", "postgres"],
        "Tools": ["git", "github", "gitlab", "npm", "yarn", "jira", "confluence", "figma", "postman", "vscode", "docker", "kubernetes", "jenkins", "selenium"]
    }

    if latest_resume:
        skills = [
            skill.strip().lower()
            for skill in latest_resume.found_skills.split(',')
            if skill.strip()
        ]
        missing_skills = [
            skill.strip().lower()
            for skill in latest_resume.missing_skills.split(',')
            if skill.strip()
        ]

        skill_counts = [len(skills), len(missing_skills)]

        ai_feedback_raw = latest_resume.ai_feedback or ""
        match = re.search(r"<ATS_BREAKDOWN>(.*?)</ATS_BREAKDOWN>", ai_feedback_raw, re.DOTALL)
        if match:
            try:
                ats_data = json.loads(match.group(1))
                ats_breakdown_values = [
                    int(float(ats_data.get("skills", 0))),
                    int(float(ats_data.get("projects", 0))),
                    int(float(ats_data.get("experience", 0))),
                    int(float(ats_data.get("formatting", 0))),
                    int(float(ats_data.get("certifications", 0)))
                ]
            except Exception as e:
                logger.error(f"ATS breakdown parse error: {e}")
                ats_breakdown_values = [
                    min(len(skills) * 5, 40),
                    20 if latest_resume.projects.strip() else 10,
                    20 if latest_resume.experience.strip() else 10,
                    15 if "format" in ai_feedback_raw.lower() else 10,
                    10 if latest_resume.certifications.strip() else 5
                ]
            latest_resume.ai_feedback = re.sub(r"<ATS_BREAKDOWN>.*?</ATS_BREAKDOWN>", "", ai_feedback_raw, flags=re.DOTALL).strip()
        else:
            ats_breakdown_values = [
                min(len(skills) * 5, 40),
                20 if latest_resume.projects.strip() else 10,
                20 if latest_resume.experience.strip() else 10,
                15 if "format" in ai_feedback_raw.lower() else 10,
                10 if latest_resume.certifications.strip() else 5
            ]

        cat_counts = [0] * len(category_labels)
        for s in skills:
            for idx, cat_name in enumerate(category_labels):
                if s in dashboard_category_map.get(cat_name, []):
                    cat_counts[idx] += 1
                    break
        category_values = cat_counts

    # Serialize all list/dict context to JSON for safe JavaScript consumption
    # Debug: log dashboard chart context (minimal, uses logger.debug)
    logger.debug(f"Dashboard context for user={request.user.username if request.user else 'anon'}: skill_labels={skill_labels}, skill_counts={skill_counts}, ats_breakdown_values={ats_breakdown_values}, category_values={category_values}")

    return render(request, 'dashboard.html', {
        'resumes': resumes,
        'latest_resume': latest_resume,
        'total_resumes': total_resumes,
        'skill_labels_json': json.dumps(skill_labels),
        'skill_counts_json': json.dumps(skill_counts),
        'ats_breakdown_labels_json': json.dumps(ats_breakdown_labels),
        'ats_breakdown_values_json': json.dumps(ats_breakdown_values),
        'category_labels_json': json.dumps(category_labels),
        'category_values_json': json.dumps(category_values),
        # Also pass raw for any template text rendering
        'skill_labels': skill_labels,
        'skill_counts': skill_counts,
        'ats_breakdown_labels': ats_breakdown_labels,
        'ats_breakdown_values': ats_breakdown_values,
        'category_labels': category_labels,
        'category_values': category_values
=======

    total_resumes = resumes.count()

    skill_labels = []

    skill_counts = []

    if latest_resume:

        skills = [
            skill.strip()
            for skill in latest_resume.found_skills.split(',')
            if skill.strip()
        ]

        import random

        skill_labels = skills

        for skill in skills:

            skill_counts.append(random.randint(5, 30))

    return render(request, 'dashboard.html', {

        'resumes': resumes,

        'latest_resume': latest_resume,

        'total_resumes': total_resumes,

        'skill_labels': skill_labels,

        'skill_counts': skill_counts

>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
    })
def generate_ai_questions(found_skills):

    prompt = f"""
    Generate 5 interview questions
    for these skills:
    {found_skills}
    """

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response.choices[0].message.content

    except Exception:

        return """
1. Explain your strongest technical skill.
2. Describe a challenging project.
3. What is object-oriented programming?
4. Explain database normalization.
5. How do you debug errors?
"""
def generate_ai_feedback(text):

    feedback = []

    text = text.lower()

    if "project" not in text:

        feedback.append(
            "Add more project descriptions to showcase practical experience."
        )

    if "internship" not in text:

        feedback.append(
            "Include internship experience to improve resume strength."
        )

    if "github" not in text:

        feedback.append(
            "Add your GitHub profile link."
        )

    if "linkedin" not in text:

        feedback.append(
            "Add your LinkedIn profile for professional visibility."
        )

    if "certification" not in text:

        feedback.append(
            "Add certifications to improve credibility."
        )

    if len(text) < 700:

        feedback.append(
            "Resume content is too short. Add more details and achievements."
        )

    if len(feedback) == 0:

        feedback.append(
            "Excellent resume with strong technical content."
        )

    return feedback

@login_required
def history(request):

    resumes = Resume.objects.filter(
        user=request.user
    ).order_by('-uploaded_at')

    search = request.GET.get('search')

    if search:

        resumes = resumes.filter(
            career__icontains=search
        )

    return render(
        request,
        'history.html',
        {'resumes': resumes}
    )

@login_required
def delete_resume(request, id):

    resume = Resume.objects.get(id=id)

    # Security check
    if resume.user == request.user:

        resume.delete()

    return redirect('/history/')

@login_required
def view_report(request, id):
<<<<<<< HEAD
    from django.shortcuts import get_object_or_404
    resume = get_object_or_404(Resume, id=id, user=request.user)

    result = {
        'score': resume.score,
        'career': resume.career,
        'found_skills': [s.strip() for s in resume.found_skills.split(',') if s.strip()],
        'missing_skills': [s.strip() for s in resume.missing_skills.split(',') if s.strip()],
        'recommendations': [r.strip() for r in resume.recommendations.split('|') if r.strip()],
        'improvements': [i.strip() for i in resume.improvements.split('|') if i.strip()],
        'education_found': bool(resume.education),
        'experience_found': bool(resume.experience),
        'questions': resume.interview_questions or "Customized interview questions not available.",
        'ai_feedback': resume.ai_feedback or "AI feedback not available."
    }

    info = {
        'name': resume.name,
        'email': resume.email or "Not detected",
        'phone': resume.phone or "Not detected",
        'education': [e.strip() for e in resume.education.split('\n') if e.strip()] if resume.education else ["Not detected"]
=======

    resume = Resume.objects.get(id=id)

    result = {

        'score': resume.score,

        'career': resume.career,

        'found_skills': resume.found_skills.split(','),

        'missing_skills': resume.missing_skills.split(','),

        'recommendations': resume.recommendations.split('|'),

        'improvements': resume.improvements.split('|'),

        'education_found': True,

        'experience_found': True,

        'questions': "Previously generated AI questions"
    }

    info = {

        'email': "Stored Email",

        'phone': "Stored Phone",

        'education': ["Bachelor of Engineering"]
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
    }

    return render(
        request,
        'success.html',
        {
            'result': result,
<<<<<<< HEAD
            'info': info,
            'resume': resume
=======
            'info': info
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
        }
    )

def welcome_page(request):
    return render(request, 'home.html')

from django.contrib.auth.models import User

def forgot_password(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        new_password = request.POST.get('new_password')

        # Password length

        if len(new_password) < 8:

            return render(request, 'forgot_password.html', {

                'error': 'Password must contain at least 8 characters'

            })

# Capital letter check

        if not re.search(r'[A-Z]', new_password):

            return render(request, 'forgot_password.html', {

                'error': 'Password must contain at least one capital letter'

            })

# Special character check

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):

            return render(request, 'forgot_password.html', {

                'error': 'Password must contain at least one special character'

            })

        try:

            user = User.objects.get(username=username)

            user.set_password(new_password)

            user.save()

            return redirect('/login/')

        except User.DoesNotExist:

            return render(request, 'forgot_password.html', {

                'error': 'Username not found'

            })

    return render(request, 'forgot_password.html')