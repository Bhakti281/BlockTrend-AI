import { QueryClient } from "@tanstack/react-query";
import { createRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";

export const getRouter = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        // Keep data fresh for 10s — avoids redundant refetches on navigation
        staleTime: 10_000,
        // Cache data for 5 minutes even when unused
        gcTime: 5 * 60_000,
        // Don't refetch on window focus for better perceived performance
        refetchOnWindowFocus: false,
        // Retry once with exponential backoff
        retry: 1,
        retryDelay: (attempt) => Math.min(1000 * 2 ** attempt, 5000),
      },
    },
  });

  const router = createRouter({
    routeTree,
    context: { queryClient },
    scrollRestoration: true,
    // Preload routes on hover/intent — reduces navigation latency
    defaultPreloadStaleTime: 30_000,
    defaultPreload: "intent",
  });

  return router;
};
