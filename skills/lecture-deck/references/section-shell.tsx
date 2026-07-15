"use client";

import { forwardRef } from "react";
import { cn } from "@/lib/utils";

interface ShellProps extends React.HTMLAttributes<HTMLElement> {
  index: number;
  children: React.ReactNode;
  className?: string;
}

const SectionShell = forwardRef<HTMLElement, ShellProps>(({ index, children, className, ...rest }, ref) => {
  return (
    <section
      ref={ref}
      className={cn(
        "min-h-[50vh] sm:min-h-screen snap-start flex items-center justify-center px-4 sm:px-12 py-12 sm:py-0",
        index % 2 !== 0 && "bg-muted/20",
        className,
      )}
      {...rest}
    >
      <div className="mx-auto w-full max-w-6xl py-16">{children}</div>
    </section>
  );
});

SectionShell.displayName = "SectionShell";
export default SectionShell;
