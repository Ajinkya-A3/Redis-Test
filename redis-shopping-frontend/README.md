# Redis Shopping Frontend

Next.js 15 frontend for Redis Shopping API with complete server-side architecture.

## Features

- Server-Side Only: All API calls via Server Actions
- Runtime Env Vars: Docker-ready with no rebuild needed
- Modern Stack: Next.js 15, React 19, TypeScript
- shadcn/ui: Beautiful, accessible components
- Secure Auth: HttpOnly cookies, middleware protection

## Quick Start

### Local Development

Install dependencies:
npm install

Copy environment file:
cp .env.example .env

Run development server:
npm run dev

Visit http://localhost:3000

### Docker Production

Build and run:
docker compose up --build

## Default Credentials

Email: user@example.com
Password: password123

## Environment Variables

Server-side only (NOT prefixed with NEXT_PUBLIC_):
API_BASE_URL=http://localhost:8000
NODE_ENV=development

## Tech Stack

- Framework: Next.js 15 (App Router)
- Language: TypeScript
- UI: shadcn/ui + Tailwind CSS
- Icons: Lucide React
- Validation: Zod
- Runtime: Node.js 22

## Available Scripts

- npm run dev - Development server
- npm run build - Production build
- npm run start - Production server
- npm run lint - ESLint

## Security Features

- Server-side API calls only
- HttpOnly session cookies
- Middleware route protection
- CSRF protection via Server Actions
- No client-side secrets

Built with Redis, FastAPI, and Next.js
