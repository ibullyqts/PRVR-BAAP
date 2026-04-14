import asyncio
import os
import re
import random
from playwright.async_api import async_playwright

# --- ⚙️ NITRO-BURST SETTINGS ---
WORKERS = 3            # 3 Browsers per machine
BATCH_SIZE = 4         # Fires 4 messages in one rapid burst
PULSE_DELAY = 120      # 120ms between bursts (Effective speed: 30ms/msg)
RESTART_CYCLE = 240    

async def hyper_worker(context, thread_id, target_name, worker_id):
    page = await context.new_page()
    
    try:
        print(f"🚀 [Worker {worker_id}] Syncing Nitro-Burst Engine...")
        # Use 'commit' to get into the chat faster
        await page.goto(f"https://www.instagram.com/direct/t/{thread_id}/", wait_until="commit")
        
        # ⚡ THE NITRO-BURST INJECTOR
        await page.evaluate("""
            async ({name, delay, batchSize}) => {
                const box = document.querySelector('div[role="textbox"], textarea[placeholder*="Message"]');
                if (!box) return;

                const emojis = ["⭕", "☣️", "🛑", "🌀", "🚨", "💠", "💮"];
                
                setInterval(() => {
                    for (let i = 0; i < batchSize; i++) {
                        const emo = emojis[Math.floor(Math.random() * emojis.length)];
                        const line = `【 ${name} 】 𝚂ᴀ𝚈 【﻿ＰＲＶＲ】 𝐃ᴀ𝐃𝐃𝐘 ${emo} ____________________/\\n`;
                        // Optimized line count for speed & visibility
                        const text = line.repeat(15) + "\\n⚡ ID: " + Math.random().toString(36).substring(5);

                        // 1. Instant Direct Injection
                        box.focus();
                        document.execCommand('insertText', false, text);
                        
                        // 2. Trigger Internal React State
                        box.dispatchEvent(new Event('input', { bubbles: true }));

                        // 3. Native Enter Dispatch
                        const enter = new KeyboardEvent('keydown', {
                            bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13
                        });
                        box.dispatchEvent(enter);

                        // 4. Force DOM Cleanup
                        box.innerHTML = "";
                    }
                }, delay);
            }
        """, {"name": target_name, "delay": PULSE_DELAY, "batchSize": BATCH_SIZE})

        print(f"🔥 [Worker {worker_id}] NITRO BURST ACTIVE: {BATCH_SIZE}x Pulse.")
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
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
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
