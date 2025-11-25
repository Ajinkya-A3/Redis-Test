'use server';

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
