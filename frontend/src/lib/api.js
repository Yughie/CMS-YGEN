const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

async function request(pathname, options = {}) {
  const { method = "GET", body } = options;
  const hasBody = body !== undefined;

  const response = await fetch(`${API_BASE_URL}${pathname}`, {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: hasBody ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let detail = "";
    try {
      const errorPayload = await response.json();
      if (errorPayload?.detail) {
        detail = ` - ${errorPayload.detail}`;
      }
    } catch {
      // Ignore JSON parsing failures and keep a generic status message.
    }
    throw new Error(`API request failed: ${response.status}${detail}`);
  }

  return response.json();
}

export function fetchContents() {
  return request("/contents/");
}

export function chatAboutListing({ message, listingContext, history }) {
  return request("/ai-chat/", {
    method: "POST",
    body: {
      message,
      listing_context: listingContext,
      history,
    },
  });
}

export { API_BASE_URL };
