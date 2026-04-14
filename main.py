import asyncio
import os
import re
import random
from playwright.async_api import async_playwright

# --- ⚙️ NITRO CONFIG ---
WORKERS = 5            
PULSE_DELAY = 120      # Slightly increased to 120ms to prevent instant silent-block
RESTART_CYCLE = 240    

async def hyper_worker(context, thread_id, target_name, worker_id):
    page = await context.new_page()
    
    try:
        print(f"🚀 [Worker {worker_id}] Syncing with Instagram...")
        # We use 'networkidle' to ensure all security tokens are loaded
        await page.goto(f"https://www.instagram.com/direct/t/{thread_id}/", wait_until="networkidle")
        
        # ⚡ THE JS INJECTION (Updated CSRF Logic)
        await page.evaluate("""
            async ({threadId, delay, name}) => {
                setInterval(async () => {
                    // Grab CSRF from IG's internal object - the most reliable way
                    const csrf = window._sharedData?.config?.csrf_token || 
                                 document.cookie.match(/csrftoken=([^;]+)/)?.[1];
                    
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

                    fetch(url, {
                        method: 'POST',
                        body: payload,
                        headers: {
                            'X-CSRFToken': csrf,
                            'X-Requested-With': 'XMLHttpRequest',
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-IG-App-ID': '936619743392459',
                            'X-Instagram-AJAX': '1'
                        }
                    }).then(res => {
                        if (res.status === 200) console.log("SUCCESS");
                        else console.log("FAILED: " + res.status);
                    });
                }, delay);
            }
        """, {"threadId": thread_id, "delay": PULSE_DELAY, "name": target_name})
        
        print(f"🔥 [Worker {worker_id}] NITRO ACTIVE - Firing Packets.")
        await asyncio.sleep(RESTART_CYCLE)
        
    except Exception as e:
        print(f"⚠️ [Worker {worker_id}] Stream Error: {e}")

async def main():
    cookie_raw = os.environ.get("INSTA_COOKIE")
    thread_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "EZRA")

    if not cookie_raw or not thread_id:
        print("❌ Secrets Missing!")
        return

    sid = re.search(r'sessionid=([^;]+)', cookie_raw)
    sid_value = sid.group(1) if sid else cookie_raw

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
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
