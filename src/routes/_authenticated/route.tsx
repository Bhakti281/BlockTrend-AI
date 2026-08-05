import { createFileRoute, redirect, Outlet } from "@tanstack/react-router";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { supabase } from "@/integrations/supabase/client";
import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { prefetchMarkets } from "@/lib/prefetch";

export const Route = createFileRoute("/_authenticated")({
  ssr: false,
  beforeLoad: async () => {
    const { data, error } = await supabase.auth.getUser();
    if (error || !data.user) throw redirect({ to: "/auth" });
    return { user: data.user };
  },
  component: Layout,
});

function Layout() {
  const queryClient = useQueryClient();

  // Prefetch market data immediately on auth layout mount
  // This warms the cache so dashboard/live-prices/multi-coin load instantly
  useEffect(() => {
    prefetchMarkets(queryClient);
  }, [queryClient]);

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar />
        <Outlet />
      </div>
    </SidebarProvider>
  );
}
