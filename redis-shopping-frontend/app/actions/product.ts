'use server';

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
