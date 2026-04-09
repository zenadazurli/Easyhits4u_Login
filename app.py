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

# Browserless (usa una chiave valida dalla tua lista)
BROWSERLESS_URL = "wss://chrome.browserless.io?token=2UGdbQnmFCJwS9Vd714eb85438cf63d00a8f878a898cfe865"

# Lascia vuoto se non usi 2captcha
CAPTCHA_API_KEY = ""
# ==================================================

def solve_turnstile(sitekey, page_url):
    if not CAPTCHA_API_KEY:
        return None
    try:
        # ... implementazione (ometto per brevità, ma puoi lasciare quella che avevi)
        pass
    except:
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
            
            # ✅ CREA LA DIRECTORY PRIMA DI SALVARE
            os.makedirs("/tmp/easyhits4u", exist_ok=True)
            with open("/tmp/easyhits4u/cookies.json", "w") as f:
                json.dump(cookies, f)
            print("💾 Cookies salvati")
        else:
            print("❌ Login fallito")
    except Exception as e:
        print(f"❌ Errore: {e}")
    finally:
        driver.quit()

def main():
    login()

if __name__ == "__main__":
    main()
