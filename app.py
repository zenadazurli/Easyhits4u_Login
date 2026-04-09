import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# ================= CONFIGURAZIONE =================
USERNAME = "sandrominori50+giorgiofaggiolini@gmail.com"
PASSWORD = "DDnmVV45!!"

# Browserless endpoint con una chiave valida (scegli una dalla tua lista)
BROWSERLESS_URL = "wss://chrome.browserless.io?token=2UGdbQnmFCJwS9Vd714eb85438cf63d00a8f878a898cfe865"

# Chiave per 2captcha (se non la usi, lascia vuota)
CAPTCHA_API_KEY = ""   # Es. "2UFyHOdxsI..." – se vuota, salta il captcha
# ==================================================

def solve_turnstile(sitekey, page_url):
    if not CAPTCHA_API_KEY:
        print("⚠️ Nessuna chiave CAPTCHA, salto risoluzione")
        return None
    print(f"🔑 Tentativo con chiave: {CAPTCHA_API_KEY[:8]}...")
    payload = {
        "key": CAPTCHA_API_KEY,
        "method": "turnstile",
        "sitekey": sitekey,
        "pageurl": page_url,
        "json": 1
    }
    try:
        start = time.time()
        r = requests.post("http://2captcha.com/in.php", data=payload)
        result = r.json()
        if result.get("status") == 1:
            captcha_id = result["request"]
            for _ in range(30):
                time.sleep(3)
                res = requests.get(f"http://2captcha.com/res.php?key={CAPTCHA_API_KEY}&action=get&id={captcha_id}&json=1")
                if res.json().get("status") == 1:
                    token = res.json()["request"]
                    print(f"   ✅ Token ({time.time() - start:.1f}s)")
                    return token
        else:
            print(f"   ❌ Errore captcha: {result}")
    except Exception as e:
        print(f"   ⚠️ Eccezione captcha: {e}")
    return None

def login():
    print("==================================================")
    print("🚀 LOGIN CON BROWSERLESS BQL")
    print("==================================================")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Remote(command_executor=BROWSERLESS_URL, options=options)
    
    try:
        driver.get("https://www.easyhits4u.com")
        wait = WebDriverWait(driver, 20)
        
        login_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        login_btn.click()
        
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        
        # Tentativo di risolvere Turnstile se presente
        try:
            turnstile = driver.find_element(By.CSS_SELECTOR, ".cf-turnstile")
            sitekey = turnstile.get_attribute("data-sitekey")
            if sitekey:
                token = solve_turnstile(sitekey, driver.current_url)
                if token:
                    driver.execute_script(f"document.querySelector('[name=cf-turnstile-response]').value = '{token}';")
        except:
            print("ℹ️ Nessun captcha Turnstile trovato, procedo...")
        
        submit_btn = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_btn.click()
        
        time.sleep(3)
        if "dashboard" in driver.current_url or "member" in driver.current_url:
            cookies = driver.get_cookies()
            user_id = None
            sesids = None
            for c in cookies:
                if c['name'] == 'user_id':
                    user_id = c['value']
                if c['name'] == 'sesids':
                    sesids = c['value']
            print(f"🎉 Login OK! user_id={user_id}, sesids={sesids}")
            
            # CREA DIRECTORY PRIMA DI SALVARE (correzione)
            os.makedirs("/tmp/easyhits4u", exist_ok=True)
            with open("/tmp/easyhits4u/cookies.json", "w") as f:
                json.dump(cookies, f)
            print("💾 Cookies salvati in /tmp/easyhits4u/cookies.json")
        else:
            print("❌ Login fallito, verificare credenziali o captcha")
            
    except Exception as e:
        print(f"❌ Errore: {e}")
    finally:
        driver.quit()

def main():
    login()

if __name__ == "__main__":
    main()