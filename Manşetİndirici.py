import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

class ModernGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EBS Manşet Resim İndirme Programı")
        self.setGeometry(100, 100, 400, 400)

        self.driver = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.title_label = QLabel("EBS Manşet Resim İndirme Programı")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Resim linkini buraya girin")
        self.link_input.setStyleSheet("padding: 5px; font-size: 14px;")

        self.download_and_upload_button = QPushButton("Resmi İndir ve Yükle")
        self.download_and_upload_button.setStyleSheet(self.get_button_style())
        self.download_and_upload_button.clicked.connect(self.download_and_upload_image)

        self.open_site_button = QPushButton("Siteyi Aç")
        self.open_site_button.setStyleSheet(self.get_button_style())
        self.open_site_button.clicked.connect(self.open_website)


        self.exit_button = QPushButton("Kapat")
        self.exit_button.setStyleSheet(self.get_button_style())
        self.exit_button.clicked.connect(self.close_application)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.link_input)
        self.layout.addWidget(self.download_and_upload_button)
        self.layout.addWidget(self.open_site_button)

        self.layout.addWidget(self.exit_button)
        self.central_widget.setLayout(self.layout)

    def get_button_style(self):
        return (
            "QPushButton {"
            "    background-color: #5D9CEC;"
            "    color: white;"
            "    border: none;"
            "    border-radius: 20px;"
            "    padding: 10px 20px;"
            "    font-size: 16px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #4A89DC;"
            "}"
        )

    def open_website(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.driver.get("https://ebubekirbastama.com.tr/ebsmansetolusturici.html")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "canvas-wrapper")))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {e}")

    def download_and_upload_image(self):
        image_url = self.link_input.text()
        if not image_url:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir resim linki girin.")
            return

        try:
            # Resmi indirme
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image_path = os.path.join(os.getcwd(), "downloaded_image.png")
                with open(image_path, "wb") as file:
                    file.write(response.content)
                #QMessageBox.information(self, "Başarılı", f"Resim indirildi: {image_path}")

                # Resmi siteye yükleme
                if not self.driver:
                    QMessageBox.warning(self, "Uyarı", "Lütfen önce siteyi açın.")
                    return

                upload_input = self.driver.find_element(By.XPATH, "//*[@id='imageInput']")
                upload_input.send_keys(image_path)

                #QMessageBox.information(self, "Başarılı", "Resim siteye yüklendi.")

                # İndirilen dosyayı silme
                os.remove(image_path)
                #QMessageBox.information(self, "Başarılı", "İndirilen resim dosyası silindi.")

                save_button = self.driver.find_element(By.XPATH, "//*[@id='saveBtn']")
                save_button.click()

            else:
                QMessageBox.critical(self, "Hata", "Resim indirilemedi. Linki kontrol edin.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {e}")


    def close_application(self):
        if self.driver:
            self.driver.quit()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("a.png"))

    window = ModernGUI()
    window.show()

    sys.exit(app.exec_())
