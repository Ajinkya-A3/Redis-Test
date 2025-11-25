#!/usr/bin/env python3
"""
Redis Shopping Frontend Generator
Generates complete Next.js 15 App Router project with shadcn/ui
"""

import os
from pathlib import Path
from typing import Dict

class FrontendGenerator:
    def __init__(self, base_dir: str = "redis-shopping-frontend"):
        self.base_dir = Path(base_dir)
        self.files: Dict[str, str] = {}
        
    def create_directory_structure(self):
        """Create all necessary directories"""
        directories = [
            "app/(auth)/login",
            "app/(shop)/product/[id]",
            "app/(shop)/cart",
            "app/actions",
            "components/ui",
            "lib",
        ]
        
        print("📁 Creating directory structure...")
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created: {directory}")
    
    def define_files(self):
        """Define all file contents"""
        
        self.files["package.json"] = """{
  "name": "redis-shopping-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "15.1.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.4",
    "tailwindcss-animate": "^1.0.7",
    "lucide-react": "^0.454.0",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^22.10.1",
    "@types/react": "^19.0.1",
    "@types/react-dom": "^19.0.2",
    "typescript": "^5.7.2",
    "tailwindcss": "^3.4.15",
    "postcss": "^8.4.49",
    "autoprefixer": "^10.4.20",
    "eslint": "^9.16.0",
    "eslint-config-next": "15.1.0"
  }
}
"""

        self.files["components.json"] = """{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
"""

        self.files["next.config.ts"] = """import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  output: 'standalone',
};

export default nextConfig;
"""

        self.files["tailwind.config.ts"] = """import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)'
      },
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))'
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))'
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))'
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))'
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))'
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))'
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))'
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        chart: {
          '1': 'hsl(var(--chart-1))',
          '2': 'hsl(var(--chart-2))',
          '3': 'hsl(var(--chart-3))',
          '4': 'hsl(var(--chart-4))',
          '5': 'hsl(var(--chart-5))'
        }
      }
    }
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
"""

        self.files["tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""

        self.files["postcss.config.mjs"] = """/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};

export default config;
"""

        self.files[".env.example"] = """# Server-side only (NOT prefixed with NEXT_PUBLIC_)
API_BASE_URL=http://localhost:8000
NODE_ENV=development
"""

        self.files[".dockerignore"] = """node_modules
.next
.git
.gitignore
README.md
.env
.env.local
.env.*.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store
"""

        self.files["Dockerfile"] = """# Stage 1: Dependencies
FROM node:22-alpine AS deps
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# Stage 2: Builder
FROM node:22-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

# Stage 3: Runner
FROM node:22-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
"""

        self.files["docker-compose.yml"] = """version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - API_BASE_URL=http://backend:8000
      - NODE_ENV=production
    depends_on:
      - backend
    networks:
      - redis-shop-network

  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      - redis
    networks:
      - redis-shop-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - redis-shop-network

networks:
  redis-shop-network:
    driver: bridge

volumes:
  redis-data:
"""

        self.files[".gitignore"] = """# dependencies
node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local
.env

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
"""

        self.files["lib/utils.ts"] = """import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPrice(price: number): string {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
  }).format(price);
}
"""

        self.files["lib/api.ts"] = """const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

export interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
}

export interface ApiResponse<T> {
  source: string;
  data: T;
}

export interface CartItem {
  pid: number;
  qty: number;
}

export interface HomepageData {
  banners: string[];
  featured: number[];
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      cache: 'no-store',
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async login(email: string, password: string): Promise<{ token: string }> {
    return this.request<{ token: string }>('/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async getMe(token: string): Promise<{ user_id: number }> {
    return this.request<{ user_id: number }>('/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async getProduct(id: number): Promise<ApiResponse<Product>> {
    return this.request<ApiResponse<Product>>(`/product/${id}`);
  }

  async getHomepage(): Promise<ApiResponse<HomepageData>> {
    return this.request<ApiResponse<HomepageData>>('/homepage');
  }

  async addToCart(token: string, pid: number, qty: number = 1): Promise<{ message: string; cart: CartItem[] }> {
    return this.request<{ message: string; cart: CartItem[] }>(`/cart/add?pid=${pid}&qty=${qty}`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async getCart(token: string): Promise<{ cart: CartItem[] }> {
    return this.request<{ cart: CartItem[] }>('/cart', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }
}

export const apiClient = new ApiClient();
"""

        self.files["lib/session.ts"] = """import { cookies } from 'next/headers';

const SESSION_COOKIE = 'redis_shop_session';

export async function setSession(token: string) {
  const cookieStore = await cookies();
  cookieStore.set(SESSION_COOKIE, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60,
    path: '/',
  });
}

export async function getSession(): Promise<string | null> {
  const cookieStore = await cookies();
  const session = cookieStore.get(SESSION_COOKIE);
  return session?.value || null;
}

export async function clearSession() {
  const cookieStore = await cookies();
  cookieStore.delete(SESSION_COOKIE);
}
"""

        self.files["middleware.ts"] = """import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('redis_shop_session')?.value;
  const { pathname } = request.nextUrl;

  const isPublicRoute = pathname === '/login';

  if (isPublicRoute && token) {
    return NextResponse.redirect(new URL('/', request.url));
  }

  if (!isPublicRoute && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
"""

        self.files["app/actions/auth.ts"] = """'use server';

import { redirect } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { setSession, clearSession, getSession } from '@/lib/session';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

export async function loginAction(formData: FormData) {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;

  const validation = loginSchema.safeParse({ email, password });
  
  if (!validation.success) {
    return {
      error: validation.error.errors[0].message,
    };
  }

  try {
    const { token } = await apiClient.login(email, password);
    await setSession(token);
    redirect('/');
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Login failed',
    };
  }
}

export async function logoutAction() {
  await clearSession();
  redirect('/login');
}

export async function getCurrentUser() {
  const token = await getSession();
  
  if (!token) {
    return null;
  }

  try {
    const user = await apiClient.getMe(token);
    return user;
  } catch (error) {
    await clearSession();
    return null;
  }
}
"""

        self.files["app/actions/product.ts"] = """'use server';

import { apiClient } from '@/lib/api';

export async function getProductAction(id: number) {
  try {
    const response = await apiClient.getProduct(id);
    return { data: response.data, source: response.source };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Failed to fetch product',
    };
  }
}

export async function getHomepageAction() {
  try {
    const response = await apiClient.getHomepage();
    return { data: response.data, source: response.source };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Failed to fetch homepage',
    };
  }
}
"""

        self.files["app/actions/cart.ts"] = """'use server';

import { revalidatePath } from 'next/cache';
import { apiClient } from '@/lib/api';
import { getSession } from '@/lib/session';

export async function addToCartAction(productId: number, quantity: number = 1) {
  const token = await getSession();

  if (!token) {
    return { error: 'Not authenticated' };
  }

  try {
    const result = await apiClient.addToCart(token, productId, quantity);
    revalidatePath('/cart');
    return { success: true, message: result.message };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Failed to add to cart',
    };
  }
}

export async function getCartAction() {
  const token = await getSession();

  if (!token) {
    return { cart: [] };
  }

  try {
    const { cart } = await apiClient.getCart(token);
    return { cart };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Failed to fetch cart',
    };
  }
}
"""

        self.files["app/globals.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 5.9% 10%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
    --card: 240 10% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 240 10% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 240 5.9% 10%;
    --secondary: 240 3.7% 15.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 240 3.7% 15.9%;
    --muted-foreground: 240 5% 64.9%;
    --accent: 240 3.7% 15.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 3.7% 15.9%;
    --input: 240 3.7% 15.9%;
    --ring: 240 4.9% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
"""

        self.files["app/layout.tsx"] = """import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Redis Shop",
  description: "Redis-powered shopping application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
"""

        self.files["app/(auth)/login/page.tsx"] = """import { redirect } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { loginAction, getCurrentUser } from '@/app/actions/auth';

export default async function LoginPage() {
  const user = await getCurrentUser();
  
  if (user) {
    redirect('/');
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Login to Redis Shop</CardTitle>
          <CardDescription>Enter your credentials to continue</CardDescription>
        </CardHeader>
        <CardContent>
          <form action={loginAction} className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">
                Email
              </label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="user@example.com"
                required
                defaultValue="user@example.com"
              />
            </div>
            
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">
                Password
              </label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="••••••••"
                required
                defaultValue="password123"
              />
            </div>

            <Button type="submit" className="w-full">
              Login
            </Button>

            <p className="text-xs text-muted-foreground text-center">
              Demo: user@example.com / password123
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
"""

        self.files["app/(shop)/layout.tsx"] = """import { redirect } from 'next/navigation';
import { Header } from '@/components/header';
import { getCurrentUser } from '@/app/actions/auth';

export default async function ShopLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const user = await getCurrentUser();

  if (!user) {
    redirect('/login');
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
}
"""

        self.files["app/(shop)/page.tsx"] = """import { Badge } from '@/components/ui/badge';
import { ProductCard } from '@/components/product-card';
import { getHomepageAction, getProductAction } from '@/app/actions/product';

export default async function HomePage() {
  const homepage = await getHomepageAction();

  if ('error' in homepage) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">{homepage.error}</p>
      </div>
    );
  }

  const products = await Promise.all(
    homepage.data.featured.map((id) => getProductAction(id))
  );

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-4xl font-bold">Welcome to Redis Shop</h1>
        <Badge variant="secondary">
          Cached from {homepage.source}
        </Badge>
      </div>

      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">Featured Products</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((result) => {
            if ('error' in result) return null;
            return <ProductCard key={result.data.id} product={result.data} />;
          })}
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">Special Offers</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {homepage.data.banners.map((banner, idx) => (
            <div
              key={idx}
              className="bg-gradient-to-r from-blue-500 to-purple-500 text-white p-8 rounded-lg"
            >
              <p className="text-xl font-bold">{banner}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
"""

        self.files["app/(shop)/product/[id]/page.tsx"] = """import { notFound } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { formatPrice } from '@/lib/utils';
import { getProductAction } from '@/app/actions/product';
import { addToCartAction } from '@/app/actions/cart';

export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const result = await getProductAction(Number(id));

  if ('error' in result) {
    notFound();
  }

  const { data: product, source } = result;

  async function handleAddToCart() {
    'use server';
    await addToCartAction(product.id, 1);
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle className="text-3xl">{product.name}</CardTitle>
              <CardDescription>Product ID: {product.id}</CardDescription>
            </div>
            <Badge variant="secondary">From {source}</Badge>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-6">
          <div>
            <p className="text-4xl font-bold">{formatPrice(product.price)}</p>
          </div>

          <div>
            <Badge variant={product.stock > 0 ? 'default' : 'destructive'}>
              {product.stock > 0 ? `${product.stock} units available` : 'Out of stock'}
            </Badge>
          </div>

          <form action={handleAddToCart}>
            <Button
              type="submit"
              size="lg"
              className="w-full"
              disabled={product.stock === 0}
            >
              Add to Cart
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
"""

        self.files["app/(shop)/cart/page.tsx"] = """import { CartItem } from '@/components/cart-item';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { formatPrice } from '@/lib/utils';
import { getCartAction } from '@/app/actions/cart';
import { getProductAction } from '@/app/actions/product';

export default async function CartPage() {
  const { cart } = await getCartAction();

  if (!cart || cart.length === 0) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold mb-4">Your Cart is Empty</h1>
        <p className="text-muted-foreground">Add some products to get started!</p>
      </div>
    );
  }

  const cartItems = await Promise.all(
    cart.map(async (item) => {
      const result = await getProductAction(item.pid);
      if ('error' in result) return null;
      return { product: result.data, quantity: item.qty };
    })
  );

  const validItems = cartItems.filter((item) => item !== null);
  const total = validItems.reduce(
    (sum, item) => sum + item.product.price * item.quantity,
    0
  );

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Shopping Cart</h1>

      <div className="space-y-4">
        {validItems.map((item) => (
          <CartItem
            key={item.product.id}
            product={item.product}
            quantity={item.quantity}
          />
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Order Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-between items-center text-2xl font-bold">
            <span>Total:</span>
            <span>{formatPrice(total)}</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
"""

        self.files["components/header.tsx"] = """import Link from 'next/link';
import { ShoppingCart, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { getCurrentUser } from '@/app/actions/auth';
import { logoutAction } from '@/app/actions/auth';

export async function Header() {
  const user = await getCurrentUser();

  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="text-2xl font-bold">
          Redis Shop
        </Link>
        
        {user && (
          <div className="flex items-center gap-4">
            <Link href="/cart">
              <Button variant="outline" size="icon">
                <ShoppingCart className="h-4 w-4" />
              </Button>
            </Link>
            
            <form action={logoutAction}>
              <Button variant="ghost" size="sm" type="submit">
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </form>
          </div>
        )}
      </div>
    </header>
  );
}
"""

        self.files["components/product-card.tsx"] = """import Link from 'next/link';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { formatPrice } from '@/lib/utils';
import { Product } from '@/lib/api';

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{product.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <p className="text-2xl font-bold">{formatPrice(product.price)}</p>
          <Badge variant={product.stock > 0 ? 'default' : 'destructive'}>
            {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
          </Badge>
        </div>
      </CardContent>
      <CardFooter>
        <Link href={`/product/${product.id}`} className="w-full">
          <Button className="w-full" disabled={product.stock === 0}>
            View Details
          </Button>
        </Link>
      </CardFooter>
    </Card>
  );
}
"""

        self.files["components/cart-item.tsx"] = """import { Card, CardContent } from '@/components/ui/card';
import { formatPrice } from '@/lib/utils';
import { Product } from '@/lib/api';

interface CartItemProps {
  product: Product;
  quantity: number;
}

export function CartItem({ product, quantity }: CartItemProps) {
  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="font-semibold">{product.name}</h3>
            <p className="text-sm text-muted-foreground">Quantity: {quantity}</p>
          </div>
          <div className="text-right">
            <p className="font-bold">{formatPrice(product.price * quantity)}</p>
            <p className="text-sm text-muted-foreground">
              {formatPrice(product.price)} each
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
"""

        self.files["components/ui/button.tsx"] = """import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default:
          "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline:
          "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
"""

        self.files["components/ui/card.tsx"] = """import * as React from "react"

import { cn } from "@/lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-xl border bg-card text-card-foreground shadow",
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("font-semibold leading-none tracking-tight", className)}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
"""

        self.files["components/ui/input.tsx"] = """import * as React from "react"

import { cn } from "@/lib/utils"

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
"""

        self.files["components/ui/badge.tsx"] = """import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80",
        secondary:
          "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive:
          "border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/80",
        outline: "text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
"""

        self.files["README.md"] = """# Redis Shopping Frontend

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
"""

    def write_files(self):
        """Write all files to disk"""
        print("\n📝 Writing files...")
        
        for file_path, content in self.files.items():
            full_path = self.base_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✓ Created: {file_path}")
    
    def generate(self):
        """Main generation method"""
        print("🚀 Redis Shopping Frontend Generator")
        print("=" * 50)
        
        self.create_directory_structure()
        
        print("\n📋 Preparing file contents...")
        self.define_files()
        print(f"  ✓ {len(self.files)} files ready")
        
        self.write_files()
        
        print("\n" + "=" * 50)
        print("✅ Frontend project generated successfully!")
        print("\n📌 Next Steps:")
        print(f"  1. cd {self.base_dir}")
        print("  2. npm install")
        print("  3. cp .env.example .env")
        print("  4. npm run dev")
        print("\n🌐 Access at: http://localhost:3000")
        print("👤 Login: user@example.com / password123")
        print("\n🐳 For Docker: docker compose up --build")
        print("=" * 50)


def main():
    """Entry point"""
    import sys
    
    dir_name = sys.argv[1] if len(sys.argv) > 1 else "redis-shopping-frontend"
    
    generator = FrontendGenerator(dir_name)
    generator.generate()


if __name__ == "__main__":
    main()
