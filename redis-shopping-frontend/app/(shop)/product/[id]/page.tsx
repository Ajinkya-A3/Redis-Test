import { notFound } from 'next/navigation';
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
