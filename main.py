import asyncio
import os
import re
import random
from playwright.async_api import async_playwright

# --- ⚙️ OVERLORD SETTINGS ---
WORKERS = 3            # 3 Browsers
BATCH_SIZE = 5         # Fires 5 messages in 1 millisecond burst
PULSE_DELAY = 150      # Delay between bursts (Total speed = ~30ms per msg)
RESTART_CYCLE = 180    

async def hyper_worker(context, thread_id, target_name, worker_id):
    page = await context.new_page()
    
    try:
        print(f"🚀 [Worker {worker_id}] Syncing Overlord Engine...")
        # Use 'commit' to get in even faster
        await page.goto(f"https://www.instagram.com/direct/t/{thread_id}/", wait_until="commit")
        
        # ⚡ THE BATCH INJECTION ENGINE
        await page.evaluate("""
            async ({name, delay, batchSize}) => {
                const box = document.querySelector('div[role="textbox"], textarea[placeholder*="Message"]');
                if (!box) return;

                const emojis = ["⭕", "☣️", "🛑", "🌀", "🚨", "💠"];
                
                setInterval(async () => {
                    for (let i = 0; i < batchSize; i++) {
                        const emo = emojis[Math.floor(Math.random() * emojis.length)];
                        const line = `【 ${name} 】 𝚂ᴀ𝚈 【﻿ＰＲＶＲ】 𝐃ᴀ𝐃𝐃𝐘 ${emo} ____________________/\\n`;
                        const payload = line.repeat(20) + "\\n⚡ ID: " + Math.random().toString(36).substring(5);

                        // Hyper-fast injection
                        box.focus();
                        document.execCommand('insertText', false, payload);
                        box.dispatchEvent(new Event('input', { bubbles: true }));

                        const enter = new KeyboardEvent('keydown', {
                            bubbles: true, key: 'Enter', code: 'Enter', keyCode: 13
                        });
                        box.dispatchEvent(enter);
                        
                        // Instant DOM Wipe
                        box.innerHTML = "";
                    }
                }, delay);
            }
        """, {"name": target_name, "delay": PULSE_DELAY, "batchSize": BATCH_SIZE})

        print(f"🔥 [Worker {worker_id}] BATCH MODE ACTIVE. Firing {BATCH_SIZE}x per pulse.")
        await asyncio.sleep(RESTART_CYCLE)

    except Exception as e:
        print(f"⚠️ [Worker {worker_id}] Error: {e}")
    finally:
        await page.close()

async def main():
    cookie_raw = os.environ.get("INSTA_COOKIE")
    thread_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "EZRA")

    if not cookie_raw or not thread_id:
        return

    sid = re.search(r'sessionid=([^;]+)', cookie_raw)
    sid_value = sid.group(1) if sid else cookie_raw

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 800, 'height': 600}
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
