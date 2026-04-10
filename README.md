# Vantage — AI Brand Deal Marketplace

A full-stack SaaS platform that connects brands with creators using AI-powered matching.

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | React 19, Tailwind CSS 3, shadcn/ui (46 components), Framer Motion, React Router 7 |
| Backend | FastAPI, Python 3.11, Motor (async MongoDB), JWT auth, Resend email |
| Database | MongoDB (local or Atlas) |
| AI | OpenAI GPT-4o-mini (audit analysis) |

---

## Quick Start

### Prerequisites
- Python 3.11
- Node.js 18+ (v24 via NVM is installed)
- MongoDB running locally on port 27017 (or Atlas connection string)

### 1 — Configure environment variables

**Backend** — edit `backend/.env`:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=vantage
JWT_SECRET=<generate: python -c "import secrets; print(secrets.token_hex(32))">
RESEND_API_KEY=re_...          # resend.com — free tier
SENDER_EMAIL=onboarding@resend.dev
FRONTEND_URL=http://localhost:3000
OPENAI_API_KEY=sk-...          # for AI audit analysis
ADMIN_EMAIL=admin@vantage.ai
ADMIN_PASSWORD=VantageAdmin123!
```

**Frontend** — `frontend/.env` is already configured:
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

### 2 — Start both servers

Double-click **`start-all.bat`** — launches backend + frontend in separate windows.

Or start individually:
- **`start-backend.bat`** → FastAPI on http://localhost:8001
- **`start-frontend.bat`** → React on http://localhost:3000

---

## Routes

| URL | Page |
|---|---|
| `/` | Landing page (hero, pricing, FAQ, waitlist) |
| `/audit` | Free 9-step AI campaign audit |
| `/login` | Login |
| `/register` | Register (brand or creator) |
| `/profile` | User profile editor |
| `/creators` | Creator discovery & search |
| `/campaigns` | Campaign listing |
| `/campaigns/new` | Create campaign |
| `/forgot-password` | Password reset request |
| `/reset-password` | Password reset (token) |
| `/verify-email` | Email verification |
| `/admin` | Admin dashboard |

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Current user |
| POST | `/api/auth/refresh` | Refresh JWT |
| POST | `/api/auth/forgot-password` | Send reset email |
| POST | `/api/auth/reset-password` | Reset with token |
| POST | `/api/waitlist/signup` | Join waitlist |
| GET | `/api/audit/questions` | Get audit questions |
| POST | `/api/audit/submit` | Submit audit + get AI results |
| GET/PUT | `/api/profile/me` | Get/update profile |
| GET | `/api/creators/` | List creators |
| POST | `/api/campaigns/` | Create campaign |
| GET | `/api/campaigns/` | List campaigns |
| GET | `/api/admin/stats` | Admin statistics |

Interactive docs: **http://localhost:8001/docs**

---

## Admin Access

```
Email:    admin@vantage.ai
Password: VantageAdmin123!
```

The admin account is automatically seeded on first backend startup.

---

## Design System

- **Colors:** Deep blacks (`#07070A`), gold accents (`#C9A55A`), subtle borders
- **Fonts:** Cormorant Garamond (serif headings), DM Sans (body), DM Mono (labels/CTAs)
- **Motion:** Framer Motion fade-up (0.8s ease), stagger children (0.1s)
- **Components:** 46 shadcn/ui components, fully customized to dark gold theme
