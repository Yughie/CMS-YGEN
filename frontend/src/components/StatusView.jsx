export function LoadingView({ message = "Loading content..." }) {
  return (
    <div className="rounded-2xl border border-stone-300/80 bg-white/90 p-8 text-center shadow-[0_20px_40px_-24px_rgba(49,35,15,0.4)]">
      <div
        className="mx-auto mb-4 h-9 w-9 animate-spin rounded-full border-2 border-amber-800/20 border-t-amber-800"
        aria-hidden="true"
      />
      <p className="font-medium text-stone-700">{message}</p>
    </div>
  );
}

export function ErrorView({ message, onRetry }) {
  return (
    <div className="rounded-2xl border border-rose-300 bg-rose-50/90 p-8 text-center shadow-[0_20px_40px_-24px_rgba(127,29,29,0.2)]">
      <h2 className="font-display text-2xl tracking-tight text-rose-900">
        Something went wrong
      </h2>
      <p className="mt-2 text-rose-700">{message}</p>
      {onRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className="mt-5 inline-flex items-center rounded-full bg-rose-900 px-4 py-2 text-sm font-semibold text-rose-50 transition hover:bg-rose-800"
        >
          Try again
        </button>
      ) : null}
    </div>
  );
}

export function EmptyView({ title, message }) {
  return (
    <div className="rounded-2xl border border-stone-300/80 bg-white/85 p-8 text-center">
      <h2 className="font-display text-2xl tracking-tight text-stone-900">
        {title}
      </h2>
      <p className="mt-2 text-stone-600">{message}</p>
    </div>
  );
}
