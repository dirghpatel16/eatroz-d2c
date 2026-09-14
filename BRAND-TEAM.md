# Eatroz Brand Team — Roster

Defined 15 Sep 2026, in response to "act as my design team, branding team, visuals team." Four roles exist as real, invocable Skills (`.claude/skills/eatroz-*`); others are named as deliberate gaps, not forgotten.

## Active roles (invoke by name or by task type — Claude routes automatically when the request matches)

| Role | Skill | Owns |
|---|---|---|
| Brand Strategist | `eatroz-brand-strategist` | Positioning, audience, competitive framing, whether a new idea fits the locked strategy |
| Visual Identity | *(DESIGN.md is the artifact; no separate skill needed — it's the reference, not a task-runner)* | Palette, type, motif system, spacing/layout tokens |
| Copywriter | `eatroz-copywriter` | Pack copy, website copy, ad copy, social captions — in the locked voice |
| Packaging Production Spec | `eatroz-packaging-spec` | Turns DESIGN.md into what Softpills actually needs to print |
| Brand Guardian | `eatroz-brand-guardian` | Reviews any new asset against DESIGN.md, flags drift, tracks the open Troz trademark risk |

Website building itself uses the general-purpose `/design-html` (gstack) skill against `DESIGN.md` — not a separate Eatroz-specific skill, since that tool is already generic and correctly system-driven.

## Deliberately not built yet (real gaps, premature to staff before the base brand/website exist)

- **Social content** — Instagram/social templates. Needs the base visual system to exist in working form first (it does now, via DESIGN.md) but no live channel yet to design for.
- **Motion/video** — ad creative, launch video. Same reasoning — premature before Phase 0/1 GTM (per the pitch deck) actually starts.
- **Performance-marketing creative** — the ad-angle/landing-page-congruence work (see `video-research/ag1_funnel_breakdown.md` for why this matters). Depends on GTM phase timing, not brand-readiness.

Revisit this list once the website ships and GTM Phase 1 (per the deck's roadmap) is actually underway — don't build these skills speculatively ahead of need.

## How these interact

`eatroz-brand-strategist` is the frame everyone else checks against. `eatroz-copywriter` and `eatroz-packaging-spec` produce things. `eatroz-brand-guardian` checks anything before it ships. None of them override the user's final call — per this project's established practice throughout, they flag and recommend, never block.
