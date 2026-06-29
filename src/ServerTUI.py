# -*- coding: utf-8 -*-
"""
命令行聊天服务器 - TUI 版本
支持12种完整语言，修复CJK对齐问题
"""
import socket
import threading
import json
import os
import sys
import time
import shutil
import unicodedata
from datetime import datetime

def vl(text):
    """计算文本显示宽度（CJK字符占2格，英文数字占1格）"""
    width = 0
    for c in text:
        if unicodedata.east_asian_width(c) in ('F', 'W'):
            width += 2
        else:
            width += 1
    return width

def pad_text(text, target_width):
    """将文本填充到指定显示宽度"""
    current_width = vl(text)
    if current_width >= target_width:
        return text
    return text + ' ' * (target_width - current_width)

def clr(wait: int = 0):
    """清屏"""
    time.sleep(wait)
    os.system('cls' if os.name == 'nt' else 'clear')

# ==================== 完整语言包（12种语言） ====================
TRANSLATIONS = {
    "中文": {
        "title": "聊天室服务器 TUI",
        "startup": "正在启动服务器...",
        "enter_port": "请输入监听端口",
        "select_ip": "请选择监听IP地址",
        "all_interfaces": "所有接口 (0.0.0.0)",
        "detected_ips": "检测到的本地IP地址",
        "custom_ip": "自定义输入",
        "enter_custom_ip": "请输入自定义IP地址",
        "port_range": "端口范围 1024-65535",
        "port_must_number": "端口必须是数字",
        "server_started": "服务器已启动",
        "listening_on": "监听地址",
        "online_users": "在线用户",
        "server_log": "日志",
        "commands": "/kick <用户> | /broadcast <消息> | /quit | /help",
        "waiting_connections": "等待连接...",
        "new_connection": "新连接",
        "from_address": "来自",
        "client_disconnected": "客户端断开",
        "user_joined": "加入了聊天室",
        "user_left": "离开了聊天室",
        "duplicate_username": "用户名已被使用",
        "duplicate_rejected": "用户名重复",
        "public_message": "[公开]",
        "private_message": "[私聊]",
        "file_transfer": "[文件]",
        "file_broadcast": "[文件广播]",
        "broadcast_message": "[广播]",
        "unknown_command": "未知命令",
        "usage_kick": "用法: /kick <用户名>",
        "usage_broadcast": "用法: /broadcast <消息>",
        "user_not_found": "用户不存在",
        "user_kicked": "已被踢出",
        "kick_reason": "被管理员踢出",
        "server_stopping": "正在停止...",
        "server_stopped": "服务器已停止",
        "none": "无",
        "error": "错误",
        "system": "系统",
        "input_prompt": "服务器> ",
        "language_select": "选择语言",
        "available_languages": "可用语言",
        "current_language": "当前语言",
        "invalid_choice": "无效选择",
        "invalid_ip": "无效IP",
    },
    "繁體中文": {
        "title": "聊天室伺服器 TUI",
        "startup": "正在啟動伺服器...",
        "enter_port": "請輸入監聽連接埠",
        "select_ip": "請選擇監聽IP位址",
        "all_interfaces": "所有介面 (0.0.0.0)",
        "detected_ips": "偵測到的本地IP位址",
        "custom_ip": "自訂輸入",
        "enter_custom_ip": "請輸入自訂IP位址",
        "port_range": "連接埠範圍 1024-65535",
        "port_must_number": "連接埠必須是數字",
        "server_started": "伺服器已啟動",
        "listening_on": "監聽位址",
        "online_users": "線上使用者",
        "server_log": "記錄",
        "commands": "/kick <使用者> | /broadcast <訊息> | /quit | /help",
        "waiting_connections": "等待連線...",
        "new_connection": "新連線",
        "from_address": "來自",
        "client_disconnected": "客戶端斷線",
        "user_joined": "加入了聊天室",
        "user_left": "離開了聊天室",
        "duplicate_username": "使用者名稱已被使用",
        "duplicate_rejected": "使用者名稱重複",
        "public_message": "[公開]",
        "private_message": "[私聊]",
        "file_transfer": "[檔案]",
        "file_broadcast": "[檔案廣播]",
        "broadcast_message": "[廣播]",
        "unknown_command": "未知命令",
        "usage_kick": "用法: /kick <使用者>",
        "usage_broadcast": "用法: /broadcast <訊息>",
        "user_not_found": "使用者不存在",
        "user_kicked": "已被踢出",
        "kick_reason": "被管理員踢出",
        "server_stopping": "正在停止...",
        "server_stopped": "伺服器已停止",
        "none": "無",
        "error": "錯誤",
        "system": "系統",
        "input_prompt": "伺服器> ",
        "language_select": "選擇語言",
        "available_languages": "可用語言",
        "current_language": "目前語言",
        "invalid_choice": "無效選擇",
        "invalid_ip": "無效IP",
    },
    "日本語": {
        "title": "チャットサーバー TUI",
        "startup": "起動中...",
        "enter_port": "ポートを入力",
        "select_ip": "待受IPを選択",
        "all_interfaces": "全インターフェース (0.0.0.0)",
        "detected_ips": "検出されたローカルIP",
        "custom_ip": "カスタム入力",
        "enter_custom_ip": "カスタムIPを入力",
        "port_range": "ポート範囲 1024-65535",
        "port_must_number": "ポートは数字で",
        "server_started": "起動完了",
        "listening_on": "待受",
        "online_users": "オンライン",
        "server_log": "ログ",
        "commands": "/kick <ユーザー> | /broadcast <メッセージ> | /quit | /help",
        "waiting_connections": "待機中...",
        "new_connection": "新規接続",
        "from_address": "接続元",
        "client_disconnected": "切断",
        "user_joined": "が参加",
        "user_left": "が退出",
        "duplicate_username": "ユーザー名重複",
        "duplicate_rejected": "重複拒否",
        "public_message": "[公開]",
        "private_message": "[非公開]",
        "file_transfer": "[ファイル]",
        "file_broadcast": "[一斉送信]",
        "broadcast_message": "[通知]",
        "unknown_command": "不明なコマンド",
        "usage_kick": "使用法: /kick <ユーザー名>",
        "usage_broadcast": "使用法: /broadcast <メッセージ>",
        "user_not_found": "ユーザーなし",
        "user_kicked": "をキック",
        "kick_reason": "管理者キック",
        "server_stopping": "停止中...",
        "server_stopped": "停止完了",
        "none": "なし",
        "error": "エラー",
        "system": "システム",
        "input_prompt": "サーバー> ",
        "language_select": "言語選択",
        "available_languages": "利用可能言語",
        "current_language": "現在の言語",
        "invalid_choice": "無効な選択",
        "invalid_ip": "無効なIP",
    },
    "한국어": {
        "title": "채팅 서버 TUI",
        "startup": "시작 중...",
        "enter_port": "포트 입력",
        "select_ip": "수신 IP 선택",
        "all_interfaces": "모든 인터페이스 (0.0.0.0)",
        "detected_ips": "감지된 로컬 IP",
        "custom_ip": "직접 입력",
        "enter_custom_ip": "IP 직접 입력",
        "port_range": "포트 범위 1024-65535",
        "port_must_number": "포트는 숫자",
        "server_started": "서버 시작됨",
        "listening_on": "수신 주소",
        "online_users": "온라인",
        "server_log": "로그",
        "commands": "/kick <사용자> | /broadcast <메시지> | /quit | /help",
        "waiting_connections": "대기 중...",
        "new_connection": "새 연결",
        "from_address": "연결처",
        "client_disconnected": "연결 해제",
        "user_joined": "참여",
        "user_left": "퇴장",
        "duplicate_username": "중복 이름",
        "duplicate_rejected": "중복 거부",
        "public_message": "[공개]",
        "private_message": "[비공개]",
        "file_transfer": "[파일]",
        "file_broadcast": "[파일 방송]",
        "broadcast_message": "[공지]",
        "unknown_command": "알 수 없는 명령",
        "usage_kick": "사용법: /kick <사용자>",
        "usage_broadcast": "사용법: /broadcast <메시지>",
        "user_not_found": "사용자 없음",
        "user_kicked": "추방됨",
        "kick_reason": "관리자 추방",
        "server_stopping": "종료 중...",
        "server_stopped": "서버 종료됨",
        "none": "없음",
        "error": "오류",
        "system": "시스템",
        "input_prompt": "서버> ",
        "language_select": "언어 선택",
        "available_languages": "사용 가능 언어",
        "current_language": "현재 언어",
        "invalid_choice": "잘못된 선택",
        "invalid_ip": "유효하지 않은 IP",
    },
    "Deutsch": {
        "title": "Chat-Server TUI",
        "startup": "Starte Server...",
        "enter_port": "Port eingeben",
        "select_ip": "IP zum Abhören wählen",
        "all_interfaces": "Alle (0.0.0.0)",
        "detected_ips": "Erkannte lokale IPs",
        "custom_ip": "Benutzerdefiniert",
        "enter_custom_ip": "IP manuell eingeben",
        "port_range": "Port 1024-65535",
        "port_must_number": "Port muss Zahl sein",
        "server_started": "Server gestartet",
        "listening_on": "Hört auf",
        "online_users": "Online",
        "server_log": "Log",
        "commands": "/kick <User> | /broadcast <Msg> | /quit | /help",
        "waiting_connections": "Warte...",
        "new_connection": "Neue Verbindung",
        "from_address": "von",
        "client_disconnected": "Getrennt",
        "user_joined": "ist beigetreten",
        "user_left": "hat Chat verlassen",
        "duplicate_username": "Name vergeben",
        "duplicate_rejected": "Doppelt, abgelehnt",
        "public_message": "[Öffentlich]",
        "private_message": "[Privat]",
        "file_transfer": "[Datei]",
        "file_broadcast": "[Datei-Broadcast]",
        "broadcast_message": "[Meldung]",
        "unknown_command": "Unbekannt",
        "usage_kick": "Nutzung: /kick <Name>",
        "usage_broadcast": "Nutzung: /broadcast <Msg>",
        "user_not_found": "Nicht gefunden",
        "user_kicked": "gekickt",
        "kick_reason": "Vom Admin gekickt",
        "server_stopping": "Beende...",
        "server_stopped": "Server gestoppt",
        "none": "Keine",
        "error": "Fehler",
        "system": "System",
        "input_prompt": "Server> ",
        "language_select": "Sprache wählen",
        "available_languages": "Verfügbar",
        "current_language": "Aktuell",
        "invalid_choice": "Ungültig",
        "invalid_ip": "Ungültige IP",
    },
    "Italiano": {
        "title": "Server Chat TUI",
        "startup": "Avvio server...",
        "enter_port": "Inserisci porta",
        "select_ip": "Seleziona IP ascolto",
        "all_interfaces": "Tutte (0.0.0.0)",
        "detected_ips": "IP locali rilevati",
        "custom_ip": "Personalizzato",
        "enter_custom_ip": "Inserisci IP manuale",
        "port_range": "Porte 1024-65535",
        "port_must_number": "La porta deve essere un numero",
        "server_started": "Server avviato",
        "listening_on": "In ascolto su",
        "online_users": "Online",
        "server_log": "Log",
        "commands": "/kick <utente> | /broadcast <msg> | /quit | /help",
        "waiting_connections": "In attesa...",
        "new_connection": "Nuova connessione",
        "from_address": "da",
        "client_disconnected": "Disconnesso",
        "user_joined": "è entrato",
        "user_left": "ha lasciato",
        "duplicate_username": "Nome già in uso",
        "duplicate_rejected": "Duplicato, rifiutato",
        "public_message": "[Pubblico]",
        "private_message": "[Privato]",
        "file_transfer": "[File]",
        "file_broadcast": "[File broadcast]",
        "broadcast_message": "[Messaggio]",
        "unknown_command": "Sconosciuto",
        "usage_kick": "Uso: /kick <nome>",
        "usage_broadcast": "Uso: /broadcast <msg>",
        "user_not_found": "Non trovato",
        "user_kicked": "espulso",
        "kick_reason": "Espulso dall'admin",
        "server_stopping": "Arresto...",
        "server_stopped": "Server arrestato",
        "none": "Nessuno",
        "error": "Errore",
        "system": "Sistema",
        "input_prompt": "Server> ",
        "language_select": "Lingua",
        "available_languages": "Disponibili",
        "current_language": "Corrente",
        "invalid_choice": "Non valido",
        "invalid_ip": "IP non valido",
    },
    "English": {
        "title": "Chat Server TUI",
        "startup": "Starting server...",
        "enter_port": "Enter port",
        "select_ip": "Select IP to listen on",
        "all_interfaces": "All interfaces (0.0.0.0)",
        "detected_ips": "Detected local IPs",
        "custom_ip": "Custom input",
        "enter_custom_ip": "Enter custom IP",
        "port_range": "Port range 1024-65535",
        "port_must_number": "Port must be a number",
        "server_started": "Server started",
        "listening_on": "Listening on",
        "online_users": "Online",
        "server_log": "Log",
        "commands": "/kick <user> | /broadcast <msg> | /quit | /help",
        "waiting_connections": "Waiting...",
        "new_connection": "New connection",
        "from_address": "from",
        "client_disconnected": "Disconnected",
        "user_joined": "joined",
        "user_left": "left",
        "duplicate_username": "Name in use",
        "duplicate_rejected": "Duplicate, rejected",
        "public_message": "[Public]",
        "private_message": "[Private]",
        "file_transfer": "[File]",
        "file_broadcast": "[File Broadcast]",
        "broadcast_message": "[Broadcast]",
        "unknown_command": "Unknown",
        "usage_kick": "Usage: /kick <name>",
        "usage_broadcast": "Usage: /broadcast <msg>",
        "user_not_found": "Not found",
        "user_kicked": "kicked",
        "kick_reason": "Kicked by admin",
        "server_stopping": "Stopping...",
        "server_stopped": "Server stopped",
        "none": "None",
        "error": "Error",
        "system": "System",
        "input_prompt": "Server> ",
        "language_select": "Select Language",
        "available_languages": "Available",
        "current_language": "Current",
        "invalid_choice": "Invalid",
        "invalid_ip": "Invalid IP",
    },
    "Français": {
        "title": "Serveur Chat TUI",
        "startup": "Démarrage...",
        "enter_port": "Entrez le port",
        "select_ip": "Choisissez l'IP",
        "all_interfaces": "Toutes (0.0.0.0)",
        "detected_ips": "IP locales détectées",
        "custom_ip": "Personnalisé",
        "enter_custom_ip": "Entrez une IP",
        "port_range": "Ports 1024-65535",
        "port_must_number": "Le port doit être un nombre",
        "server_started": "Serveur démarré",
        "listening_on": "Écoute sur",
        "online_users": "En ligne",
        "server_log": "Journal",
        "commands": "/kick <user> | /broadcast <msg> | /quit | /help",
        "waiting_connections": "En attente...",
        "new_connection": "Nouvelle connexion",
        "from_address": "de",
        "client_disconnected": "Déconnecté",
        "user_joined": "a rejoint",
        "user_left": "a quitté",
        "duplicate_username": "Nom déjà utilisé",
        "duplicate_rejected": "Doublon refusé",
        "public_message": "[Public]",
        "private_message": "[Privé]",
        "file_transfer": "[Fichier]",
        "file_broadcast": "[Diffusion]",
        "broadcast_message": "[Message]",
        "unknown_command": "Inconnu",
        "usage_kick": "Usage: /kick <nom>",
        "usage_broadcast": "Usage: /broadcast <msg>",
        "user_not_found": "Introuvable",
        "user_kicked": "expulsé",
        "kick_reason": "Expulsé par admin",
        "server_stopping": "Arrêt...",
        "server_stopped": "Serveur arrêté",
        "none": "Aucun",
        "error": "Erreur",
        "system": "Système",
        "input_prompt": "Serveur> ",
        "language_select": "Langue",
        "available_languages": "Disponibles",
        "current_language": "Actuelle",
        "invalid_choice": "Invalide",
        "invalid_ip": "IP invalide",
    },
    "Español": {
        "title": "Servidor Chat TUI",
        "startup": "Iniciando...",
        "enter_port": "Ingrese puerto",
        "select_ip": "Seleccione IP",
        "all_interfaces": "Todas (0.0.0.0)",
        "detected_ips": "IPs detectadas",
        "custom_ip": "Personalizado",
        "enter_custom_ip": "Ingrese IP",
        "port_range": "Puertos 1024-65535",
        "port_must_number": "El puerto debe ser número",
        "server_started": "Servidor iniciado",
        "listening_on": "Escuchando en",
        "online_users": "En línea",
        "server_log": "Registro",
        "commands": "/kick <user> | /broadcast <msg> | /quit | /help",
        "waiting_connections": "Esperando...",
        "new_connection": "Nueva conexión",
        "from_address": "desde",
        "client_disconnected": "Desconectado",
        "user_joined": "se unió",
        "user_left": "salió",
        "duplicate_username": "Nombre en uso",
        "duplicate_rejected": "Duplicado, rechazado",
        "public_message": "[Público]",
        "private_message": "[Privado]",
        "file_transfer": "[Archivo]",
        "file_broadcast": "[Difusión]",
        "broadcast_message": "[Mensaje]",
        "unknown_command": "Desconocido",
        "usage_kick": "Uso: /kick <nombre>",
        "usage_broadcast": "Uso: /broadcast <msg>",
        "user_not_found": "No encontrado",
        "user_kicked": "expulsado",
        "kick_reason": "Expulsado por admin",
        "server_stopping": "Deteniendo...",
        "server_stopped": "Servidor detenido",
        "none": "Ninguno",
        "error": "Error",
        "system": "Sistema",
        "input_prompt": "Servidor> ",
        "language_select": "Idioma",
        "available_languages": "Disponibles",
        "current_language": "Actual",
        "invalid_choice": "Inválido",
        "invalid_ip": "IP inválida",
    },
    "Русский": {
        "title": "Чат-сервер TUI",
        "startup": "Запуск...",
        "enter_port": "Введите порт",
        "select_ip": "Выберите IP",
        "all_interfaces": "Все (0.0.0.0)",
        "detected_ips": "Найденные IP",
        "custom_ip": "Свой IP",
        "enter_custom_ip": "Введите IP",
        "port_range": "Порты 1024-65535",
        "port_must_number": "Порт - число",
        "server_started": "Сервер запущен",
        "listening_on": "Слушаем",
        "online_users": "Онлайн",
        "server_log": "Журнал",
        "commands": "/kick <имя> | /broadcast <текст> | /quit | /help",
        "waiting_connections": "Ожидание...",
        "new_connection": "Новое подключение",
        "from_address": "от",
        "client_disconnected": "Отключен",
        "user_joined": "зашёл",
        "user_left": "вышел",
        "duplicate_username": "Имя занято",
        "duplicate_rejected": "Дубль, отказ",
        "public_message": "[Общее]",
        "private_message": "[Личное]",
        "file_transfer": "[Файл]",
        "file_broadcast": "[Рассылка]",
        "broadcast_message": "[Сообщение]",
        "unknown_command": "Неизв.",
        "usage_kick": "Формат: /kick <имя>",
        "usage_broadcast": "Формат: /broadcast <текст>",
        "user_not_found": "Не найден",
        "user_kicked": "отключён",
        "kick_reason": "Отключён админом",
        "server_stopping": "Остановка...",
        "server_stopped": "Сервер остановлен",
        "none": "Нет",
        "error": "Ошибка",
        "system": "Система",
        "input_prompt": "Сервер> ",
        "language_select": "Выбор языка",
        "available_languages": "Доступно",
        "current_language": "Текущий",
        "invalid_choice": "Неверно",
        "invalid_ip": "Неверный IP",
    }
}

LANGUAGE_LIST = list(TRANSLATIONS.keys())


class ChatServerTUI:
    def __init__(self):
        self.server = None
        self.clients = {}
        self.buffer_size = 4096
        self.is_running = False
        self.lock = threading.Lock()
        self.current_language = '中文'
        self.logs = []
        self.max_logs = 100

    def t(self, key, *args):
        text = TRANSLATIONS.get(self.current_language, {}).get(key, key)
        if args:
            return text.format(*args)
        return text

    def add_log(self, msg, tag=""):
        timestamp = datetime.now().strftime('%H:%M:%S')
        if tag:
            log_entry = f"[{timestamp}] [{tag}] {msg}"
        else:
            log_entry = f"[{timestamp}] {msg}"
        self.logs.append(log_entry)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

    def select_language(self):
        """选择语言"""
        while True:
            try:
                clr()
                W = 50
                print("╭" + "─" * (W - 2) + "╮")
                print("│   " + pad_text("TUI Server", W - 5) + "│")
                print("├" + "─" * (W - 2) + "┤")
                print("│   " + pad_text("Select Language", W - 5) + "│")
                print("├" + "─" * (W - 2) + "┤")
                for i, lang in enumerate(LANGUAGE_LIST, 1):
                    line = f"  {i:2d}. {lang}"
                    print("│" + pad_text(line, W - 2) + "│")
                print("├" + "─" * (W - 2) + "┤")
                print("│ " + pad_text("Sorry, the TUI server does not support Arabic.", W - 5) + " │")
                print("│ " + pad_text("If you need Arabic, please use the GUI Server.", W - 5) + " │")
                print("╰" + "─" * (W - 2) + "╯")
                choice = input(f"[1-{len(LANGUAGE_LIST)}]: ").strip()
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(LANGUAGE_LIST):
                        self.current_language = LANGUAGE_LIST[idx]
                        break
                elif choice in LANGUAGE_LIST:
                    self.current_language = choice
                    break
                print(f"[{self.t('error')}] {self.t('invalid_choice')}")
                time.sleep(1)
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)

    def get_local_ips(self):
        ip_list = []
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            if local_ip != '127.0.0.1':
                ip_list.append(local_ip)
            for iface in socket.getaddrinfo(hostname, None):
                ip = iface[4][0]
                if ip not in ip_list and not ip.startswith('127.') and not ':' in ip:    #排除IPv6
                    ip_list.append(ip)
        except:
            pass
        if not ip_list:
            ip_list = ['127.0.0.1']
        return ip_list

    def select_ip(self):
        ip_list = self.get_local_ips()
        while True:
            try:
                clr()
                W = 50
                print("╭" + "─" * (W - 2) + "╮")
                print("│ " + pad_text(self.t('select_ip'), W - 3) + "│")
                print("├" + "─" * (W - 2) + "┤")
                print("│ " + pad_text(f"0. {self.t('all_interfaces')}", W - 3) + "│")
                print("│" + " " * (W - 2) + "│")
                print("│ " + pad_text(self.t('detected_ips') + ":", W - 3) + "│")
                for i, ip in enumerate(ip_list, 1):
                    print("│ " + pad_text(f"  {i}. {ip}", W - 3) + "│")
                print("│ " + pad_text(f"  {len(ip_list) + 1}. {self.t('custom_ip')}", W - 3) + "│")
                print("╰" + "─" * (W - 2) + "╯")
                choice = input(f"[0-{len(ip_list) + 1}]: ").strip()
                if choice == '0':
                    return '0.0.0.0'
                elif choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(ip_list):
                        return ip_list[idx]
                    elif idx == len(ip_list):
                        return self.input_custom_ip()
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)

    def input_custom_ip(self):
        while True:
            ip = input(f"{self.t('enter_custom_ip')}: ").strip()
            if not ip:
                continue
            parts = ip.split('.')
            if len(parts) == 4:
                try:
                    if all(0 <= int(p) <= 255 for p in parts):
                        return ip
                except ValueError:
                    pass
            print(f"[{self.t('error')}] {self.t('invalid_ip')}")

    def render_ui(self):
        """渲染TUI界面 - 使用 pad_text 确保对齐"""
        clr()
        W = 60
        try:
            term_height = shutil.get_terminal_size().lines
        except:
            term_height = 24

        # 标题栏
        print("╭" + "─" * (W - 2) + "╮")
        title = f" {self.t('title')} - {self.t('listening_on')}: {self.host}:{self.port} "
        print("│" + pad_text(title, W - 2) + "│")
        print("├" + "─" * (W - 2) + "┤")

        # 在线用户
        with self.lock:
            if self.clients:
                users_str = ", ".join(info['username'] for info in self.clients.values())
            else:
                users_str = self.t('none')
        user_line = f" {self.t('online_users')}: {users_str}"
        print("│" + pad_text(user_line, W - 2) + "│")
        print("├" + "─" * (W - 2) + "┤")

        # 命令提示
        cmd_line = f" {self.t('commands')}"
        print("│" + pad_text(cmd_line, W - 2) + "│")
        print("├" + "─" * (W - 2) + "┤")

        # 日志区域
        log_lines = max(term_height - 7, 1)
        recent_logs = self.logs[-log_lines:] if len(self.logs) > log_lines else self.logs
        for log in recent_logs:
            if vl(log) > W - 3:
                log = log[:W - 6] + "..."
            print("│ " + pad_text(log, W - 3) + "│")

        for _ in range(log_lines - len(recent_logs)):
            print("│" + " " * (W - 2) + "│")

        print("╰" + "─" * (W - 2) + "╯")
        print(self.t('input_prompt'), end='', flush=True)

    def start(self):
        clr()
        print(self.t('startup'))
        self.host = self.select_ip()

        while True:
            port_str = input(f"\n{self.t('enter_port')} [55555]: ").strip()
            if not port_str:
                port_str = "55555"
            try:
                self.port = int(port_str)
                if 1024 <= self.port <= 65535:
                    break
                print(f"[{self.t('error')}] {self.t('port_range')}")
            except ValueError:
                print(f"[{self.t('error')}] {self.t('port_must_number')}")

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            self.server.settimeout(0.5)
            self.is_running = True

            self.add_log(self.t('server_started'), self.t('system'))
            self.add_log(f"{self.t('listening_on')}: {self.host}:{self.port}", self.t('system'))
            self.add_log(self.t('waiting_connections'), self.t('system'))

            accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
            accept_thread.start()
            self.main_loop()

        except Exception as e:
            print(f"\n[{self.t('error')}] {str(e)}")
            sys.exit(1)

    # ... 其余方法与之前相同 ...
    def accept_clients(self):
        while self.is_running:
            try:
                client_socket, address = self.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True)
                thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.is_running:
                    self.add_log(str(e), self.t('error'))
                break

    def recv_all(self, client_socket, length):
        data = b''
        while len(data) < length:
            try:
                chunk = client_socket.recv(min(self.buffer_size, length - len(data)))
                if not chunk:
                    return None
                data += chunk
            except socket.timeout:
                continue
        return data

    def recv_msg(self, client_socket):
        h = self.recv_all(client_socket, 4)
        if not h:
            return None
        msg_len = int.from_bytes(h, 'big')
        d = self.recv_all(client_socket, msg_len)
        return d.decode('utf-8') if d else None

    def send_to(self, client_socket, msg):
        d = msg.encode('utf-8')
        h = len(d).to_bytes(4, 'big')
        try:
            client_socket.sendall(h + d)
            return True
        except:
            return False

    def handle_client(self, client_socket, address):
        username = None
        try:
            username = self.recv_msg(client_socket)
            if not username:
                return

            with self.lock:
                if any(info['username'] == username for info in self.clients.values()):
                    self.send_to(client_socket, json.dumps({
                        'type': 'system',
                        'message': self.t('duplicate_username')
                    }))
                    client_socket.close()
                    self.add_log(f"{self.t('duplicate_rejected')}: {username} ({address[0]}:{address[1]})", self.t('system'))
                    return

                self.clients[client_socket] = {
                    'username': username,
                    'address': f"{address[0]}:{address[1]}",
                    'connect_time': datetime.now().strftime('%H:%M:%S')
                }

            self.add_log(f"{self.t('new_connection')}: {username} {self.t('from_address')} {address[0]}:{address[1]}", self.t('system'))

            self.broadcast(json.dumps({
                'type': 'system',
                'message': f"{username} {self.t('user_joined')}",
                'time': datetime.now().strftime('%H:%M:%S')
            }), client_socket)
            self.update_user_list()

            while self.is_running:
                msg = self.recv_msg(client_socket)
                if not msg:
                    break

                try:
                    md = json.loads(msg)
                except:
                    continue

                if md['type'] == 'public':
                    self.broadcast(json.dumps({
                        'type': 'public',
                        'username': username,
                        'message': md['message'],
                        'time': datetime.now().strftime('%H:%M:%S')
                    }), client_socket)
                    self.add_log(f"{self.t('public_message')} {username}: {md['message'][:40]}")

                elif md['type'] == 'private':
                    pm = json.dumps({
                        'type': 'private',
                        'from': username,
                        'message': md['message'],
                        'time': datetime.now().strftime('%H:%M:%S')
                    })
                    if not self.send_private(pm, md['to']):
                        self.send_to(client_socket, json.dumps({
                            'type': 'system',
                            'message': self.t('user_not_found')
                        }))

                elif md['type'] == 'file_start':
                    self.handle_file(client_socket, username, md)

        except Exception as e:
            if self.is_running:
                self.add_log(str(e), self.t('error'))
        finally:
            if username:
                self.remove_client(client_socket)

    def handle_file(self, client_socket, username, data):
        try:
            fd = self.recv_all(client_socket, data['size'])
            if not fd:
                return
            fm = json.dumps({
                'type': 'file',
                'from': username,
                'filename': data['filename'],
                'size': data['size'],
                'time': datetime.now().strftime('%H:%M:%S')
            })
            target = data.get('to')
            if target:
                with self.lock:
                    for c, info in self.clients.items():
                        if info['username'] == target:
                            if self.send_to(c, fm):
                                c.send(data['size'].to_bytes(8, 'big'))
                                c.sendall(fd)
                            break
                self.add_log(f"{self.t('file_transfer')}: {username} -> {target}: {data['filename']}")
            else:
                with self.lock:
                    for c in list(self.clients.keys()):
                        if c != client_socket:
                            try:
                                self.send_to(c, fm)
                                c.send(data['size'].to_bytes(8, 'big'))
                                c.sendall(fd)
                            except:
                                self.remove_client(c)
                self.add_log(f"{self.t('file_broadcast')}: {username}: {data['filename']}")
        except Exception as e:
            self.add_log(str(e), self.t('error'))

    def broadcast(self, msg, sender=None):
        failed = []
        with self.lock:
            for c in list(self.clients.keys()):
                if c != sender and not self.send_to(c, msg):
                    failed.append(c)
        for c in failed:
            self.remove_client(c)

    def send_private(self, msg, target):
        with self.lock:
            for c, info in self.clients.items():
                if info['username'] == target:
                    if self.send_to(c, msg):
                        return True
                    self.remove_client(c)
                    return False
        return False

    def update_user_list(self):
        with self.lock:
            users = [info['username'] for info in self.clients.values()]
            msg = json.dumps({'type': 'user_list', 'users': users})
            failed = [c for c in list(self.clients.keys()) if not self.send_to(c, msg)]
        for c in failed:
            self.remove_client(c)

    def remove_client(self, client_socket):
        with self.lock:
            if client_socket in self.clients:
                username = self.clients[client_socket]['username']
                del self.clients[client_socket]
                try:
                    client_socket.close()
                except:
                    pass
                self.broadcast(json.dumps({
                    'type': 'system',
                    'message': f"{username} {self.t('user_left')}",
                    'time': datetime.now().strftime('%H:%M:%S')
                }))
                self.add_log(f"{self.t('client_disconnected')}: {username}", self.t('system'))
                self.update_user_list()

    def kick_user(self, username):
        with self.lock:
            for cs, info in list(self.clients.items()):
                if info['username'] == username:
                    self.send_to(cs, json.dumps({
                        'type': 'system',
                        'message': self.t('kick_reason')
                    }))
                    self.remove_client(cs)
                    self.add_log(f"{username} {self.t('user_kicked')}", self.t('system'))
                    return True
        return False

    def main_loop(self):
        while self.is_running:
            try:
                self.render_ui()
                cmd = input().strip()
            except (EOFError, KeyboardInterrupt):
                self.add_log(self.t('server_stopping'), self.t('system'))
                self.stop()
                break

            if not cmd:
                continue

            if cmd.startswith('/'):
                self.handle_command(cmd)

    def handle_command(self, cmd):
        parts = cmd.split(' ', 2)
        command = parts[0].lower()

        if command == '/quit' or command == '/exit':
            self.add_log(self.t('server_stopping'), self.t('system'))
            self.stop()
            clr()
            print(f"[{self.t('system')}] {self.t('server_stopped')}")
            sys.exit(0)

        elif command == '/help':
            self.add_log(self.t('commands'), self.t('system'))

        elif command == '/kick':
            if len(parts) >= 2:
                if not self.kick_user(parts[1]):
                    self.add_log(f"{self.t('user_not_found')}: {parts[1]}", self.t('error'))
            else:
                self.add_log(self.t('usage_kick'), self.t('error'))

        elif command == '/broadcast':
            if len(parts) >= 2:
                msg = json.dumps({
                    'type': 'system',
                    'message': f"{self.t('broadcast_message')}: {parts[1]}",
                    'time': datetime.now().strftime('%H:%M:%S')
                })
                self.broadcast(msg)
                self.add_log(f"{self.t('broadcast_message')}: {parts[1]}", self.t('system'))
            else:
                self.add_log(self.t('usage_broadcast'), self.t('error'))

        else:
            self.add_log(f"{self.t('unknown_command')}: {command}", self.t('error'))

    def stop(self):
        self.is_running = False
        with self.lock:
            for cs in list(self.clients.keys()):
                try:
                    cs.close()
                except:
                    pass
            self.clients.clear()
        if self.server:
            try:
                self.server.close()
            except:
                pass
            self.server = None

    def run(self):
        self.select_language()
        self.start()


if __name__ == "__main__":
    ChatServerTUI().run()
