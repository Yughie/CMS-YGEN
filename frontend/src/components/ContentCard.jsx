import { Link } from "react-router-dom";

function getPrimaryImage(images) {
  if (!Array.isArray(images) || images.length === 0) return null;
  return images.find((item) => item.is_primary) || images[0];
}

function getMetaValue(content, key) {
  return content?.metadata?.[key] || "";
}

export function ContentCard({ content }) {
  const primaryImage = getPrimaryImage(content.images);
  const city = getMetaValue(content, "city");
  const listingType =
    getMetaValue(content, "listing_type") || content.industry.replace("_", " ");

  return (
    <article className="group overflow-hidden rounded-[1.4rem] border border-stone-300/80 bg-white/92 shadow-[0_28px_65px_-38px_rgba(37,24,10,0.65)] transition duration-400 hover:-translate-y-1.5 hover:shadow-[0_35px_75px_-34px_rgba(37,24,10,0.7)]">
      <div className="relative h-60 overflow-hidden bg-stone-200">
        {primaryImage ? (
          <img
            src={primaryImage.image_url}
            alt={primaryImage.alt_text || content.title}
            className="h-full w-full object-cover transition duration-700 group-hover:scale-110"
            loading="lazy"
          />
        ) : (
          <div className="grid h-full place-items-center bg-[linear-gradient(135deg,#e7dfd3,#cfc4b0)] text-xs tracking-[0.16em] text-stone-600 uppercase">
            No image
          </div>
        )}

        <div className="absolute inset-x-0 bottom-0 h-24 bg-[linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,0.65))]" />
        <span className="absolute left-3 top-3 rounded-full bg-white/92 px-3 py-1 text-[11px] font-semibold tracking-[0.12em] text-stone-900 uppercase">
          {content.industry.replace("_", " ")}
        </span>
        {city ? (
          <span className="absolute bottom-3 left-3 rounded-full bg-black/50 px-3 py-1 text-xs font-medium text-stone-100 backdrop-blur-sm">
            {city}
          </span>
        ) : null}
      </div>

      <div className="space-y-5 p-5 sm:p-6">
        <div>
          <h2 className="font-display text-[1.75rem] leading-tight tracking-tight text-stone-900">
            {content.title}
          </h2>
          <p className="mt-2 line-clamp-3 text-sm leading-6 text-stone-600">
            {content.excerpt || content.description || "No summary provided."}
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <span className="rounded-full border border-stone-200 bg-stone-50 px-3 py-1 text-[11px] font-semibold tracking-[0.08em] text-stone-700 uppercase">
            {listingType}
          </span>
          <span className="rounded-full border border-stone-200 bg-stone-50 px-3 py-1 text-[11px] font-semibold tracking-[0.08em] text-stone-700 uppercase">
            {content.status}
          </span>
        </div>

        <Link
          to={`/content/${content.slug}`}
          className="inline-flex items-center gap-2 rounded-full bg-stone-900 px-5 py-2.5 text-sm font-semibold text-stone-50 transition hover:bg-stone-700"
        >
          Explore Listing
          <span aria-hidden="true">-&gt;</span>
        </Link>
      </div>
    </article>
  );
}
