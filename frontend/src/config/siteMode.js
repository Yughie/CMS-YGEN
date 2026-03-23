export const ACTIVE_INDUSTRY = "real_estate";

const INDUSTRY_COPY = {
  real_estate: {
    siteName: "YGEN Estates",
    heroFallbackTitle: "Premium Real Estate Showcase",
    heroHomeTitle: "Discover Extraordinary Homes Crafted for Modern Living",
    domainLabel: "Estates",
  },
  product: {
    siteName: "YGEN Products",
    heroFallbackTitle: "Premium Product Showcase",
    heroHomeTitle: "Discover Signature Products Designed to Define Categories",
    domainLabel: "Products",
  },
};

export const activeIndustryCopy =
  INDUSTRY_COPY[ACTIVE_INDUSTRY] || INDUSTRY_COPY.real_estate;

export function filterByActiveIndustry(contents) {
  if (!Array.isArray(contents)) return [];
  return contents.filter((item) => item.industry === ACTIVE_INDUSTRY);
}
