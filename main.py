import os
import time
import random
import instagrapi.extractors
from instagrapi import Client
from concurrent.futures import ThreadPoolExecutor

# =======================================================
# 🛠️ CRITICAL FIX: PINNED CHANNELS MONKEY PATCH
# This prevents the 'pinned_channels_info' error you saw.
# =======================================================
original_extract_user_short = instagrapi.extractors.extract_user_short

def patched_extract_user_short(data):
    if isinstance(data, dict):
        # Inject the missing key if it's not there
        data['pinned_channels_info'] = data.get('pinned_channels_info', {})
    return original_extract_user_short(data)

# Apply the patch to the library at runtime
instagrapi.extractors.extract_user_short = patched_extract_user_short
# =======================================================

# --- ⚙️ V-MAX SETTINGS ---
SESSION_ID = os.environ.get("INSTA_COOKIE")
THREAD_ID = os.environ.get("TARGET_THREAD_ID")
TARGET_NAME = os.environ.get("TARGET_NAME", "TARGET")

AGENTS = 10         # 10 simultaneous shooters per machine
BLOCK_COUNT = 5     # 5 blocks = faster delivery than 15
DELAY = 0.05        # 50ms rapid pulse

def rapid_agent(cl, thread_id, target_name, agent_id):
    """High-speed agent with low-latency payload"""
    emojis = ["💠", "💮", "🌀", "🚨", "⭕", "☣️", "🛑"]
    print(f"⚡ [Agent {agent_id}] Online & Synchronized.")
    
    while True:
        try:
            emo = random.choice(emojis)
            
            # --- THE RAPID-BLOCK CONSTRUCTION ---
            line = f"【﻿ {target_name} 】 𝚂ᴀ𝚈 【﻿ＰＲＶＲ】 𝐃ᴀᴅᴅ𝐘 {emo}\n"
            message_payload = (line * BLOCK_COUNT) 
            message_payload += f"⚡ ID: {random.randint(100, 999)}"

            # Direct API Broadcast
            cl.direct_send(message_payload, thread_ids=[thread_id])
            print(f"💥 [Agent {agent_id}] Injected!")
            
            if DELAY > 0:
                time.sleep(DELAY)
                
        except Exception as e:
            # Handle common 2026 Rate Limits
            if "429" in str(e):
                print(f"⚠️ [Agent {agent_id}] Rate Limit (429). Cooling down 15s...")
                time.sleep(15)
            elif "Challenge" in str(e):
                print(f"❌ [Agent {agent_id}] Account Flagged/Checkpoint. Stopping.")
                break
            else:
                print(f"⚠️ [Agent {agent_id}] Error: {e}")
                time.sleep(5)

def main():
    if not SESSION_ID or not THREAD_ID:
        print("❌ ERROR: Missing SESSION_ID or THREAD_ID in environment!")
        return

    cl = Client()
    
    # Randomize User-Agent to look like a modern Android device
    cl.set_user_agent("Instagram 393.1.0.50.76 Android (29/10; 480dpi; 1080x2175; samsung; SM-G960F; starlte; samsungexynos9810; it_IT; 776586932)")

    try:
        print("📡 Establishing Handshake with Instagram API...")
        cl.login_by_sessionid(SESSION_ID)
        print(f"🔓 Authenticated. Targeting Thread: {THREAD_ID}")
        
        print(f"🔥 DEPLOYING {AGENTS} AGENTS...")
        with ThreadPoolExecutor(max_workers=AGENTS) as executor:
            for i in range(AGENTS):
                executor.submit(rapid_agent, cl, THREAD_ID, TARGET_NAME, i+1)
                
    except Exception as e:
        print(f"❌ Login Failed: {e}")

if __name__ == "__main__":
    main()
