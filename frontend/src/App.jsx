import { useCallback, useEffect, useMemo, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { Shell } from "./components/Shell";
import { ErrorView, LoadingView } from "./components/StatusView";
import { filterByActiveIndustry } from "./config/siteMode";
import { fetchContents } from "./lib/api";
import { ContentDetailPage } from "./pages/ContentDetailPage";
import { ContentListPage } from "./pages/ContentListPage";

function normalizeContents(raw) {
  if (!Array.isArray(raw)) return [];
  return raw
    .map((item) => ({
      ...item,
      images: Array.isArray(item.images) ? item.images : [],
      blocks: Array.isArray(item.blocks) ? item.blocks : [],
      metadata: item.metadata || {},
      real_estate_details: item.real_estate_details || null,
      product_details: item.product_details || null,
    }))
    .sort((a, b) => {
      const left = a.updated_at || "";
      const right = b.updated_at || "";
      return left < right ? 1 : -1;
    });
}

function App() {
  const [contents, setContents] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const contentsResponse = await fetchContents();
      setContents(normalizeContents(contentsResponse));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const contentData = useMemo(
    () => filterByActiveIndustry(contents),
    [contents],
  );

  return (
    <BrowserRouter>
      <Shell>
        {loading ? <LoadingView message="Preparing showcase..." /> : null}
        {!loading && error ? (
          <ErrorView message={error} onRetry={load} />
        ) : null}
        {!loading && !error ? (
          <Routes>
            <Route
              path="/"
              element={<ContentListPage contents={contentData} />}
            />
            <Route
              path="/listing/:slug"
              element={<ContentDetailPage contents={contentData} />}
            />
          </Routes>
        ) : null}
      </Shell>
    </BrowserRouter>
  );
}

export default App;
