import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QLabel
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
        self.setGeometry(100, 100, 400, 300)

        self.driver = None


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)


        self.layout = QVBoxLayout()


        self.title_label = QLabel("EBS Manşet Resim İndirme Programı")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.open_site_button = QPushButton("Siteyi Aç")
        self.open_site_button.setStyleSheet(self.get_button_style())
        self.open_site_button.clicked.connect(self.open_website)

        self.screenshot_button = QPushButton("Ekran Görüntüsü Al")
        self.screenshot_button.setStyleSheet(self.get_button_style())
        self.screenshot_button.clicked.connect(self.capture_screenshot)

        self.exit_button = QPushButton("Kapat")
        self.exit_button.setStyleSheet(self.get_button_style())
        self.exit_button.clicked.connect(self.close_application)


        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.open_site_button)
        self.layout.addWidget(self.screenshot_button)
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

    def capture_screenshot(self):
        if not self.driver:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce siteyi açın.")
            return

        try:
            canvas_wrapper = self.driver.find_element(By.ID, "canvas-wrapper")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", canvas_wrapper)

            screenshot_path = os.path.join(os.getcwd(), "canvas_screenshot.png")
            canvas_wrapper.screenshot(screenshot_path)

            cropped_path = os.path.join(os.getcwd(), "canvas_screenshot_cropped.png")
            with Image.open(screenshot_path) as img:
                width, height = img.size
                left = (width - 684) // 2 if width > 684 else 0
                top = (height - 525) // 2 if height > 525 else 0
                right = left + 684 if width > 684 else width
                bottom = top + 525 if height > 525 else height

                cropped_img = img.crop((left, top, right, bottom))
                cropped_img.save(cropped_path)

            QMessageBox.information(self, "Başarılı", f"Ekran görüntüsü kırpıldı ve kaydedildi: {cropped_path}")
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
