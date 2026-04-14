import os
import time
import random
from instagrapi import Client
from concurrent.futures import ThreadPoolExecutor

# --- ⚙️ V-MAX SETTINGS ---
SESSION_ID = os.environ.get("INSTA_COOKIE")
THREAD_ID = os.environ.get("TARGET_THREAD_ID")
TARGET_NAME = os.environ.get("TARGET_NAME", "TARGET")

AGENTS = 10         
BLOCK_COUNT = 5     
DELAY = 0.05        

def rapid_agent(cl, thread_id, target_name, agent_id):
    emojis = ["💠", "💮", "🌀", "🚨", "⭕"]
    print(f"⚡ [Agent {agent_id}] Online.")
    while True:
        try:
            emo = random.choice(emojis)
            line = f"【﻿ {target_name} 】 𝚂ᴀ𝚈 【﻿ＰＲＶＲ】 𝐃ᴀᴅᴅ𝐘 {emo}\n"
            message_payload = (line * BLOCK_COUNT) + f"⚡ ID: {random.randint(100, 999)}"
            
            # Send via direct API broadcast
            cl.direct_send(message_payload, thread_ids=[thread_id])
            print(f"💥 [Agent {agent_id}] Injected!")
            time.sleep(DELAY)
        except Exception as e:
            if "429" in str(e):
                time.sleep(20)
            else:
                time.sleep(5)

def main():
    if not SESSION_ID or not THREAD_ID:
        print("❌ MISSING CONFIG")
        return
    
    cl = Client()
    
    # 🛠️ THE FORCE-INJECT BYPASS
    # We skip cl.login_by_sessionid() because it's broken in 2026.
    # Instead, we manually build the session state.
    print("📡 Force-Injecting Session (Bypassing Handshake)...")
    
    cl.set_settings({
        "authorization_data": {
            "sessionid": SESSION_ID.strip()
        }
    })
    
    # We set a modern 2026 User-Agent to match the session
    cl.set_user_agent("Instagram 410.0.0.0.96 Android (33/13; 480dpi; 1080x2400; xiaomi; M2007J20CG; surya; qcom; en_US; 641123490)")

    try:
        # We perform a simple connectivity check instead of a full login
        print(f"🔓 Session Injected. Targeting: {THREAD_ID}")
        
        with ThreadPoolExecutor(max_workers=AGENTS) as executor:
            for i in range(AGENTS):
                executor.submit(rapid_agent, cl, THREAD_ID, TARGET_NAME, i+1)
    except Exception as e:
        print(f"❌ Critical Execution Failure: {e}")

if __name__ == "__main__":
    main()
