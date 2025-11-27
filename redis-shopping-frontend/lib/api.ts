const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

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
