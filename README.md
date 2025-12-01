OptoTask


Overview

OptoTask is a full-stack Progressive Web Application (PWA) designed to streamline patient management workflows in optometry practices. The application addresses the challenge of tracking patient referrals, follow-ups, and task completion in a busy clinical environment.


Technologies: React, FastAPI, PostgreSQL, JWT Authentication, SQLAlchemy, TailwindCSS

Target Audience: Optometrists & Ophthalmologists.

Features:

JWT implementation allows secure multi-user authentication
CRUD operations designed for comprehensive patient management via a 'ticketing' system
Task completion tracking with visual status indicators
Referral workflow management with color-coded priority system
Responsive design for desktop and mobile access
Real-time database synchronization across users for GDPR & NHS governance adherance

Tech Stack:

Frontend: React, JavaScript, TailwindCSS, PWA
Backend: Python, FastAPI, SQLAlchemy
Database: PostgreSQL
Authentication: JWT, bcrypt
Deployment: Render
Version Control: Git, GitHub

Project Structure
'''optotask/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── database.py
|   |   └── main.py
│   ├── requirements.txt
│   
├── frontend/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── Dashboard.js
│   ├── public/
│   └── package.json
└── README.md'''

API Endpoints

POST /auth/register - User registration
POST /auth/login - User authentication
GET /tickets - Retrieve all patient tickets
POST /tickets - Create new patient ticket
PUT /tickets/{id} - Update ticket status
DELETE /tickets/{id} - Delete ticket

Deployment
The application is deployed on Render with the following production setup:

Backend service with PostgreSQL database
Environment variables for secure credential management
CORS configuration for frontend-backend communication
Production-grade gunicorn server

Future Improvements

Implement appointment scheduling functionality
Add patient communication system with automated reminders
Integrate with practice management software APIs
Develop analytics dashboard for practice performance metrics
Add export functionality for patient records
Task postponement functionality with date tracking
