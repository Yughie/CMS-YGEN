import { Link, useLocation } from "react-router-dom";
import { activeIndustryCopy } from "../config/siteMode";

export function Shell({ children }) {
  const location = useLocation();
  const isHome = location.pathname === "/";

  return (
    <div className="relative min-h-screen overflow-hidden bg-[radial-gradient(circle_at_15%_-10%,#d9d0be_0,#efe8dc_35%,#f4f0e7_70%,#f6f3ed_100%)] text-stone-900">
      <header className="fixed inset-x-0 top-0 z-40 border-b border-white/25 bg-white/45 backdrop-blur-xl">
        <div className="mx-auto flex max-w-[1400px] flex-wrap items-center justify-between gap-4 px-5 py-3 sm:px-8 lg:px-12">
          <Link to="/" className="group flex items-center gap-3">
            <span className="inline-grid h-10 w-10 place-items-center rounded-xl bg-[linear-gradient(145deg,#1f150e,#4c3321)] text-sm font-semibold tracking-wide text-amber-50 transition-transform duration-300 group-hover:scale-105">
              YG
            </span>
            <div>
              <p className="font-display text-xl leading-none tracking-tight text-stone-900">
                {activeIndustryCopy.siteName}
              </p>
              <p className="text-[10px] tracking-[0.2em] text-stone-600 uppercase">
                Immersive Showcase
              </p>
            </div>
          </Link>

          {isHome ? (
            <nav className="hidden items-center gap-1 rounded-full border border-stone-300/60 bg-white/70 p-1 sm:flex">
              <a
                href="#story"
                className="rounded-full px-3 py-1.5 text-[11px] font-semibold tracking-wide text-stone-700 transition hover:bg-stone-900 hover:text-white"
              >
                Story
              </a>
              <a
                href="#collection"
                className="rounded-full px-3 py-1.5 text-[11px] font-semibold tracking-wide text-stone-700 transition hover:bg-stone-900 hover:text-white"
              >
                Collection
              </a>
              <a
                href="#experience"
                className="rounded-full px-3 py-1.5 text-[11px] font-semibold tracking-wide text-stone-700 transition hover:bg-stone-900 hover:text-white"
              >
                Listings
              </a>
              <a
                href="#inquire"
                className="rounded-full px-3 py-1.5 text-[11px] font-semibold tracking-wide text-stone-700 transition hover:bg-stone-900 hover:text-white"
              >
                Inquire
              </a>
            </nav>
          ) : (
            <Link
              to="/"
              className="hidden rounded-full border border-stone-300 bg-white px-4 py-2 text-[11px] font-semibold tracking-wide text-stone-700 transition hover:border-stone-900 hover:text-stone-900 sm:inline-flex"
            >
              Back to showcase
            </Link>
          )}
        </div>
      </header>

      <div className="pt-20">{children}</div>

      <footer className="border-t border-stone-300/60 bg-white/55 px-6 py-4 text-xs tracking-wide text-stone-600 backdrop-blur-sm sm:px-10">
        <div className="mx-auto flex max-w-[1400px] flex-wrap items-center justify-between gap-2">
          <p>
            Crafted to present listings with confidence, depth, and editorial
            precision.
          </p>
          <p className="font-semibold text-stone-700">YGEN Showcase</p>
        </div>
      </footer>
    </div>
  );
}
