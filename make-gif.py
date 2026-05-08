#!/usr/bin/env python3
"""Capture じしゃくの もよう gameplay -> GIF via playwright + Pillow."""
import asyncio
import io
import math
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

URL = "http://127.0.0.1:8062/"
OUT = Path("/tmp/pndshch-hub/assets/jishaku-moyo.gif")
W, H = 375, 720
SCALE = 0.55
COLORS = 32

frames: list[Image.Image] = []
durations: list[int] = []


async def capture(page, ms=120):
    png = await page.screenshot(type="png")
    img = Image.open(io.BytesIO(png)).convert("RGB")
    frames.append(img)
    durations.append(ms)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": W, "height": H}, device_scale_factor=2
        )
        page = await ctx.new_page()
        await page.goto(URL, wait_until="networkidle")
        await page.wait_for_timeout(700)
        await page.evaluate("__demo.hideHint()")
        await page.wait_for_timeout(150)

        # 1-magnet mode: orbit the magnet around center
        cx, cy = W / 2, H / 2 + 30
        R = 70
        steps = 12
        for i in range(steps):
            t = (i / steps) * 2 * math.pi
            x = cx + R * math.cos(t)
            y = cy + R * math.sin(t)
            ang = t  # rotate the bar so it points outward
            await page.evaluate(f"__demo.setMagnetPos(0, {x}, {y})")
            await page.evaluate(f"__demo.setMagnetAngle(0, {ang})")
            await page.wait_for_timeout(70)
            await capture(page, 95)

        # Switch to 2-magnet mode
        await page.evaluate("__demo.setMode('two')")
        await page.evaluate("__demo.hideHint()")
        await page.wait_for_timeout(220)

        # 2 magnets attract / approach: move them closer then back
        for k in range(8):
            t = k / 8
            sep = 0.32 + 0.12 * math.sin(t * 2 * math.pi)
            await page.evaluate(f"__demo.setMagnetPos(0, {W * (0.5 - sep)}, {cy})")
            await page.evaluate(f"__demo.setMagnetPos(1, {W * (0.5 + sep)}, {cy})")
            await page.wait_for_timeout(60)
            await capture(page, 95)

        # Flip second magnet -> repulsion pattern
        await page.evaluate("__demo.flip(1)")
        await page.wait_for_timeout(120)
        for k in range(6):
            t = k / 6
            sep = 0.25 + 0.10 * math.sin(t * 2 * math.pi)
            await page.evaluate(f"__demo.setMagnetPos(0, {W * (0.5 - sep)}, {cy})")
            await page.evaluate(f"__demo.setMagnetPos(1, {W * (0.5 + sep)}, {cy})")
            await page.wait_for_timeout(60)
            await capture(page, 95)

        # Switch to horseshoe + trail mode
        await page.evaluate("__demo.setMode('horseshoe')")
        await page.evaluate("__demo.hideHint()")
        await page.evaluate("__demo.setTrail(true)")
        await page.wait_for_timeout(220)

        # Wiggle horseshoe so trails draw
        for k in range(14):
            t = k / 14
            x = W / 2 + 50 * math.cos(t * 2 * math.pi)
            y = cy + 25 * math.sin(t * 2 * math.pi)
            ang = -math.pi / 2 + 0.35 * math.sin(t * 2 * math.pi)
            await page.evaluate(f"__demo.setMagnetPos(0, {x}, {y})")
            await page.evaluate(f"__demo.setMagnetAngle(0, {ang})")
            await page.wait_for_timeout(70)
            await capture(page, 95)

        await browser.close()


asyncio.run(main())

out_w = int(W * SCALE)
out_h = int(H * SCALE)
small = [
    f.resize((out_w, out_h), Image.LANCZOS).convert("P", palette=Image.ADAPTIVE, colors=COLORS)
    for f in frames
]
print(f"frames: {len(small)}  total ms: {sum(durations)}")
OUT.parent.mkdir(parents=True, exist_ok=True)
small[0].save(
    OUT,
    save_all=True,
    append_images=small[1:],
    duration=durations,
    loop=0,
    optimize=True,
    disposal=2,
)
print(f"wrote {OUT}  ({OUT.stat().st_size/1024:.1f} KB)")
