import { Badge } from '@/components/ui/badge';
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
