# OpenPayStack — Day 05 Authentication Foundation & Registration Workflow

## Overview

Today marked the transition from infrastructure and database setup into application development.

The primary objective was to build the first complete business workflow:

```txt
User Registration
```

This workflow includes:

* Request validation
* Password hashing
* User creation
* Wallet creation
* Database transaction management
* API response serialization

At the end of the session, OpenPayStack successfully registered users through a FastAPI endpoint and persisted data into PostgreSQL.

---

# Objectives Completed

## Password Security Layer

Created:

```txt
app/core/security.py
```

Implemented:

* hash_password()
* verify_password()

Using:

```txt
passlib
bcrypt
```

### Learning

Passwords should never be stored in plaintext.

Instead:

```txt
Password
    ↓
bcrypt
    ↓
Hash
```

Only hashes are stored in the database.

---

# Password Verification Testing

Created a standalone testing module.

Verified:

```txt
hash_password()
verify_password()
```

Output confirmed:

```txt
Password Hashing
    ✅

Password Verification
    ✅
```

---

# API Schemas

Created:

```txt
app/schemas/user.py
```

Implemented:

## UserRegisterRequest

Request contract for registration.

Fields:

* email
* username
* password

Validation:

* Email validation
* Username length validation
* Password length validation

---

## UserResponse

Response contract returned to API consumers.

Fields:

* id
* email
* username
* is_verified

Excluded:

* password
* hashed_password

### Learning

Sensitive information must never be exposed through API responses.

---

# Service Layer

Created:

```txt
app/services/user_service.py
```

Implemented:

```python
register_user()
```

Responsibilities:

* Check existing user
* Hash password
* Create user
* Create wallet
* Commit transaction

### Learning

Business logic belongs in services, not API routes.

Architecture:

```txt
Route
    ↓
Service
    ↓
Database
```

---

# Database Session Dependency

Created:

```txt
app/api/dependencies.py
```

Implemented:

```python
get_db()
```

Purpose:

* Create database session
* Provide session to endpoint
* Automatically close session

### Learning

Every request should receive its own database session.

Improper session handling can lead to:

* Connection leaks
* Pool exhaustion
* Application instability

---

# Authentication Routes

Created:

```txt
app/api/routes/auth.py
```

Implemented:

```txt
POST /auth/register
```

Workflow:

```txt
Request
    ↓
Validation
    ↓
Service
    ↓
Database
    ↓
Response
```

---

# FastAPI Integration

Connected router to:

```txt
app/main.py
```

Registered:

```txt
/auth/register
```

Verified through:

```txt
Swagger UI
```

---

# Debugging & Lessons Learned

## Import Errors

Resolved multiple module import issues.

### Learning

Python imports depend heavily on package structure and execution context.

---

## bcrypt Compatibility Issue

Encountered compatibility issues between:

```txt
passlib
bcrypt 5.x
```

Resolved by downgrading bcrypt.

### Learning

Dependency compatibility is a real-world engineering concern.

---

## Foreign Key Issue

Resolved:

```txt
ForeignKey("user.id")
```

Changed to:

```txt
ForeignKey("users.id")
```

### Learning

Foreign keys reference table names, not class names.

---

## HTTPException Error

Incorrect:

```python
status=400
```

Correct:

```python
status_code=400
```

### Learning

Framework APIs must be followed exactly.

---

## ResponseValidationError

Encountered:

```txt
UUID returned
String expected
```

Resolved:

```python
id: UUID
```

instead of:

```python
id: str
```

### Learning

API schemas should accurately represent actual data types.

---

## Validation Errors

Experienced:

```txt
422 Unprocessable Entity
```

### Learning

422 indicates:

```txt
Request reached server
Validation failed
```

This is different from:

```txt
500 Internal Server Error
```

which indicates application failure.

---

# Successful Registration Flow

Final workflow:

```txt
Client
    ↓
POST /auth/register
    ↓
Pydantic Validation
    ↓
Hash Password
    ↓
Create User
    ↓
Create Wallet
    ↓
Commit Transaction
    ↓
Return Response
```

Successful response:

```json
{
  "id": "e3a8f98f-0e52-43f2-b391-85aa7766fa10",
  "email": "user@example.com",
  "username": "user123",
  "is_verified": false
}
```

---

# Security Achievements

Implemented:

```txt
Password Hashing
    ✅

Password Verification
    ✅

Response Sanitization
    ✅

Input Validation
    ✅

Unique User Protection
    ✅
```

Not exposed:

```txt
password
hashed_password
```

---

# Current Architecture

```txt
FastAPI
   │
Authentication Layer
   │
Service Layer
   │
SQLAlchemy
   │
PostgreSQL
```

---

# Current OpenPayStack Status

Infrastructure

```txt
Docker
PostgreSQL
SQLAlchemy
Alembic
```

Domain

```txt
User
Wallet
```

Security

```txt
bcrypt
Password Hashing
Password Verification
```

Application

```txt
Registration Endpoint
Swagger Testing
Database Transactions
```

---

# Key Engineering Lessons

* Passwords should be hashed, never stored directly.
* Business logic belongs in services.
* Validation belongs in schemas.
* Database sessions must be managed carefully.
* APIs should never expose sensitive fields.
* Database types and API types must remain consistent.
* Registration is the first step toward authentication.

---

# Next Steps

Upcoming implementation:

```txt
Login Endpoint
    ↓
Password Verification
    ↓
JWT Access Token
    ↓
Protected Routes
```

OpenPayStack will move from user registration to full authentication and authorization.
