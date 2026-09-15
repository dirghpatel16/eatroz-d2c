import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { Storefront } from "@/components/storefront";

vi.mock("gsap", () => ({ default: { registerPlugin: vi.fn(), context: vi.fn(() => ({ revert: vi.fn() })), fromTo: vi.fn(), to: vi.fn() } }));
vi.mock("gsap/ScrollTrigger", () => ({ ScrollTrigger: {} }));

describe("Storefront", () => {
  it("renders a complete claim-safe prelaunch journey", () => {
    render(<Storefront commerce={{ mode: "prelaunch", checkoutUrl: null }} />);
    expect(screen.getByRole("heading", { name: /your evening ritual/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /four forms/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /closer look/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /before orders open/i })).toBeInTheDocument();
    expect(screen.queryByText(/customer reviews/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/in stock/i)).not.toBeInTheDocument();
  });
});
