import sys, threading, webbrowser, json, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QProgressBar, QAction, QMenu, QInputDialog,
    QMessageBox, QToolBar
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QTimer, QTime
from PyQt5.QtGui import QPixmap, QFont
import auth
import logger

BOOKMARKS_FILE = "bookmarks.json"

def load_bookmarks():
    return json.load(open(BOOKMARKS_FILE)) if os.path.exists(BOOKMARKS_FILE) else []

def save_bookmarks(bm):
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(bm, f, indent=2)

class BrowserTab(QWebEngineView):
    def __init__(self, main, username):
        super().__init__(main.tabs)
        self.main = main
        self.username = username
        self.setFocusPolicy(Qt.StrongFocus)
        self.urlChanged.connect(self.url_changed)
        self.loadStarted.connect(self.on_start)
        self.loadProgress.connect(self.main.progress.setValue)
        self.loadFinished.connect(self.on_finish)
        self.setUrl(QUrl("https://www.google.com"))

    def url_changed(self, qurl):
        url = qurl.toString()
        self.main.url_bar.setText(url)
        self.main.tabs.setTabText(self.main.tabs.indexOf(self), self.title() or "New Tab")
        threading.Thread(target=logger.log_activity, args=(self.username, url)).start()

    def on_start(self):
        self.main.setCursor(Qt.BusyCursor)
        self.main.progress.show()

    def on_finish(self):
        self.main.setCursor(Qt.ArrowCursor)
        self.main.progress.hide()
        self.setFocus()

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"🔮 RetroGlassTabs — {username}")
        self.setGeometry(100, 80, 1280, 840)
        self.setStyleSheet(self.retro_theme())
        font = QFont("Courier New", 11)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.tab_doubleclick)
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.setCentralWidget(self.tabs)

        # Nav toolbar
        toolbar = QToolBar("Browser Toolbar", self)
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbar.setStyleSheet("QToolBar { background: rgba(35, 38, 65, 0.85); }")

        self.back_btn = QPushButton("⬅")
        self.fwd_btn = QPushButton("➡")
        self.reload_btn = QPushButton("↻")
        self.home_btn = QPushButton("⌂")
        self.copy_btn = QPushButton("📄")
        self.ext_btn = QPushButton("🌐")
        self.full_btn = QPushButton("⛶")
        self.bookmark_btn = QPushButton("☆")
        self.bm_menu_btn = QPushButton("★")
        self.logout_btn = QPushButton("🚪")
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("🔍 Enter URL or search...")

        for w in [self.back_btn, self.fwd_btn, self.reload_btn, self.home_btn,
                  self.copy_btn, self.ext_btn, self.full_btn,
                  self.bookmark_btn, self.bm_menu_btn, self.logout_btn]:
            w.setFont(font)
            toolbar.addWidget(w)

        toolbar.addWidget(self.url_bar)

        self.url_bar.setFont(font)
        self.url_bar.returnPressed.connect(self.load_url)

        # Toolbar buttons connect to current tab
        self.back_btn.clicked.connect(lambda: self.current_tab().back())
        self.fwd_btn.clicked.connect(lambda: self.current_tab().forward())
        self.reload_btn.clicked.connect(lambda: self.current_tab().reload())
        self.home_btn.clicked.connect(lambda: self.current_tab().setUrl(QUrl("https://www.google.com")))
        self.full_btn.clicked.connect(self.toggle_fullscreen)
        self.copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(self.current_tab().url().toString()))
        self.ext_btn.clicked.connect(lambda: webbrowser.open(self.current_tab().url().toString()))
        self.bookmark_btn.clicked.connect(self.bookmark_page)
        self.bm_menu_btn.clicked.connect(self.show_bookmarks)
        self.logout_btn.clicked.connect(self.logout)

        # Logo + Clock
        logo = QLabel()
        try:
            logo.setPixmap(QPixmap("assets/company_logo.png").scaled(28, 28))
        except:
            logo.setText("🌐")
        self.clock = QLabel()
        self.clock.setFont(font)
        self.clock.setStyleSheet("color: #8af0ea")
        toolbar.addSeparator()
        toolbar.addWidget(logo)
        toolbar.addWidget(self.clock)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(4)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: #82eefd;
            }
        """)
        self.addToolBarBreak()
        self.progress_bar = QToolBar()
        self.progress_bar.addWidget(self.progress)
        self.addToolBar(Qt.TopToolBarArea, self.progress_bar)
        self.progress.hide()

        # Initialize browser tab
        self.add_tab()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.is_full = False

    def add_tab(self, url=QUrl("https://www.google.com")):
        tab = BrowserTab(self, self.username)
        tab.setUrl(url)
        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)

    def current_tab(self):
        return self.tabs.currentWidget()

    def close_tab(self, i):
        if self.tabs.count() == 1:
            return
        self.tabs.removeTab(i)

    def tab_doubleclick(self, index):
        if index == -1:
            self.add_tab()

    def load_url(self):
        url = self.url_bar.text().strip()
        if not url.startswith('http'):
            url = "https://" + url
        self.current_tab().setUrl(QUrl(url))

    def update_url_bar(self, index):
        if index >= 0:
            tab = self.tabs.widget(index)
            self.url_bar.setText(tab.url().toString())

    def update_clock(self):
        self.clock.setText("🕒 " + QTime.currentTime().toString("hh:mm:ss"))

    def logout(self):
        self.close()
        self.login = LoginWindow()
        self.login.show()

    def toggle_fullscreen(self):
        if self.is_full:
            self.showNormal()
        else:
            self.showFullScreen()
        self.is_full = not self.is_full

    def bookmark_page(self):
        url = self.current_tab().url().toString()
        title = self.current_tab().title() or url
        bm = load_bookmarks()
        bm.append({"title": title, "url": url})
        save_bookmarks(bm)
        QMessageBox.information(self, "Bookmarked", f"{title}\n{url}")

    def show_bookmarks(self):
        bm = load_bookmarks()
        menu = QMenu()
        if not bm:
            menu.addAction("No Bookmarks Yet")
        for item in bm:
            act = QAction(item["title"], self)
            act.triggered.connect(lambda _, u=item["url"]: self.current_tab().setUrl(QUrl(u)))
            menu.addAction(act)
        menu.exec_(self.bm_menu_btn.mapToGlobal(self.bm_menu_btn.rect().bottomLeft()))

    def retro_theme(self):
        return """
        QMainWindow, QWidget {
            background-color: #1f1f2b;
            color: #ccffcc;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        QPushButton {
            background: rgba(255,255,255,0.08);
            border: 1px solid #88cccc;
            padding: 6px;
            border-radius: 14px;
            color: #ccffcc;
        }
        QPushButton:hover {
            background: rgba(122,255,255, 0.2);
        }
        QLineEdit {
            background: rgba(255,255,255,0.12);
            border: 1px solid #7cc;
            border-radius: 14px;
            padding: 8px;
            color: #c0f0e0;
        }
        QScrollBar:vertical {
            width: 9px;
            background: rgba(255,255,255,0.05);
        }
        """

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Retro Login")
        self.setGeometry(400, 200, 400, 180)
        self.setStyleSheet("""
            QWidget {
                background-color: #1c1f26;
                color: #c0e0ff;
                font-family: 'Courier New';
                font-size: 15px;
            }
            QPushButton {
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #99ccff;
                background: rgba(255,255,255,0.07);
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.2);
            }
        """)
        layout = QVBoxLayout(self)
        self.login_btn = QPushButton("🖋 Login")
        self.signup_btn = QPushButton("🎉 Signup")
        layout.addWidget(self.login_btn)
        layout.addWidget(self.signup_btn)
        self.login_btn.clicked.connect(self.login)
        self.signup_btn.clicked.connect(self.signup)

    def login(self):
        u, ok1 = QInputDialog.getText(self, "Login", "Username:")
        p, ok2 = QInputDialog.getText(self, "Login", "Password:", QLineEdit.Password)
        if ok1 and ok2:
            if auth.verify_user(u, p):
                self.browser = MainWindow(u)
                self.browser.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid credentials.")

    def signup(self):
        u, ok1 = QInputDialog.getText(self, "Signup", "Username:")
        p, ok2 = QInputDialog.getText(self, "Signup", "Password:", QLineEdit.Password)
        if ok1 and ok2:
            if auth.signup_user(u, p):
                QMessageBox.information(self, "Success", "Signup complete. Login now.")
            else:
                QMessageBox.warning(self, "Error", "Username already exists.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())
