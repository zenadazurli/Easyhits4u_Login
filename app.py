import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================= CONFIGURAZIONE =================
USERNAME = "sandrominori50+giorgiofaggiolini@gmail.com"
PASSWORD = "DDnmVV45!!"

# Lista di token Browserless (tutti quelli validi dalla tua lista)
TOKENS = [
    "2UIuKcJvun4R77F313307382c902416a7b4182b41c60ab655",
    "2UIuLDWh7ajw1fw0fd8db3599f49f5b207c36196b317535d9",
    "2UIuNFMS3ilf9tL483dca9443bd696161cd6494703ad11a9a",
    "2UIuOg7KoH653yJ253de7b452f459e6c1aaa2d3877ebd7ff1",
    "2UIuQ7WsV43MTaWbf7af91b6c2d9439f19383068c67226507",
    "2UIuRxMmqCueYZT245387bdde3541387530ac4a4cdac8210d",
    "2UIuTk4NV9YEZYfec7d8ff7af421dcf1ac9be09634c3592dc",
    "2UIuUGtgLIBTdned851acb58282b709b857b533e24d3ec6bf",
    "2UIuWUpXw9Us1hkcb5496c4a18956f3f2c527b39327a99641",
    "2UIuYDMCnULuk1u51de7efb0404eb2f8347f0cecb2d87d330",
    "2UIuaQmu1XK4W5k354a019269ea140dcc45b088ec477b8c87",
    "2UIubwkm21RIi9Yf891666901a176d8776a02480b6b816550",
    "2UIudm3HYaNK5Qw4cbf85baee95be4de5a49f6e509b4c92f8",
    # Aggiungi qui tutte le altre chiavi valide (quelle da 2UG..., 2UI..., ecc.)
]
# ==================================================

def login_with_token(token):
    """Tenta il login con un singolo token Browserless"""
    browserless_url = f"wss://chrome.browserless.io?token={token}"
    print(f"🔑 Tentativo con token: {token[:10]}...")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Remote(command_executor=browserless_url, options=options)
    except Exception as e:
        print(f"   ❌ Connessione fallita: {e}")
        return None
    
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
            user_id = next((c['value'] for c in cookies if c['name'] == 'user_id'), None)
            sesids = next((c['value'] for c in cookies if c['name'] == 'sesids'), None)
            print(f"   ✅ Login OK! user_id={user_id}, sesids={sesids}")
            
            os.makedirs("/tmp/easyhits4u", exist_ok=True)
            with open("/tmp/easyhits4u/cookies.json", "w") as f:
                json.dump(cookies, f)
            print("   💾 Cookies salvati")
            return True
        else:
            print("   ❌ Login fallito (credenziali o captcha)")
            return False
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return False
    finally:
        driver.quit()

def login():
    """Prova tutti i token in sequenza finché uno non funziona"""
    print("==================================================")
    print("🚀 LOGIN CON BROWSERLESS (rotazione automatica)")
    print("==================================================")
    
    for token in TOKENS:
        success = login_with_token(token)
        if success:
            print(f"🎉 Token valido trovato: {token[:10]}...")
            return True
        print(f"   ⏭️  Passo al prossimo token...")
    print("❌ Nessun token funzionante tra quelli disponibili")
    return False

if __name__ == "__main__":
    login()
