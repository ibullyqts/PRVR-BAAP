import os
import time
import random
import instagrapi.extractors
from instagrapi import Client
from concurrent.futures import ThreadPoolExecutor

# =======================================================
# 🛠️ 2026 TRIPLE-PATCH (Fixes Login Errors)
# =======================================================
def patched_extract_broadcast_channel(data): return []
original_extract_user_gql = instagrapi.extractors.extract_user_gql
def patched_extract_user_gql(data):
    if isinstance(data, dict):
        data['pinned_channels_info'] = data.get('pinned_channels_info', {})
        data['broadcast_channel'] = []
    return original_extract_user_gql(data)
instagrapi.extractors.extract_broadcast_channel = patched_extract_broadcast_channel
instagrapi.extractors.extract_user_gql = patched_extract_user_gql
# =======================================================

SESSION_ID = os.environ.get("INSTA_COOKIE")
THREAD_ID = os.environ.get("TARGET_THREAD_ID")
TARGET_NAME = os.environ.get("TARGET_NAME", "TARGET")

AGENTS = 8          # 8 Agents per machine (48 Total across 6 machines)
BLOCKS = 8          # Visual wall size
DELAY = 0.05        # 50ms pulse

def rapid_agent(cl, thread_id, target_name, agent_id):
    emojis = ["💠", "💮", "🌀", "🚨", "⭕", "☣️"]
    while True:
        try:
            emo = random.choice(emojis)
            line = f"【﻿ {target_name} 】 𝚂ᴀ𝚈 【﻿ＰＲＶＲ】 𝐃ᴀᴅᴅ𝐘 {emo}\n"
            message = (line * BLOCKS) + f"⚡ ID: {random.randint(1000, 9999)}"
            cl.direct_send(message, thread_ids=[str(thread_id)])
            print(f"💥 [Agent {agent_id}] Wall Injected.")
            time.sleep(DELAY)
        except Exception as e:
            if "429" in str(e):
                time.sleep(20) # Rate limit cooling
            else:
                time.sleep(5)

def main():
    if not SESSION_ID or not THREAD_ID:
        print("❌ CONFIG MISSING")
        return

    cl = Client()
    # 2026 Device Signature
    cl.set_user_agent("Instagram 410.0.0.0.96 Android (33/13; 1080x2400; Xiaomi; M2007J20CG)")

    try:
        print("📡 Syncing API (Patches Active)...")
        cl.login_by_sessionid(SESSION_ID)
        print(f"🔓 Authenticated. Machine locking to thread {THREAD_ID}")

        # Deploy agents into background threads
        executor = ThreadPoolExecutor(max_workers=AGENTS)
        for i in range(AGENTS):
            executor.submit(rapid_agent, cl, THREAD_ID, TARGET_NAME, i+1)
        
        # --- INFINITY LOCK ---
        # Keeps the GitHub Action machine alive indefinitely
        while True:
            time.sleep(60)

    except Exception as e:
        print(f"❌ Critical Failure: {e}")

if __name__ == "__main__":
    main()
