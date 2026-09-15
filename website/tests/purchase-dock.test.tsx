import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { PurchaseDock } from "@/components/commerce/purchase-dock";

describe("PurchaseDock", () => {
  it("uses lead capture in prelaunch", () => {
    const action = vi.fn();
    render(<PurchaseDock mode="prelaunch" onAction={action} />);
    fireEvent.click(screen.getByRole("button", { name: /join the first drop/i }));
    expect(action).toHaveBeenCalledOnce();
    expect(screen.queryByText(/in stock/i)).not.toBeInTheDocument();
  });
  it("fails live mode back to lead capture while price is pending", () => {
    render(<PurchaseDock mode="live" onAction={vi.fn()} />);
    expect(screen.getByRole("button", { name: /join the first drop/i })).toBeInTheDocument();
  });
});
