import type { ReactNode } from "react";
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";
import { Bell, Search } from "lucide-react";
import { Input } from "@/components/ui/input";

export function PageShell({
  title,
  subtitle,
  actions,
  children,
}: {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  children: ReactNode;
}) {
  return (
    <SidebarInset>
      <header className="sticky top-0 z-20 flex h-14 items-center gap-3 border-b border-border/60 bg-background/60 px-4 backdrop-blur-xl">
        <SidebarTrigger />
        <Separator orientation="vertical" className="h-5" />
        <div className="flex flex-1 items-center gap-3">
          <div className="hidden md:flex items-center gap-2 rounded-lg border border-border/60 bg-secondary/40 px-3 py-1.5 text-sm text-muted-foreground w-72">
            <Search className="h-3.5 w-3.5" />
            <Input
              placeholder="Search coins, indicators, signals…"
              className="h-6 border-0 bg-transparent p-0 text-xs shadow-none focus-visible:ring-0"
            />
          </div>
        </div>
        <button className="rounded-md p-2 text-muted-foreground hover:bg-secondary hover:text-foreground">
          <Bell className="h-4 w-4" />
        </button>
      </header>

      <div className="p-4 md:p-8">
        <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="font-display text-2xl md:text-3xl font-bold tracking-tight">{title}</h1>
            {subtitle && (
              <p className="mt-1 text-sm text-muted-foreground max-w-2xl">{subtitle}</p>
            )}
          </div>
          {actions && <div className="flex flex-wrap items-center gap-2">{actions}</div>}
        </div>
        {children}
      </div>
    </SidebarInset>
  );
}
