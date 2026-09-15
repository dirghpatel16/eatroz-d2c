import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { HeroFilm } from "@/components/hero/hero-film";

describe("HeroFilm", () => {
  it("exposes the first-drop action and motion control", () => {
    render(<HeroFilm mode="prelaunch" onAction={vi.fn()} />);
    expect(screen.getByRole("heading", { name: /your evening ritual/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /pause motion/i })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /pause motion/i }));
    expect(screen.getByRole("button", { name: /play motion/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /join the first drop/i })).toBeInTheDocument();
  });
});
