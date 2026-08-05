// Prefetch utilities for warming React Query cache on route entry.
// This reduces perceived latency by starting data fetches before components mount.

import type { QueryClient } from "@tanstack/react-query";
import { fetchMarkets, COIN_META } from "./coingecko.functions";

const ids = Object.values(COIN_META).map((c) => c.id);

/**
 * Prefetch market data into the query cache.
 * Called on authenticated layout mount to ensure dashboard/live-prices/multi-coin
 * have data ready immediately.
 */
export function prefetchMarkets(queryClient: QueryClient) {
  queryClient.prefetchQuery({
    queryKey: ["markets", ids.join(",")],
    queryFn: () => fetchMarkets({ data: { ids } }),
    staleTime: 15_000,
  });
}
