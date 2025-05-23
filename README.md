# 🎬 Movie Reservation System

A backend service to manage a movie theater’s ticket booking operations. The system supports movie listings, showtimes, seat selection, real-time updates via WebSockets, and simulated payment processing. Built with modularity, atomic seat reservations, and containerized deployment in mind.

---

## 🧾 Project Overview

This system allows users to:

- Browse and search for movies by genre, actor, or date.
- View real-time seat availability and select seats.
- Lock and book seats securely without double-booking.
- Receive instant updates on seat availability via WebSockets.
- Simulate payments (with Stripe test keys or mocks).
- Deploy the full system with Docker and Docker Compose.

---

## 📌 Features

### 🎥 Movie Listings & Search

- Database-managed movies, genres, actors, and showtimes.
- Filter movies by genre, actor, or date range.
- Searchable movie catalog with start and end date validation.

### 🪑 Theater & Seating

- Configurable theater layout (rows x columns).
- Each showtime has an isolated seating map.
- Users can view and select available seats.

### 🔒 Seat Reservation Logic

- Atomic seat booking to prevent double-booking.
- Temporary seat locks to handle concurrent selections.
- Optimized logic to handle real-time concurrency.

### 🔔 Real-Time Notifications

- WebSocket-based updates for:
  - Seat selection (locking).
  - Successful bookings.
- Enables all users watching a showtime to stay in sync.

### 💳 Payment Simulation

- Simulated checkout flow using Stripe (test keys) or mocks.
- Reservation confirmed only after successful payment.

---

## 📦 Deployment with Docker

### 🛠 Dockerized Architecture

- Backend API containerized with `Dockerfile`.
- PostgreSQL (or MySQL) database containerized.
- Optional services (e.g., Redis) can be included.

### 🧩 Docker Compose

Uses `docker-compose.yml` to orchestrate:

- Backend API
- Database
- Supporting services

**Run the project:**

```bash
docker-compose up --build
