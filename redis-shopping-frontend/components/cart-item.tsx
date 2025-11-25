import { Card, CardContent } from '@/components/ui/card';
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
