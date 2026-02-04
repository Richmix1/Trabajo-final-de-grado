import { describe, expect, it } from "vitest";

import { buildAuthHeaders } from "./api.js";

describe("buildAuthHeaders", () => {
  it("returns empty object when no token", () => {
    expect(buildAuthHeaders()).toEqual({});
  });

  it("returns Authorization header when token is provided", () => {
    expect(buildAuthHeaders("abc123")).toEqual({ Authorization: "Bearer abc123" });
  });
});
