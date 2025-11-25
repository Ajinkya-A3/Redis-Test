import { CartItem } from '@/components/cart-item';
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
