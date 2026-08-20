import React from "react";
import { NormalizedProductData } from "@/types";
import { ExternalLink, ShieldCheck, ShoppingBag } from "lucide-react";

interface ProductCardProps {
  product: NormalizedProductData;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const currencySymbol = product.currency === "EUR" ? "€" : "$";
  const formattedPrice = `${currencySymbol}${product.price.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;

  return (
    <div className="bg-[#16120e] border border-[#261f18] hover:border-[#3d2e22] rounded-xl p-5 shadow-md transition-all duration-200 flex flex-col justify-between">
      <div>
        {/* Track-style numbered header */}
        <div className="flex items-center justify-between gap-3 mb-4 pb-3 border-b border-[#261f18]">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-[#f59e0b] font-mono tracking-wider">
              01 — SCRAPED ITEM
            </span>
          </div>

          {product.is_in_stock ? (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              In Stock
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-rose-400" />
              Out of Stock
            </span>
          )}
        </div>

        {/* Product Information Header */}
        <div className="flex items-start gap-3 mb-4">
          {product.image_url ? (
            <div className="w-12 h-12 rounded-lg overflow-hidden bg-[#0e0b08] border border-[#261f18] shrink-0">
              <img
                src={product.image_url}
                alt={product.product_name}
                className="w-full h-full object-cover"
                onError={(e) => {
                  (e.target as HTMLElement).style.display = "none";
                }}
              />
            </div>
          ) : (
            <div className="w-12 h-12 rounded-lg bg-[#0e0b08] border border-[#261f18] flex items-center justify-center shrink-0 text-[#f59e0b]">
              <ShoppingBag className="w-5 h-5" />
            </div>
          )}

          <div>
            <h3 className="text-base font-bold text-[#f5f0eb] tracking-tight line-clamp-1">
              {product.product_name}
            </h3>
            {product.description && (
              <p className="text-xs text-[#a8a29e] line-clamp-2 mt-1 leading-relaxed">
                {product.description}
              </p>
            )}
          </div>
        </div>

        {/* Metric Price Display */}
        <div className="grid grid-cols-2 gap-3 my-4 p-3.5 rounded-lg bg-[#0e0b08] border border-[#261f18]">
          <div>
            <span className="text-[11px] text-[#a8a29e] font-medium block">Normalized Price</span>
            <span className="text-2xl font-black text-[#f5f0eb] font-mono mt-0.5 block">
              {formattedPrice}
            </span>
          </div>
          <div>
            <span className="text-[11px] text-[#a8a29e] font-medium block">Currency Code</span>
            <span className="text-xs font-bold text-[#f59e0b] font-mono inline-block px-2.5 py-0.5 rounded bg-[#f59e0b]/10 border border-[#f59e0b]/20 mt-1">
              {product.currency || "USD"}
            </span>
          </div>
        </div>
      </div>

      {/* Footer Meta */}
      <div className="flex items-center justify-between pt-3 border-t border-[#261f18] text-xs">
        <div className="flex items-center gap-1.5 text-[#a8a29e]">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Gemini AI Validated</span>
        </div>
        {product.url && (
          <a
            href={product.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-[#f59e0b] hover:text-amber-400 font-semibold transition-colors"
          >
            <span>Target URL</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>
    </div>
  );
};
