# 🏨 Hotel Booking Backend API

A scalable Hotel Booking Backend System built with FastAPI, PostgreSQL, and Docker, supporting authentication, room management, bookings, and integrated payments via .

## 🚀 Features

* 🔐 JWT-based Authentication (Register/Login)
* 🏨 Room Management (Create, Delete, Search)
* 📅 Booking System with availability logic
* 💳 Payment Integration (Razorpay Payment Links)
* 🔄 Booking & Payment Status Sync
* 🐳 Dockerized Deployment
* 🧩 Layered Architecture (API → Service → DB)

## 🏗️ Architecture
```
src/
├── api/           # FastAPI routes (controllers)
├── services/      # Business logic
├── db/            # Database queries
├── schemas/       # Pydantic + SQL schema
├── core/          # Config & utilities (JWT, decorators)
└── main.py        # Entry point
```
## ⚙️ Tech Stack
* Backend: FastAPI
* Database: PostgreSQL
* ORM/Driver: psycopg2
* Auth: JWT + bcrypt
* Payments: Razorpay API
* Containerization: Docker + Docker Compose

## 🐳 Setup (Docker)
### 1. Clone the repo
```
git clone git@github.com:mdismailquraishicse/hotel-booking-backend.git
cd hotel-booking-backend
```
### 2. Create .env
```
RAZOR_KEY=your_key
RAZOR_SECRET=your_secret
```
### 3. Run the app
```
docker-compose up --build
```
## 🌐 API Base URL
```
http://localhost:8000/api/v1
```
## 🔑 Authentication
* Uses JWT token
* Pass token in header:
```
Authorization: Bearer <token>
```
## 📌 Core APIs
* POST /auth/register
* POST /auth/login
## Rooms
* GET /rooms/search-available-rooms
* POST /rooms/create-room
* DELETE /rooms/delete-room/{id}
## Bookings
* POST /bookings/book-now
* GET /bookings/fetch-bookings
* DELETE /bookings/delete-booking/{id}
## Payments
* POST /pay/create-payment-link
* GET /pay/check-payment-status/{link_id}
## 🔄 Workflow
* User registers & logs in → gets JWT
* Searches available rooms
* Books a room → status = pending
* Creates payment link via Razorpay
* Payment status checked & updated
* Booking confirmed after payment
## 🧠 Key Highlights
* Clean Layered Architecture
* Secure password hashing using bcrypt
* Dynamic room availability logic (date overlap handling)
* Payment-to-booking synchronization
* Fully containerized (plug & play)
## ⚠️ Notes
* Currently uses manual payment status polling (no webhook)
* Designed for easy extension (webhooks, caching, scaling)
