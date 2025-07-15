from instagrapi import Client
from keep_alive import keep_alive
import os
import time
import uuid
import random
import itertools
from dotenv import load_dotenv

# 🔃 Load .env variables
load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")
SPAM_MESSAGE = os.getenv("SPAM_MESSAGE", "BLACK TERI MA KA BHOSDA CHOD DU?")
SPAM_DELAY_MIN = int(os.getenv("SPAM_DELAY_MIN", 25))
SPAM_DELAY_MAX = int(os.getenv("SPAM_DELAY_MAX", 40))

cl = Client()

def login_safe():
    try:
        # Try loading settings if file exists
        if os.path.exists("settings.json"):
            cl.load_settings("settings.json")
            cl.login(USERNAME, PASSWORD)
            print("✅ Fast login via settings.json")
        else:
            raise FileNotFoundError

        # Dump updated session
        cl.dump_settings("settings.json")

    except Exception as e:
        print("⚠️ Login via settings.json failed:", e)
        try:
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings("settings.json")
            print("✅ Fresh login successful, settings saved.")
        except Exception as ee:
            print("❌ Login failed completely:", ee)

def get_gc_thread_id():
    try:
        threads = cl.direct_threads(amount=5)
        for thread in threads:
            if thread.is_group:
                return thread.id
    except Exception as e:
        print("⚠️ Failed to get GC:", e)
    return None

def safe_send_msg(thread_id, msg):
    try:
        cl.direct_answer(thread_id, msg)
    except Exception as e:
        print("⚠️ Send failed. Retrying login...")
        try:
            login_safe()
            cl.direct_answer(thread_id, msg)
        except Exception as ee:
            print("❌ Permanent fail:", ee)
            time.sleep(60)

def start_spamming():
    thread_id = get_gc_thread_id()
    if not thread_id:
        print("❌ No group chat found.")
        return

    print(f"🚀 Spamming GC: {thread_id}")

    msgs = [
        f"{SPAM_MESSAGE} 🤣",
        f"{SPAM_MESSAGE} 😂",
        f"{SPAM_MESSAGE} 😆",
        f"{SPAM_MESSAGE}\nID: {uuid.uuid4()}"
    ]

    msg_cycle = itertools.cycle(msgs)

    while True:
        msg = next(msg_cycle)
        print(f"📤 Sending: {msg[:30]}...")
        safe_send_msg(thread_id, msg)
        time.sleep(random.randint(SPAM_DELAY_MIN, SPAM_DELAY_MAX))

# 🌐 Start bot
keep_alive()
login_safe()
start_spamming()
