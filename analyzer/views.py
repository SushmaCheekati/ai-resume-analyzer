from random import random

from django.shortcuts import render
from .forms import ResumeForm
import PyPDF2
import docx2txt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Resume
import re
import spacy
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from xhtml2pdf import pisa

from openai import OpenAI
from dotenv import load_dotenv
import os
from django.shortcuts import render, redirect
import re
from django.contrib import messages

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

nlp = spacy.load("en_core_web_sm")

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

            extracted_text = extract_resume_text(file_path)

            result = analyze_resume(extracted_text)

            info = extract_information(extracted_text)

            resume.score = result['score']

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

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:

        return HttpResponse(
            'Error generating PDF'
        )

    return response

@login_required
def dashboard(request):

    resumes = Resume.objects.filter(
        user=request.user
    ).order_by('-uploaded_at')

    latest_resume = resumes.first()

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
    }

    return render(
        request,
        'success.html',
        {
            'result': result,
            'info': info
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