"""
כלי בדיקה ל-External API
============================
אפליקציית שולחן עבודה לבדיקת ה-API של מערכת השליחה.
תומך בהודעות טקסט, הודעות עם קבצים, ושמירת הגדרות.

דרישות התקנה:
    pip install PySide6 requests

הרצה:
    python api_tester.py
"""

import sys
import json
import os
from datetime import datetime

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget, QFileDialog,
        QCheckBox, QSpinBox, QGroupBox, QListWidget, QListWidgetItem,
        QMessageBox, QStatusBar, QSplitter
    )
    from PySide6.QtCore import Qt, QThread, Signal, QSettings
except ImportError:
    print("❌ PySide6 לא מותקן. הרץ: pip install PySide6 requests")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("❌ requests לא מותקן. הרץ: pip install requests")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════
# עיצוב - Dark theme
# ═══════════════════════════════════════════════════════════════════
STYLESHEET = """
QMainWindow, QWidget {
    background-color: #0f172a;
    color: #e2e8f0;
    font-family: "Segoe UI", "Assistant", Arial, sans-serif;
    font-size: 13px;
}

QGroupBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    margin-top: 14px;
    padding-top: 14px;
    font-weight: 600;
    font-size: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    right: 14px;
    padding: 0 8px;
    color: #60a5fa;
    background-color: #0f172a;
}

QLineEdit, QTextEdit, QSpinBox {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 10px;
    color: #f1f5f9;
    selection-background-color: #3b82f6;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
    border: 1px solid #3b82f6;
}

QPushButton {
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #2563eb;
}

QPushButton:pressed {
    background-color: #1d4ed8;
}

QPushButton:disabled {
    background-color: #475569;
    color: #94a3b8;
}

QPushButton#secondary {
    background-color: #475569;
}

QPushButton#secondary:hover {
    background-color: #64748b;
}

QPushButton#danger {
    background-color: #dc2626;
}

QPushButton#danger:hover {
    background-color: #b91c1c;
}

QTabWidget::pane {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    top: -1px;
}

QTabBar::tab {
    background-color: #1e293b;
    color: #94a3b8;
    padding: 10px 22px;
    border: 1px solid #334155;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 500;
    margin-left: 2px;
}

QTabBar::tab:selected {
    background-color: #3b82f6;
    color: white;
    font-weight: 600;
}

QTabBar::tab:hover:!selected {
    background-color: #334155;
    color: #e2e8f0;
}

QListWidget {
    background-color: #0f172a;
    border: 1px dashed #334155;
    border-radius: 6px;
    padding: 6px;
}

QListWidget::item {
    background-color: #1e293b;
    border-radius: 4px;
    padding: 6px 10px;
    margin: 2px 0;
}

QCheckBox {
    spacing: 8px;
    color: #cbd5e1;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #475569;
    background-color: #0f172a;
}

QCheckBox::indicator:checked {
    background-color: #3b82f6;
    border: 1px solid #3b82f6;
}

QLabel {
    color: #cbd5e1;
}

QLabel#title {
    color: #60a5fa;
    font-size: 22px;
    font-weight: 700;
}

QLabel#subtitle {
    color: #94a3b8;
    font-size: 12px;
}

QLabel#hint {
    color: #94a3b8;
    font-size: 11px;
}

QLabel#statusOk {
    color: #4ade80;
    font-weight: 600;
    background-color: rgba(34, 197, 94, 0.15);
    padding: 4px 10px;
    border-radius: 4px;
}

QLabel#statusError {
    color: #f87171;
    font-weight: 600;
    background-color: rgba(239, 68, 68, 0.15);
    padding: 4px 10px;
    border-radius: 4px;
}

QLabel#statusWarn {
    color: #facc15;
    font-weight: 600;
    background-color: rgba(234, 179, 8, 0.15);
    padding: 4px 10px;
    border-radius: 4px;
}

QTextEdit#responseView {
    background-color: #020617;
    border: 1px solid #334155;
    font-family: "Cascadia Code", "Consolas", "Menlo", monospace;
    font-size: 12px;
}

QStatusBar {
    background-color: #1e293b;
    color: #94a3b8;
    border-top: 1px solid #334155;
}

QSplitter::handle {
    background-color: #334155;
}

QScrollBar:vertical {
    background-color: #1e293b;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #475569;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #64748b;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
"""


# ═══════════════════════════════════════════════════════════════════
# Thread לביצוע בקשה ברקע (כדי שה-UI לא יתקע)
# ═══════════════════════════════════════════════════════════════════
class RequestWorker(QThread):
    finished_signal = Signal(dict)

    def __init__(self, method, url, headers=None, json_data=None, files=None, form_data=None):
        super().__init__()
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.json_data = json_data
        self.files = files
        self.form_data = form_data

    def run(self):
        start = datetime.now()
        result = {"success": False, "duration_ms": 0}

        try:
            if self.files:
                # multipart/form-data
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    data=self.form_data,
                    files=self.files,
                    timeout=60
                )
            elif self.json_data is not None:
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    json=self.json_data,
                    timeout=30
                )
            else:
                response = requests.request(
                    self.method, self.url, headers=self.headers, timeout=30
                )

            duration = (datetime.now() - start).total_seconds() * 1000
            result.update({
                "success": True,
                "status_code": response.status_code,
                "status_text": response.reason,
                "body": response.text,
                "duration_ms": int(duration),
            })
        except requests.exceptions.Timeout:
            result["error"] = "השרת לא הגיב בזמן (timeout)"
        except requests.exceptions.ConnectionError as e:
            result["error"] = f"שגיאת חיבור: לא ניתן להגיע לשרת\n{e}"
        except Exception as e:
            result["error"] = f"שגיאה לא צפויה: {e}"
        finally:
            # סגירת קבצים אם יש
            if self.files:
                for _, file_tuple in self.files:
                    try:
                        file_tuple[1].close()
                    except Exception:
                        pass

        self.finished_signal.emit(result)


# ═══════════════════════════════════════════════════════════════════
# החלון הראשי
# ═══════════════════════════════════════════════════════════════════
class ApiTesterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.worker = None
        self.settings = QSettings("ApiTester", "ExternalApiTester")

        self.setWindowTitle("🧪 כלי בדיקה - External API")
        self.setMinimumSize(1000, 800)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.setup_ui()
        self.load_settings()

    # ───────────────────────────────────────────────────────────────
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # כותרת
        title = QLabel("🧪 כלי בדיקה ל-External API")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("בדיקה מקיפה של שליחת הודעות טקסט וקבצים")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)

        # חלוקה: למעלה הגדרות+טאבים, למטה התגובה
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self._build_top_section())
        splitter.addWidget(self._build_response_section())
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        main_layout.addWidget(splitter)

        # סרגל סטטוס
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("מוכן לשליחת בקשות")

    # ───────────────────────────────────────────────────────────────
    def _build_top_section(self):
        top = QWidget()
        layout = QVBoxLayout(top)
        layout.setContentsMargins(0, 0, 0, 0)

        # הגדרות חיבור
        conn_group = QGroupBox("⚙️ הגדרות חיבור")
        conn_layout = QVBoxLayout(conn_group)

        # Base URL
        url_row = QHBoxLayout()
        url_label = QLabel("Base URL:")
        url_label.setMinimumWidth(90)
        self.base_url_input = QLineEdit()
        self.base_url_input.setPlaceholderText("https://your-domain.com")
        self.base_url_input.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        url_row.addWidget(url_label)
        url_row.addWidget(self.base_url_input)
        conn_layout.addLayout(url_row)

        # API Key
        key_row = QHBoxLayout()
        key_label = QLabel("API Key:")
        key_label.setMinimumWidth(90)
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("your-api-key-here")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.show_key_cb = QCheckBox("הצג")
        self.show_key_cb.toggled.connect(
            lambda checked: self.api_key_input.setEchoMode(
                QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
            )
        )
        key_row.addWidget(key_label)
        key_row.addWidget(self.api_key_input)
        key_row.addWidget(self.show_key_cb)
        conn_layout.addLayout(key_row)

        hint = QLabel("💡 הגדרות אלו נשמרות אוטומטית בין הפעלות")
        hint.setObjectName("hint")
        conn_layout.addWidget(hint)

        layout.addWidget(conn_group)

        # טאבים
        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_text_tab(), "💬 הודעת טקסט")
        self.tabs.addTab(self._build_files_tab(), "📎 הודעה עם קבצים")
        layout.addWidget(self.tabs)

        return top

    # ───────────────────────────────────────────────────────────────
    def _build_text_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        endpoint = QLabel("<b>POST</b> /api/external/post")
        endpoint.setStyleSheet("color: #60a5fa; padding: 4px 0;")
        layout.addWidget(endpoint)

        # Author
        layout.addWidget(QLabel("שם המחבר:"))
        self.text_author = QLineEdit("Test Bot")
        layout.addWidget(self.text_author)

        # Content
        layout.addWidget(QLabel("תוכן ההודעה:"))
        self.text_content = QTextEdit()
        self.text_content.setPlainText("שלום! זוהי הודעת בדיקה מכלי ה-API 🧪")
        self.text_content.setMaximumHeight(120)
        layout.addWidget(self.text_content)

        # replyTo + isThread
        row = QHBoxLayout()
        row.addWidget(QLabel("replyTo:"))
        self.text_reply_to = QSpinBox()
        self.text_reply_to.setRange(0, 999999999)
        self.text_reply_to.setMaximumWidth(140)
        row.addWidget(self.text_reply_to)
        self.text_is_thread = QCheckBox("isThread (שלח כ-thread reply)")
        row.addWidget(self.text_is_thread)
        row.addStretch()
        layout.addLayout(row)

        # Timestamp option
        self.text_use_timestamp = QCheckBox(
            "שלח timestamp מותאם (אחרת השרת יקבע אוטומטית)"
        )
        layout.addWidget(self.text_use_timestamp)

        # Send button
        send_row = QHBoxLayout()
        send_row.addStretch()
        self.send_text_btn = QPushButton("🚀 שלח הודעת טקסט")
        self.send_text_btn.setMinimumHeight(42)
        self.send_text_btn.clicked.connect(self.send_text_message)
        send_row.addWidget(self.send_text_btn)
        layout.addLayout(send_row)

        layout.addStretch()
        return widget

    # ───────────────────────────────────────────────────────────────
    def _build_files_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        endpoint = QLabel("<b>POST</b> /api/external/post-with-files")
        endpoint.setStyleSheet("color: #60a5fa; padding: 4px 0;")
        layout.addWidget(endpoint)

        # Author
        layout.addWidget(QLabel("שם המחבר:"))
        self.files_author = QLineEdit("Test Bot")
        layout.addWidget(self.files_author)

        # Content
        layout.addWidget(QLabel("תוכן ההודעה:"))
        self.files_content = QTextEdit()
        self.files_content.setPlainText("בדיקת שליחת קבצים 📎")
        self.files_content.setMaximumHeight(80)
        layout.addWidget(self.files_content)

        # File picker
        file_row = QHBoxLayout()
        self.pick_files_btn = QPushButton("📁 בחר קבצים...")
        self.pick_files_btn.setObjectName("secondary")
        self.pick_files_btn.clicked.connect(self.pick_files)
        self.clear_files_btn = QPushButton("🗑️ נקה")
        self.clear_files_btn.setObjectName("secondary")
        self.clear_files_btn.clicked.connect(self.clear_files)
        file_row.addWidget(self.pick_files_btn)
        file_row.addWidget(self.clear_files_btn)
        file_row.addStretch()
        layout.addLayout(file_row)

        hint = QLabel("מקסימום 5 קבצים · עד 5MB לקובץ")
        hint.setObjectName("hint")
        layout.addWidget(hint)

        # File list
        self.files_list = QListWidget()
        self.files_list.setMaximumHeight(140)
        layout.addWidget(self.files_list)

        # replyTo + isThread
        row = QHBoxLayout()
        row.addWidget(QLabel("replyTo:"))
        self.files_reply_to = QSpinBox()
        self.files_reply_to.setRange(0, 999999999)
        self.files_reply_to.setMaximumWidth(140)
        row.addWidget(self.files_reply_to)
        self.files_is_thread = QCheckBox("isThread")
        row.addWidget(self.files_is_thread)
        row.addStretch()
        layout.addLayout(row)

        # Send button
        send_row = QHBoxLayout()
        send_row.addStretch()
        self.send_files_btn = QPushButton("🚀 שלח הודעה עם קבצים")
        self.send_files_btn.setMinimumHeight(42)
        self.send_files_btn.clicked.connect(self.send_files_message)
        send_row.addWidget(self.send_files_btn)
        layout.addLayout(send_row)

        layout.addStretch()
        return widget

    # ───────────────────────────────────────────────────────────────
    def _build_response_section(self):
        group = QGroupBox("📬 תגובת השרת")
        layout = QVBoxLayout(group)

        # Header row
        header_row = QHBoxLayout()
        self.status_label = QLabel("—")
        self.status_label.setMinimumWidth(120)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.meta_label = QLabel("")
        self.meta_label.setObjectName("hint")

        copy_btn = QPushButton("📋 העתק תגובה")
        copy_btn.setObjectName("secondary")
        copy_btn.clicked.connect(self.copy_response)

        clear_btn = QPushButton("🗑️ נקה")
        clear_btn.setObjectName("secondary")
        clear_btn.clicked.connect(self.clear_response)

        header_row.addWidget(self.status_label)
        header_row.addWidget(self.meta_label)
        header_row.addStretch()
        header_row.addWidget(copy_btn)
        header_row.addWidget(clear_btn)
        layout.addLayout(header_row)

        # Response body
        self.response_view = QTextEdit()
        self.response_view.setObjectName("responseView")
        self.response_view.setReadOnly(True)
        self.response_view.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.response_view.setPlaceholderText("תגובת השרת תופיע כאן לאחר שליחת בקשה...")
        layout.addWidget(self.response_view)

        return group

    # ═══════════════════════════════════════════════════════════════
    # לוגיקה
    # ═══════════════════════════════════════════════════════════════
    def validate_config(self):
        if not self.base_url_input.text().strip():
            QMessageBox.warning(self, "חסרים פרטים", "יש להזין Base URL")
            return False
        if not self.api_key_input.text().strip():
            QMessageBox.warning(self, "חסרים פרטים", "יש להזין API Key")
            return False
        return True

    def build_url(self, path):
        base = self.base_url_input.text().strip().rstrip("/")
        return base + path

    # ───────────────────────────────────────────────────────────────
    def send_text_message(self):
        if not self.validate_config():
            return

        payload = {
            "text": self.text_content.toPlainText(),
            "author": self.text_author.text(),
            "replyTo": self.text_reply_to.value(),
            "isThread": self.text_is_thread.isChecked(),
        }
        if self.text_use_timestamp.isChecked():
            payload["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        headers = {
            "X-API-Key": self.api_key_input.text().strip(),
            "Content-Type": "application/json",
        }

        self._show_sent_preview(payload, "application/json")
        self._start_request(
            method="POST",
            url=self.build_url("/api/external/post"),
            headers=headers,
            json_data=payload,
            sent_preview=payload,
        )

    # ───────────────────────────────────────────────────────────────
    def send_files_message(self):
        if not self.validate_config():
            return
        if not self.selected_files:
            QMessageBox.warning(self, "חסרים קבצים", "יש לבחור לפחות קובץ אחד")
            return

        # בדיקת גודל קבצים
        oversized = [
            f for f in self.selected_files if os.path.getsize(f) > 5 * 1024 * 1024
        ]
        if oversized:
            names = "\n".join(f"• {os.path.basename(f)}" for f in oversized)
            reply = QMessageBox.question(
                self,
                "קבצים גדולים מ-5MB",
                f"הקבצים הבאים גדולים מ-5MB ועלולים להידחות:\n\n{names}\n\nהאם להמשיך בכל זאת?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        message_data = {
            "text": self.files_content.toPlainText(),
            "author": self.files_author.text(),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "replyTo": self.files_reply_to.value(),
            "isThread": self.files_is_thread.isChecked(),
        }

        headers = {"X-API-Key": self.api_key_input.text().strip()}

        form_data = {"message": json.dumps(message_data, ensure_ascii=False)}
        files = []
        for path in self.selected_files:
            files.append(
                ("files", (os.path.basename(path), open(path, "rb")))
            )

        preview = {
            "message": message_data,
            "files": [os.path.basename(f) for f in self.selected_files],
        }
        self._show_sent_preview(preview, "multipart/form-data")
        self._start_request(
            method="POST",
            url=self.build_url("/api/external/post-with-files"),
            headers=headers,
            form_data=form_data,
            files=files,
            sent_preview=preview,
        )

    # ───────────────────────────────────────────────────────────────
    def _start_request(self, method, url, headers, json_data=None,
                       form_data=None, files=None, sent_preview=None):
        self._set_buttons_enabled(False)
        self.status_label.setText("⏳ שולח...")
        self.status_label.setObjectName("statusWarn")
        self.status_label.setStyleSheet("")  # refresh
        self.status_label.style().polish(self.status_label)
        self.status_bar.showMessage(f"שולח בקשה ל-{url}...")

        self.worker = RequestWorker(
            method=method,
            url=url,
            headers=headers,
            json_data=json_data,
            form_data=form_data,
            files=files,
        )
        self._sent_preview = sent_preview
        self.worker.finished_signal.connect(self._on_request_done)
        self.worker.start()

    # ───────────────────────────────────────────────────────────────
    def _on_request_done(self, result):
        self._set_buttons_enabled(True)

        if not result["success"]:
            self.status_label.setText("❌ שגיאה")
            self.status_label.setObjectName("statusError")
            self.status_label.style().polish(self.status_label)
            self.meta_label.setText("")
            self.response_view.setPlainText(
                f"❌ שגיאת רשת\n\n{result['error']}\n\n"
                "בדוק:\n"
                "• שה-Base URL נכון\n"
                "• שהשרת פעיל ונגיש\n"
                "• חיבור האינטרנט שלך\n"
                "• חומת אש / VPN"
            )
            self.status_bar.showMessage("הבקשה נכשלה")
            return

        status = result["status_code"]
        # סיווג סטטוס
        if 200 <= status < 300:
            self.status_label.setText(f"✓ {status} {result['status_text']}")
            self.status_label.setObjectName("statusOk")
        elif 400 <= status < 500:
            self.status_label.setText(f"⚠ {status} {result['status_text']}")
            self.status_label.setObjectName("statusWarn")
        else:
            self.status_label.setText(f"✗ {status} {result['status_text']}")
            self.status_label.setObjectName("statusError")
        self.status_label.style().polish(self.status_label)

        self.meta_label.setText(
            f"⏱ {result['duration_ms']} ms · {datetime.now().strftime('%H:%M:%S')}"
        )

        # עיצוב התגובה
        body = result["body"]
        try:
            parsed = json.loads(body)
            formatted_body = json.dumps(parsed, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            formatted_body = body

        sent_str = json.dumps(self._sent_preview, indent=2, ensure_ascii=False)

        output = (
            f"// ═══ נשלח ═══\n"
            f"{sent_str}\n\n"
            f"// ═══ תגובה ({status}) ═══\n"
            f"{formatted_body}"
        )
        self.response_view.setPlainText(output)
        self.status_bar.showMessage(
            f"הושלם: {status} {result['status_text']} ({result['duration_ms']}ms)"
        )

    # ───────────────────────────────────────────────────────────────
    def _show_sent_preview(self, data, content_type):
        preview_str = json.dumps(data, indent=2, ensure_ascii=False)
        self.response_view.setPlainText(
            f"// ═══ מכין בקשה ({content_type}) ═══\n{preview_str}\n\n⏳ ממתין לתגובת השרת..."
        )

    # ───────────────────────────────────────────────────────────────
    def _set_buttons_enabled(self, enabled):
        self.send_text_btn.setEnabled(enabled)
        self.send_files_btn.setEnabled(enabled)

    # ───────────────────────────────────────────────────────────────
    def pick_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "בחר קבצים לשליחה", "", "כל הקבצים (*.*)"
        )
        if not files:
            return

        total = len(self.selected_files) + len(files)
        if total > 5:
            QMessageBox.warning(
                self,
                "יותר מדי קבצים",
                f"ניתן לשלוח עד 5 קבצים בלבד. נבחרו {total} קבצים.",
            )
            return

        self.selected_files.extend(files)
        self._refresh_file_list()

    # ───────────────────────────────────────────────────────────────
    def clear_files(self):
        self.selected_files = []
        self._refresh_file_list()

    # ───────────────────────────────────────────────────────────────
    def _refresh_file_list(self):
        self.files_list.clear()
        for i, path in enumerate(self.selected_files, 1):
            try:
                size = os.path.getsize(path)
                size_mb = size / (1024 * 1024)
                warn = "  ⚠️ גדול מ-5MB" if size > 5 * 1024 * 1024 else ""
                text = f"{i}. {os.path.basename(path)}  ·  {size_mb:.2f} MB{warn}"
            except OSError:
                text = f"{i}. {os.path.basename(path)}  ·  (שגיאה בקריאת הקובץ)"
            item = QListWidgetItem(text)
            item.setToolTip(path)
            self.files_list.addItem(item)

    # ───────────────────────────────────────────────────────────────
    def copy_response(self):
        text = self.response_view.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.status_bar.showMessage("הועתק ללוח", 2000)

    def clear_response(self):
        self.response_view.clear()
        self.status_label.setText("—")
        self.status_label.setObjectName("")
        self.status_label.style().polish(self.status_label)
        self.meta_label.setText("")

    # ───────────────────────────────────────────────────────────────
    def load_settings(self):
        self.base_url_input.setText(self.settings.value("base_url", ""))
        self.api_key_input.setText(self.settings.value("api_key", ""))

    def save_settings(self):
        self.settings.setValue("base_url", self.base_url_input.text())
        self.settings.setValue("api_key", self.api_key_input.text())

    def closeEvent(self, event):
        self.save_settings()
        event.accept()


# ═══════════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    window = ApiTesterWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
