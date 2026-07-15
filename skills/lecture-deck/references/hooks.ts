"use client";

import { useState, useEffect, useCallback, type RefObject } from "react";
import { cn } from "@/lib/utils";

export function useRevealAnimation() {
  const [revealedSections, setRevealedSections] = useState<Set<number>>(new Set());
  const [activeSection, setActiveSection] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setRevealedSections(new Set([0]));
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    setRevealedSections((prev) => {
      if (prev.has(activeSection)) return prev;
      const next = new Set(prev);
      next.add(activeSection);
      return next;
    });
  }, [activeSection]);

  const anim = useCallback(
    (idx: number) =>
      cn(
        "transition-all duration-700 ease-out",
        revealedSections.has(idx) ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6",
      ),
    [revealedSections],
  );

  return { activeSection, setActiveSection, anim };
}

export function useSectionObserver(
  containerRef: RefObject<HTMLDivElement | null>,
  sectionRefs: RefObject<(HTMLElement | null)[]>,
  setActiveSection: (idx: number) => void,
) {
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const idx = sectionRefs.current?.findIndex((s) => s === entry.target) ?? -1;
            if (idx !== -1) setActiveSection(idx);
          }
        }
      },
      { root: container, threshold: 0.1 },
    );

    sectionRefs.current?.forEach((s) => {
      if (s) observer.observe(s);
    });

    return () => observer.disconnect();
  }, [containerRef, sectionRefs, setActiveSection]);
}

export function useKeyboardNav(
  activeSection: number,
  sectionCount: number,
  sectionRefs: RefObject<(HTMLElement | null)[]>,
) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      let next = activeSection;
      if (e.key === "ArrowDown" || e.key === " ") {
        e.preventDefault();
        next = Math.min(activeSection + 1, sectionCount - 1);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        next = Math.max(activeSection - 1, 0);
      }
      if (next !== activeSection) {
        sectionRefs.current?.[next]?.scrollIntoView({ behavior: "smooth" });
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [activeSection, sectionCount, sectionRefs]);
}
