# HealthOS

## Overview
HealthOS is a full stack health assessment platform that collects data from users on areas such as physical activity, lifestyle, bloodwork,
body composition, and biometric data to generate comprehensive results including scores, a confidence rating, section specific weaknesses
and blindspots. The application assesses the user in the following categories:
- Strength
- Cardio
- Flexibility
- Nutrition
- Recovery
- Metabolic Health

## Features
### Authentication:
- Secure user registration and login system
- Email verification
- Password hashing
- Password reset
- Session management
- Account Deletion

### Assessment:
- Category-specific scoring
- Support for unknown or unanswered responses
- Weighted overall health score
- Custom scoring curves for different questions
- Dynamic assessment questions

### Results
- Overall health score
- Category-by-category breakdown
- Weakness identification
- Health blind-spot identification
- Confidence rating

## Tech Stack
### Frontend:
- HTML
- CSS
- Javascript

### Backend:
- Python
- Flask
- REST APIs

### Database:
- PostgreSQL

### Deployment:
- Frontend: Netlify
- Backend: Render
- Database: Neon

## Local Setup
Initially I had deployed the website online as mentioned above under the deployment category; however, due to inactivity on render, api requests can take minutes to complete, hence, I later thought it would be more appropriate to just host the project locally and provide a setup guide. The guide is as follows:
### Clone repository
```
git clone https://github.com/GarvitBhasin/HealthOS/
cd HealthOS
```
### Create venv
```
python3 -m venv .venv
source .venv/bin/activate
```
### Install dependencies 
```
python3 -m venv .venv
source .venv/bin/activate
```
### DB configuration
```
schema.sql into an sql editor and config
```
### Configure venv variables
```
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_password
```
### Run backend 
```
python3 backend.py
```
## What I Learnt
I learnt many new useful concepts while developing this project; however, I didn't just learn them conceptually, I also constantly applied them. Some of these things include:
- REST API development and HTTP codes
- Password and token hashing (bcrypt and sha256)
- Writing complex javascript code:
  - Input validation and error handling
  - Asynchronous API requests
  - Dynamically updating UI
  - Event delegation
- SMTP and email.message 
- CORS and cloud deployment
- Database API componenets (psycopg and mysql.connector)
- Cookies and session management
- Good software engineering practices:
  - Creating venv and env files to store sensitive information and isolate dependencies
  - Managing dependencies with `requirements.txt`
  - Sorting backend logic and javascript logic into helper functions for better code reusability and efficiency
  - Using HTTP methods and status codes appropriately
  - Using git and github appropriately for version control (git commit workflow was not setup properly as I migrated to a new laptop resulting in commits not being pushed to the repository for a significant portion of the project).

## Future Versions
Future planned updates include adding features:
- Tracking historical data to show progress
- Data visualization
- Improved assessment structure and scoring algorithm
- Introduction of `dashboard.html` and `consultation.html`
- Adding a rate limiter to login, signup and email verifications.

## AI Assistance
A substantial portion of development and implimentation of this project was carried out by me. AI tools including ChatGPT and Gemini were used by me to help me through multiple processes such as debugging both frontend and backend bugs, explaining unfamiliar concepts, exploring alternative implementations, improving documentation, and assisting in developing basic HTML and CSS code. All application architecture, implementation decisions, code integration, testing, and final verification were performed by me.

## Disclaimer
HealthOS is an educational software project and is not intended to provide medical diagnoses or replace professional medical advice.
