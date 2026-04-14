import asyncio
import os
import re
import random
from playwright.async_api import async_playwright

# --- ⚙️ NITRO CONFIG ---
WORKERS = 5            # Total streams per machine
PULSE_DELAY = 100      # 100ms (Hyper-speed pulse)
RESTART_CYCLE = 240    # Reset every 4 mins to clear browser cache/lag

async def hyper_worker(context, thread_id, target_name, worker_id):
    """Bypasses UI and uses the browser's internal Fetch to fire messages"""
    page = await context.new_page()
    
    try:
        # Establish the session handshake
        print(f"🚀 [Worker {worker_id}] Syncing with Instagram...")
        await page.goto(f"https://www.instagram.com/direct/t/{thread_id}/", wait_until="domcontentloaded")
        
        # ⚡ THE JS INJECTION (The actual spamming engine)
        await page.evaluate("""
            async ({text_fn, threadId, delay, name}) => {
                setInterval(async () => {
                    const csrf = document.cookie.match(/csrftoken=([^;]+)/)?.[1];
                    const url = `/api/v1/web/direct_v2/threads/${threadId}/items/send_text/`;
                    
                    const emojis = ["⭕", "☣️", "🛑", "🌀", "🚨", "💠"];
                    const emo = emojis[Math.floor(Math.random() * emojis.length)];
                    const branding = `【 ${name} 】 𝚂ᴀ𝚈 【﻿ＰＲＶＲ】 𝐃ᴀ𝐃𝐃𝐘 ${emo} ____________________/\\n`.repeat(20);
                    const salt = "\\n⚡ ID: " + Math.random().toString(36).substring(7);

                    const payload = new URLSearchParams();
                    payload.append('text', branding + salt);
                    payload.append('client_context', Math.random().toString(36));
                    payload.append('mutation_token', Math.random().toString(36));
                    payload.append('offline_threading_id', Math.random().toString(36));

                    await fetch(url, {
                        method: 'POST',
                        body: payload,
                        headers: {
                            'X-CSRFToken': csrf,
                            'X-Requested-With': 'XMLHttpRequest',
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    });
                }, delay);
            }
        """, {"threadId": thread_id, "delay": PULSE_DELAY, "name": target_name})
        
        print(f"🔥 [Worker {worker_id}] NITRO ACTIVE at {PULSE_DELAY}ms")
        await asyncio.sleep(RESTART_CYCLE)
        
    except Exception as e:
        print(f"⚠️ [Worker {worker_id}] Stream Error: {e}")

async def main():
    cookie_raw = os.environ.get("INSTA_COOKIE")
    thread_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "EZRA")

    if not cookie_raw or not thread_id:
        print("❌ CRITICAL ERROR: Missing Secrets (INSTA_COOKIE or TARGET_THREAD_ID)!")
        return

    # Extract sessionid value
    sid = re.search(r'sessionid=([^;]+)', cookie_raw)
    sid_value = sid.group(1) if sid else cookie_raw

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Emulate iPad to get a faster, lighter DOM
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        
        await context.add_cookies([{
            "name": "sessionid",
            "value": sid_value.strip(),
            "domain": ".instagram.com",
            "path": "/"
        }])

        workers = [hyper_worker(context, thread_id, target_name, i+1) for i in range(WORKERS)]
        await asyncio.gather(*workers)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
