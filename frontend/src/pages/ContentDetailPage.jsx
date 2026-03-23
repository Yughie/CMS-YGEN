import { useEffect, useMemo, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";

import { BlockRenderer } from "../components/BlockRenderer";
import { ListingAssistantChat } from "../components/ListingAssistantChat";

function getPrimaryImage(content) {
  if (!Array.isArray(content?.images)) return null;
  return (
    content.images.find((item) => item.is_primary) || content.images[0] || null
  );
}

function formatCurrency(value, currency = "USD") {
  const amount = Number(value);
  if (Number.isNaN(amount)) return String(value || "By request");
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(amount);
}

function getMetaValue(content, keys) {
  const metadata = content?.metadata || {};
  const lower = Object.fromEntries(
    Object.entries(metadata).map(([key, value]) => [key.toLowerCase(), value]),
  );

  for (const key of keys) {
    const value = lower[key.toLowerCase()];
    if (value !== undefined && value !== null && String(value).trim() !== "") {
      return String(value);
    }
  }

  return null;
}

function getRealEstateDetails(content) {
  if (!content || content.industry !== "real_estate") return null;

  const details = content.real_estate_details || {};
  const bedrooms =
    details.bedrooms ?? getMetaValue(content, ["bedrooms", "beds"]);
  const bathrooms =
    details.bathrooms ?? getMetaValue(content, ["bathrooms", "baths"]);
  const areaSqft =
    details.area_sqft ??
    getMetaValue(content, ["area_sqft", "sqft", "area", "size"]);
  const address =
    details.address_line ||
    getMetaValue(content, ["address", "location", "city"]);
  const price = details.listing_price
    ? formatCurrency(details.listing_price, details.currency || "USD")
    : getMetaValue(content, ["price", "list_price", "value"]) || "By request";

  return {
    address,
    price,
    bedrooms: bedrooms != null && bedrooms !== "" ? String(bedrooms) : null,
    bathrooms: bathrooms != null && bathrooms !== "" ? String(bathrooms) : null,
    areaSqft: areaSqft != null && areaSqft !== "" ? String(areaSqft) : null,
  };
}

function getHeroFacts(content, realEstateDetails) {
  return [
    {
      label: "Location",
      value:
        realEstateDetails?.address ||
        getMetaValue(content, [
          "city",
          "location",
          "neighborhood",
          "address",
        ]) ||
        "Prime district",
    },
    {
      label: "Value",
      value:
        realEstateDetails?.price ||
        getMetaValue(content, ["price", "list_price", "value"]) ||
        "By request",
    },
    {
      label: "Type",
      value:
        getMetaValue(content, ["property_type", "listing_type", "category"]) ||
        content.industry.replace("_", " "),
    },
  ];
}

function getHighlightChips(content, realEstateDetails) {
  const candidates = [
    realEstateDetails?.bedrooms ? `${realEstateDetails.bedrooms} Beds` : null,
    realEstateDetails?.bathrooms
      ? `${realEstateDetails.bathrooms} Baths`
      : null,
    realEstateDetails?.areaSqft ? `${realEstateDetails.areaSqft} Sq Ft` : null,
    getMetaValue(content, ["bedrooms", "beds"]),
    getMetaValue(content, ["bathrooms", "baths"]),
    getMetaValue(content, ["area", "sqft", "size"]),
    getMetaValue(content, ["parking", "garage"]),
  ].filter(Boolean);

  if (candidates.length > 0) {
    return candidates.map((item) => String(item));
  }

  return ["Architectural detail", "Natural light", "Private access"];
}

function RealEstateSpecStrip({ details }) {
  if (!details) return null;

  const specs = [
    { label: "Price", value: details.price },
    {
      label: "Bedrooms",
      value: details.bedrooms ? `${details.bedrooms}` : null,
    },
    {
      label: "Bathrooms",
      value: details.bathrooms ? `${details.bathrooms}` : null,
    },
    {
      label: "Area",
      value: details.areaSqft ? `${details.areaSqft} sq ft` : null,
    },
    { label: "Address", value: details.address },
  ].filter((item) => item.value);

  if (specs.length === 0) return null;

  return (
    <section
      className="reveal-block border-y border-stone-300/60 bg-[linear-gradient(180deg,rgba(253,252,248,0.95),rgba(241,236,227,0.88))] px-6 py-10 sm:px-10 lg:px-14"
      data-reveal
    >
      <div className="mx-auto max-w-[1500px]">
        <p className="text-xs tracking-[0.2em] text-stone-500 uppercase">
          Property Details
        </p>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {specs.map((spec) => (
            <div key={spec.label} className="border-l border-stone-500/60 pl-3">
              <p className="text-[10px] tracking-[0.15em] text-stone-500 uppercase">
                {spec.label}
              </p>
              <p className="mt-1 text-base font-semibold text-stone-900">
                {spec.value}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function MetadataPanel({ content }) {
  const entries = Object.entries(content.metadata || {});
  if (entries.length === 0) return null;

  return (
    <section className="border-l border-stone-400/70 pl-5">
      <h2 className="font-display text-2xl tracking-tight text-stone-900">
        Metadata
      </h2>
      <dl className="mt-4 grid gap-3 sm:grid-cols-2">
        {entries.map(([key, value]) => (
          <div key={key} className="border-b border-stone-300/70 pb-2">
            <dt className="text-xs tracking-[0.12em] text-stone-500 uppercase">
              {key}
            </dt>
            <dd className="mt-1 text-sm font-medium text-stone-800">
              {String(value)}
            </dd>
          </div>
        ))}
      </dl>
    </section>
  );
}

function ScatteredGallery({ content }) {
  const images = useMemo(
    () => (Array.isArray(content.images) ? content.images : []),
    [content.images],
  );

  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    if (images.length <= 1) return;

    const interval = window.setInterval(() => {
      setActiveIndex((previous) => (previous + 1) % images.length);
    }, 3600);

    return () => window.clearInterval(interval);
  }, [images.length]);

  const display = useMemo(() => {
    if (images.length === 0) {
      return {
        leadImage: null,
        supportImages: [],
        editorialImages: [],
        normalizedIndex: 0,
      };
    }

    const normalizedIndex = activeIndex % images.length;
    const leadImage = images[normalizedIndex];

    const supportIndices = [1, 2, 3]
      .map((offset) => (normalizedIndex + offset) % images.length)
      .filter((value, index, array) => array.indexOf(value) === index)
      .slice(0, Math.min(3, Math.max(0, images.length - 1)));

    const supportImages = supportIndices.map((index) => images[index]);
    const used = new Set([normalizedIndex, ...supportIndices]);
    const editorialImages = images.filter((_, index) => !used.has(index));

    return { leadImage, supportImages, editorialImages, normalizedIndex };
  }, [activeIndex, images]);

  if (images.length === 0 || !display.leadImage) return null;

  return (
    <section className="reveal-block visual-story-stage" data-reveal>
      <div className="mb-4 flex flex-wrap items-end justify-between gap-3 px-1 sm:px-2">
        <h2 className="font-display text-xl tracking-tight text-stone-900 sm:text-3xl">
          Visual Story
        </h2>
        <p className="max-w-md text-xs tracking-[0.18em] text-stone-500 uppercase">
          Immersive gallery
        </p>
      </div>

      <div className="grid gap-2 lg:grid-cols-[1.25fr_0.75fr]">
        <figure className="visual-lead group relative aspect-[16/10] max-h-[300px] overflow-hidden bg-stone-900 sm:max-h-[360px] lg:max-h-[400px]">
          <img
            key={`lead-backdrop-${display.leadImage.id}`}
            src={display.leadImage.image_url}
            alt=""
            aria-hidden="true"
            className="absolute inset-0 h-full w-full scale-110 object-cover blur-md"
            loading="lazy"
          />
          <div className="pointer-events-none absolute inset-0 bg-black/45" />
          <img
            key={display.leadImage.id}
            src={display.leadImage.image_url}
            alt={display.leadImage.alt_text}
            className="visual-lead-image relative z-10 h-full w-full object-cover"
            loading="lazy"
          />
          <div className="pointer-events-none absolute inset-0 z-10 bg-[linear-gradient(140deg,rgba(0,0,0,0.08),rgba(0,0,0,0.58))]" />
          <figcaption className="absolute inset-x-0 bottom-0 px-4 py-4 text-stone-100 sm:px-6 sm:py-5">
            <p className="text-[10px] tracking-[0.2em] uppercase">Lead Frame</p>
            <p className="font-display text-lg sm:text-2xl">
              {display.leadImage.caption || display.leadImage.alt_text}
            </p>
          </figcaption>
        </figure>

        <div className="grid gap-2 sm:grid-cols-3 lg:grid-cols-1">
          {display.supportImages.map((image, index) => (
            <figure
              key={`support-${image.id}`}
              className="visual-support group relative h-[120px] overflow-hidden bg-stone-900 sm:h-[136px]"
              style={{ animationDelay: `${index * 140}ms` }}
            >
              <img
                src={image.image_url}
                alt=""
                aria-hidden="true"
                className="absolute inset-0 h-full w-full scale-110 object-cover blur-sm"
                loading="lazy"
              />
              <div className="pointer-events-none absolute inset-0 bg-black/50" />
              <img
                src={image.image_url}
                alt={image.alt_text}
                className="relative z-10 h-full w-full object-cover transition duration-[1300ms] group-hover:scale-105"
                loading="lazy"
              />
              <div className="pointer-events-none absolute inset-0 z-10 bg-[linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,0.65))]" />
              <figcaption className="absolute inset-x-0 bottom-0 z-20 px-3 py-2 text-xs text-stone-100">
                {image.caption ||
                  `Moment ${String(index + 1).padStart(2, "0")}`}
              </figcaption>
            </figure>
          ))}
        </div>
      </div>

      {display.editorialImages.length > 0 ? (
        <div className="no-scrollbar mt-2 flex gap-2 overflow-x-auto pb-1">
          {display.editorialImages.map((image, index) => {
            return (
              <figure
                key={image.id}
                className="editorial-tile group relative h-24 min-w-[145px] overflow-hidden bg-stone-900 sm:h-32 sm:min-w-[195px]"
                style={{ animationDelay: `${index * 120}ms` }}
              >
                <img
                  src={image.image_url}
                  alt=""
                  aria-hidden="true"
                  className="absolute inset-0 h-full w-full scale-110 object-cover blur-sm"
                  loading="lazy"
                />
                <div className="pointer-events-none absolute inset-0 bg-black/50" />
                <img
                  src={image.image_url}
                  alt={image.alt_text}
                  className="relative z-10 h-full w-full object-cover transition duration-[1400ms] group-hover:scale-105"
                  loading="lazy"
                />
                <figcaption className="absolute inset-x-0 bottom-0 z-20 px-4 py-3 text-xs text-stone-100">
                  {image.caption || image.alt_text}
                </figcaption>
              </figure>
            );
          })}
        </div>
      ) : null}

      {images.length > 1 ? (
        <div className="mt-4 flex items-center justify-center gap-2">
          {images.map((image, index) => (
            <button
              key={`dot-${image.id}`}
              type="button"
              aria-label={`Show image ${index + 1}`}
              onClick={() => setActiveIndex(index)}
              className={`h-2.5 rounded-full transition-all duration-300 ${
                display.normalizedIndex === index
                  ? "w-8 bg-stone-900"
                  : "w-2.5 bg-stone-400/60 hover:bg-stone-500"
              }`}
            />
          ))}
        </div>
      ) : null}
    </section>
  );
}

export function ContentDetailPage({ contents }) {
  const { slug } = useParams();
  const content = contents.find((item) => item.slug === slug);
  const primaryImage = getPrimaryImage(content);
  const realEstateDetails = content ? getRealEstateDetails(content) : null;
  const heroFacts = content ? getHeroFacts(content, realEstateDetails) : [];
  const highlightChips = content
    ? getHighlightChips(content, realEstateDetails)
    : [];

  useEffect(() => {
    const nodes = document.querySelectorAll("[data-reveal]");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2 },
    );

    nodes.forEach((node) => observer.observe(node));
    return () => observer.disconnect();
  }, []);

  if (!slug) return <Navigate to="/" replace />;
  if (!content) {
    return (
      <main className="space-y-6 px-6 py-10 sm:px-10 lg:px-14">
        <Link
          to="/"
          className="text-sm font-semibold text-stone-700 hover:text-stone-900"
        >
          ← Back to Content List
        </Link>
        <section className="border-y border-stone-300/80 py-8 text-center">
          <h1 className="font-display text-3xl tracking-tight text-stone-900">
            Content Not Found
          </h1>
          <p className="mt-2 text-stone-600">
            The requested slug does not exist in the latest API response.
          </p>
        </section>
      </main>
    );
  }

  return (
    <>
      <main className="space-y-0 overflow-hidden">
        <section
          className="reveal-block immersive-film relative min-h-[92vh] overflow-hidden bg-stone-900 text-stone-100"
          data-reveal
        >
          {primaryImage ? (
            <img
              src={primaryImage.image_url}
              alt={primaryImage.alt_text || content.title}
              className="cinema-pan absolute inset-0 h-full w-full object-cover opacity-60"
            />
          ) : null}
          <div className="absolute inset-0 bg-[linear-gradient(120deg,rgba(8,6,4,0.88),rgba(8,6,4,0.55)_60%,rgba(8,6,4,0.25))]" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_65%_20%,rgba(255,233,191,0.18),rgba(255,233,191,0))]" />
          <div className="relative mx-auto grid min-h-[84vh] max-w-[1500px] gap-10 px-6 py-14 sm:px-10 lg:grid-cols-[1fr_360px] lg:items-end lg:px-14">
            <div>
              <p className="text-xs tracking-[0.22em] text-amber-200 uppercase">
                {content.industry.replace("_", " ")}
              </p>
              <h1 className="mt-3 max-w-5xl font-display text-5xl leading-[0.9] tracking-tight sm:text-7xl lg:text-8xl">
                {content.title}
              </h1>
              {content.description ? (
                <p className="mt-5 max-w-3xl text-stone-100 sm:text-xl">
                  {content.description}
                </p>
              ) : null}
              <div className="mt-8 flex flex-wrap gap-3">
                {highlightChips.map((item) => (
                  <span
                    key={item}
                    className="border border-white/35 bg-black/15 px-4 py-1.5 text-[11px] tracking-[0.16em] text-stone-100 uppercase backdrop-blur-sm"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>

            <aside className="border-l border-white/35 pl-6 backdrop-blur-sm">
              <p className="text-[11px] tracking-[0.18em] text-stone-200 uppercase">
                Listing Snapshot
              </p>
              <div className="mt-4 space-y-4">
                {heroFacts.map((fact) => (
                  <div key={fact.label} className="space-y-1">
                    <p className="text-[10px] tracking-[0.16em] text-stone-300 uppercase">
                      {fact.label}
                    </p>
                    <p className="text-lg font-semibold text-white">
                      {fact.value}
                    </p>
                  </div>
                ))}
                <div className="border-t border-white/25 pt-3 text-sm">
                  <span className="text-stone-300">Status</span>
                  <span className="ml-2 font-semibold text-white">
                    {content.status}
                  </span>
                </div>
              </div>
            </aside>
          </div>
        </section>

        <section className="relative px-4 py-8 sm:px-6 lg:px-8">
          <div className="pointer-events-none absolute inset-x-0 top-0 h-20 bg-[linear-gradient(180deg,rgba(0,0,0,0.08),rgba(0,0,0,0))]" />
          <div className="mx-auto max-w-[1220px]">
            <ScatteredGallery content={content} />
          </div>
        </section>

        <RealEstateSpecStrip details={realEstateDetails} />

        <section className="border-t border-stone-300/60 px-6 py-10 sm:px-10 lg:px-14">
          <div className="mx-auto grid max-w-[1400px] gap-8 xl:grid-cols-[1fr_320px]">
            <div className="space-y-6 reveal-block" data-reveal>
              <BlockRenderer content={content} />
            </div>
            <div
              className="reveal-block xl:sticky xl:top-24 xl:self-start"
              data-reveal
            >
              <MetadataPanel content={content} />
            </div>
          </div>
        </section>

        <section
          className="reveal-block bg-[linear-gradient(120deg,#12100c,#21180f)] px-6 py-12 text-stone-100 sm:px-10 lg:px-14"
          data-reveal
        >
          <div className="mx-auto max-w-[1400px]">
            <p className="text-xs tracking-[0.22em] text-amber-300 uppercase">
              Private Inquiry
            </p>
            <h2 className="mt-3 max-w-3xl font-display text-4xl tracking-tight sm:text-6xl">
              Interested in this listing experience?
            </h2>
            <p className="mt-4 max-w-2xl text-stone-300">
              This immersive page is generated from your CMS content blocks,
              metadata, and uploaded images. Tailor every section to your brand
              voice in admin.
            </p>
          </div>
        </section>
      </main>
      <ListingAssistantChat content={content} />
    </>
  );
}
