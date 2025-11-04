import sys
import json
import threading
import time
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QGridLayout, QScrollArea, QSpacerItem,
    QSizePolicy, QProgressBar, QGroupBox, QRadioButton, QButtonGroup,
    QCheckBox, QStackedLayout, QFormLayout, QLineEdit, QSpinBox,
    QTabWidget, QTextEdit, QSplitter, QMenuBar, QStatusBar,
    QDialog, QInputDialog, QMessageBox, QFileDialog, QProgressDialog,
    QSystemTrayIcon, QStyle
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QTranslator, QLocale, QLibraryInfo,
    QPropertyAnimation, QEasingCurve, QRect, QUrl, QEvent, QObject,
    QMimeData, QDateTime, QTimeZone, QParallelAnimationGroup, QSettings,
    QStandardPaths, QPointF
)
from PyQt6.QtGui import (
    QFont, QPixmap, QIcon, QPalette, QColor, QLinearGradient,
    QBrush, QPainter, QFontDatabase, QEnterEvent, QMouseEvent,
    QClipboard, QShortcut, QDesktopServices, QValidator,
    QAction, QKeySequence  # QAction و QKeySequence در QtGui هستند
)
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import logging
import hashlib
import sqlite3
import uuid
import webbrowser
import platform
import subprocess
import shutil
import zipfile
import tempfile

# ====================== Global App Instance (Fixed QPixmap Error) ======================
app = None

def create_placeholder_pixmap(size=64, color=QColor("#0078D4"), shape="circle"):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    if shape == "circle":
        painter.setBrush(color)
        painter.setPen(QColor("white"))
        painter.drawEllipse(4, 4, size-8, size-8)
    elif shape == "star":
        painter.setBrush(color if "filled" in shape else Qt.GlobalColor.transparent)
        painter.setPen(color)
        points = [
            QPointF(size//2, 4), QPointF(size*0.6, size*0.35), QPointF(size-4, size*0.35),
            QPointF(size*0.7, size*0.55), QPointF(size*0.8, size-4), QPointF(size//2, size*0.7),
            QPointF(size*0.2, size-4), QPointF(size*0.3, size*0.55), QPointF(4, size*0.35),
            QPointF(size*0.4, size*0.35)
        ]
        painter.drawPolygon(points)
    elif shape == "arrow":
        painter.setBrush(color)
        painter.drawPolygon(QPointF(size*0.3, size*0.4), QPointF(size//2, size*0.7), QPointF(size*0.7, size*0.4))
    
    painter.end()
    return pixmap

def ensure_icons():
    icons_dir = "icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    icons = {
        "app_icon.png": (64, "#0078D4", "circle"),
        "soccer_ball.png": (64, "#FFFFFF", "circle"),
        "star.png": (32, "#FFD700", "star"),
        "star_filled.png": (32, "#FFD700", "star_filled"),
        "down_arrow.png": (24, "#0078D4", "arrow"),
        "filter.png": (24, "#0078D4", "arrow"),
        "refresh.png": (24, "#0078D4", "arrow"),
        "settings.png": (24, "#0078D4", "circle"),
        "notification.png": (24, "#FF6B6B", "circle")
    }
    
    for name, (size, color_str, shape) in icons.items():
        path = os.path.join(icons_dir, name)
        if not os.path.exists(path):
            color = QColor(color_str)
            pixmap = create_placeholder_pixmap(size, color, shape)
            pixmap.save(path)

# ====================== Configuration & Constants ======================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"
UPDATE_INTERVAL = 5000
ANIMATION_DURATION = 300
MAX_RETRIES = 5
CACHE_DURATION = 60

LANGUAGES = {
    "en": {"name": "English", "flag": "us", "direction": Qt.LayoutDirection.LeftToRight},
    "fa": {"name": "فارسی", "flag": "ir", "direction": Qt.LayoutDirection.RightToLeft},
    "zh": {"name": "中文", "flag": "cn", "direction": Qt.LayoutDirection.LeftToRight},
    "ru": {"name": "Русский", "flag": "ru", "direction": Qt.LayoutDirection.LeftToRight}
}

SPORT_MAPPING = {
    "football": {"api": "Soccer", "icon": "soccer_ball.png"},
    "basketball": {"api": "Basketball", "icon": "basketball"},
    "tennis": {"api": "Tennis", "icon": "tennis"},
    "volleyball": {"api": "Volleyball", "icon": "volleyball"},
    "handball": {"api": "Handball", "icon": "handball"}
}

# ====================== Translation System ======================
class Translator:
    def __init__(self):
        self.translations = self.load_translations()
        self.current_lang = "en"

    def load_translations(self):
        return {
            "en": {
                "app_name": "Live Sports Hub",
                "title": "Live Sports Scores",
                "subtitle": "Real-time updates from around the world",
                "select_sport": "Select Sport",
                "select_league": "Select League",
                "refresh": "Refresh Now",
                "auto_update": "Auto Update (5s)",
                "language": "Language",
                "theme": "Theme",
                "light": "Light",
                "dark": "Dark",
                "system": "System",
                "red": "Red Alert",
                "blue": "Ocean Blue",
                "loading": "Loading live scores...",
                "no_data": "No live matches available at the moment.",
                "vs": "vs",
                "live": "LIVE",
                "ft": "FULL TIME",
                "ht": "HALF TIME",
                "postponed": "POSTPONED",
                "cancelled": "CANCELLED",
                "football": "Football",
                "basketball": "Basketball",
                "tennis": "Tennis",
                "volleyball": "Volleyball",
                "handball": "Handball",
                "status": "Status",
                "home": "Home",
                "away": "Away",
                "score": "Score",
                "time": "Time",
                "league": "League",
                "update_time": "Updated",
                "error_api": "API Error: Unable to fetch data.",
                "network_error": "Network Error. Retrying...",
                "settings": "Settings",
                "about": "About",
                "exit": "Exit",
                "version": "Version",
                "developer": "Developed by",
                "source": "Source Code",
                "website": "Website",
                "donate": "Support Project",
                "search": "Search matches...",
                "filter": "Filter",
                "all_leagues": "All Leagues",
                "favorite": "Add to Favorites",
                "unfavorite": "Remove from Favorites",
                "notification": "Enable Notifications",
                "sound": "Play Sound on Goal",
                "fullscreen": "Toggle Fullscreen",
                "minimize": "Minimize to Tray",
                "statistics": "Statistics",
                "goals": "Goals",
                "yellow_cards": "Yellow Cards",
                "red_cards": "Red Cards",
                "corners": "Corners",
                "possession": "Possession",
                "shots": "Shots",
                "shots_on_target": "On Target",
                "fouls": "Fouls",
                "offside": "Offside",
                "saves": "Saves",
                "team_form": "Form",
                "last_matches": "Last 5 Matches",
                "win": "W",
                "draw": "D",
                "loss": "L",
                "points": "Pts",
                "position": "Pos",
                "played": "P",
                "goal_difference": "GD",
                "export": "Export Data",
                "import": "Import Data",
                "backup": "Create Backup",
                "restore": "Restore Backup",
                "clear_cache": "Clear Cache",
                "debug_mode": "Debug Mode",
                "api_key": "API Key",
                "save": "Save",
                "cancel": "Cancel",
                "close": "Close",
                "yes": "Yes",
                "no": "No",
                "ok": "OK",
                "apply": "Apply",
                "reset": "Reset",
                "default": "Default",
                "advanced": "Advanced",
                "proxy": "Proxy Settings",
                "timeout": "Timeout (s)",
                "retries": "Retries",
                "user_agent": "User Agent",
                "headers": "Custom Headers",
                "logs": "View Logs",
                "update_available": "Update Available!",
                "download": "Download",
                "later": "Later",
                "install": "Install Now",
                "changelog": "View Changelog",
                "checking_updates": "Checking for updates...",
                "up_to_date": "You are using the latest version.",
                "error_update": "Failed to check for updates.",
                "new_version": "New version {version} is available!",
                "current_version": "Current: {current}",
                "latest_version": "Latest: {latest}",
                "release_date": "Released: {date}",
                "size": "Size: {size}",
                "download_progress": "Downloading: {progress}%",
                "installing": "Installing update...",
                "restart_required": "Restart required to apply update.",
                "restart": "Restart Now"
            },
            "fa": {
                "app_name": "مرکز نتایج زنده ورزشی",
                "title": "نتایج زنده ورزشی",
                "subtitle": "به‌روزرسانی لحظه‌ای از سراسر جهان",
                "select_sport": "انتخاب ورزش",
                "select_league": "انتخاب لیگ",
                "refresh": "به‌روزرسانی فوری",
                "auto_update": "به‌روزرسانی خودکار (۵ث)",
                "language": "زبان",
                "theme": "تم",
                "light": "روشن",
                "dark": "تیره",
                "system": "سیستم",
                "red": "هشدار قرمز",
                "blue": "آبی اقیانوسی",
                "loading": "در حال بارگذاری نتایج زنده...",
                "no_data": "در حال حاضر هیچ مسابقه زنده‌ای وجود ندارد.",
                "vs": "در مقابل",
                "live": "زنده",
                "ft": "پایان بازی",
                "ht": "نیمه اول",
                "postponed": "تعویق افتاده",
                "cancelled": "لغو شده",
                "football": "فوتبال",
                "basketball": "بسکتبال",
                "tennis": "تنیس",
                "volleyball": "والیبال",
                "handball": "هندبال",
                "status": "وضعیت",
                "home": "میزبان",
                "away": "میهمان",
                "score": "امتیاز",
                "time": "زمان",
                "league": "لیگ",
                "update_time": "به‌روزرسانی",
                "error_api": "خطای API: دریافت اطلاعات ممکن نیست.",
                "network_error": "خطای شبکه. در حال تلاش مجدد...",
                "settings": "تنظیمات",
                "about": "درباره",
                "exit": "خروج",
                "version": "نسخه",
                "developer": "توسعه‌دهنده",
                "source": "کد منبع",
                "website": "وب‌سایت",
                "donate": "حمایت از پروژه",
                "search": "جستجوی مسابقات...",
                "filter": "فیلتر",
                "all_leagues": "همه لیگ‌ها",
                "favorite": "اضافه به علاقه‌مندی‌ها",
                "unfavorite": "حذف از علاقه‌مندی‌ها",
                "notification": "فعال‌سازی اعلان‌ها",
                "sound": "صدا هنگام گل",
                "fullscreen": "تمام‌صفحه",
                "minimize": "کوچک کردن به سینی",
                "statistics": "آمار",
                "goals": "گل‌ها",
                "yellow_cards": "کارت زرد",
                "red_cards": "کارت قرمز",
                "corners": "کرنر",
                "possession": "مالکیت توپ",
                "shots": "شوت",
                "shots_on_target": "شوت در چارچوب",
                "fouls": "خطا",
                "offside": "آفساید",
                "saves": "دفاع",
                "team_form": "فرم",
                "last_matches": "۵ بازی آخر",
                "win": "ب",
                "draw": "م",
                "loss": "ش",
                "points": "ا",
                "position": "رتبه",
                "played": "بازی",
                "goal_difference": "تفاضل",
                "export": "خروجی داده",
                "import": "ورودی داده",
                "backup": "تهیه پشتیبان",
                "restore": "بازیابی پشتیبان",
                "clear_cache": "پاک کردن حافظه موقت",
                "debug_mode": "حالت دیباگ",
                "api_key": "کلید API",
                "save": "ذخیره",
                "cancel": "انصراف",
                "close": "بستن",
                "yes": "بله",
                "no": "خیر",
                "ok": "تایید",
                "apply": "اعمال",
                "reset": "بازنشانی",
                "default": "پیش‌فرض",
                "advanced": "پیشرفته",
                "proxy": "تنظیمات پراکسی",
                "timeout": "تایم‌اوت (ثانیه)",
                "retries": "تلاش مجدد",
                "user_agent": "عامل کاربری",
                "headers": "هدرهای سفارشی",
                "logs": "مشاهده لاگ‌ها",
                "update_available": "به‌روزرسانی موجود است!",
                "download": "دانلود",
                "later": "بعداً",
                "install": "نصب اکنون",
                "changelog": "تغییرات",
                "checking_updates": "در حال بررسی به‌روزرسانی...",
                "up_to_date": "شما از آخرین نسخه استفاده می‌کنید.",
                "error_update": "خطا در بررسی به‌روزرسانی.",
                "new_version": "نسخه جدید {version} موجود است!",
                "current_version": "نسخه فعلی: {current}",
                "latest_version": "آخرین نسخه: {latest}",
                "release_date": "انتشار: {date}",
                "size": "حجم: {size}",
                "download_progress": "در حال دانلود: {progress}%",
                "installing": "در حال نصب به‌روزرسانی...",
                "restart_required": "برای اعمال به‌روزرسانی نیاز به ری‌استارت است.",
                "restart": "ری‌استارت اکنون"
            },
            "zh": {
                "app_name": "实时体育中心",
                "title": "实时体育比分",
                "subtitle": "全球实时更新",
                "select_sport": "选择运动",
                "select_league": "选择联赛",
                "refresh": "立即刷新",
                "auto_update": "自动更新 (5秒)",
                "language": "语言",
                "theme": "主题",
                "light": "明亮",
                "dark": "暗黑",
                "system": "系统",
                "red": "红色警报",
                "blue": "海洋蓝",
                "loading": "正在加载实时比分...",
                "no_data": "当前无进行中的比赛。",
                "vs": "对",
                "live": "直播",
                "ft": "完场",
                "ht": "中场",
                "postponed": "延期",
                "cancelled": "取消",
                "football": "足球",
                "basketball": "篮球",
                "tennis": "网球",
                "volleyball": "排球",
                "handball": "手球",
                "status": "状态",
                "home": "主队",
                "away": "客队",
                "score": "比分",
                "time": "时间",
                "league": "联赛",
                "update_time": "更新于",
                "error_api": "API 错误：无法获取数据。",
                "network_error": "网络错误。正在重试...",
                "settings": "设置",
                "about": "关于",
                "exit": "退出",
                "version": "版本",
                "developer": "开发者",
                "source": "源代码",
                "website": "官方网站",
                "donate": "支持项目",
                "search": "搜索比赛...",
                "filter": "筛选",
                "all_leagues": "所有联赛",
                "favorite": "加入收藏",
                "unfavorite": "移除收藏",
                "notification": "启用通知",
                "sound": "进球声音",
                "fullscreen": "全屏模式",
                "minimize": "最小化到托盘",
                "statistics": "统计",
                "goals": "进球",
                "yellow_cards": "黄牌",
                "red_cards": "红牌",
                "corners": "角球",
                "possession": "控球率",
                "shots": "射门",
                "shots_on_target": "射正",
                "fouls": "犯规",
                "offside": "越位",
                "saves": "扑救",
                "team_form": "状态",
                "last_matches": "近5场",
                "win": "胜",
                "draw": "平",
                "loss": "负",
                "points": "积分",
                "position": "排名",
                "played": "场",
                "goal_difference": "净胜",
                "export": "导出数据",
                "import": "导入数据",
                "backup": "创建备份",
                "restore": "恢复备份",
                "clear_cache": "清除缓存",
                "debug_mode": "调试模式",
                "api_key": "API 密钥",
                "save": "保存",
                "cancel": "取消",
                "close": "关闭",
                "yes": "是",
                "no": "否",
                "ok": "确定",
                "apply": "应用",
                "reset": "重置",
                "default": "默认",
                "advanced": "高级",
                "proxy": "代理设置",
                "timeout": "超时(秒)",
                "retries": "重试次数",
                "user_agent": "用户代理",
                "headers": "自定义请求头",
                "logs": "查看日志",
                "update_available": "有可用更新！",
                "download": "下载",
                "later": "稍后",
                "install": "立即安装",
                "changelog": "更新日志",
                "checking_updates": "正在检查更新...",
                "up_to_date": "您使用的是最新版本。",
                "error_update": "检查更新失败。",
                "new_version": "新版本 {version} 已发布！",
                "current_version": "当前版本: {current}",
                "latest_version": "最新版本: {latest}",
                "release_date": "发布日期: {date}",
                "size": "大小: {size}",
                "download_progress": "下载中: {progress}%",
                "installing": "正在安装更新...",
                "restart_required": "需要重启以应用更新。",
                "restart": "立即重启"
            },
            "ru": {
                "app_name": "Центр живых спортивных результатов",
                "title": "Живые спортивные результаты",
                "subtitle": "Мгновенные обновления со всего мира",
                "select_sport": "Выбрать вид спорта",
                "select_league": "Выбрать лигу",
                "refresh": "Обновить сейчас",
                "auto_update": "Автообновление (5с)",
                "language": "Язык",
                "theme": "Тема",
                "light": "Светлая",
                "dark": "Тёмная",
                "system": "Системная",
                "red": "Красная тревога",
                "blue": "Океанский синий",
                "loading": "Загрузка живых результатов...",
                "no_data": "В данный момент нет живых матчей.",
                "vs": "против",
                "live": "Прямая",
                "ft": "Финал",
                "ht": "Перерыв",
                "postponed": "Отложено",
                "cancelled": "Отменено",
                "football": "Футбол",
                "basketball": "Баскетбол",
                "tennis": "Теннис",
                "volleyball": "Волейбол",
                "handball": "Гандбол",
                "status": "Статус",
                "home": "Дом",
                "away": "Гости",
                "score": "Счёт",
                "time": "Время",
                "league": "Лига",
                "update_time": "Обновлено",
                "error_api": "Ошибка API: не удалось получить данные.",
                "network_error": "Ошибка сети. Повторная попытка...",
                "settings": "Настройки",
                "about": "О программе",
                "exit": "Выход",
                "version": "Версия",
                "developer": "Разработчик",
                "source": "Исходный код",
                "website": "Веб-сайт",
                "donate": "Поддержать проект",
                "search": "Поиск матчей...",
                "filter": "Фильтр",
                "all_leagues": "Все лиги",
                "favorite": "Добавить в избранное",
                "unfavorite": "Убрать из избранного",
                "notification": "Включить уведомления",
                "sound": "Звук при голе",
                "fullscreen": "Полный экран",
                "minimize": "Свернуть в трей",
                "statistics": "Статистика",
                "goals": "Голы",
                "yellow_cards": "Жёлтые карточки",
                "red_cards": "Красные карточки",
                "corners": "Угловые",
                "possession": "Владение мячом",
                "shots": "Удары",
                "shots_on_target": "Удары в створ",
                "fouls": "Фолы",
                "offside": "Офсайд",
                "saves": "Сейвы",
                "team_form": "Форма",
                "last_matches": "Последние 5 матчей",
                "win": "П",
                "draw": "Н",
                "loss": "Пор",
                "points": "Очки",
                "position": "Поз",
                "played": "И",
                "goal_difference": "Разн",
                "export": "Экспорт данных",
                "import": "Импорт данных",
                "backup": "Создать резервную копию",
                "restore": "Восстановить из копии",
                "clear_cache": "Очистить кэш",
                "debug_mode": "Режим отладки",
                "api_key": "Ключ API",
                "save": "Сохранить",
                "cancel": "Отмена",
                "close": "Закрыть",
                "yes": "Да",
                "no": "Нет",
                "ok": "ОК",
                "apply": "Применить",
                "reset": "Сбросить",
                "default": "По умолчанию",
                "advanced": "Дополнительно",
                "proxy": "Настройки прокси",
                "timeout": "Таймаут (сек)",
                "retries": "Попытки",
                "user_agent": "User Agent",
                "headers": "Пользовательские заголовки",
                "logs": "Просмотр логов",
                "update_available": "Доступно обновление!",
                "download": "Скачать",
                "later": "Позже",
                "install": "Установить сейчас",
                "changelog": "Список изменений",
                "checking_updates": "Проверка обновлений...",
                "up_to_date": "У вас последняя версия.",
                "error_update": "Ошибка проверки обновлений.",
                "new_version": "Доступна новая версия {version}!",
                "current_version": "Текущая: {current}",
                "latest_version": "Последняя: {latest}",
                "release_date": "Дата: {date}",
                "size": "Размер: {size}",
                "download_progress": "Загрузка: {progress}%",
                "installing": "Установка обновления...",
                "restart_required": "Требуется перезапуск.",
                "restart": "Перезапустить сейчас"
            }
        }

    def tr(self, key):
        return self.translations.get(self.current_lang, self.translations["en"]).get(key, key)

    def set_language(self, lang):
        if lang in self.translations:
            self.current_lang = lang
            return True
        return False

    def get_direction(self):
        return LANGUAGES.get(self.current_lang, LANGUAGES["en"])["direction"]

translator = Translator()

# ====================== Database Manager ======================
class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            try:
                config_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
                os.makedirs(config_dir, exist_ok=True)
                db_path = os.path.join(config_dir, "sports_hub.db")
            except:
                db_path = "sports_hub.db"
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    event_id TEXT PRIMARY KEY,
                    sport TEXT,
                    home TEXT,
                    away TEXT,
                    league TEXT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def get_setting(self, key, default=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else default

    def set_setting(self, key, value):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO settings (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """, (key, value))

    def add_favorite(self, event):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR IGNORE INTO favorites (event_id, sport, home, away, league)
                VALUES (?, ?, ?, ?, ?)
            """, (event["idEvent"], event["strSport"], 
                  event.get("strHomeTeam", ""), event.get("strAwayTeam", ""), event["strLeague"]))

    def remove_favorite(self, event_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM favorites WHERE event_id = ?", (event_id,))

    def get_favorites(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM favorites ORDER BY added_at DESC")
            return cursor.fetchall()

    def set_cache(self, key, data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO cache (key, data) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET data = excluded.data, timestamp = CURRENT_TIMESTAMP
            """, (key, json.dumps(data)))

    def get_cache(self, key, max_age=60):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT data, timestamp FROM cache WHERE key = ?
            """, (key,))
            row = cursor.fetchone()
            if row:
                data, timestamp = row
                if (datetime.now() - datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")).seconds < max_age:
                    return json.loads(data)
        return None

# ====================== API Worker Thread ======================
class APIWorker(QThread):
    data_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, sport="Soccer", league=None, use_cache=True):
        super().__init__()
        self.sport = sport
        self.league = league
        self.use_cache = use_cache
        self.running = True
        self.db = DatabaseManager()
        self.session = requests.Session()
        retry = Retry(total=MAX_RETRIES, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.headers.update({
            "User-Agent": "LiveSportsHub/2.0 (+https://github.com/yourname/livesportshub)"
        })

    def run(self):
        cache_key = f"events_{self.sport}_{self.league or 'all'}_{datetime.now().strftime('%Y-%m-%d')}"
        if self.use_cache:
            cached = self.db.get_cache(cache_key)
            if cached:
                self.data_ready.emit(cached)
                self.progress.emit(100)

        while self.running:
            try:
                self.fetch_live_events()
            except Exception as e:
                mock_data = self.generate_mock_data()
                self.data_ready.emit(mock_data)
            time.sleep(UPDATE_INTERVAL / 1000)

    def fetch_live_events(self):
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"{API_BASE_URL}/eventsday.php"
        params = {"d": today, "s": self.sport}
        if self.league:
            params["l"] = self.league

        self.progress.emit(30)
        response = self.session.get(url, params=params, timeout=15)
        self.progress.emit(70)

        if response.status_code == 200:
            data = response.json()
            events = data.get("events", [])
            enriched_events = self.enrich_events(events)
            result = {"events": enriched_events, "timestamp": datetime.now().isoformat()}
            self.db.set_cache(f"events_{self.sport}_{self.league or 'all'}_{today}", result)
            self.data_ready.emit(result)
            self.progress.emit(100)
        else:
            raise Exception(f"HTTP {response.status_code}")

    def enrich_events(self, events):
        enriched = []
        for event in events:
            event.setdefault("strHomeTeam", event["strEvent"].split(" vs ")[0] if " vs " in event["strEvent"] else "Team A")
            event.setdefault("strAwayTeam", event["strEvent"].split(" vs ")[-1] if " vs " in event["strEvent"] else "Team B")
            event.setdefault("intHomeScore", "0")
            event.setdefault("intAwayScore", "0")
            event.setdefault("strStatus", "Scheduled")
            event.setdefault("strProgress", event.get("strTime", "00:00"))
            enriched.append(event)
        return enriched

    def generate_mock_data(self):
        teams = [
            ("Real Madrid", "Barcelona"), ("Manchester United", "Liverpool"),
            ("Bayern Munich", "Dortmund"), ("Juventus", "Inter Milan"),
            ("PSG", "Marseille"), ("Chelsea", "Arsenal")
        ]
        import random
        events = []
        for i in range(6):
            home, away = random.choice(teams)
            score_home = random.randint(0, 4)
            score_away = random.randint(0, 4)
            status = random.choice(["Live", "HT", "FT", "Scheduled"])
            minute = random.randint(1, 90) if status == "Live" else 45 if status == "HT" else 90
            events.append({
                "idEvent": str(1000 + i),
                "strEvent": f"{home} vs {away}",
                "strLeague": random.choice(["La Liga", "Premier League", "Bundesliga", "Serie A"]),
                "strSport": self.sport,
                "strStatus": status,
                "intHomeScore": str(score_home),
                "intAwayScore": str(score_away),
                "strProgress": f"{minute}'" if status == "Live" else status,
                "strHomeTeam": home,
                "strAwayTeam": away,
                "dateEvent": datetime.now().strftime("%Y-%m-%d"),
                "strTime": f"{random.randint(12, 23):02d}:00"
            })
        return {"events": events, "timestamp": datetime.now().isoformat()}

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

# ====================== Modern UI Components ======================
class GlassEffect(QWidget):
    def __init__(self, opacity=0.15, blur_radius=20, parent=None):
        super().__init__(parent)
        self.opacity = opacity
        self.blur_radius = blur_radius
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(255, 255, 255, int(255 * self.opacity)))
        painter.setPen(QColor(255, 255, 255, 80))
        painter.drawRoundedRect(self.rect(), 20, 20)

class ModernButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(44)
        self.setIconSize(QSize(20, 20))
        if icon:
            self.setIcon(QIcon(icon))
        font = QFont("Segoe UI", 10, QFont.Weight.Medium)
        self.setFont(font)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(1, 1, -1, -1)

        if not self.isEnabled():
            color1 = QColor("#CCCCCC")
            color2 = QColor("#AAAAAA")
            text_color = QColor("#666666")
        elif self.isDown():
            color1 = QColor("#005A9E")
            color2 = QColor("#004478")
            text_color = QColor("white")
        elif self.underMouse():
            color1 = QColor("#1080EF")
            color2 = QColor("#0066CC")
            text_color = QColor("white")
        else:
            color1 = QColor("#0078D4")
            color2 = QColor("#106EBE")
            text_color = QColor("white")

        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0, color1)
        gradient.setColorAt(1, color2)
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 12, 12)

        painter.setPen(text_color)
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())

class IconButton(QPushButton):
    def __init__(self, icon_path, size=24, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(size, size))
        self.setFixedSize(size + 16, size + 16)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 4px;
            }
            QPushButton:hover {
                background: rgba(0, 120, 212, 0.2);
            }
            QPushButton:pressed {
                background: rgba(0, 120, 212, 0.4);
            }
        """)

# ====================== Main Application Window ======================
class LiveSportsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.worker = None
        self.current_sport = "Soccer"
        self.current_league = None
        self.auto_update = True
        self.favorites = set()
        self.sound_effect = QSoundEffect()
        self.last_data = {}
        self.init_ui()
        self.load_settings()
        self.apply_theme()
        self.start_worker()

    def init_ui(self):
        self.setWindowTitle(translator.tr("app_name"))
        self.setWindowIcon(QIcon("icons/app_icon.png"))
        self.resize(1400, 900)
        self.setMinimumSize(1000, 600)

        if platform.system() == "Windows" and int(platform.release()) >= 10:
            try:
                import ctypes
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    self.winId().__int__(),
                    20,
                    ctypes.byref(ctypes.c_int(2)),
                    ctypes.sizeof(ctypes.c_int)
                )
            except:
                pass

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.create_menu_bar()
        self.header = self.create_header()
        self.controls = self.create_controls_panel()
        self.content = self.create_main_content()

        layout.addWidget(self.header)
        layout.addWidget(self.controls)
        layout.addWidget(self.content, 1)

        self.status_bar = self.statusBar()
        self.status_label = QLabel()
        self.update_status(translator.tr("loading"))
        self.status_bar.addPermanentWidget(self.status_label)

        self.apply_language_direction()

    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background: transparent;
                color: #0078D4;
                font-weight: bold;
                padding: 8px;
            }
            QMenuBar::item:selected {
                background: rgba(0, 120, 212, 0.2);
                border-radius: 8px;
            }
        """)

        file_menu = menubar.addMenu(translator.tr("settings"))
        file_menu.addAction(translator.tr("export"), self.export_data)
        file_menu.addAction(translator.tr("import"), self.import_data)
        file_menu.addSeparator()
        file_menu.addAction(translator.tr("exit"), self.close)

        view_menu = menubar.addMenu("View")
        # QAction و QKeySequence از QtGui ایمپورت شدند
        fullscreen_action = QAction(translator.tr("fullscreen"), self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        help_menu = menubar.addMenu(translator.tr("about"))
        help_menu.addAction(translator.tr("about"), self.show_about)

    def create_header(self):
        header = QFrame()
        header.setFixedHeight(120)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0078D4, stop:0.5 #00C6FF, stop:1 #0078D4);
                border-bottom: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(15)

        logo = QLabel()
        logo_pixmap = QPixmap("icons/app_icon.png").scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(logo_pixmap)
        logo_layout.addWidget(logo)

        title_layout = QVBoxLayout()
        title = QLabel(translator.tr("title"))
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title_layout.addWidget(title)

        subtitle = QLabel(translator.tr("subtitle"))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 14px;")
        title_layout.addWidget(subtitle)
        logo_layout.addLayout(title_layout)
        logo_layout.addStretch()

        layout.addLayout(logo_layout, 1)

        lang_group = QHBoxLayout()
        lang_group.addWidget(QLabel(translator.tr("language") + ":"))
        self.lang_combo = QComboBox()
        for code, info in LANGUAGES.items():
            self.lang_combo.addItem(info["name"], code)
        self.lang_combo.setCurrentIndex(list(LANGUAGES.keys()).index(translator.current_lang))
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        self.lang_combo.setStyleSheet(self.get_combobox_style())
        lang_group.addWidget(self.lang_combo)
        layout.addLayout(lang_group)

        return header

    def create_controls_panel(self):
        panel = GlassEffect(opacity=0.1)
        panel.setFixedHeight(100)
        
        layout = QGridLayout(panel)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)
        layout.setColumnStretch(5, 1)

        layout.addWidget(QLabel(translator.tr("select_sport") + ":"), 0, 0)
        self.sport_combo = QComboBox()
        for sport, info in SPORT_MAPPING.items():
            self.sport_combo.addItem(translator.tr(sport), info["api"])
        self.sport_combo.currentIndexChanged.connect(self.on_sport_changed)
        self.sport_combo.setStyleSheet(self.get_combobox_style())
        layout.addWidget(self.sport_combo, 0, 1)

        layout.addWidget(QLabel(translator.tr("select_league") + ":"), 0, 2)
        self.league_combo = QComboBox()
        self.league_combo.addItem(translator.tr("all_leagues"), "")
        self.league_combo.setStyleSheet(self.get_combobox_style())
        layout.addWidget(self.league_combo, 0, 3)

        self.refresh_btn = ModernButton(translator.tr("refresh"), "icons/refresh.png")
        self.refresh_btn.clicked.connect(self.manual_refresh)
        layout.addWidget(self.refresh_btn, 0, 4)

        self.auto_update_cb = QCheckBox(translator.tr("auto_update"))
        self.auto_update_cb.setChecked(True)
        self.auto_update_cb.stateChanged.connect(self.toggle_auto_update)
        self.auto_update_cb.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(self.auto_update_cb, 0, 5, Qt.AlignmentFlag.AlignRight)

        return panel

    def create_main_content(self):
        content = QFrame()
        content.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)

        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(translator.tr("search"))
        self.search_edit.textChanged.connect(self.filter_table)
        self.search_edit.setStyleSheet(self.get_lineedit_style())
        search_layout.addWidget(self.search_edit)

        self.filter_btn = IconButton("icons/filter.png", 20)
        search_layout.addWidget(self.filter_btn)

        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            translator.tr("league"), translator.tr("home"), translator.tr("score"),
            translator.tr("away"), translator.tr("status"), translator.tr("time"),
            translator.tr("favorite"), translator.tr("update_time")
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet(self.get_table_style())
        self.table.itemClicked.connect(self.on_table_item_clicked)

        layout.addWidget(self.table, 1)
        return content

    def get_combobox_style(self):
        return """
            QComboBox {
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid #0078D4;
                border-radius: 12px;
                padding: 10px 16px;
                font-weight: bold;
                color: #0078D4;
                min-height: 20px;
            }
            QComboBox::drop-down {
                border: 0px;
                width: 36px;
                border-left: 1px solid #0078D4;
            }
            QComboBox QAbstractItemView {
                background: white;
                selection-background-color: #0078D4;
                selection-color: white;
                border-radius: 8px;
                padding: 4px;
            }
        """

    def get_lineedit_style(self):
        return """
            QLineEdit {
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid #0078D4;
                border-radius: 12px;
                padding: 10px 16px;
                font-size: 14px;
                color: #001F3F;
            }
            QLineEdit:focus {
                border-color: #00C6FF;
            }
        """

    def get_table_style(self):
        return """
            QTableWidget {
                background: rgba(255, 255, 255, 0.95);
                gridline-color: rgba(0, 0, 0, 0.1);
                font-size: 14px;
                color: #001F3F;
                border-radius: 16px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            }
            QTableWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078D4, stop:1 #00C6FF);
                color: white;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078D4, stop:1 #005A9E);
                color: white;
                padding: 14px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }
        """

    def start_worker(self):
        if self.worker:
            self.worker.stop()

        api_sport = self.sport_combo.currentData()
        self.worker = APIWorker(sport=api_sport, league=self.current_league)
        self.worker.data_ready.connect(self.update_table)
        self.worker.error_occurred.connect(self.show_error)
        self.worker.progress.connect(self.update_progress)
        self.worker.start()

    def update_table(self, data):
        self.last_data = data
        self.table.setRowCount(0)
        events = data.get("events", [])
        
        if not events:
            self.show_empty_state()
            return

        for event in events:
            row = self.table.rowCount()
            self.table.insertRow(row)

            league_item = QTableWidgetItem(event.get("strLeague", "N/A"))
            league_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, league_item)

            home = event.get("strHomeTeam", "Team A")
            home_item = QTableWidgetItem(home)
            home_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, home_item)

            score = f"{event.get('intHomeScore', '0')} - {event.get('intAwayScore', '0')}"
            status = event.get("strStatus", "")
            if status == "Live":
                score = f"{score}"
            score_item = QTableWidgetItem(score)
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            score_item.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            if status == "Live":
                score_item.setForeground(QColor("#FF6B6B"))
            self.table.setItem(row, 2, score_item)

            away = event.get("strAwayTeam", "Team B")
            away_item = QTableWidgetItem(away)
            away_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, away_item)

            status_map = {
                "Live": translator.tr("live"),
                "FT": translator.tr("ft"),
                "HT": translator.tr("ht"),
                "Postponed": translator.tr("postponed"),
                "Cancelled": translator.tr("cancelled")
            }
            status_text = status_map.get(status, status)
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, status_item)

            time_str = event.get("strProgress", event.get("strTime", "N/A"))
            time_item = QTableWidgetItem(time_str)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 5, time_item)

            fav_btn = QPushButton()
            event_id = event["idEvent"]
            is_fav = event_id in self.favorites
            fav_btn.setIcon(QIcon("icons/star_filled.png" if is_fav else "icons/star.png"))
            fav_btn.setStyleSheet("border: none; padding: 4px;")
            fav_btn.clicked.connect(lambda checked, eid=event_id: self.toggle_favorite(eid))
            self.table.setCellWidget(row, 6, fav_btn)

            update_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
            update_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 7, update_item)

        self.update_status(f"{len(events)} {translator.tr('update_time').lower()}")

    def show_empty_state(self):
        self.table.setRowCount(1)
        item = QTableWidgetItem(translator.tr("no_data"))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setForeground(QColor("#666666"))
        font = QFont("Segoe UI", 16, QFont.Weight.Medium)
        item.setFont(font)
        self.table.setItem(0, 0, item)
        self.table.setSpan(0, 0, 1, 8)

    def show_error(self, msg):
        self.update_status(translator.tr("network_error"))

    def update_progress(self, value):
        pass

    def change_language(self, index):
        lang_code = self.lang_combo.currentData()
        if translator.set_language(lang_code):
            self.retranslate_ui()
            self.apply_language_direction()
            self.db.set_setting("language", lang_code)
            self.start_worker()

    def retranslate_ui(self):
        self.setWindowTitle(translator.tr("app_name"))
        self.sport_combo.clear()
        for sport in SPORT_MAPPING.keys():
            self.sport_combo.addItem(translator.tr(sport), SPORT_MAPPING[sport]["api"])
        self.table.setHorizontalHeaderLabels([
            translator.tr("league"), translator.tr("home"), translator.tr("score"),
            translator.tr("away"), translator.tr("status"), translator.tr("time"),
            translator.tr("favorite"), translator.tr("update_time")
        ])
        self.refresh_btn.setText(translator.tr("refresh"))
        self.auto_update_cb.setText(translator.tr("auto_update"))
        self.search_edit.setPlaceholderText(translator.tr("search"))

    def apply_language_direction(self):
        direction = translator.get_direction()
        QApplication.instance().setLayoutDirection(direction)
        self.setLayoutDirection(direction)

    def apply_theme(self):
        theme = self.db.get_setting("theme", "system")
        style = ""
        if theme == "light":
            style = self.get_light_theme()
        elif theme == "dark":
            style = self.get_dark_theme()
        elif theme == "red":
            style = self.get_red_theme()
        elif theme == "blue":
            style = self.get_blue_theme()
        else:
            if QApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
                style = self.get_dark_theme()
            else:
                style = self.get_light_theme()
        QApplication.instance().setStyleSheet(style)

    def get_light_theme(self):
        return """
            QWidget { background: #F5F5F5; color: #001F3F; }
            QMainWindow { background: #EEEEEE; }
            QFrame { background: transparent; }
            QPushButton { color: white; }
        """

    def get_dark_theme(self):
        return """
            QWidget { background: #1E1E1E; color: #FFFFFF; }
            QMainWindow { background: #2D2D2D; }
            QTableWidget { background: #2D2D2D; color: #FFFFFF; }
            QLineEdit { background: #3D3D3D; color: #FFFFFF; border: 1px solid #555555; }
        """

    def get_red_theme(self):
        return """
            QWidget { background: #2B0000; color: #FFD1D1; }
            QTableWidget { background: #3F0000; color: #FFFFFF; }
            QHeaderView::section { background: #D40000; }
        """

    def get_blue_theme(self):
        return """
            QWidget { background: #001F3F; color: #A0D8FF; }
            QTableWidget { background: #003366; color: #FFFFFF; }
            QHeaderView::section { background: #0078D4; }
        """

    def on_sport_changed(self):
        self.start_worker()

    def manual_refresh(self):
        self.start_worker()

    def toggle_auto_update(self, state):
        self.auto_update = state == Qt.CheckState.Checked.value

    def toggle_favorite(self, event_id):
        if event_id in self.favorites:
            self.favorites.remove(event_id)
            self.db.remove_favorite(event_id)
        else:
            self.favorites.add(event_id)
        self.update_table(self.last_data)

    def filter_table(self, text):
        for row in range(self.table.rowCount()):
            show = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    show = True
                    break
            self.table.setRowHidden(row, not show)

    def export_data(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Data", "", "JSON Files (*.json)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.last_data, f, ensure_ascii=False, indent=2)

    def import_data(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Data", "", "JSON Files (*.json)")
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.update_table(data)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def show_about(self):
        QMessageBox.about(self, translator.tr("about"), 
                         f"{translator.tr('app_name')} v2.0\n"
                         f"{translator.tr('developer')}: Your Name\n"
                         "© 2025 All rights reserved.")

    def on_table_item_clicked(self, item):
        pass

    def update_status(self, text):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status_label.setText(f"{text} | {current_time}")

    def load_settings(self):
        lang = self.db.get_setting("language", "en")
        translator.set_language(lang)
        self.lang_combo.setCurrentIndex(list(LANGUAGES.keys()).index(lang))

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
        self.db.set_setting("geometry", self.saveGeometry().toHex().data().decode())
        super().closeEvent(event)

# ====================== Application Entry ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI Variable", 10))
    app.setApplicationName(translator.tr("app_name"))
    app.setApplicationVersion("2.0")
    app.setOrganizationName("YourName")

    ensure_icons()

    window = LiveSportsApp()
    window.show()
    
    sys.exit(app.exec())