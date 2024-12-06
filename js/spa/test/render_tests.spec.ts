import { test, expect } from "@self/tootils";

test("Test every= works in render", async ({ page }) => {
	const timebox = page.getByLabel("Time");
	const box_1 = page.getByLabel("Render 1");
	const slider = page.getByLabel("number input for Slider");
	let timebox_value_start = parseFloat(await timebox.inputValue());
	let box_1_value_start = parseFloat(await box_1.inputValue());

	await page.waitForTimeout(500);
	let timebox_value_end = parseFloat(await timebox.inputValue());
	expect(timebox_value_end).toBeGreaterThan(timebox_value_start);

	await page.waitForTimeout(500);
	await slider.fill("4");
	const box_2 = page.getByLabel("Render 2");
	let box_2_value_start = parseFloat(await box_2.inputValue());
	expect(box_2_value_start).toBeGreaterThan(box_1_value_start);

	await page.waitForTimeout(500);
	let box_2_value_end = parseFloat(await box_2.inputValue());
	expect(box_2_value_end).toBeGreaterThan(box_2_value_start);
});

test("Test event/selection data works in render", async ({ page }) => {
	const selected_button = page.getByLabel("Selected Button");
	const slider = page.getByLabel("number input for Slider");
	await slider.fill("3");
	await page.getByRole("button", { name: "Button 2" }).click();

	await expect(selected_button).toHaveValue("Button 2");

	const selected_chat = page.getByLabel("Selected Chat");
	await page.getByText("Hi").click();
	await expect(selected_chat).toHaveValue("[0, 1]");
});