import openai
from PyPDF2 import PdfReader
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.html import escape
from io import BytesIO
from finalProject import settings
from service.forms import RegisterForm, LoginForm
from service.models import ChatHistory, CVStructure, CoverLetterStructure

openai.api_key = settings.OPENAI_API_KEY


def chat(request):
    try:
        if request.method == 'POST':
            user_input = request.POST.get('user_input')
            uploaded_file = request.FILES.get("uploaded_file", None)
            formatted_user = escape(user_input)

            if uploaded_file:
                if uploaded_file.content_type == 'application/pdf':

                    file_content = uploaded_file.read()
                    file_to_pdf = BytesIO(file_content)

                    reader = PdfReader(file_to_pdf)
                    data = ""
                    for page in reader.pages:
                        data += page.extract_text() + "\n"

                    response_var = f"CV or Cover Letter: {data}\n\n User Query: {user_input}"

                    bot_response = response(response_var).replace("\n", "<br>")

                    ChatHistory.objects.create(
                        user=request.user,
                        message=formatted_user,
                        sender='user'
                    )

                    ChatHistory.objects.create(
                        user=request.user,
                        message=bot_response,
                        sender='bot'
                    )
                    return JsonResponse({'bot_response': bot_response})

            else:

                formatted_user = escape(user_input)
                bot_response = response(formatted_user).replace("\n", "<br>")

                ChatHistory.objects.create(
                    user=request.user,
                    message=formatted_user,
                    sender='user'
                )
                ChatHistory.objects.create(
                    user=request.user,
                    message=bot_response,
                    sender='bot'
                )

                return JsonResponse({'bot_response': bot_response})

        chat_history = ChatHistory.objects.filter(user=request.user)

        return render(request, 'chat.html', {'chat_history': chat_history})

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'Something went wrong'}, status=500)


def advert(request):
    return render(request, 'advert.html')


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
            else:
                login(request, user)
                return redirect('chat')  # Redirect to a home page after login

    return render(request, 'login.html', {'form': form})


def gpt_prompt(query):
    # Constructing a prompt using SQL data and user's query
    try:
        sections = CVStructure.objects.all().order_by('order')

        section_info = "\n".join([f"Position in CV: {section.order}\n"
                                  f"Section: {section.section_name}\n"
                                  f"Description: {section.description}\n"
                                  f"Mandatory: {'Yes' if section.is_mandatory else 'No'}\n"
                                  for section in sections])

        cl_sections = CoverLetterStructure.objects.all().order_by('order')

        cl_sec_info = "\n".join([f"Position in Cover Letter: {cl_section.order}\n"
                                 f"Section: {cl_section.section_name}\n"
                                 f"Description: {cl_section.description}\n"
                                 f"Mandatory: {'Yes' if cl_section.is_mandatory else 'No'}\n"
                                 for cl_section in cl_sections])

        return gpt_generic_prompt(section_info, cl_sec_info, query)
    except Exception as e:
        return f"Error with GPT: {str(e)}"


def gpt_generic_prompt(cv_info, cl_info, query):
    try:
        prompt = (
            f"Based on the following information for CV's:\n{cv_info},\n\n"
            f"and based on the following information for Cover Letter's:\n{cl_info}\n\n"
            f"Answer the following query: {query}."
            f"DON'T use formal terms like 'position', 'section name', 'description', 'mandatory' but ensure you cover all steps and outcomes in a natural way."
            f"DO NOT USE '*' or any other special characters to represent lists or points. Use full sentences or numbers instead."
            f"When using numbers to represent points, write them with the number followed by a closing parenthesis and a space. Then write the corresponding point or statement."
            f"If the user's question is irrelevant or outside the provided information, kindly apologize and ask if they need help with something else."
            f"If they have uploaded their CV or Cover Letter Analyze it, provide feedback with a rating, and suggest improvements."
            f"If the current question is a follow-up to the previous question, incorporate that context into your response, "
            f"focusing on the previous question's content. Otherwise, provide a general response, based on the database."
            f"Begin by mentioning any necessary conditions or requirements before proceeding."
            f"For each step, clearly describe the action and what the user should expect as a result of that step."

        )
        return chat_model(prompt)
    except Exception as e:
        return f"Error with GPT: {str(e)}"


def chat_model(prompt):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}  # User's query
        ]

        resp = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Correct model name
            messages=messages,  # List of messages to pass to the model
            max_tokens=2000,
            temperature=0.3
        )
        return resp['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"Error with GPT: {str(e)}"


def clear_chat(request):
    if request.method == 'POST':
        ChatHistory.objects.filter(user=request.user).delete()  # Remove chat history from the session
        chat_history = ChatHistory.objects.filter(user=request.user)
        return render(request, 'chat.html', {'chat_history': chat_history})

    return redirect('chat')


def response(user_input):
    try:
        question_response = gpt_prompt(user_input)  # Passes the question as parameter for the response method.

        formatted_response = question_response.replace("\n",
                                                       "<br>")  # Replacing the new-line character with the HTML new-line character
        return formatted_response
    except Exception as e:
        return f"Error generating response: {str(e)}"


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('register')
            else:
                user = form.save(commit=False)
                user.is_staff = False
                user.is_superuser = False
                user.save()
                return redirect('login')  # Redirect to login page

        else:
            # If the form is invalid, display the form with errors
            messages.error(request,
                           'Password must be over 8 characters, with uppercase and special characters (e.g., !@#$%^&*).'
                           'Try a different username if issues persist.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password.html'  # Ensure this template exists
    email_template_name = 'password_reset_instructions.txt'  # Ensure this template exists
    subject_template_name = 'password_reset_subject.txt'  # Ensure this template exists
    success_url = '/password_reset/done/'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'change_password.html'  # Ensure this template exists
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'  # Ensure this template exists
