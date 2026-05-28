# OpenPayStack — Day 03 Database Foundation

## Overview

Today focused on building the foundational database architecture and persistence layer for OpenPayStack.

The goal was to establish a production-inspired backend foundation capable of safely handling trusted financial state.

This phase introduced:
- ORM architecture
- PostgreSQL integration
- database sessions
- relational modeling
- UUID-based entity design
- financial-safe numeric handling

---

# Objectives Completed

## Database Architecture Initialization
- Configured SQLAlchemy engine
- Configured session management
- Created declarative ORM base
- Connected FastAPI backend to PostgreSQL

---

# ORM Understanding

## What is ORM?

ORM (Object Relational Mapper) maps Python objects to relational database tables.

### Example

| Python Object | Database Table |
|---|---|
| User class | users table |
| Wallet class | wallets table |

ORM allows backend systems to interact with databases using Python abstractions while still relying on relational database guarantees internally.

---

# Database Core Setup

## File Created

```txt
app/core/database.py
```

### Responsibilities
- database engine creation
- connection management
- session creation
- ORM base initialization

---

# SQLAlchemy Engine

## Purpose

The SQLAlchemy engine acts as the application's database communication layer.

It manages:
- connection pooling
- SQL execution
- PostgreSQL communication

### Important Learning

The engine does NOT maintain a single permanent connection.

Instead, it manages reusable database connections efficiently through connection pooling.

---

# Connection Pooling

## Why It Matters

Without pooling:
- every request creates a new database connection
- performance degrades significantly under load

Connection pooling improves:
- scalability
- efficiency
- resource utilization

---

# Database Sessions

## Important Clarification

Database sessions are NOT user authentication sessions.

### Database Session Meaning

A SQLAlchemy session represents:

```txt
A managed transaction workspace between the application and the database.
```

The session manages:
- inserts
- updates
- queries
- commits
- rollbacks

---

# Why Database Sessions Matter in FinTech

Financial systems require transactional safety.

### Example Risk

```txt
Deduct sender balance
Receiver update fails
```

Without proper rollback handling:
- money may disappear
- balances become corrupted

Database sessions help prevent partial transaction corruption.

---

# Environment Variables

## .env Configuration

Added environment-based configuration handling.

### Example Variable

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/openpaystack
```

---

# Security Principle

Sensitive values should NEVER be hardcoded into source code.

Examples:
- database credentials
- JWT secrets
- API keys

Environment variables improve:
- security
- portability
- deployment flexibility

---

# Models Directory Structure

## Created

```txt
app/models/
```

### Initial Models
- user.py
- wallet.py

---

# User Entity Design

## User Model

Represents:
- identity
- authentication ownership
- platform access control

### Fields
- id
- email
- username
- hashed_password
- role
- is_verified
- created_at

---

# UUID Strategy

## Why UUIDs Were Chosen

Instead of sequential IDs like:

```txt
1, 2, 3, 4
```

UUIDs provide:
- globally unique identifiers
- harder-to-predict IDs
- improved distributed-system compatibility

### Security Benefit

UUIDs reduce predictable resource enumeration risks.

---

# Constraints & Validation

## Database-Level Integrity

Applied:
- unique constraints
- nullable restrictions
- indexes

### Important Learning

Frontend validation alone is NOT sufficient.

The database itself must enforce integrity rules.

---

# Indexing

## Why Indexes Matter

Indexes improve query performance.

Without indexes:
- database scans entire tables
- performance degrades under scale

Indexes become critical for:
- authentication lookups
- wallet retrieval
- transaction queries

---

# Wallet Entity Design

## Wallet Model

Represents:
- financial ownership
- balance container
- transaction participation

### Fields
- id
- user_id
- balance
- currency
- is_locked
- created_at

---

# Foreign Key Relationships

## user_id → users.id

Established relational ownership between:
- users
- wallets

### Important Learning

Foreign keys enforce:
- ownership integrity
- relational consistency
- prevention of orphan records

---

# Financial Precision

## Why Float Was Avoided

Financial systems should NEVER use floating-point arithmetic for money calculations.

### Risk

Floating-point arithmetic introduces:
- rounding errors
- precision inconsistencies

### Solution

Used:

```python
Numeric(12, 2)
```

for precise decimal handling.

This is critical in financial system engineering.

---

# Table Creation Layer

## File Created

```txt
app/create_tables.py
```

### Purpose
- register ORM metadata
- create PostgreSQL tables
- initialize database schema

---

# Initial Persistent Entities

## Current Database Entities

```txt
User
Wallet
```

These represent the first persistent trusted-state layer of OpenPayStack.

---

# Key Backend Engineering Learnings

Today introduced several foundational backend concepts:

- ORM architecture
- database sessions
- transaction management
- relational modeling
- UUID-based design
- indexing strategy
- foreign key integrity
- financial precision handling
- persistence layer architecture

---

# Important Engineering Principle

The database is the source of truth.

Not:
- frontend state
- client payloads
- cached values

This principle is especially critical in financial systems.

---

# Current System Status

## Completed
- Backend foundation
- PostgreSQL integration
- ORM architecture
- User model
- Wallet model
- Table creation workflow

## Pending
- Relationships
- migrations
- authentication implementation
- transaction lifecycle
- ledger system
- secure session management

---

# Next Steps

Upcoming focus areas:

- SQLAlchemy relationships
- Alembic migrations
- Database constraints
- Auth architecture implementation
- Password hashing
- JWT lifecycle
- Session persistence

---

# Development Philosophy

OpenPayStack follows:

```txt
Build
→ Analyze
→ Attack
→ Fix
→ Harden
→ Scale
→ Observe
```

The project prioritizes engineering depth and architectural understanding over rapid feature development.