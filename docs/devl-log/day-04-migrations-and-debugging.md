# OpenPayStack — Day 04 Migrations & Database Versioning

## Overview

Today focused on completing the database foundation layer by introducing schema versioning with Alembic and resolving several real-world infrastructure issues.

The goal was to move from manually creating tables toward a professional database migration workflow.

---

# Objectives Completed

## Docker Infrastructure

### PostgreSQL Container

Successfully started PostgreSQL using Docker Compose.

### Port Mapping

Configured:

```txt
Host:      5434
Container: 5432
```

### Learning

Docker allows local development environments to remain isolated and reproducible.

The application communicates with PostgreSQL through the mapped host port.

---

# Environment Configuration

## DATABASE_URL

Configured database connection through environment variables.

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/openpaystack
```

### Learning

Environment variables separate configuration from source code and prevent sensitive information from being hardcoded.

---

# Debugging Session

## Docker Compose Validation Error

### Error

```txt
volumes must be a mapping
```

### Root Cause

Incorrect volume declaration:

```yaml
volumes:
  postgres_data
```

### Fix

```yaml
volumes:
  postgres_data:
```

### Learning

YAML syntax errors can prevent infrastructure from starting.

Understanding configuration files is as important as understanding application code.

---

# Database Connectivity Verification

Verified:

```txt
Python Application
        ↓
SQLAlchemy
        ↓
Docker Networking
        ↓
PostgreSQL Container
```

### Learning

Backend systems should always be tested layer by layer instead of debugging multiple components simultaneously.

---

# Foreign Key Debugging

## Error

```txt
NoReferencedTableError
```

### Root Cause

Wallet model referenced:

```python
ForeignKey("user.id")
```

while the actual table name was:

```python
__tablename__ = "users"
```

### Fix

```python
ForeignKey("users.id")
```

### Learning

Foreign keys reference database table names, not Python class names.

---

# Database Table Creation

Successfully executed:

```bash
python -m app.create_tables
```

### Tables Created

- users
- wallets

### Generated Database Components

- primary keys
- foreign keys
- unique constraints
- indexes
- timestamps

### Learning

SQLAlchemy metadata generates actual SQL statements which are executed against PostgreSQL.

---

# Alembic Installation

Installed:

```bash
pip install alembic
```

### Purpose

Alembic provides schema versioning and migration management for relational databases.

---

# Alembic Initialization

Executed:

```bash
alembic init alembic
```

### Generated Structure

```txt
alembic/
├── versions/
├── env.py
├── script.py.mako

alembic.ini
```

### Learning

Alembic creates the framework required to manage database schema history.

---

# Metadata Registration

Configured:

```python
target_metadata = Base.metadata
```

inside:

```txt
alembic/env.py
```

Registered models:

- User
- Wallet

### Learning

Alembic uses SQLAlchemy metadata to discover database structure and schema changes.

---

# First Migration

Generated first migration:

```bash
alembic revision --autogenerate -m "create users and wallets tables"
```

### Result

Migration file created inside:

```txt
alembic/versions/
```

### Learning

Alembic compares:

```txt
SQLAlchemy Models
        VS
Current Database State
```

and generates migration operations automatically.

---

# Important Backend Concepts Learned

## Foreign Keys

Maintain ownership and relational integrity.

Example:

```txt
wallet.user_id
        ↓
users.id
```

---

## Referential Integrity

Prevents invalid relationships and orphan records.

---

## Database Versioning

Database schemas should be version-controlled just like application code.

---

## Migrations

Migrations allow schema evolution without manually modifying production databases.

---

## Infrastructure Debugging

A professional debugging approach:

```txt
Infrastructure
        ↓
Database
        ↓
ORM
        ↓
Application
```

instead of debugging everything simultaneously.

---

# Current Architecture Status

```txt
Docker
   │
PostgreSQL
   │
SQLAlchemy
   │
Alembic
   │
User
   │
Wallet
```

All foundational persistence layers are operational.

---

# Git Management

## Commit Alembic

The following should be committed:

```txt
alembic/
alembic.ini
alembic/versions/
```

### Reason

Migration files represent database history and are part of the application's source code.

---

# Key Engineering Lessons

Today reinforced several critical backend engineering principles:

- Infrastructure should be validated layer-by-layer.
- Foreign keys reference table names, not class names.
- Database schemas are code.
- Migrations are the professional way to evolve databases.
- Dockerized services should be treated as production-like infrastructure.
- Debugging is a structured process, not trial and error.

---

# Development Philosophy

OpenPayStack follows:

```txt
Build
→ Analyze
→ Debug
→ Fix
→ Harden
→ Scale
→ Observe
```

Each stage is intended to build deep understanding rather than simply producing working code.

---

# Next Steps

Upcoming focus:

- Authentication Architecture
- Password Hashing
- Registration Flow
- Dependency Injection
- Database Session Lifecycle
- JWT Foundation
- Secure Authentication Design