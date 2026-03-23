import { useEffect } from "react";
import { Link } from "react-router-dom";

import { activeIndustryCopy } from "../config/siteMode";
import { EmptyView } from "../components/StatusView";

function pickHeroContent(contents) {
  return contents[0] || null;
}

function getPrimaryImage(content) {
  if (!content || !Array.isArray(content.images)) return null;
  return (
    content.images.find((item) => item.is_primary) || content.images[0] || null
  );
}

function getGallery(contents) {
  return contents
    .flatMap((content) => (Array.isArray(content.images) ? content.images : []))
    .slice(0, 10);
}

export function ContentListPage({ contents }) {
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
      { threshold: 0.18 },
    );

    nodes.forEach((node) => observer.observe(node));
    return () => observer.disconnect();
  }, []);

  const total = contents.length;
  const heroContent = pickHeroContent(contents);
  const heroImage = getPrimaryImage(heroContent);
  const gallery = getGallery(contents);

  return (
    <main id="top" className="pb-16">
      <section
        className="showcase-glow reveal-block relative isolate min-h-[84vh] overflow-hidden px-6 py-12 text-stone-100 sm:px-10 sm:py-16 lg:px-14"
        data-reveal
      >
        {heroImage ? (
          <img
            src={heroImage.image_url}
            alt={heroImage.alt_text || "Homepage showcase"}
            className="absolute inset-0 h-full w-full object-cover opacity-50"
          />
        ) : null}
        <div className="absolute inset-0 bg-[linear-gradient(110deg,rgba(8,6,4,0.95),rgba(8,6,4,0.73)_45%,rgba(8,6,4,0.35))]" />

        <div className="relative mx-auto grid min-h-[70vh] max-w-[1400px] gap-10 lg:grid-cols-[1.2fr_0.8fr] lg:items-end">
          <div className="space-y-5">
            <p className="text-xs tracking-[0.28em] text-amber-200 uppercase">
              2026 Signature Collection
            </p>
            <h1 className="font-display text-4xl leading-[0.9] tracking-tight sm:text-6xl lg:text-8xl">
              {activeIndustryCopy.heroHomeTitle ||
                activeIndustryCopy.heroFallbackTitle}
            </h1>
            <p className="max-w-2xl text-sm leading-7 text-stone-200 sm:text-lg lg:text-xl">
              A cinematic one-page experience built to make every listing feel
              iconic, curated, and deeply trustworthy.
            </p>
            <div className="flex flex-wrap gap-5 pt-3 text-xs tracking-[0.2em] text-stone-200 uppercase">
              <span className="border-b border-white/45 pb-1">
                Curated Listings
              </span>
              <span className="border-b border-white/45 pb-1">
                Concierge Standards
              </span>
              <span className="border-b border-white/45 pb-1">
                Narrative First
              </span>
            </div>
            <a
              href="#story"
              className="mt-4 inline-flex border-b border-white pb-1 text-xs font-semibold tracking-[0.2em] text-white uppercase"
            >
              Start the tour
            </a>
          </div>

          <div className="grid grid-cols-3 gap-4 border-l border-white/25 pl-4 lg:pl-7">
            <div>
              <p className="font-display text-4xl text-white sm:text-5xl">
                {total}
              </p>
              <p className="text-[11px] tracking-[0.12em] text-stone-200 uppercase">
                Signature Listings
              </p>
            </div>
            <div>
              <p className="font-display text-2xl text-white sm:text-3xl">
                Prime Locations
              </p>
              <p className="text-[11px] tracking-[0.12em] text-stone-200 uppercase">
                Curated across premium neighborhoods
              </p>
            </div>
            <div>
              <p className="font-display text-2xl text-white sm:text-3xl">
                Private Viewings
              </p>
              <p className="text-[11px] tracking-[0.12em] text-stone-200 uppercase">
                Concierge-led, invitation-first tours
              </p>
            </div>
          </div>
        </div>
      </section>

      {total === 0 ? (
        <EmptyView
          title="No content available"
          message="Add content in Django Admin, then refresh to render cards here."
        />
      ) : (
        <>
          <section
            id="story"
            className="reveal-block grid gap-8 border-y border-stone-300/60 bg-[linear-gradient(180deg,rgba(250,248,243,0.94),rgba(241,236,227,0.84))] px-6 py-12 sm:px-10 lg:grid-cols-3 lg:px-14"
            data-reveal
          >
            <div className="border-l border-stone-900/55 pl-4">
              <p className="text-xs tracking-[0.2em] text-amber-200 uppercase">
                Market Reach
              </p>
              <p className="mt-2 font-display text-5xl text-stone-900">
                {total}
              </p>
              <p className="mt-1 text-sm text-stone-700">
                active {activeIndustryCopy.domainLabel.toLowerCase()} entries
              </p>
            </div>
            <div className="border-l border-stone-700/35 pl-4 text-stone-900">
              <p className="text-xs tracking-[0.2em] text-stone-600 uppercase">
                Buyer Confidence
              </p>
              <p className="mt-2 font-display text-4xl">Verified Listings</p>
              <p className="mt-1 text-sm text-stone-600">
                Every listing is editorially reviewed before publication
              </p>
            </div>
            <div className="border-l border-stone-700/35 pl-4 text-stone-900">
              <p className="text-xs tracking-[0.2em] text-stone-600 uppercase">
                White-Glove Service
              </p>
              <p className="mt-2 font-display text-4xl">Concierge Support</p>
              <p className="mt-1 text-sm text-stone-600">
                Tailored guidance from inquiry through closing
              </p>
            </div>
          </section>

          <section
            id="collection"
            className="reveal-block bg-stone-100/60 px-6 py-10 sm:px-10 lg:px-14"
            data-reveal
          >
            <div className="mx-auto flex max-w-[1400px] items-center justify-between">
              <h2 className="font-display text-4xl tracking-tight text-stone-900">
                Curated Collection
              </h2>
              <p className="text-xs tracking-[0.18em] text-stone-500 uppercase">
                Swipe through gallery
              </p>
            </div>
            <div className="no-scrollbar mx-auto mt-5 flex max-w-[1400px] gap-2 overflow-x-auto pb-2">
              {gallery.map((image) => (
                <figure
                  key={image.id}
                  className="relative min-w-[320px] max-w-[320px] overflow-hidden bg-stone-100"
                >
                  <img
                    src={image.image_url}
                    alt={image.alt_text}
                    className="h-72 w-full object-cover transition duration-700 hover:scale-105"
                    loading="lazy"
                  />
                  <figcaption className="absolute inset-x-0 bottom-0 bg-[linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,0.7))] px-4 py-3 text-xs text-stone-100">
                    {image.caption || image.alt_text}
                  </figcaption>
                </figure>
              ))}
            </div>
          </section>

          <section id="experience" className="space-y-0">
            {contents.map((content, index) => {
              const image = getPrimaryImage(content);
              return (
                <article
                  key={content.id}
                  className="reveal-block grid min-h-[76vh] items-stretch border-y border-stone-300/50 bg-[linear-gradient(120deg,rgba(255,255,255,0.45),rgba(244,239,231,0.76))] lg:grid-cols-2"
                  data-reveal
                >
                  <div
                    className={`${index % 2 === 1 ? "lg:order-2" : ""} overflow-hidden`}
                  >
                    {image ? (
                      <img
                        src={image.image_url}
                        alt={image.alt_text || content.title}
                        className="h-[360px] w-full object-cover transition duration-700 hover:scale-105 sm:h-[440px] lg:h-full"
                      />
                    ) : (
                      <div className="grid h-[320px] place-items-center bg-stone-200 text-sm text-stone-600">
                        No image available
                      </div>
                    )}
                  </div>
                  <div
                    className={`${index % 2 === 1 ? "lg:order-1" : ""} flex flex-col justify-center px-6 py-8 sm:px-10 lg:px-14`}
                  >
                    <p className="text-xs tracking-[0.2em] text-stone-500 uppercase">
                      {content.industry.replace("_", " ")}
                    </p>
                    <h3 className="mt-2 font-display text-4xl leading-[0.95] tracking-tight text-stone-900 sm:text-6xl">
                      {content.title}
                    </h3>
                    <p className="mt-4 max-w-2xl text-sm leading-7 text-stone-700 sm:text-lg">
                      {content.description ||
                        content.excerpt ||
                        "No description provided."}
                    </p>
                    <div className="mt-5 flex flex-wrap gap-2">
                      <span className="border-b border-stone-500/60 pb-1 text-[11px] font-semibold tracking-[0.12em] text-stone-700 uppercase">
                        {content.status}
                      </span>
                      <span className="border-b border-stone-500/60 pb-1 text-[11px] font-semibold tracking-[0.12em] text-stone-700 uppercase">
                        {content.images.length} image
                        {content.images.length === 1 ? "" : "s"}
                      </span>
                    </div>
                    <Link
                      to={`/listing/${content.slug}`}
                      className="mt-7 inline-flex w-fit border-b border-stone-900 pb-1 text-xs font-semibold tracking-[0.2em] text-stone-900 uppercase"
                    >
                      Enter immersive listing
                    </Link>
                  </div>
                </article>
              );
            })}
          </section>

          <section
            id="inquire"
            className="reveal-block bg-[linear-gradient(122deg,#12100c,#21180f)] px-6 py-12 text-stone-100 sm:px-10 lg:px-14"
            data-reveal
          >
            <div className="mx-auto max-w-[1400px]">
              <p className="text-xs tracking-[0.22em] text-amber-300 uppercase">
                Private Consultation
              </p>
              <h2 className="mt-3 max-w-3xl font-display text-4xl tracking-tight sm:text-6xl">
                Ready to turn this showcase into your live flagship property
                platform?
              </h2>
              <p className="mt-4 max-w-2xl text-stone-300">
                Everything on this page is already driven by your CMS API. The
                next step is refining content strategy and extending
                interactions.
              </p>
              <a
                href="#top"
                className="mt-8 inline-flex border-b border-white pb-1 text-xs font-semibold tracking-[0.18em] uppercase"
              >
                Return to top
              </a>
            </div>
          </section>
        </>
      )}
    </main>
  );
}
