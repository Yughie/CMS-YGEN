import { useMemo, useState } from "react";

import { chatAboutListing } from "../lib/api";

function clipText(value, maxLength = 300) {
  const text = String(value || "").trim();
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
}

function normalizeContentForPrompt(content) {
  if (!content || typeof content !== "object") return {};

  return {
    id: content.id,
    slug: content.slug,
    title: content.title,
    industry: content.industry,
    status: content.status,
    description: clipText(content.description || "", 500),
    metadata: content.metadata || {},
    real_estate_details: content.real_estate_details || null,
    product_details: content.product_details || null,
    blocks: Array.isArray(content.blocks)
      ? content.blocks.slice(0, 8).map((block) => ({
          block_type: block.block_type,
          title: clipText(block.title, 140),
          body: clipText(block.body, 260),
          position: block.position,
        }))
      : [],
    images: Array.isArray(content.images)
      ? content.images.slice(0, 12).map((image) => ({
          alt_text: image.alt_text,
          caption: clipText(image.caption, 180),
          is_primary: image.is_primary,
          sort_order: image.sort_order,
        }))
      : [],
  };
}

export function ListingAssistantChat({ content }) {
  const [isOpen, setIsOpen] = useState(true);
  const [inputValue, setInputValue] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [messages, setMessages] = useState(() => [
    {
      role: "assistant",
      content:
        "Ask me anything about this listing. I answer using the listing data shown on this page.",
    },
  ]);

  const listingContext = useMemo(
    () => normalizeContentForPrompt(content),
    [content],
  );

  const canSubmit = inputValue.trim().length > 0 && !submitting;

  async function handleSubmit(event) {
    event.preventDefault();
    if (!canSubmit) return;

    const question = inputValue.trim();
    const nextMessages = [...messages, { role: "user", content: question }];
    setMessages(nextMessages);
    setInputValue("");
    setSubmitting(true);
    setError("");

    try {
      const response = await chatAboutListing({
        message: question,
        listingContext,
        history: nextMessages,
      });

      const reply =
        typeof response?.reply === "string" && response.reply.trim()
          ? response.reply.trim()
          : "I could not produce a response right now.";

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: reply,
        },
      ]);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Something went wrong while calling the assistant.";
      setError(message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <aside className="listing-assistant fixed bottom-4 left-4 z-50 w-[min(90vw,360px)] sm:bottom-6 sm:left-6">
      <div className="overflow-hidden border border-stone-300/80 bg-white/95 shadow-2xl backdrop-blur-md">
        <button
          type="button"
          className="flex w-full items-center justify-between border-b border-stone-300/80 bg-[linear-gradient(135deg,#17120d,#3a2617)] px-4 py-3 text-left text-stone-100"
          onClick={() => setIsOpen((previous) => !previous)}
          aria-expanded={isOpen}
          aria-controls="listing-assistant-panel"
        >
          <span>
            <span className="block text-[11px] tracking-[0.2em] text-amber-200 uppercase">
              Listing AI
            </span>
            <span className="font-display text-lg leading-tight">
              Concierge Chat
            </span>
          </span>
          <span className="text-xs font-semibold tracking-wide">
            {isOpen ? "Minimize" : "Open"}
          </span>
        </button>

        {isOpen ? (
          <div id="listing-assistant-panel" className="flex h-[460px] flex-col">
            <div className="listing-assistant-scroll flex-1 space-y-3 overflow-y-auto bg-[linear-gradient(180deg,#f9f6ef,#f2ede4)] p-3">
              {messages.map((message, index) => (
                <article
                  key={`${message.role}-${index}`}
                  className={`max-w-[92%] rounded-sm px-3 py-2 text-sm leading-6 shadow-sm ${
                    message.role === "user"
                      ? "ml-auto border border-stone-700/10 bg-white text-stone-900"
                      : "mr-auto border border-amber-900/15 bg-amber-50 text-stone-800"
                  }`}
                >
                  <p className="mb-1 text-[10px] tracking-[0.16em] text-stone-500 uppercase">
                    {message.role === "user" ? "You" : "Assistant"}
                  </p>
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </article>
              ))}
              {submitting ? (
                <p className="text-xs tracking-wide text-stone-600">
                  Thinking...
                </p>
              ) : null}
            </div>

            <form
              className="border-t border-stone-300/80 bg-white p-3"
              onSubmit={handleSubmit}
            >
              <label htmlFor="listing-ai-input" className="sr-only">
                Ask about this listing
              </label>
              <textarea
                id="listing-ai-input"
                rows={2}
                value={inputValue}
                onChange={(event) => setInputValue(event.target.value)}
                placeholder="Ask about price, amenities, metadata, blocks, and images..."
                className="w-full resize-none border border-stone-300 px-3 py-2 text-sm text-stone-900 outline-none transition focus:border-stone-900"
              />
              {error ? (
                <p className="mt-2 text-xs font-medium text-red-700">{error}</p>
              ) : null}
              <div className="mt-2 flex justify-end">
                <button
                  type="submit"
                  disabled={!canSubmit}
                  className="border border-stone-900 bg-stone-900 px-3 py-1.5 text-xs font-semibold tracking-[0.12em] text-white uppercase transition disabled:cursor-not-allowed disabled:opacity-45"
                >
                  {submitting ? "Sending" : "Send"}
                </button>
              </div>
            </form>
          </div>
        ) : null}
      </div>
    </aside>
  );
}
