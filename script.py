# manual_page_login_test.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Browser detach ile açık kalsın
    opts = Options()
    opts.add_experimental_option("detach", True)

    # ChromeDriver başlat
    driver = webdriver.Chrome(options=opts, service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Login sayfasını aç
    driver.get("https://the-internet.herokuapp.com/login")

    # JS snippet’i enjekte et
    js = r'''
    (function(){
      if (window.__loginInterceptor) return;
      window.__loginInterceptor = true;
      const form = document.querySelector('form');
      form.addEventListener('submit', e => {
        e.preventDefault();  // gerçek post’u iptal et
        const u = document.getElementById('username').value;
        const p = document.getElementById('password').value;
        const old = document.getElementById('custom-login-msg');
        if (old) old.remove();
        const box = document.createElement('div');
        box.id = 'custom-login-msg';
        Object.assign(box.style, {
          position: 'fixed', top: '10px', right: '10px',
          padding: '12px 18px', color: 'white',
          fontSize: '18px', borderRadius: '6px',
          zIndex: 9999,
          backgroundColor: (u==='tomsmith' && p==='SuperSecretPassword!') ? 'green' : 'red'
        });
        box.innerText = (u==='tomsmith' && p==='SuperSecretPassword!')
          ? '✅ GİRİŞ BAŞARILI'
          : '❌ HATALI GİRİŞ';
        document.body.appendChild(box);
      });
    })();
    '''
    driver.execute_script(js)

    # Artık tarayıcı açık, istediğin kullanıcı adı ve şifreyi kendin gir,
    # Login butonuna tıkla. Sonuç sağ üstte görünecek.
    print("🔎 Tarayıcı hazır, formu manuel doldurup Login'e tıkla. Sonucu sayfada göreceksin.")

if __name__ == "__main__":
    main()
