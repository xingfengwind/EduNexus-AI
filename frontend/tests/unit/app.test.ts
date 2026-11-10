import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import App from "../../src/app/App.vue";
describe("P00-04 Web entry", () => {
  it("identifies the platform and does not offer nonfunctional business actions", () => {
    const page = mount(App);
    expect(page.get("h1").text()).toBe("EduNexus AI");
    expect(page.text()).toContain("教学资料智能处理与知识服务平台");
    expect(page.findAll("button")).toHaveLength(0);
  });
});
