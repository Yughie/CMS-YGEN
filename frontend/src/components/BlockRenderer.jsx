function CtaButton({ block, tone = "light" }) {
  const href = block.cta_href || block.payload?.cta_href;
  const label = block.cta_label || block.payload?.cta_label || "Learn more";
  const style = block.cta_style || block.payload?.cta_style || "primary";

  const lightStyleMap = {
    primary: "border-b border-stone-900 text-stone-900",
    secondary: "border-b border-amber-700 text-amber-800",
    ghost: "border-b border-stone-500 text-stone-700",
  };

  const darkStyleMap = {
    primary: "border-b border-white text-white",
    secondary: "border-b border-amber-300 text-amber-100",
    ghost: "border-b border-stone-200 text-stone-100",
  };

  const styleMap = tone === "dark" ? darkStyleMap : lightStyleMap;

  if (!href) return null;

  return (
    <a
      href={href}
      target={block.cta_target || block.payload?.cta_target || "_self"}
      rel="noreferrer"
      className={`inline-flex pb-1 text-xs font-semibold tracking-[0.18em] uppercase transition ${styleMap[style] || styleMap.primary}`}
    >
      {label}
    </a>
  );
}

function renderGalleryImages(content, block) {
  const allImages = Array.isArray(content.images) ? content.images : [];
  const limit = Number(block.payload?.limit || 6);
  return allImages.slice(0, limit);
}

function getBackdropImage(content, position) {
  const images = Array.isArray(content.images) ? content.images : [];
  if (images.length === 0) return null;
  return images[position % images.length];
}

export function BlockRenderer({ content }) {
  const blocks = Array.isArray(content.blocks)
    ? [...content.blocks]
        .filter((item) => item.is_active)
        .sort((a, b) => a.position - b.position)
    : [];

  return (
    <div className="space-y-0 border-y border-stone-300/55">
      {blocks.map((block) => {
        const backdrop = getBackdropImage(content, block.position);

        if (block.block_type === "hero") {
          return (
            <section
              key={block.id}
              className="relative isolate overflow-hidden border-t border-stone-300/50 px-6 py-12 text-stone-100 sm:px-10 sm:py-14"
            >
              {backdrop ? (
                <img
                  src={backdrop.image_url}
                  alt={backdrop.alt_text || "Block background"}
                  className="absolute inset-0 -z-20 h-full w-full object-cover opacity-45"
                  loading="lazy"
                />
              ) : null}
              <div className="absolute inset-0 -z-10 bg-[linear-gradient(125deg,rgba(10,7,4,0.92),rgba(10,7,4,0.72)_55%,rgba(10,7,4,0.5))]" />
              <p className="text-xs tracking-[0.22em] text-amber-300 uppercase">
                Featured Hero
              </p>
              <h2 className="mt-2 font-display text-4xl leading-[0.95] tracking-tight sm:text-6xl">
                {block.title || content.title}
              </h2>
              {block.body ? (
                <p className="mt-4 max-w-2xl leading-7 text-stone-200">
                  {block.body}
                </p>
              ) : null}
              <div className="mt-6">
                <CtaButton block={block} tone="dark" />
              </div>
            </section>
          );
        }

        if (block.block_type === "rich_text") {
          return (
            <section
              key={block.id}
              className="relative isolate overflow-hidden border-t border-stone-300/50 px-6 py-12 text-stone-100 sm:px-10"
            >
              {backdrop ? (
                <img
                  src={backdrop.image_url}
                  alt={backdrop.alt_text || "Story background"}
                  className="absolute inset-0 -z-20 h-full w-full object-cover opacity-28"
                  loading="lazy"
                />
              ) : null}
              <div className="absolute inset-0 -z-10 bg-[linear-gradient(132deg,rgba(18,14,10,0.88),rgba(18,14,10,0.74)_45%,rgba(18,14,10,0.55))]" />
              {block.title ? (
                <h3 className="font-display text-4xl tracking-tight text-white sm:text-5xl">
                  {block.title}
                </h3>
              ) : null}
              {block.body ? (
                <p className="mt-4 max-w-4xl leading-8 text-stone-100/90">
                  {block.body}
                </p>
              ) : null}
            </section>
          );
        }

        if (block.block_type === "gallery") {
          const galleryImages = renderGalleryImages(content, block);

          return (
            <section
              key={block.id}
              className="border-t border-stone-300/55 bg-stone-100/85 px-6 py-12 sm:px-10"
            >
              {block.title ? (
                <h3 className="font-display text-4xl tracking-tight text-stone-900 sm:text-5xl">
                  {block.title}
                </h3>
              ) : null}
              <div className="mt-6 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
                {galleryImages.length === 0 ? (
                  <p className="text-sm text-stone-500">
                    No gallery images available.
                  </p>
                ) : (
                  galleryImages.map((image) => (
                    <figure
                      key={image.id}
                      className="group relative overflow-hidden bg-stone-100"
                    >
                      <img
                        src={image.image_url}
                        alt={image.alt_text}
                        className="h-44 w-full object-cover transition duration-700 group-hover:scale-110"
                        loading="lazy"
                      />
                      <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,0.35))]" />
                      {image.caption ? (
                        <figcaption className="absolute inset-x-0 bottom-0 px-3 py-2 text-xs text-stone-100">
                          {image.caption}
                        </figcaption>
                      ) : null}
                    </figure>
                  ))
                )}
              </div>
            </section>
          );
        }

        if (block.block_type === "cta") {
          return (
            <section
              key={block.id}
              className="relative isolate overflow-hidden border-t border-stone-300/55 px-6 py-12 text-stone-100 sm:px-10"
            >
              {backdrop ? (
                <img
                  src={backdrop.image_url}
                  alt={backdrop.alt_text || "CTA background"}
                  className="absolute inset-0 -z-20 h-full w-full object-cover opacity-35"
                  loading="lazy"
                />
              ) : null}
              <div className="absolute inset-0 -z-10 bg-[linear-gradient(122deg,rgba(34,23,12,0.92),rgba(34,23,12,0.72))]" />
              {block.title ? (
                <h3 className="font-display text-4xl tracking-tight text-white sm:text-5xl">
                  {block.title}
                </h3>
              ) : null}
              {block.body ? (
                <p className="mt-3 max-w-3xl text-stone-100/90">{block.body}</p>
              ) : null}
              <div className="mt-6">
                <CtaButton block={block} tone="dark" />
              </div>
            </section>
          );
        }

        return (
          <section
            key={block.id}
            className="border-t border-stone-300/55 bg-white/70 px-6 py-12 sm:px-10"
          >
            <h3 className="font-display text-xl text-stone-900">
              Unsupported block type: {block.block_type}
            </h3>
            <p className="mt-2 text-sm text-stone-600">
              This block type has no renderer yet.
            </p>
          </section>
        );
      })}
    </div>
  );
}
