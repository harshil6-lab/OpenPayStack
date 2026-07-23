# OpenPayStack

Open-source financial systems sandbox for learning backend architecture, payment orchestration, security, and distributed systems.

> ⚠️ **Status: Active development.** Core authentication is implemented but has known wiring bugs . Not production-ready. Do not use to handle real funds or real user credentials.

---

## Overview

OpenPayStack is an educational engineering project exploring how modern financial systems work internally — backend architecture, secure authentication, transaction orchestration, and distributed infrastructure — through hands-on implementation rather than theory.

It is **not** a real banking platform. It does not process real transactions or connect to real banking infrastructure. All security experiments and attack simulations are meant to run only in controlled local environments.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| Database | PostgreSQL |
| ORM / migrations | SQLAlchemy + Alembic |
| Auth | JWT (`python-jose`), `passlib[bcrypt]` |
| Config | `pydantic-settings` (`.env`) |
| Server | Uvicorn |
| Local infra | Docker Compose |

Planned additions: Redis (caching), RabbitMQ (queues), NGINX, Prometheus/Grafana.

---

## Features

### Implemented
- User registration with unique email/username enforcement
- Password hashing via bcrypt (`passlib`)
- JWT access + refresh token issuance
- **Refresh token rotation** — every refresh invalidates the old token and issues a new pair
- **Refresh token reuse detection** — if a revoked/rotated refresh token is replayed, all active sessions for that user are revoked (stolen-token mitigation)
- Per-device session tracking (IP address, user agent, revocation state) backed by a dedicated `sessions` table
- Logout (single session) and logout-all-devices
- Wallet record auto-created on user registration
- `/users/me` authenticated profile endpoint

### Planned
- Ledger engine & transaction consistency
- Payment orchestration flow
- Redis caching layer
- Queue-based async transaction processing
- Rate limiting & brute-force protection
- Security testing lab (SQLi, XSS, CSRF, replay, token tampering)
- Observability stack (logging, metrics, monitoring)

---

## Architecture

```
app/
├── api/
│   ├── routes/
│   │   ├── auth.py        # /auth/register, /login, /refresh, /logout, /sessions
│   │   └── user.py        # /users/me
│   └── dependencies.py    # get_db, get_current_user (OAuth2 bearer)
├── core/
│   ├── database.py        # SQLAlchemy engine/session
│   ├── security.py        # password hashing, JWT encode/decode
│   └── device.py
├── models/
│   ├── user.py
│   ├── wallet.py
│   └── sessions.py
├── schemas/                # Pydantic request/response models
├── services/
│   ├── user_service.py     # registration, login, logout
│   └── token_service.py    # token issuance, rotation, reuse detection
└── main.py

config/settings.py          # env-driven settings (SECRET_KEY, DB URL, token TTLs)
alembic/                     # DB migrations
docker/docker-compose.yml    # local Postgres
```

---

## Authentication Flow

1. **Register** (`POST /auth/register`) — creates a `User` + linked `Wallet`, password hashed with bcrypt.
2. **Login** (`POST /auth/login`) — verifies credentials (OAuth2 password form), issues an access token (short-lived) and a refresh token (long-lived), and records a `Session` row with device metadata.
3. **Authenticated requests** — send `Authorization: Bearer <access_token>`; `get_current_user` decodes and validates the token on every request.
4. **Refresh** (`POST /auth/refresh`) — exchanges a valid refresh token for a new access/refresh pair. The old refresh token is marked `revoked`. If a revoked token is ever presented again, it's treated as theft: `reuse_detected` is set and **every active session for that user is revoked.**
5. **Logout** (`POST /auth/logout`) — revokes the session tied to the given refresh token.
6. **Logout all devices** (`POST /auth/logout_all_devices`) — revokes every active session for the current user.
7. **Sessions** (`GET /auth/sessions`) — lists the current user's session history.

### Token design
- Access token: short TTL (default 15 min), carries `sub`, `email`, `role`, `type=access`, `jti`.
- Refresh token: long TTL (default 30 days), carries `sub`, `type=refresh`, `jti`. The `jti` is persisted server-side in `sessions.refresh_jti`, which is what makes rotation and reuse detection possible — a stateless-only JWT setup can't do this.

---

## Known Issues

These currently prevent the auth flow from running end-to-end and should be the first things fixed:

1. **`UserService.login_user`** calls `TokenService.generate_token_pair(user)` but the method requires a `device` argument — login will raise `TypeError`.
2. **`TokenService.rotate_refresh_token`** calls `self.create_session(user=user, refresh_jti=newjti)` without `device` — `/auth/refresh` will raise `TypeError`.
3. **`app/api/routes/auth.py`** references `status.HTTP_200_OK` but never imports `status` from `fastapi` — `/auth/sessions` will raise `NameError`.
4. **`GET /auth/sessions`** passes the full `current_user` object into `UserService.get_sessions`, but the service expects a `UUID` and filters `Session.user_id == user_id` — this comparison won't match as written.

None of these are architectural problems — the token rotation and reuse-detection design is sound — they're integration bugs from arguments not being threaded through consistently.

### Not yet hardened for production use
- No rate limiting on `/auth/login` (there's a load-test script, `testing_login.py`, but no corresponding protection)
- Access tokens can't be revoked before expiry — only refresh tokens are tracked server-side
- `User.is_verified` exists but no email-verification flow enforces it
- `User.role` is embedded in the access token but nothing currently checks it (no RBAC enforcement layer)
- No CORS configuration or security headers set on the FastAPI app

---

## Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- `pip`

### 1. Clone and install dependencies
```bash
git clone <repo-url>
cd OpenPayStack
pip install -r requirements.txt
```

### 2. Start PostgreSQL
```bash
cd docker
docker compose up -d
```
This starts Postgres on `localhost:5434` (db `openpaystack`, user/pass `postgres`/`postgres`).

### 3. Configure environment
Create a `.env` file in the project root:
```env
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/openpaystack
```

### 4. Run migrations
```bash
alembic upgrade head
```
(Alternatively, `python -m app.create_tables` will create tables directly from the models for quick local testing — this bypasses Alembic history, so prefer migrations once the schema stabilizes.)

### 5. Run the API
```bash
uvicorn app.main:app --reload
```
API available at `http://127.0.0.1:8000`, interactive docs at `http://127.0.0.1:8000/docs`.

---

## API Reference

| Method | Path | Auth required | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Create a new user + wallet |
| POST | `/auth/login` | No | Exchange credentials for access/refresh tokens |
| POST | `/auth/refresh` | No (refresh token in body) | Rotate refresh token, issue new pair |
| POST | `/auth/logout` | No (refresh token in body) | Revoke a single session |
| POST | `/auth/logout_all_devices` | Yes | Revoke all sessions for the current user |
| GET | `/auth/sessions` | Yes | List current user's sessions |
| GET | `/users/me` | Yes | Get the current authenticated user's profile |
| GET | `/` | No | Health check |

---

## Roadmap

- [x] Core authentication system (JWT, rotation, reuse detection, sessions)
- [ ] Fix known auth wiring bugs
- [ ] Rate limiting & brute-force protection
- [ ] Wallet & transaction module
- [ ] Ledger engine
- [ ] Payment orchestration flow
- [ ] Redis caching layer
- [ ] Queue-based transaction processing
- [ ] Security testing lab
- [ ] Observability stack
- [ ] Scalability simulations

---

## Disclaimer

This project is for educational and research purposes only. It does not process real financial transactions or connect to real banking infrastructure. All attack simulations and security experiments are intended to run only in controlled local environments.

## License

MIT License — see [LICENSE](LICENSE).
