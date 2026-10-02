import { fireEvent, render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import Page from "../app/page";

describe("single-product PDP", () => {
  it("puts product imagery and a clear action ahead of storytelling", () => {
    render(<Page />);
    expect(screen.getByRole("region", { name: /product images/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /magnesium gummies/i, level: 1 })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /1 pouch/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /2 pouches/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /3 pouches/i })).toBeInTheDocument();
    expect(screen.getAllByRole("button", { name: /get first access/i }).length).toBeGreaterThan(0);
    expect(screen.queryByText(/₹\s*\d/)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /add to cart/i })).not.toBeInTheDocument();
  });

  it("changes the visible image when a gallery thumbnail is selected", () => {
    render(<Page />);
    fireEvent.click(screen.getByRole("button", { name: /view gummy detail/i }));
    expect(screen.getByTestId("active-product-image").getAttribute("src")).toContain("eatroz-gummy-beads-v3.png");
  });

  it("makes preview pack selection explicit without inventing a sale", () => {
    render(<Page />);
    fireEvent.click(screen.getByRole("button", { name: /2 pouches/i }));
    expect(screen.getByRole("button", { name: /2 pouches/i })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByText(/your preview selection: 2 pouches/i)).toBeInTheDocument();
  });

  it("explains that live registration is not connected", () => {
    render(<Page />);
    fireEvent.click(screen.getAllByRole("button", { name: /get first access/i })[0]);
    const dialog = screen.getByRole("dialog", { name: /first access/i });
    expect(dialog).toBeInTheDocument();
    expect(within(dialog).getByText(/registration is not connected yet/i)).toBeInTheDocument();
    fireEvent.click(within(dialog).getByRole("button", { name: /save interest on this device/i }));
    expect(within(dialog).getByText(/saved on this device only/i)).toBeInTheDocument();
  });
});
