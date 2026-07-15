"use client";
import { forwardRef } from "react";
import SectionShell from "./section-shell"; // 공유 shell 재사용 시 "../deck/section-shell"
import { cn } from "@/lib/utils";

interface P { anim: (i: number) => string; index: number; }

// 슬라이드 데이터 — 3~7개, 2열 그리드로 렌더
const items = [
  { num: "01", title: "핵심 포인트 제목", desc: "한두 문장 설명. 회색 본문으로 근거를 편다." },
  { num: "02", title: "두 번째 포인트", desc: "짧고 단정적으로. 텍스트 벽 금지." },
  { num: "03", title: "세 번째 포인트", desc: "필요하면 full 플래그로 풀폭.", full: true },
];

const S = forwardRef<HTMLElement, P>(({ anim, index }, ref) => (
  <SectionShell ref={ref} index={index}>
    <p className={cn("font-mono text-xs tracking-widest text-muted-foreground uppercase mb-3", anim(index))}>
      Part 1 · Section
    </p>
    <h2 className={cn("text-3xl font-bold tracking-tight sm:text-5xl mb-2", anim(index))}>
      슬라이드 제목 — 결론 먼저
    </h2>
    <p className={cn("text-base text-muted-foreground mb-8", anim(index))} style={{ transitionDelay: "80ms" }}>
      부제 한 줄로 맥락을 준다
    </p>

    <div className={cn("grid grid-cols-1 sm:grid-cols-2 gap-3", anim(index))} style={{ transitionDelay: "150ms" }}>
      {items.map((item) => (
        <div
          key={item.num}
          className={cn(
            "rounded-2xl border border-border/40 bg-card/80 p-4 shadow-sm backdrop-blur-sm flex gap-3 items-start",
            item.full && "sm:col-span-2",
          )}
        >
          <span className="font-mono text-sm text-primary shrink-0 mt-0.5">{item.num}</span>
          <div>
            <p className="text-sm font-semibold mb-1">{item.title}</p>
            <p className="text-sm text-muted-foreground leading-relaxed">{item.desc}</p>
          </div>
        </div>
      ))}
    </div>
  </SectionShell>
));
S.displayName = "SlideTemplate";
export default S;
