# Live Sports Hub – Real-Time Scores Dashboard

---

## English

### Overview
**Live Sports Hub** is a **powerful, modern, and fully-featured desktop application** built with **PyQt6** that delivers **real-time sports scores** for **Football, Basketball, Tennis, Volleyball, and Handball** — **instantly and beautifully**.

Powered by **TheSportsDB API**, this app offers **live match updates every 5 seconds**, **multilingual support**, **dynamic theming**, **favorites system**, **smart caching**, **offline mock data**, and **professional UI/UX** — all in a **single, standalone Python script**.

Perfect for **sports fans, analysts, journalists, and developers** who want a **fast, reliable, and stylish** live scoreboard.

---

### Key Features
- **5 Sports Supported**:
  - Football • Basketball • Tennis • Volleyball • Handball
- **Real-Time Updates** (every 5 seconds)
- **Live Match Details**:
  - Score • Status • Time • League • Teams
- **Smart Caching** (60-second cache with SQLite)
- **Offline Fallback** (mock data when API fails)
- **Favorites System** (persist across sessions)
- **4 Languages**:
  - English • فارسی • 中文 • Русский
  - Full **RTL layout** support for Persian
- **5 Stunning Themes**:
  - System • Light • Dark • Red Alert • Ocean Blue
- **Glassmorphism UI** with smooth animations
- **Search & Filter** matches instantly
- **Export/Import** data in JSON
- **Auto-Update Engine** (with progress tracking)
- **Sound Alerts** on goals (optional)
- **Fullscreen Mode** (F11)
- **System Tray Minimization**
- **Robust Error Handling** with retry logic
- **No external assets** – icons generated at runtime

---

### Requirements
- Python 3.8+
- PyQt6
- requests
- sqlite3 (built-in)

---

### Installation
```bash
pip install PyQt6 requests
```

Save the script as `live_sports_hub.py` and run:
```bash
python live_sports_hub.py
```

---

### Usage
1. **Select your sport** from the dropdown
2. Choose a **league** or view all
3. Watch **live scores update every 5 seconds**
4. **Star** matches to add to favorites
5. Use **search bar** to find teams/leagues
6. Toggle **auto-update**, **sound**, or **theme**
7. Press **F11** for fullscreen
8. **Export** current data or **import** backups

> **Pro Tip**: Enable **"Red Alert"** theme during intense matches!

---

### Project Structure
```
live_sports_hub.py      ← Complete standalone app
icons/                  ← Auto-generated at first run
~/.config/LiveSportsHub/sports_hub.db  ← Settings & cache
```

---

### API
Uses **[TheSportsDB](https://www.thesportsdb.com/)** free API:
- `eventsday.php` – Daily live & scheduled matches
- No API key required

---

### Contributing
We welcome contributions!  
Ideas:
- Add **push notifications**
- Support **live commentary**
- Add **team logos**
- Implement **match timeline**
- Add **dark mode auto-sync**
- Export to **CSV/PDF**

Submit a **Pull Request** with clear description.

---

### License
Released under the **MIT License**. Free for personal and commercial use.

---

## فارسی

### نمای کلی
**مرکز نتایج زنده ورزشی** یک برنامه دسکتاپ **مدرن، قدرتمند و کاملاً مجهز** است که با **PyQt6** ساخته شده و **نتایج زنده مسابقات** در رشته‌های **فوتبال، بسکتبال، تنیس، والیبال و هندبال** را — **فوری و زیبا** — نمایش می‌دهد.

با استفاده از **API TheSportsDB**، این برنامه **هر ۵ ثانیه به‌روزرسانی می‌شود**، از **چندزبانه بودن**، **تم‌های پویا**، **سیستم علاقه‌مندی**، **کش هوشمند**، **داده آفلاین** و **رابط کاربری حرفه‌ای** پشتیبانی می‌کند — همه در یک **فایل پایتون مستقل**.

مناسب برای **علاقه‌مندان به ورزش، تحلیلگران، خبرنگاران و توسعه‌دهندگان** که به یک **تابلوی امتیازدهی سریع، قابل اعتماد و شیک** نیاز دارند.

---

### ویژگی‌های کلیدی
- **۵ رشته ورزشی پشتیبانی‌شده**:
  - فوتبال • بسکتبال • تنیس • والیبال • هندبال
- **به‌روزرسانی لحظه‌ای** (هر ۵ ثانیه)
- **جزئیات زنده بازی**:
  - امتیاز • وضعیت • زمان • لیگ • تیم‌ها
- **کش هوشمند** (۶۰ ثانیه با SQLite)
- **داده آفلاین** (در صورت قطعی API)
- **سیستم علاقه‌مندی** (دائمی)
- **۴ زبان**:
  - فارسی • انگلیسی • چینی • روسی
  - پشتیبانی کامل از **چیدمان راست‌به‌چپ**
- **۵ تم خیره‌کننده**:
  - سیستم • روشن • تیره • هشدار قرمز • آبی اقیانوسی
- **رابط کاربری شیشه‌ای** با انیمیشن نرم
- **جستجو و فیلتر** فوری
- **خروجی/ورودی** داده در JSON
- **موتور به‌روزرسانی خودکار**
- **هشدار صوتی** هنگام گل (اختیاری)
- **حالت تمام‌صفحه** (F11)
- **کوچک‌سازی به سینی سیستم**
- **مدیریت خطا قوی** با تلاش مجدد
- **بدون نیاز به فایل خارجی** – آیکون‌ها در لحظه ساخته می‌شوند

---

### پیش‌نیازها
- پایتون ۳.۸ یا بالاتر
- PyQt6
- requests
- sqlite3 (داخلی)

---

### نصب
```bash
pip install PyQt6 requests
```

فایل را با نام `live_sports_hub.py` ذخیره کنید و اجرا کنید:
```bash
python live_sports_hub.py
```

---

### نحوه استفاده
1. **ورزش مورد نظر** را از منوی کشویی انتخاب کنید
2. **لیگ** را انتخاب کنید یا همه را ببینید
3. **نتایج هر ۵ ثانیه به‌روزرسانی می‌شوند**
4. روی **ستاره** کلیک کنید تا به علاقه‌مندی‌ها اضافه شود
5. از **نوار جستجو** برای یافتن تیم/لیگ استفاده کنید
6. **به‌روزرسانی خودکار**، **صدا** یا **تم** را تغییر دهید
7. کلید **F11** برای تمام‌صفحه
8. داده را **خروجی** یا **وارد** کنید

> **نکته حرفه‌ای**: در بازی‌های حساس، تم **«هشدار قرمز»** را فعال کنید!

---

### ساختار پروژه
```
live_sports_hub.py      ← برنامه کامل و مستقل
icons/                  ← به صورت خودکار در اولین اجرا ساخته می‌شود
~/.config/LiveSportsHub/sports_hub.db  ← تنظیمات و کش
```

---

### API
از **[TheSportsDB](https://www.thesportsdb.com/)** رایگان استفاده می‌کند:
- `eventsday.php` – مسابقات زنده و برنامه‌ریزی‌شده روزانه
- بدون نیاز به کلید API

---

### مشارکت
مشارکت شما بسیار ارزشمند است!  
ایده‌ها:
- افزودن **اعلان فوری**
- پشتیبانی از **شرح زنده**
- افزودن **لوگو تیم‌ها**
- پیاده‌سازی **تایم‌لاین بازی**
- همگام‌سازی خودکار **حالت تیره**
- خروجی به **CSV/PDF**

درخواست کشش (Pull Request) با توضیح واضح ارسال کنید.

---

### مجوز
تحت **مجوز MIT** منتشر شده است. آزاد برای استفاده شخصی و تجاری.

---

## 中文

### 项目概览
**实时体育中心** 是一款**功能强大、现代且特性丰富的桌面应用程序**，使用 **PyQt6** 构建，为**足球、篮球、网球、排球和手球**提供**实时比分** — **即时且精美**。

基于 **TheSportsDB API**，该应用**每 5 秒更新一次**，支持**多语言**、**动态主题**、**收藏系统**、**智能缓存**、**离线模拟数据**和**专业 UI/UX** — 全部包含在**单个独立 Python 脚本**中。

非常适合**体育迷、分析师、记者和开发者**，他们需要一个**快速、可靠且时尚**的实时记分牌。

---

### 核心功能
- **支持 5 种运动**：
  - 足球 • 篮球 • 网球 • 排球 • 手球
- **实时更新**（每 5 秒）
- **比赛详情**：
  - 比分 • 状态 • 时间 • 联赛 • 球队
- **智能缓存**（60 秒，SQLite 存储）
- **离线回退**（API 失败时显示模拟数据）
- **收藏系统**（跨会话持久化）
- **4 种语言**：
  - 中文 • 英语 • 波斯语 • 俄语
  - 完整支持**从右到左 (RTL)**
- **5 种惊艳主题**：
  - 系统 • 明亮 • 暗黑 • 红色警报 • 海洋蓝
- **毛玻璃效果** UI，流畅动画
- **即时搜索与筛选**
- **JSON 导入/导出**数据
- **自动更新引擎**（带进度条）
- **进球声音提醒**（可选）
- **全屏模式**（F11）
- **最小化到系统托盘**
- **健壮的错误处理**，支持重试
- **无需外部资源** — 图标运行时生成

---

### 系统要求
- Python 3.8+
- PyQt6
- requests
- sqlite3（内置）

---

### 安装步骤
```bash
pip install PyQt6 requests
```

将脚本保存为 `live_sports_hub.py` 并运行：
```bash
python live_sports_hub.py
```

---

### 使用指南
1. 从下拉菜单**选择运动**
2. 选择**联赛**或查看全部
3. **比分每 5 秒更新**
4. 点击**星星**加入收藏
5. 使用**搜索栏**查找球队/联赛
6. 切换**自动更新**、**声音**或**主题**
7. 按 **F11** 进入全屏
8. **导出**当前数据或**导入**备份

> **专业提示**：在激烈比赛中使用 **“红色警报”** 主题！

---

### 项目结构
```
live_sports_hub.py      ← 完整独立应用
icons/                  ← 首次运行时自动生成
~/.config/LiveSportsHub/sports_hub.db  ← 设置与缓存
```

---

### API
使用免费的 **[TheSportsDB](https://www.thesportsdb.com/)**：
- `eventsday.php` – 当日直播与赛程
- 无需 API 密钥

---

### 贡献代码
我们欢迎贡献！  
建议：
- 添加**推送通知**
- 支持**实时解说**
- 添加**球队徽标**
- 实现**比赛时间线**
- 自动同步**深色模式**
- 导出为 **CSV/PDF**

请提交带有详细说明的 **Pull Request**。

---

### 许可证
基于 **MIT 许可证**发布。个人和商业用途完全免费。