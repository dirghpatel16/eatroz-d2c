import { render } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Lenis from "lenis";
import { SmoothScroll } from "@/components/motion/smooth-scroll";

vi.mock("lenis", () => ({ default: vi.fn(function MockLenis() { return { destroy: vi.fn() }; }) }));

describe("SmoothScroll", () => {
  beforeEach(() => vi.mocked(Lenis).mockClear());
  it("keeps native scrolling for reduced motion", () => {
    window.matchMedia = vi.fn((query: string) => ({ matches: query.includes("reduced-motion"), media: query } as MediaQueryList));
    render(<SmoothScroll><p>Content</p></SmoothScroll>);
    expect(Lenis).not.toHaveBeenCalled();
  });
  it("enhances scrolling only for a fine pointer", () => {
    window.matchMedia = vi.fn((query: string) => ({ matches: query.includes("pointer: fine"), media: query } as MediaQueryList));
    render(<SmoothScroll><p>Content</p></SmoothScroll>);
    expect(Lenis).toHaveBeenCalledOnce();
  });
});
