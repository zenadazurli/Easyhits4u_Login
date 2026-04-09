#!/usr/bin/env python3
# app.py - Login con Browserless BQL (per Render)

import requests
import json
import time
import os
from datetime import datetime
from pathlib import Path

# ==================== CHIAVI VALIDE (60) ====================
VALID_KEYS = [
    "2UFyHOdxsID23VMa0518a22c6b683ea3c11c1bdca148d5381",
    "2UIAf0U41Twctlr77ecbfa2545692634758496b2eb88a170c",
    "2UIAhSj6AMSpgLM5400cb96e68c36236805887d583fa1c1a8",
    "2UIAkQ4DGbDLMB06db1a95369b032405097bcfe53b9b8d444",
    "2UIAoK9f3FItlml3f95c43bb78d2b15d3e274da5c52fcb5cd",
    "2UIArIu84xpGFuV1b4e825a86352e4bec7b54db59df943bf0",
    "2UIAsvzIYtc0o6Pa719bbb072a635a0140cee8591aec0e617",
    "2UIAzLYxMfMvBTTf24fef2bee78bd26ccc8e423b6dbd9d72c",
    "2UIB0BADWlWBhpUd9b3113aae7aec11928693179b8e97adf7",
    "2UIB8rlEnDrj6Cv44d507f520ec52fa50046e7a70c30df6c6",
    "2UIB9J2tCnemabr9e97eff9685066c2072e18a52cfa283aa9",
    "2UIBB3QQ3H39YFu7d4fd1c778669ef19c8db22610905f23bb",
    "2UIBC8fgRMkg9wZ41fe0fe622994483be7093f33c02e53835",
    "2UIBGwfAlxxB6ni8919255b5bc976ec9ff72e0e7ee7f020de",
    "2UIBHpFuiMsVdXx3403174d9c61f08000e61d09260287e390",
    "2UIBJUl1ne3E92ya0949e27d64225c71a87e1d01458304c98",
    "2UIBKJ1ZL4HeXTTef781aa5c7c90ff94cc7d8e04545cf5ff9",
    "2UIBMTvCwvbW8zyeb1a2c2fc6d628643d2fc7837706f662d4",
    "2UIBOuJaRF5cBah589a83ba07a2bf4b4ae1e0bede889db139",
    "2UIBQDGaiPhyK5cc7d8d10689c2376b516809e26a4331bbe7",
    "2UIBRMkIfmmc5wU462f920ea771e4b0e8c29a96509179becd",
    "2UIBTMXwg0OXKdLdb313c233f7b40884382642b1336a75475",
    "2UIBUw762KYlNYe436d56b56b785ae327aea06af5c57b0856",
    "2UIBWGd7CenkAZP4e84a28fc45390849c04ec824c6b70c4aa",
    "2UIBX2qFOoT6UfQf0dca472d23a39ee0d2cc679711254df6e",
    "2UIBZ6iew6q5MjY587ca12d2ba6a8a7dec2887c680e0a295d",
    "2UIBalRcxjMmhLraa054e3a3fcc66019fa02e4756d40a97ca",
    "2UIBcJf0KJwjIJCc6aa92098f4b4d9677b277fa08bddaa52f",
    "2UIBdWa0VtcPa7l291b4497fca8ed7ad26b5c4d5927f54c52",
    "2UIBfg3C0DBareT4b3bc7b9de04934615085d885e0037c6a9",
    "2UIBg9igA9Adum65d15c87a1ebdbdd8462f2b769b9e6d0534",
    "2UIBiv7UFTo86PL7733f37e8662dc5ac1e44fbbfa69938c47",
    "2UIBjq41So7iISXc9b6488e29439c45ac81ec6655413598b7",
    "2UIBlZtTVvSSd9Mef4e7f74c7dadf262e366cf0d52a9278e1",
    "2UIBmotaoPEgiLGb4d8ff65588ad03856bca142e29d10f9d7",
    "2UIBoXymrMnL6rB7c0bf5d89b1d24423cf95f989c717a93da",
    "2UIBqLMCQct1MEc93871eac596a18158adf155055ea891b82",
    "2UIBsC5kqg908ss2b15a06dfd516f5477e644f4970239c2f3",
    "2UIBtryD9TY1rfLf40876aea895c6b19cfccd6d0423bb1a5a",
    "2UIBvZWEqIfKMABdb7ad2379d49b5fdb791668c5b8ae2872c",
    "2UIBwI8LlOkgnR2401030dc085c656433e9d9967c05cb8500",
    "2UIBzkNUiIo3aqf0fcbbefa77c3d721bcc90d6ea330d21b4b",
    "2UIC0txEnUKbs2e2011d4dbfcaccbf586e7cfd303ee25846c",
    "2UIC2RQTla00fnx09c8e8e078bda0be2ee065f87912fcf3ec",
    "2UIC3HmfnANB85ua2fafaa2b7d15fcddfaf43257ea8207a86",
    "2UIC5oOQStd9GOdd78704a1c13ede87f1ad076b3a3c5c014a",
    "2UIC6fQE3KZWxxF95f4c1b1514c6dd3d62ba0670368dbbdf0",
    "2UIC8HXKajhflGK4f6a4fc65b90703c46867dc5868233557d",
    "2UIC9N5NnxkvkiXc269dcbc7d2611f06b19dd6ac170a0e6a4",
    "2UICByRoMWLCFQP85171e81920c71c994e70f565ea94a5af9",
    "2UICCligGnceGaqb0567585836c440c4d21449a570494dfa6",
    "2UICEY4jAqkhpY0f3ecd736fb3d2b1df0f72a5ee544acf341",
    "2UICFz5KhinMtoGa87a2e4a5e156bb3e991297a8f794509c0",
    "2UICIQvD2zirSr161b5959fe434bec1ebe8e5ba0c62a03892",
    "2UICJ88uL7vxQXI13806d1cc2aab512c879ea4b47488aff01",
    "2UICLD7cUOCd06oe31be2d953915e565572bfc9990c96074b",
    "2UICM5P6tkSm3Qv2adc61218a5a7d6ea2f680320cd4db32ea",
    "2UICOGF3whhFISb5a4d943b2f658a0948de3321458f644f73",
    "2UICPYnut7CE37off5de03b2042b14aae1e1c8916eec85f6a",
    "2UICRMpGaWJQKP954bdcecee3ff7068055ac6c06af038c9e1",
]

BROWSERLESS_URL = "https://production-sfo.browserless.io/chrome/bql"

# Account EasyHits4U (da modificare con le tue credenziali)
EASYHITS_EMAIL = "clarabassoni2+borevunechi@gmail.com"
EASYHITS_PASSWORD = "DF45$!daza"
REFERER_URL = "https://www.easyhits4u.com/?ref=nicolacaporale"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_cf_token(api_key):
    query = """
    mutation {
      goto(url: "https://www.easyhits4u.com/logon/", waitUntil: networkIdle, timeout: 60000) {
        status
      }
      solve(type: cloudflare, timeout: 60000) {
        solved
        token
        time
      }
    }
    """
    
    url = f"{BROWSERLESS_URL}?token={api_key}"
    
    try:
        start = time.time()
        response = requests.post(url, json={"query": query}, headers={"Content-Type": "application/json"}, timeout=120)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        if "errors" in data:
            return None
        
        solve_info = data.get("data", {}).get("solve", {})
        
        if solve_info.get("solved"):
            token = solve_info.get("token")
            log(f"   ✅ Token ({time.time()-start:.1f}s)")
            return token
        return None
    except Exception as e:
        log(f"   ❌ Errore: {e}")
        return None

def login_with_token(token):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/148.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': REFERER_URL,
    }
    
    data = {
        'manual': '1',
        'fb_id': '',
        'fb_token': '',
        'google_code': '',
        'username': EASYHITS_EMAIL,
        'password': EASYHITS_PASSWORD,
        'cf-turnstile-response': token,
    }
    
    session.get(REFERER_URL)
    response = session.post("https://www.easyhits4u.com/logon/", data=data, headers=headers, allow_redirects=True, timeout=30)
    final_cookies = session.cookies.get_dict()
    
    if 'user_id' in final_cookies:
        log(f"   ✅ Login OK! user_id: {final_cookies['user_id']}")
        return final_cookies
    return None

def main():
    log("=" * 50)
    log("🚀 LOGIN CON BROWSERLESS BQL")
    log("=" * 50)
    
    for api_key in VALID_KEYS:
        log(f"🔑 Tentativo con chiave: {api_key[:10]}...")
        
        token = get_cf_token(api_key)
        if not token:
            log(f"   ❌ Token non ottenuto")
            continue
        
        cookies = login_with_token(token)
        if cookies:
            log(f"🎉 Login OK! user_id={cookies.get('user_id')}, sesids={cookies.get('sesids')}")
            # Salva i cookie per usarli nello script di surf
            with open("/tmp/easyhits4u/cookies.json", "w") as f:
                json.dump(cookies, f)
            return
        
        log(f"   ❌ Login fallito")
    
    log("❌ Login fallito con tutte le chiavi")

if __name__ == "__main__":
    main()
