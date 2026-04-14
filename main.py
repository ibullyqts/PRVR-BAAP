import os
import time
import random
from instagrapi import Client
from concurrent.futures import ThreadPoolExecutor

# --- ⚙️ V-MAX SETTINGS ---
SESSION_ID = os.environ.get("INSTA_COOKIE")
THREAD_ID = os.environ.get("TARGET_THREAD_ID")
TARGET_NAME = os.environ.get("TARGET_NAME", "EZRA")

# THE NEW STRATEGY: More agents, smaller payloads
AGENTS = 10         # 10 simultaneous shooters
BLOCK_COUNT = 5     # Reduced from 15 to 5 for instant delivery
DELAY = 0.05        # 50ms delay (Near-zero)

def rapid_agent(cl, thread_id, target_name, agent_id):
    """High-speed agent with low-latency payload"""
    emojis = ["💠", "💮", "🌀", "🚨", "⭕"]
    print(f"⚡ [Agent {agent_id}] Online.")
    
    while True:
        try:
            emo = random.choice(emojis)
            
            # Slimmer wall for faster processing
            line = f"【﻿ {target_name} 】 𝚂ᴀ𝚈 【﻿ＰＲＶＲ】 𝐃ᴀᴅᴅ𝐘 {emo}\n"
            message_payload = line * BLOCK_COUNT 
            message_payload += f"⚡ {random.randint(100, 999)}"

            # Direct Broadcast
            cl.direct_send(message_payload, thread_ids=[thread_id])
            
            # Visual confirmation
            print(f"💥 [Agent {agent_id}] Hit!")
            
            if DELAY > 0:
                time.sleep(DELAY)
                
        except Exception as e:
            # If you see '429', the agent must rest
            if "429" in str(e):
                print(f"⚠️ [Agent {agent_id}] Rate Limited. Sleeping 10s...")
                time.sleep(10)
            else:
                print(f"⚠️ [Agent {agent_id}] Error: {e}")
                time.sleep(2)

def main():
    if not SESSION_ID or not THREAD_ID:
        print("❌ MISSING CONFIG")
        return

    # Use ONE client for ALL agents to keep the socket warm
    cl = Client()
    try:
        cl.login_by_sessionid(SESSION_ID)
        print("🔓 Master Session Authenticated.")
    except Exception as e:
        print(f"❌ Login Error: {e}")
        return

    print(f"🔥 DEPLOYING {AGENTS} AGENTS...")

    with ThreadPoolExecutor(max_workers=AGENTS) as executor:
        for i in range(AGENTS):
            executor.submit(rapid_agent, cl, THREAD_ID, TARGET_NAME, i+1)

if __name__ == "__main__":
    main()
