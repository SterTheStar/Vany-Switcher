import sys
import os
import ctypes
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QPushButton, QMainWindow, QMessageBox, QWidget, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import winreg

# Função para verificar permissões de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Função para atualizar o registro
def set_registry_value(value):
    try:
        registry_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options"
        key_name = "DevOverrideEnable"

        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
            winreg.SetValueEx(key, key_name, 0, winreg.REG_DWORD, value)

        return True, None
    except Exception as e:
        return False, str(e)

# Função para verificar ou criar o caminho do registro
def ensure_registry_path():
    try:
        registry_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ):
            return False, "Path already exists."
    except FileNotFoundError:
        try:
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, registry_path):
                return True, None
        except Exception as e:
            return False, str(e)

# Textos para tradução
translations = {
    "en": {
        "title": "Vany Switcher",
        "description": "Easily switch registry settings for Valorant and Sony Vegas.",
        "set_valorant": "Set for Valorant",
        "set_sony": "Set for Sony Vegas",
        "fix_path": "Fix Registry Path",
        "info": "Choose the configuration or fix registry path if needed.",
        "success": "Success",
        "error": "Error",
        "permission_error": "This tool requires administrator privileges.",
        "registry_set": "Registry set to {value}. Restart your PC to apply changes.",
        "registry_fix_success": "Registry path created successfully.",
        "registry_fix_exists": "Registry path already exists. No changes made.",
        "registry_fix_error": "Failed to fix registry path. Error: {error}",
        "registry_update_error": "Failed to update the registry. Error: {error}"
    },
    "pt": {
        "title": "Vany Switcher",
        "description": "Altere facilmente as configurações de registro para Valorant e Sony Vegas.",
        "set_valorant": "Configurar para Valorant",
        "set_sony": "Configurar para Sony Vegas",
        "fix_path": "Corrigir Caminho do Registro",
        "info": "Escolha a configuração ou corrija o caminho do registro, se necessário.",
        "success": "Sucesso",
        "error": "Erro",
        "permission_error": "Esta ferramenta requer privilégios de administrador.",
        "registry_set": "Registro definido para {value}. Reinicie o PC para aplicar as mudanças.",
        "registry_fix_success": "Caminho do registro criado com sucesso.",
        "registry_fix_exists": "O caminho do registro já existe. Nenhuma alteração foi feita.",
        "registry_fix_error": "Falha ao corrigir o caminho do registro. Erro: {error}",
        "registry_update_error": "Falha ao atualizar o registro. Erro: {error}"
    }
}

# Janela principal
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = "en"
        self.setWindowTitle(translations[self.language]["title"])
        self.setGeometry(300, 300, 700, 400)
        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout()

        # Seleção de idioma
        self.language_selector = QComboBox()
        self.language_selector.addItems(["English", "Português"])
        self.language_selector.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.language_selector)

        # Título
        self.title = QLabel(translations[self.language]["title"])
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Mensagem de descrição
        self.description = QLabel(translations[self.language]["description"])
        self.description.setFont(QFont("Arial", 14))
        self.description.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.description)

        # Botões para alternar
        self.btn_valorant = QPushButton(translations[self.language]["set_valorant"])
        self.btn_valorant.setFont(QFont("Arial", 12))
        self.btn_valorant.clicked.connect(lambda: self.change_registry(0))
        layout.addWidget(self.btn_valorant)

        self.btn_sony = QPushButton(translations[self.language]["set_sony"])
        self.btn_sony.setFont(QFont("Arial", 12))
        self.btn_sony.clicked.connect(lambda: self.change_registry(1))
        layout.addWidget(self.btn_sony)

        # Botão para corrigir o caminho do registro
        self.btn_fix = QPushButton(translations[self.language]["fix_path"])
        self.btn_fix.setFont(QFont("Arial", 12))
        self.btn_fix.clicked.connect(self.fix_registry_path)
        layout.addWidget(self.btn_fix)

        # Mensagem de informação
        self.info_label = QLabel(translations[self.language]["info"])
        self.info_label.setFont(QFont("Arial", 12))
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)

        # Configuração da central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def change_language(self):
        self.language = "pt" if self.language_selector.currentIndex() == 1 else "en"
        self.update_texts()

    def update_texts(self):
        self.setWindowTitle(translations[self.language]["title"])
        self.title.setText(translations[self.language]["title"])
        self.description.setText(translations[self.language]["description"])
        self.btn_valorant.setText(translations[self.language]["set_valorant"])
        self.btn_sony.setText(translations[self.language]["set_sony"])
        self.btn_fix.setText(translations[self.language]["fix_path"])
        self.info_label.setText(translations[self.language]["info"])

    def change_registry(self, value):
        if not is_admin():
            QMessageBox.warning(self, translations[self.language]["error"], translations[self.language]["permission_error"])
            return

        success, error = set_registry_value(value)
        if success:
            QMessageBox.information(self, translations[self.language]["success"], translations[self.language]["registry_set"].format(value=value))
        else:
            QMessageBox.critical(self, translations[self.language]["error"], translations[self.language]["registry_update_error"].format(error=error))

    def fix_registry_path(self):
        if not is_admin():
            QMessageBox.warning(self, translations[self.language]["error"], translations[self.language]["permission_error"])
            return

        success, error = ensure_registry_path()
        if success:
            QMessageBox.information(self, translations[self.language]["success"], translations[self.language]["registry_fix_success"])
        elif error == "Path already exists.":
            QMessageBox.information(self, translations[self.language]["success"], translations[self.language]["registry_fix_exists"])
        else:
            QMessageBox.critical(self, translations[self.language]["error"], translations[self.language]["registry_fix_error"].format(error=error))

# Inicialização do aplicativo
if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
