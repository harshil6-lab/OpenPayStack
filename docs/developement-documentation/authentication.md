# Authentication Module

## Overview

Authentication verifies the identity of a user before allowing access to protected resources.

OpenPayStack follows a layered authentication architecture inspired by production fintech systems.

---

# Objectives

- Secure user registration
- Secure login
- Password hashing
- Password verification
- JWT Authentication (Upcoming)
- Refresh Tokens (Upcoming)
- RBAC (Upcoming)
- OAuth2 (Upcoming)
- MFA (Upcoming)

---

# Current Authentication Flow

## Registration

Client

↓

POST /auth/register

↓

Request Validation

↓

Check Existing User

↓

Hash Password (bcrypt)

↓

Create User

↓

Create Wallet

↓

Commit Transaction

↓

Return Safe Response

---

## Login

Client

↓

POST /auth/login

↓

Validate Request

↓

Find User

↓

Verify Password

↓

Return Safe Response

---

# Current Endpoints

POST /auth/register

Creates a new user and automatically provisions a wallet.

---

POST /auth/login

Authenticates user credentials.

(Currently returns user information.)

JWT integration will replace this response.

---

# Password Security

Passwords are never stored.

Passwords are hashed using bcrypt.

Verification is performed using bcrypt.verify().

---

# Security Decisions

User enumeration prevention.

Instead of:

User not found

or

Wrong password

API always returns

Invalid credentials

---

# Current Architecture

Client

↓

FastAPI Router

↓

Service Layer

↓

SQLAlchemy

↓

PostgreSQL

---

# Future Roadmap

- JWT Access Tokens
- Refresh Tokens
- Token Rotation
- Logout
- Token Blacklisting
- Redis
- OAuth2
- MFA
- Passkeys
- RBAC
- API Keys
- Device Trust
- Session Management

---

# Lessons Learned

- Layered Architecture
- Dependency Injection
- Password Hashing
- Password Verification
- Secure Response Models
- Generic Error Responses
- Docker Infrastructure
- Database Connectivity
- Production-style Debugging