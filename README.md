# Resume & Cover Letter Enhancement Tool

**Live Project:** [View the application here](https://c366sree.pythonanywhere.com/)

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)

---

## About the Project

This is a Django-based web application designed to enhance CV and cover letter structures. The application integrates the OpenAI API to deliver an intuitive and efficient user experience. Users can upload documents, receive AI-driven feedback, and improve their profiles effortlessly.

---

## Features
- **User Authentication**: Login, registration, and password reset functionality.
- **Document Upload and Analysis**: Easily upload documents for detailed analysis and feedback.
- **AI-Driven Customization**: Powered by GPT-4 Turbo for intelligent and tailored responses.

---

## Technologies Used
- **Django**: Web framework
- **Python**: Backend programming
- **HTML/CSS**: Frontend styling and layout
- **JavaScript**: Interactivity 
- **SQLite**: Database management
- **OpenAI API**: For chatbot functionality


---

## Setup Instructions

### Prerequisites
- Python 3.x installed on your system
- Virtual environment tool (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Sreehari05055/ResumeCoverLetterETool.git

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Edit the settings.py file:
   Add your OpenAI API key, email address, and its app-specific password in the relevant configuration fields.


5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

6. Start the development server:
   ```bash
   python manage.py runserver
