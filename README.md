# OptoTask


## Overview

OptoTask is a full-stack Progressive Web Application (PWA) designed to streamline patient management workflows in optometry practices. The application addresses the challenge of tracking patient referrals, follow-ups, and task completion in a busy clinical environment.


Target Audience: Optometrists & Ophthalmologists.

## Features:

JWT implementation allows secure multi-user authentication
CRUD operations designed for comprehensive patient management via a 'ticketing' system
Task completion tracking with visual status indicators
Referral workflow management with color-coded priority system
Responsive design for desktop and mobile access
Real-time database synchronization across users for GDPR & NHS governance adherance

## Tech Stack:

Frontend: React, JavaScript, TailwindCSS, PWA
Backend: Python, FastAPI, SQLAlchemy
Database: PostgreSQL
Authentication: JWT, bcrypt
Deployment: Render
Version Control: Git, GitHub

## Project Structure
optotask/
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
└── README.md

## API Endpoints

### Public Endpoints
1.GET / → Welcome endpoint (returns a simple message)
2.GET /health → Health check (used by Render to verify service is running)

### Authentication Endpoints
3.POST /signup → Create a new user account
4.POST /login → Login with username & password, receive JWT access token
5.GET /me → Get current authenticated user’s information

### Patient/Task CRUD Endpoints (Protected — require JWT)
6.POST /create → Create a new patient task

7.GET /read/{patient_id} → Read a single patient task by ID

8.GET /see_all → Get all non-archived patient tasks for current user

9.GET /read_archive → Get all archived patient tasks for current user

10.GET /search_archive/{patient_id} → Search for a specific patient in archive

11.GET /tickets/open → Get all open tickets for current user

12.PUT /update/{patient_id} → Update a patient task by ID

13.DELETE /tasks/{patient_id}

## Deployment
The application is deployed on <u>Render</u> with the following production setup:

-Backend service with PostgreSQL database
-Environment variables for secure credential management
-CORS configuration for frontend-backend communication
-Production-grade gunicorn server

# Future Improvements
The future for my project lies in its availability after further functional improvements:
## Functional improvments:
[] Implement task postponement  reminders before due date and display postponed task based on date requested
[] Develop keyword analytics dashboard for referral counts based on pathology
[] Add export functionality for patient audit proofs

## Availability
[] Containerise with Docker
[] Deploy on AWS for large scale use
[] Produce availability on Google Playstore 

