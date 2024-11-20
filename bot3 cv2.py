import time
import random
import datetime
import os
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TikTokBot:
    def __init__(self):
        # Configuración del navegador con opciones adicionales
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.driver = uc.Chrome(options=self.chrome_options)

        # Carpeta para guardar las imágenes del captcha
        self.image_folder = os.path.expanduser("~/Desktop/fotosparaia")
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

    def open_url(self, url):
        """Abre la URL proporcionada y espera que la página cargue completamente."""
        print(f"Abriendo TikTok: {url}")
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

    def create_account(self, email, password):
        print("Creando cuenta en TikTok...")
        try:
            self.driver.get("https://www.tiktok.com/signup")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Usar número de teléfono o correo electrónico')]"))
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Registrarse con un correo electrónico')]"))
            ).click()

            # Rellenar la fecha de nacimiento
            self.fill_birthdate()

            # Ingresar el correo
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Dirección de correo electrónico']"))
            )
            email_field.send_keys(email)

            # Ingresar la contraseña
            password_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Contraseña']")
            password_field.send_keys(password)

            # Hacer clic en el botón "Enviar código" antes de capturar las imágenes
            self.click_send_code()

            # Detectar y guardar imágenes del captcha
            self.save_captcha_images()

        except Exception as e:
            print(f"Error al crear la cuenta: {e}")
            self.driver.save_screenshot("error_tiktok.png")
            print("Captura de pantalla guardada como 'error_tiktok.png'.")
        finally:
            # Mantener el navegador abierto para inspección manual
            print("Navegador abierto para inspección manual.")
            while True:
                time.sleep(100)

    def fill_birthdate(self):
        """Rellena la fecha de nacimiento de forma rápida (mayor de 18 y menor de 30 años)."""
        print("Rellenando la fecha de nacimiento rápidamente...")
        try:
            current_year = datetime.datetime.now().year
            birth_year = random.randint(current_year - 30, current_year - 18)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)

            month_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Mes')]"))
            )
            month_button.click()
            time.sleep(0.5)

            # Seleccionar mes
            months = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']"))
            )
            months[birth_month - 1].click()

            time.sleep(0.5)
            # Seleccionar día
            day_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Día')]"))
            )
            day_button.click()

            time.sleep(0.5)
            day_option = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@role='option'][text()='{birth_day}']"))
            )
            day_option.click()

            time.sleep(0.5)
            # Seleccionar año
            year_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Año')]"))
            )
            year_button.click()

            time.sleep(0.5)
            year_option = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@role='option'][text()='{birth_year}']"))
            )
            year_option.click()
            time.sleep(0.5)

            print("Fecha de nacimiento seleccionada.")
        except Exception as e:
            print(f"Error al rellenar la fecha de nacimiento: {e}")
            self.driver.save_screenshot("birthdate_error.png")
            print("Captura de pantalla guardada como 'birthdate_error.png'.")

    def click_send_code(self):
        """Hacer clic en el botón 'Enviar código'."""
        try:
            print("Buscando el botón 'Enviar código'...")
            send_code_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='send-code-button']"))
            )
            send_code_button.click()
            print("Botón 'Enviar código' presionado. Esperando imágenes del captcha.")
            time.sleep(3)  # Esperar a que aparezcan las imágenes
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Enviar código': {e}")
            raise

    def save_captcha_images(self):
        """Descarga las imágenes del captcha y las guarda en la carpeta especificada."""
        try:
            print("Buscando imágenes del captcha...")

            # Localizar la imagen exterior
            exterior_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[9]/div/div/div/div[2]/div[1]/img[1]"))
            )
            exterior_url = exterior_element.get_attribute("src")

            # Localizar la imagen interior
            interior_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[9]/div/div/div/div[2]/div[1]/img[2]"))
            )
            interior_url = interior_element.get_attribute("src")

            # Guardar las imágenes
            self.download_image(exterior_url, "exterior")
            self.download_image(interior_url, "interior")

            print("Imágenes del captcha guardadas exitosamente.")
        except Exception as e:
            print(f"Error al guardar las imágenes del captcha: {e}")

    def download_image(self, url, image_type):
        """Descarga una imagen desde una URL y la guarda en la carpeta de imágenes."""
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Definir el nombre de archivo con timestamp para evitar duplicados
                filename = f"{image_type}_{int(time.time())}.jpeg"
                filepath = os.path.join(self.image_folder, filename)
                with open(filepath, "wb") as file:
                    file.write(response.content)
                print(f"Imagen {image_type} guardada como {filename}")
            else:
                print(f"No se pudo descargar la imagen {image_type}. HTTP {response.status_code}")
        except Exception as e:
            print(f"Error al descargar la imagen {image_type}: {e}")

    def close_browser(self):
        """Cierra el navegador."""
        self.driver.quit()


if __name__ == "__main__":
    bot = TikTokBot()
    bot.open_url("https://www.tiktok.com/signup")

    # Suponiendo que tienes un correo y una contraseña predefinidos
    email = "correo414141@gmail.com"
    password = "Contrña@@a123"
    bot.create_account(email, password)