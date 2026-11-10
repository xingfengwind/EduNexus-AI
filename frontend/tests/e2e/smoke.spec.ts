import { test, expect } from "@playwright/test";
test("P00-04 Web entry is readable on desktop and phone", async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "EduNexus AI" }),
  ).toBeVisible();
  await page.setViewportSize({ width: 375, height: 812 });
  await expect(page.getByRole("heading")).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});
