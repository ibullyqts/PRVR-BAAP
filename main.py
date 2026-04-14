import os
import time
import random
import instagrapi.extractors
from instagrapi import Client
from concurrent.futures import ThreadPoolExecutor

# =======================================================
# 🛠️ 2026 EMERGENCY PATCH: Bypasses 'pinned_channels_info'
# =======================================================
original_extract_user_short = instagrapi.extractors.extract_user_short

def patched_extract_user_short(data):
    if isinstance(data, dict):
        # Inject missing 2026 keys to prevent KeyError
        data['pinned_channels_info'] = data.get('pinned_channels_info', {})
        data['broadcast_channel'] = data.get('broadcast_channel', [])
    return original_extract_user_short(data)

# Apply patch to the extractor
instagrapi.extractors.extract_user_short = patched_extract_user_short
# =======================================================

# --- ⚙️ V-MAX SETTINGS ---
SESSION_ID = os.environ.get("INSTA_COOKIE")
THREAD_ID = os.environ.get("TARGET_THREAD_ID")
TARGET_NAME = os.environ.get("TARGET_NAME", "TARGET")

AGENTS = 10         # Parallel shooters
BLOCK_COUNT = 5     # Small payload for max delivery speed
DELAY = 0.05        # 50ms pulse

def rapid_agent(cl, thread_id, target_name, agent_id):
    emojis = ["💠", "💮", "🌀", "🚨", "⭕"]
    print(f"⚡ [Agent {agent_id}] Online.")
    
    while True:
        try:
            emo = random.choice(emojis)
            line = f"【﻿ {target_name} 】 𝚂ᴀ𝚈 【﻿ＰＲＶＲ】 𝐃ᴀᴅᴅ𝐘 {emo}\n"
            message_payload = (line * BLOCK_COUNT) + f"⚡ ID: {random.randint(100, 999)}"

            cl.direct_send(message_payload, thread_ids=[thread_id])
            print(f"💥 [Agent {agent_id}] Injected!")
            time.sleep(DELAY)
            
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ [Agent {agent_id}] Rate Limit. Resting 20s...")
                time.sleep(20)
            else:
                time.sleep(5)

def main():
    if not SESSION_ID or not THREAD_ID:
        print("❌ MISSING CONFIG")
        return

    cl = Client()
    
    # Use a modern Android User-Agent to match the 2026 API signature
    cl.set_user_agent("Instagram 410.0.0.0.96 Android (33/13; 480dpi; 1080x2400; xiaomi; M2007J20CG; surya; qcom; en_US; 641123490)")

    try:
        print("📡 Syncing API Session (Patch Active)...")
        cl.login_by_sessionid(SESSION_ID)
        print(f"🔓 Authenticated. Targeting Thread: {THREAD_ID}")
        
        with ThreadPoolExecutor(max_workers=AGENTS) as executor:
            for i in range(AGENTS):
                executor.submit(rapid_agent, cl, THREAD_ID, TARGET_NAME, i+1)
                
    except Exception as e:
        print(f"❌ Login Failed even with patch: {e}")

if __name__ == "__main__":
    main()
