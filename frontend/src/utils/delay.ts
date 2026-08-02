/** Promise-based sleep, used to pace the mock research pipeline simulation. */
export function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
