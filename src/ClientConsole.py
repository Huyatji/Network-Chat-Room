# -*- coding: utf-8 -*-
import socket
import threading
import json
import os
import time
import sys
from datetime import datetime

# ==================== 语言包（12种语言） ====================
TRANSLATIONS = {
    "中文": {
        "title": "网络聊天室 - 命令行版",
        "welcome": "欢迎来到聊天室",
        "username": "请输入用户名",
        "server_address": "请输入服务器地址",
        "port": "请输入端口",
        "connecting": "正在连接...",
        "connecting_success": "成功连接到服务器",
        "connecting_timeout": "连接服务器超时",
        "connection_refused": "服务器拒绝连接",
        "connection_failed": "无法连接到服务器",
        "disconnected": "与服务器断开连接",
        "send_failed": "发送失败",
        "file_send_failed": "文件发送失败",
        "file_saved": "文件已保存",
        "file_receive_failed": "文件接收失败",
        "file_not_found": "文件不存在",
        "file_sent": "文件已发送",
        "file_received": "收到文件",
        "usage_hint": "输入消息发送，/msg 用户名 消息 发私聊，/file 路径 发文件，/users 查在线，/help 帮助，/quit 退出",
        "help_text": "命令列表:\n  /msg <用户名> <消息> - 发送私聊消息\n  /file <文件路径> - 发送文件\n  /users - 查看在线用户\n  /help - 显示帮助\n  /lang - 显示语言信息\n  /quit - 退出聊天室\n  直接输入文字 - 发送公开消息",
        "input_prompt": "[{}] 输入: ",
        "me": "我",
        "you": "你",
        "private_to": "私聊 →",
        "private_from": "私聊 ←",
        "system": "系统",
        "error": "错误",
        "language_select": "选择语言",
        "available_languages": "可用语言",
        "current_language": "当前语言",
        "online_users": "在线用户",
        "goodbye": "再见!",
        "disconnected_msg": "已断开连接",
        "port_range": "端口范围 1024-65535",
        "port_must_number": "端口必须是数字",
        "username_empty": "用户名不能为空",
        "invalid_choice": "无效选择",
        "unknown_command": "未知命令",
        "usage_private": "用法: /msg <用户名> <消息>",
        "usage_file": "用法: /file <文件路径>",
        "none": "无"
    },
    "繁體中文": {
        "title": "網路聊天室 - 命令列版",
        "welcome": "歡迎來到聊天室",
        "username": "請輸入使用者名稱",
        "server_address": "請輸入伺服器位址",
        "port": "請輸入連接埠",
        "connecting": "正在連線...",
        "connecting_success": "成功連線到伺服器",
        "connecting_timeout": "連線伺服器逾時",
        "connection_refused": "伺服器拒絕連線",
        "connection_failed": "無法連線到伺服器",
        "disconnected": "與伺服器中斷連線",
        "send_failed": "傳送失敗",
        "file_send_failed": "檔案傳送失敗",
        "file_saved": "檔案已儲存",
        "file_receive_failed": "檔案接收失敗",
        "file_not_found": "檔案不存在",
        "file_sent": "檔案已傳送",
        "file_received": "收到檔案",
        "usage_hint": "輸入訊息傳送，/msg 使用者 訊息 發私聊，/file 路徑 發檔案，/users 查線上，/help 幫助，/quit 退出",
        "help_text": "命令列表:\n  /msg <使用者> <訊息> - 發送私聊訊息\n  /file <檔案路徑> - 發送檔案\n  /users - 檢視線上使用者\n  /help - 顯示幫助\n  /lang - 顯示語言資訊\n  /quit - 退出聊天室\n  直接輸入文字 - 發送公開訊息",
        "input_prompt": "[{}] 輸入: ",
        "me": "我",
        "you": "你",
        "private_to": "私聊 →",
        "private_from": "私聊 ←",
        "system": "系統",
        "error": "錯誤",
        "language_select": "選擇語言",
        "available_languages": "可用語言",
        "current_language": "目前語言",
        "online_users": "線上使用者",
        "goodbye": "再見!",
        "disconnected_msg": "已中斷連線",
        "port_range": "連接埠範圍 1024-65535",
        "port_must_number": "連接埠必須是數字",
        "username_empty": "使用者名稱不能為空",
        "invalid_choice": "無效選擇",
        "unknown_command": "未知命令",
        "usage_private": "用法: /msg <使用者> <訊息>",
        "usage_file": "用法: /file <檔案路徑>",
        "none": "無"
    },
    "日本語": {
        "title": "ネットワークチャット - CLI",
        "welcome": "チャットルームへようこそ",
        "username": "ユーザー名を入力",
        "server_address": "サーバーアドレスを入力",
        "port": "ポートを入力",
        "connecting": "接続中...",
        "connecting_success": "サーバーに接続しました",
        "connecting_timeout": "接続タイムアウト",
        "connection_refused": "接続が拒否されました",
        "connection_failed": "接続できません",
        "disconnected": "切断されました",
        "send_failed": "送信失敗",
        "file_send_failed": "ファイル送信失敗",
        "file_saved": "ファイル保存完了",
        "file_receive_failed": "ファイル受信失敗",
        "file_not_found": "ファイルが見つかりません",
        "file_sent": "ファイル送信完了",
        "file_received": "ファイル受信",
        "usage_hint": "入力で送信、/msg ユーザー メッセージ で私聊、/file パス でファイル、/users で一覧、/help、/quit",
        "help_text": "コマンド:\n  /msg <ユーザー> <メッセージ>\n  /file <パス>\n  /users\n  /help\n  /lang\n  /quit",
        "input_prompt": "[{}] 入力: ",
        "me": "自分",
        "you": "あなた",
        "private_to": "プライベート →",
        "private_from": "プライベート ←",
        "system": "システム",
        "error": "エラー",
        "language_select": "言語選択",
        "available_languages": "利用可能な言語",
        "current_language": "現在の言語",
        "online_users": "オンラインユーザー",
        "goodbye": "さようなら!",
        "disconnected_msg": "切断されました",
        "port_range": "ポート範囲 1024-65535",
        "port_must_number": "ポートは数字で入力",
        "username_empty": "ユーザー名を入力してください",
        "invalid_choice": "無効な選択",
        "unknown_command": "不明なコマンド",
        "usage_private": "使用法: /msg <ユーザー> <メッセージ>",
        "usage_file": "使用法: /file <パス>",
        "none": "なし"
    },
    "한국어": {
        "title": "네트워크 채팅 - CLI",
        "welcome": "채팅방에 오신 것을 환영합니다",
        "username": "사용자 이름 입력",
        "server_address": "서버 주소 입력",
        "port": "포트 입력",
        "connecting": "연결 중...",
        "connecting_success": "서버에 연결되었습니다",
        "connecting_timeout": "연결 시간 초과",
        "connection_refused": "연결이 거부되었습니다",
        "connection_failed": "연결할 수 없습니다",
        "disconnected": "연결이 끊어졌습니다",
        "send_failed": "전송 실패",
        "file_send_failed": "파일 전송 실패",
        "file_saved": "파일 저장 완료",
        "file_receive_failed": "파일 수신 실패",
        "file_not_found": "파일을 찾을 수 없습니다",
        "file_sent": "파일 전송 완료",
        "file_received": "파일 수신",
        "usage_hint": "입력하여 전송, /msg 사용자 메시지, /file 경로, /users, /help, /quit",
        "help_text": "명령어:\n  /msg <사용자> <메시지>\n  /file <경로>\n  /users\n  /help\n  /lang\n  /quit",
        "input_prompt": "[{}] 입력: ",
        "me": "나",
        "you": "너",
        "private_to": "비공개 →",
        "private_from": "비공개 ←",
        "system": "시스템",
        "error": "오류",
        "language_select": "언어 선택",
        "available_languages": "사용 가능한 언어",
        "current_language": "현재 언어",
        "online_users": "온라인 사용자",
        "goodbye": "안녕히 가세요!",
        "disconnected_msg": "연결이 끊어졌습니다",
        "port_range": "포트 범위 1024-65535",
        "port_must_number": "포트는 숫자여야 합니다",
        "username_empty": "사용자 이름은 비워둘 수 없습니다",
        "invalid_choice": "잘못된 선택",
        "unknown_command": "알 수 없는 명령",
        "usage_private": "사용법: /msg <사용자> <메시지>",
        "usage_file": "사용법: /file <경로>",
        "none": "없음"
    },
    "Deutsch": {
        "title": "Netzwerk-Chat - CLI",
        "welcome": "Willkommen im Chatraum",
        "username": "Benutzername eingeben",
        "server_address": "Serveradresse eingeben",
        "port": "Port eingeben",
        "connecting": "Verbinde...",
        "connecting_success": "Erfolgreich verbunden",
        "connecting_timeout": "Verbindungs timeout",
        "connection_refused": "Verbindung abgelehnt",
        "connection_failed": "Verbindung fehlgeschlagen",
        "disconnected": "Verbindung getrennt",
        "send_failed": "Senden fehlgeschlagen",
        "file_send_failed": "Datei senden fehlgeschlagen",
        "file_saved": "Datei gespeichert",
        "file_receive_failed": "Dateiempfang fehlgeschlagen",
        "file_not_found": "Datei nicht gefunden",
        "file_sent": "Datei gesendet",
        "file_received": "Datei empfangen",
        "usage_hint": "Eingabe senden, /msg Benutzer Nachricht, /file Pfad, /users, /help, /quit",
        "help_text": "Befehle:\n  /msg <Benutzer> <Nachricht>\n  /file <Pfad>\n  /users\n  /help\n  /lang\n  /quit",
        "input_prompt": "[{}] Eingabe: ",
        "me": "Ich",
        "you": "Du",
        "private_to": "Privat →",
        "private_from": "Privat ←",
        "system": "System",
        "error": "Fehler",
        "language_select": "Sprache wählen",
        "available_languages": "Verfügbare Sprachen",
        "current_language": "Aktuelle Sprache",
        "online_users": "Online-Benutzer",
        "goodbye": "Auf Wiedersehen!",
        "disconnected_msg": "Verbindung getrennt",
        "port_range": "Portbereich 1024-65535",
        "port_must_number": "Port muss eine Zahl sein",
        "username_empty": "Benutzername darf nicht leer sein",
        "invalid_choice": "Ungültige Auswahl",
        "unknown_command": "Unbekannter Befehl",
        "usage_private": "Verwendung: /msg <Benutzer> <Nachricht>",
        "usage_file": "Verwendung: /file <Pfad>",
        "none": "Keine"
    },
    "Italiano": {
        "title": "Chat di Rete - CLI",
        "welcome": "Benvenuto nella Chat",
        "username": "Inserisci nome utente",
        "server_address": "Inserisci indirizzo server",
        "port": "Inserisci porta",
        "connecting": "Connessione in corso...",
        "connecting_success": "Connesso con successo",
        "connecting_timeout": "Timeout connessione",
        "connection_refused": "Connessione rifiutata",
        "connection_failed": "Connessione fallita",
        "disconnected": "Disconnesso",
        "send_failed": "Invio fallito",
        "file_send_failed": "Invio file fallito",
        "file_saved": "File salvato",
        "file_receive_failed": "Ricezione file fallita",
        "file_not_found": "File non trovato",
        "file_sent": "File inviato",
        "file_received": "File ricevuto",
        "usage_hint": "Digita per inviare, /msg utente msg, /file percorso, /users, /help, /quit",
        "help_text": "Comandi:\n  /msg <utente> <msg>\n  /file <percorso>\n  /users\n  /help\n  /lang\n  /quit",
        "input_prompt": "[{}] Input: ",
        "me": "Io",
        "you": "Tu",
        "private_to": "Privato →",
        "private_from": "Privato ←",
        "system": "Sistema",
        "error": "Errore",
        "language_select": "Seleziona lingua",
        "available_languages": "Lingue disponibili",
        "current_language": "Lingua corrente",
        "online_users": "Utenti online",
        "goodbye": "Arrivederci!",
        "disconnected_msg": "Disconnesso",
        "port_range": "Intervallo porte 1024-65535",
        "port_must_number": "La porta deve essere un numero",
        "username_empty": "Il nome utente non può essere vuoto",
        "invalid_choice": "Scelta non valida",
        "unknown_command": "Comando sconosciuto",
        "usage_private": "Uso: /msg <utente> <msg>",
        "usage_file": "Uso: /file <percorso>",
        "none": "Nessuno"
    },
    "English": {
        "title": "Network Chat Room - CLI",
        "welcome": "Welcome to the Chat Room",
        "username": "Enter username",
        "server_address": "Enter server address",
        "port": "Enter port",
        "connecting": "Connecting...",
        "connecting_success": "Successfully connected to server",
        "connecting_timeout": "Connection timeout",
        "connection_refused": "Connection refused",
        "connection_failed": "Cannot connect to server",
        "disconnected": "Disconnected from server",
        "send_failed": "Send failed",
        "file_send_failed": "File send failed",
        "file_saved": "File saved",
        "file_receive_failed": "File receive failed",
        "file_not_found": "File not found",
        "file_sent": "File sent",
        "file_received": "File received",
        "usage_hint": "Type to send, /msg user msg for private, /file path for file, /users to list, /help, /quit",
        "help_text": "Commands:\n  /msg <user> <msg> - Private message\n  /file <path> - Send file\n  /users - List online users\n  /help - Show help\n  /lang - Show language info\n  /quit - Exit chat",
        "input_prompt": "[{}] Input: ",
        "me": "Me",
        "you": "You",
        "private_to": "Private →",
        "private_from": "Private ←",
        "system": "System",
        "error": "Error",
        "language_select": "Select language",
        "available_languages": "Available languages",
        "current_language": "Current language",
        "online_users": "Online users",
        "goodbye": "Goodbye!",
        "disconnected_msg": "Disconnected",
        "port_range": "Port range 1024-65535",
        "port_must_number": "Port must be a number",
        "username_empty": "Username cannot be empty",
        "invalid_choice": "Invalid choice",
        "unknown_command": "Unknown command",
        "usage_private": "Usage: /msg <user> <msg>",
        "usage_file": "Usage: /file <path>",
        "none": "None"
    },
    "Français": {
        "title": "Chat Réseau - CLI",
        "welcome": "Bienvenue dans le Chat",
        "username": "Entrez le nom d'utilisateur",
        "server_address": "Entrez l'adresse du serveur",
        "port": "Entrez le port",
        "connecting": "Connexion en cours...",
        "connecting_success": "Connecté avec succès",
        "connecting_timeout": "Délai de connexion dépassé",
        "connection_refused": "Connexion refusée",
        "connection_failed": "Connexion impossible",
        "disconnected": "Déconnecté du serveur",
        "send_failed": "Échec de l'envoi",
        "file_send_failed": "Échec de l'envoi du fichier",
        "file_saved": "Fichier sauvegardé",
        "file_receive_failed": "Échec de réception",
        "file_not_found": "Fichier introuvable",
        "file_sent": "Fichier envoyé",
        "file_received": "Fichier reçu",
        "usage_hint": "Tapez pour envoyer, /msg utilisateur msg, /file chemin, /users, /help, /quit",
        "help_text": "Commandes:\n  /msg <utilisateur> <msg>\n  /file <chemin>\n  /users\n  /help\n  /lang\n  /quit",
        "input_prompt": "[{}] Entrée: ",
        "me": "Moi",
        "you": "Vous",
        "private_to": "Privé →",
        "private_from": "Privé ←",
        "system": "Système",
        "error": "Erreur",
        "language_select": "Choisir la langue",
        "available_languages": "Langues disponibles",
        "current_language": "Langue actuelle",
        "online_users": "Utilisateurs en ligne",
        "goodbye": "Au revoir!",
        "disconnected_msg": "Déconnecté",
        "port_range": "Plage de ports 1024-65535",
        "port_must_number": "Le port doit être un nombre",
        "username_empty": "Le nom d'utilisateur ne peut pas être vide",
        "invalid_choice": "Choix invalide",
        "unknown_command": "Commande inconnue",
        "usage_private": "Usage: /msg <utilisateur> <msg>",
        "usage_file": "Usage: /file <chemin>",
        "none": "Aucun"
    },
    "Español": {
        "title": "Chat en Red - CLI",
        "welcome": "Bienvenido al Chat",
        "username": "Ingrese nombre de usuario",
        "server_address": "Ingrese dirección del servidor",
        "port": "Ingrese puerto",
        "connecting": "Conectando...",
        "connecting_success": "Conectado exitosamente",
        "connecting_timeout": "Tiempo de conexión agotado",
        "connection_refused": "Conexión rechazada",
        "connection_failed": "No se puede conectar",
        "disconnected": "Desconectado del servidor",
        "send_failed": "Envío fallido",
        "file_send_failed": "Envío de archivo fallido",
        "file_saved": "Archivo guardado",
        "file_receive_failed": "Recepción de archivo fallida",
        "file_not_found": "Archivo no encontrado",
        "file_sent": "Archivo enviado",
        "file_received": "Archivo recibido",
        "usage_hint": "Escriba para enviar, /msg usuario msg, /file ruta, /users, /help, /quit",
        "help_text": "Comandos:\n  /msg <usuario> <msg>\n  /file <ruta>\n  /users\n  /help\n  /lang\n  /quit",
        "input_prompt": "[{}] Entrada: ",
        "me": "Yo",
        "you": "Tú",
        "private_to": "Privado →",
        "private_from": "Privado ←",
        "system": "Sistema",
        "error": "Error",
        "language_select": "Seleccionar idioma",
        "available_languages": "Idiomas disponibles",
        "current_language": "Idioma actual",
        "online_users": "Usuarios en línea",
        "goodbye": "¡Adiós!",
        "disconnected_msg": "Desconectado",
        "port_range": "Rango de puertos 1024-65535",
        "port_must_number": "El puerto debe ser un número",
        "username_empty": "El nombre de usuario no puede estar vacío",
        "invalid_choice": "Selección inválida",
        "unknown_command": "Comando desconocido",
        "usage_private": "Uso: /msg <usuario> <msg>",
        "usage_file": "Uso: /file <ruta>",
        "none": "Ninguno"
    },
    "Русский": {
        "title": "Сетевой чат - CLI",
        "welcome": "Добро пожаловать в чат",
        "username": "Введите имя пользователя",
        "server_address": "Введите адрес сервера",
        "port": "Введите порт",
        "connecting": "Подключение...",
        "connecting_success": "Успешно подключено",
        "connecting_timeout": "Таймаут подключения",
        "connection_refused": "Подключение отклонено",
        "connection_failed": "Не удалось подключиться",
        "disconnected": "Отключено от сервера",
        "send_failed": "Ошибка отправки",
        "file_send_failed": "Ошибка отправки файла",
        "file_saved": "Файл сохранён",
        "file_receive_failed": "Ошибка получения файла",
        "file_not_found": "Файл не найден",
        "file_sent": "Файл отправлен",
        "file_received": "Файл получен",
        "usage_hint": "Ввод для отправки, /msg пользователь текст, /file путь, /users, /help, /quit",
        "help_text": "Команды:\n  /msg <пользователь> <текст>\n  /file <путь>\n  /users\n  /help\n  /lang\n  /quit",
        "input_prompt": "[{}] Ввод: ",
        "me": "Я",
        "you": "Вы",
        "private_to": "Личное →",
        "private_from": "Личное ←",
        "system": "Система",
        "error": "Ошибка",
        "language_select": "Выберите язык",
        "available_languages": "Доступные языки",
        "current_language": "Текущий язык",
        "online_users": "Пользователи онлайн",
        "goodbye": "До свидания!",
        "disconnected_msg": "Отключено",
        "port_range": "Диапазон портов 1024-65535",
        "port_must_number": "Порт должен быть числом",
        "username_empty": "Имя пользователя не может быть пустым",
        "invalid_choice": "Неверный выбор",
        "unknown_command": "Неизвестная команда",
        "usage_private": "Использование: /msg <пользователь> <текст>",
        "usage_file": "Использование: /file <путь>",
        "none": "Нет"
    }
}

LANGUAGE_LIST = list(TRANSLATIONS.keys())
LANGUAGE_LIST.sort()

class ChatClientCLI:
    def __init__(self):
        self.client = None
        self.username = ""
        self.buffer_size = 4096
        self.current_language = '中文'
        self.running = True
        self.receive_thread = None
        self.users = []

    def t(self, key):
        return TRANSLATIONS.get(self.current_language, {}).get(key, key)

    def select_language(self):
        """选择语言"""
        print("=" * 50)
        print('Network Chat Hall')
        print("=" * 50)
        print('Select Language')
        print("-" * 50)
        for i, lang in enumerate(LANGUAGE_LIST, 1):
            print(f"  {i:2d}. {lang}")
        print("-" * 50)

        while True:
            try:
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
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)

        print(f"{self.t('current_language')}: {self.current_language}")
        print("=" * 50)

    def connect(self):
        """连接服务器"""
        print(self.t('welcome'))

        # 获取用户名
        while True:
            username = input(self.t('username') + ": ").strip()
            if username:
                break
            print(f"[{self.t('error')}] {self.t('username_empty')}")

        # 获取服务器地址
        host = input(self.t('server_address') + " [127.0.0.1]: ").strip()
        if not host:
            host = "127.0.0.1"

        # 获取端口
        while True:
            port_str = input(self.t('port') + " [55555]: ").strip()
            if not port_str:
                port_str = "55555"
            try:
                port = int(port_str)
                if 1024 <= port <= 65535:
                    break
                print(f"[{self.t('error')}] {self.t('port_range')}")
            except ValueError:
                print(f"[{self.t('error')}] {self.t('port_must_number')}")

        print(self.t('connecting'))

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(10)
            self.client.connect((host, port))
            self.send_to_server(username)
            self.username = username

            # 启动接收线程
            self.receive_thread = threading.Thread(target=self.receive_loop)
            self.receive_thread.daemon = True
            self.receive_thread.start()

            print(f"{self.t('connecting_success')} {host}:{port}")
            print(f"[{self.t('system')}] {self.t('usage_hint')}")
            print()

        except socket.timeout:
            print(f"[{self.t('error')}] {self.t('connecting_timeout')}")
            sys.exit(1)
        except ConnectionRefusedError:
            print(f"[{self.t('error')}] {self.t('connection_refused')}")
            sys.exit(1)
        except Exception as e:
            print(f"[{self.t('error')}] {self.t('connection_failed')}: {str(e)}")
            sys.exit(1)

    def recv_all(self, length):
        """接收完整数据"""
        data = b''
        while len(data) < length:
            try:
                chunk = self.client.recv(min(self.buffer_size, length - len(data)))
                if not chunk:
                    return None
                data += chunk
            except socket.timeout:
                continue
        return data

    def recv_msg(self):
        """接收消息"""
        h = self.recv_all(4)
        if not h:
            return None
        msg_len = int.from_bytes(h, 'big')
        d = self.recv_all(msg_len)
        return d.decode('utf-8') if d else None

    def send_to_server(self, msg):
        """发送消息到服务器"""
        d = msg.encode('utf-8')
        h = len(d).to_bytes(4, 'big')
        try:
            self.client.sendall(h + d)
            return True
        except:
            return False

    def receive_loop(self):
        """接收消息循环"""
        while self.running:
            try:
                if not self.client:
                    break
                msg = self.recv_msg()
                if not msg:
                    print(f"\n[{self.t('system')}] {self.t('disconnected')}")
                    self.running = False
                    break

                try:
                    md = json.loads(msg)
                except:
                    continue

                if md['type'] == 'user_list':
                    self.users = md['users']
                    print(f"\r[{self.t('system')}] {self.t('online_users')}: {', '.join(self.users)}")
                    print(self.t('input_prompt').format(self.username), end='', flush=True)

                elif md['type'] == 'system':
                    print(f"\r[{self.t('system')}] {md['message']}")
                    print(self.t('input_prompt').format(self.username), end='', flush=True)

                elif md['type'] == 'public':
                    user = md['username']
                    display_user = self.t('me') if user == self.username else user
                    print(f"\r[{md.get('time', '')}] {display_user}: {md['message']}")
                    print(self.t('input_prompt').format(self.username), end='', flush=True)

                elif md['type'] == 'private':
                    print(f"\r[{md.get('time', '')}] {self.t('private_from')} {md['from']}: {md['message']}")
                    print(self.t('input_prompt').format(self.username), end='', flush=True)

                elif md['type'] == 'file':
                    try:
                        sb = self.recv_all(8)
                        if sb and len(sb) == 8:
                            fs = int.from_bytes(sb, 'big')
                            fd = self.recv_all(fs)
                            if fd:
                                self.save_file(md, fd)
                            else:
                                print(f"\r[{self.t('error')}] {self.t('file_receive_failed')}")
                        print(self.t('input_prompt').format(self.username), end='', flush=True)
                    except Exception as e:
                        print(f"\r[{self.t('error')}] {str(e)}")
                        print(self.t('input_prompt').format(self.username), end='', flush=True)

            except Exception as e:
                if self.running:
                    print(f"\r[{self.t('error')}] {str(e)}")
                    print(self.t('input_prompt').format(self.username), end='', flush=True)
                break

    def save_file(self, info, data):
        """保存接收的文件"""
        os.makedirs('received', exist_ok=True)
        fn = f"received/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{info.get('from','unknown')}_{info['filename']}"
        with open(fn, 'wb') as f:
            f.write(data)
        print(f"\r[{self.t('system')}] {self.t('file_saved')}: {fn} ({len(data)} bytes)")
        print(self.t('input_prompt').format(self.username), end='', flush=True)

    def send_message(self, message):
        """发送公开消息"""
        if not self.client:
            return
        try:
            self.send_to_server(json.dumps({'type': 'public', 'message': message}))
        except Exception as e:
            print(f"[{self.t('error')}] {self.t('send_failed')}: {str(e)}")

    def send_private(self, target, message):
        """发送私聊消息"""
        if not self.client:
            return
        try:
            self.send_to_server(json.dumps({'type': 'private', 'to': target, 'message': message}))
            print(f"{self.t('private_to')} {target}: {message}")
        except Exception as e:
            print(f"[{self.t('error')}] {self.t('send_failed')}: {str(e)}")

    def send_file(self, filepath):
        """发送文件"""
        if not self.client:
            return
        if not os.path.exists(filepath):
            print(f"[{self.t('error')}] {self.t('file_not_found')}: {filepath}")
            return
        try:
            fn = os.path.basename(filepath)
            fs = os.path.getsize(filepath)
            self.send_to_server(json.dumps({'type': 'file_start', 'filename': fn, 'size': fs, 'to': None}))
            time.sleep(0.1)
            with open(filepath, 'rb') as f:
                self.client.sendall(f.read())
            print(f"[{self.t('system')}] {self.t('file_sent')}: {fn} ({fs} bytes)")
        except Exception as e:
            print(f"[{self.t('error')}] {self.t('file_send_failed')}: {str(e)}")

    def input_loop(self):
        """输入循环"""
        while self.running:
            try:
                msg = input(self.t('input_prompt').format(self.username)).strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{self.t('goodbye')}")
                break

            if not msg:
                continue

            if msg.startswith('/'):
                self.handle_command(msg)
            else:
                self.send_message(msg)

    def handle_command(self, msg):
        """处理命令"""
        parts = msg.split(' ', 2)
        cmd = parts[0].lower()

        if cmd == '/quit' or cmd == '/exit':
            self.running = False
            print(f"[{self.t('system')}] {self.t('goodbye')}")

        elif cmd == '/help':
            print(self.t('help_text'))

        elif cmd == '/users':
            if self.users:
                print(f"[{self.t('system')}] {self.t('online_users')}: {', '.join(self.users)}")
            else:
                print(f"[{self.t('system')}] {self.t('online_users')}: {self.t('none')}")

        elif cmd == '/msg':
            if len(parts) >= 3:
                self.send_private(parts[1], parts[2])
            else:
                print(f"[{self.t('error')}] {self.t('usage_private')}")

        elif cmd == '/file':
            if len(parts) >= 2:
                self.send_file(parts[1])
            else:
                print(f"[{self.t('error')}] {self.t('usage_file')}")

        elif cmd == '/lang':
            print(f"[{self.t('system')}] {self.t('available_languages')}: {', '.join(LANGUAGE_LIST)}")
            print(f"[{self.t('system')}] {self.t('current_language')}: {self.current_language}")

        else:
            print(f"[{self.t('error')}] {self.t('unknown_command')}: {cmd}")
            print(self.t('usage_hint'))

    def run(self):
        """运行客户端"""
        self.select_language()
        self.connect()
        self.input_loop()

        # 清理
        if self.client:
            try:
                self.client.close()
            except:
                pass
        print(f"[{self.t('system')}] {self.t('disconnected_msg')}")


if __name__ == "__main__":
    ChatClientCLI().run()
