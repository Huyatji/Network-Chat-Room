 # -*- coding: utf-8 -*-
"""
命令行聊天服务器 - 支持12种语言，自动检测本地IP
"""
import socket
import threading
import json
import os
import sys
import time
from datetime import datetime

# ==================== 语言包（12种语言） ====================
TRANSLATIONS = {
    "中文": {
        "title": "命令行聊天服务器",
        "startup": "正在启动服务器...",
        "enter_port": "请输入监听端口",
        "select_ip": "请选择监听IP地址",
        "all_interfaces": "所有网络接口 (0.0.0.0)",
        "detected_ips": "检测到以下本地IP地址",
        "custom_ip": "自定义输入",
        "enter_custom_ip": "请输入自定义IP地址",
        "port_range": "端口范围 1024-65535",
        "port_must_number": "端口必须是数字",
        "server_started": "服务器已启动",
        "listening_on": "监听地址",
        "waiting_connections": "等待客户端连接...",
        "press_ctrl_c": "按 Ctrl+C 停止服务器",
        "commands": "服务器命令: /users 查看在线, /kick <用户> 踢出, /broadcast <消息> 广播, /help 帮助, /quit 退出",
        "help_text": "可用命令:\n  /users - 查看在线用户\n  /kick <用户名> - 踢出用户\n  /broadcast <消息> - 广播消息\n  /help - 显示帮助\n  /quit - 停止服务器并退出",
        "new_connection": "新客户端连接",
        "from_address": "来自",
        "client_disconnected": "客户端断开",
        "user_joined": "加入了聊天室",
        "user_left": "离开了聊天室",
        "duplicate_username": "用户名已被使用",
        "duplicate_rejected": "用户名重复，拒绝连接",
        "public_message": "[公开]",
        "private_message": "[私聊]",
        "file_transfer": "[文件传输]",
        "file_broadcast": "[文件广播]",
        "broadcast_message": "[服务器广播]",
        "unknown_command": "未知命令",
        "usage_kick": "用法: /kick <用户名>",
        "usage_broadcast": "用法: /broadcast <消息>",
        "user_not_found": "用户不存在",
        "user_kicked": "用户已被踢出",
        "kick_reason": "被管理员踢出",
        "server_stopping": "正在停止服务器...",
        "server_stopped": "服务器已停止",
        "online_users": "在线用户",
        "none": "无",
        "error": "错误",
        "system": "系统",
        "input_prompt": "服务器> ",
        "language_select": "选择语言",
        "available_languages": "可用语言",
        "current_language": "当前语言",
        "invalid_choice": "无效选择",
        "invalid_ip": "无效的IP地址",
    },
    "繁體中文": {
        "title": "命令列聊天伺服器",
        "startup": "正在啟動伺服器...",
        "enter_port": "請輸入監聽連接埠",
        "select_ip": "請選擇監聽IP位址",
        "all_interfaces": "所有網路介面 (0.0.0.0)",
        "detected_ips": "偵測到以下本地IP位址",
        "custom_ip": "自訂輸入",
        "enter_custom_ip": "請輸入自訂IP位址",
        "port_range": "連接埠範圍 1024-65535",
        "port_must_number": "連接埠必須是數字",
        "server_started": "伺服器已啟動",
        "listening_on": "監聽位址",
        "waiting_connections": "等待客戶端連線...",
        "press_ctrl_c": "按 Ctrl+C 停止伺服器",
        "commands": "伺服器命令: /users 檢視線上, /kick <使用者> 踢出, /broadcast <訊息> 廣播, /help 幫助, /quit 退出",
        "help_text": "可用命令:\n  /users - 檢視線上使用者\n  /kick <使用者名稱> - 踢出使用者\n  /broadcast <訊息> - 廣播訊息\n  /help - 顯示幫助\n  /quit - 停止伺服器並退出",
        "new_connection": "新客戶端連線",
        "from_address": "來自",
        "client_disconnected": "客戶端中斷連線",
        "user_joined": "加入了聊天室",
        "user_left": "離開了聊天室",
        "duplicate_username": "使用者名稱已被使用",
        "duplicate_rejected": "使用者名稱重複，拒絕連線",
        "public_message": "[公開]",
        "private_message": "[私聊]",
        "file_transfer": "[檔案傳輸]",
        "file_broadcast": "[檔案廣播]",
        "broadcast_message": "[伺服器廣播]",
        "unknown_command": "未知命令",
        "usage_kick": "用法: /kick <使用者名稱>",
        "usage_broadcast": "用法: /broadcast <訊息>",
        "user_not_found": "使用者不存在",
        "user_kicked": "使用者已被踢出",
        "kick_reason": "被管理員踢出",
        "server_stopping": "正在停止伺服器...",
        "server_stopped": "伺服器已停止",
        "online_users": "線上使用者",
        "none": "無",
        "error": "錯誤",
        "system": "系統",
        "input_prompt": "伺服器> ",
        "language_select": "選擇語言",
        "available_languages": "可用語言",
        "current_language": "目前語言",
        "invalid_choice": "無效選擇",
        "invalid_ip": "無效的IP位址",
    },
    "日本語": {
        "title": "コマンドラインチャットサーバー",
        "startup": "サーバーを起動中...",
        "enter_port": "ポートを入力",
        "select_ip": "待受IPアドレスを選択",
        "all_interfaces": "すべてのネットワーク (0.0.0.0)",
        "detected_ips": "検出されたローカルIPアドレス",
        "custom_ip": "カスタム入力",
        "enter_custom_ip": "カスタムIPアドレスを入力",
        "port_range": "ポート範囲 1024-65535",
        "port_must_number": "ポートは数字で入力",
        "server_started": "サーバーが起動しました",
        "listening_on": "待受アドレス",
        "waiting_connections": "クライアントの接続を待っています...",
        "press_ctrl_c": "Ctrl+C でサーバーを停止",
        "commands": "コマンド: /users 一覧, /kick <ユーザー> キック, /broadcast <メッセージ> ブロードキャスト, /help, /quit",
        "help_text": "コマンド一覧:\n  /users - オンラインユーザー表示\n  /kick <ユーザー名> - ユーザーをキック\n  /broadcast <メッセージ> - 全員にメッセージ\n  /help - ヘルプ表示\n  /quit - サーバー停止",
        "new_connection": "新しい接続",
        "from_address": "接続元",
        "client_disconnected": "切断",
        "user_joined": "が参加しました",
        "user_left": "が退出しました",
        "duplicate_username": "ユーザー名は既に使用されています",
        "duplicate_rejected": "ユーザー名重複、接続拒否",
        "public_message": "[公開]",
        "private_message": "[プライベート]",
        "file_transfer": "[ファイル転送]",
        "file_broadcast": "[ファイルブロードキャスト]",
        "broadcast_message": "[サーバー通知]",
        "unknown_command": "不明なコマンド",
        "usage_kick": "使用法: /kick <ユーザー名>",
        "usage_broadcast": "使用法: /broadcast <メッセージ>",
        "user_not_found": "ユーザーが見つかりません",
        "user_kicked": "をキックしました",
        "kick_reason": "管理者によりキック",
        "server_stopping": "サーバーを停止中...",
        "server_stopped": "サーバーが停止しました",
        "online_users": "オンラインユーザー",
        "none": "なし",
        "error": "エラー",
        "system": "システム",
        "input_prompt": "サーバー> ",
        "language_select": "言語選択",
        "available_languages": "利用可能な言語",
        "current_language": "現在の言語",
        "invalid_choice": "無効な選択",
        "invalid_ip": "無効なIPアドレス",
    },
    "한국어": {
        "title": "명령줄 채팅 서버",
        "startup": "서버 시작 중...",
        "enter_port": "포트 입력",
        "select_ip": "수신 IP 주소 선택",
        "all_interfaces": "모든 네트워크 (0.0.0.0)",
        "detected_ips": "감지된 로컬 IP 주소",
        "custom_ip": "직접 입력",
        "enter_custom_ip": "IP 주소 직접 입력",
        "port_range": "포트 범위 1024-65535",
        "port_must_number": "포트는 숫자여야 함",
        "server_started": "서버가 시작되었습니다",
        "listening_on": "수신 주소",
        "waiting_connections": "클라이언트 연결 대기 중...",
        "press_ctrl_c": "Ctrl+C로 서버 중지",
        "commands": "명령: /users 목록, /kick <사용자> 강퇴, /broadcast <메시지> 방송, /help, /quit",
        "help_text": "명령어:\n  /users - 온라인 사용자\n  /kick <사용자> - 강제 퇴장\n  /broadcast <메시지> - 전체 방송\n  /help - 도움말\n  /quit - 서버 종료",
        "new_connection": "새 연결",
        "from_address": "연결처",
        "client_disconnected": "연결 해제",
        "user_joined": "님이 참여했습니다",
        "user_left": "님이 나갔습니다",
        "duplicate_username": "이미 사용 중인 이름",
        "duplicate_rejected": "중복 이름, 연결 거부",
        "public_message": "[공개]",
        "private_message": "[비공개]",
        "file_transfer": "[파일 전송]",
        "file_broadcast": "[파일 방송]",
        "broadcast_message": "[서버 공지]",
        "unknown_command": "알 수 없는 명령",
        "usage_kick": "사용법: /kick <사용자>",
        "usage_broadcast": "사용법: /broadcast <메시지>",
        "user_not_found": "사용자를 찾을 수 없음",
        "user_kicked": "강제 퇴장됨",
        "kick_reason": "관리자에 의해 강퇴",
        "server_stopping": "서버 종료 중...",
        "server_stopped": "서버가 종료되었습니다",
        "online_users": "온라인 사용자",
        "none": "없음",
        "error": "오류",
        "system": "시스템",
        "input_prompt": "서버> ",
        "language_select": "언어 선택",
        "available_languages": "사용 가능한 언어",
        "current_language": "현재 언어",
        "invalid_choice": "잘못된 선택",
        "invalid_ip": "유효하지 않은 IP 주소",
    },
    "Deutsch": {
        "title": "Befehlszeilen-Chatserver",
        "startup": "Server wird gestartet...",
        "enter_port": "Port eingeben",
        "select_ip": "IP-Adresse zum Abhören wählen",
        "all_interfaces": "Alle Schnittstellen (0.0.0.0)",
        "detected_ips": "Erkannte lokale IP-Adressen",
        "custom_ip": "Benutzerdefiniert",
        "enter_custom_ip": "Benutzerdefinierte IP eingeben",
        "port_range": "Portbereich 1024-65535",
        "port_must_number": "Port muss eine Zahl sein",
        "server_started": "Server gestartet",
        "listening_on": "Hört auf",
        "waiting_connections": "Warte auf Verbindungen...",
        "press_ctrl_c": "Ctrl+C zum Beenden",
        "commands": "Befehle: /users Liste, /kick <User>, /broadcast <Msg>, /help, /quit",
        "help_text": "Befehle:\n  /users - Online-Benutzer\n  /kick <Name> - Benutzer kicken\n  /broadcast <Msg> - An alle senden\n  /help - Hilfe\n  /quit - Beenden",
        "new_connection": "Neue Verbindung",
        "from_address": "von",
        "client_disconnected": "Client getrennt",
        "user_joined": "ist beigetreten",
        "user_left": "hat den Chat verlassen",
        "duplicate_username": "Benutzername bereits vergeben",
        "duplicate_rejected": "Doppelter Name, abgelehnt",
        "public_message": "[Öffentlich]",
        "private_message": "[Privat]",
        "file_transfer": "[Dateitransfer]",
        "file_broadcast": "[Datei-Broadcast]",
        "broadcast_message": "[Server-Meldung]",
        "unknown_command": "Unbekannter Befehl",
        "usage_kick": "Verwendung: /kick <Name>",
        "usage_broadcast": "Verwendung: /broadcast <Msg>",
        "user_not_found": "Benutzer nicht gefunden",
        "user_kicked": "wurde gekickt",
        "kick_reason": "Vom Admin gekickt",
        "server_stopping": "Server wird beendet...",
        "server_stopped": "Server gestoppt",
        "online_users": "Online-Benutzer",
        "none": "Keine",
        "error": "Fehler",
        "system": "System",
        "input_prompt": "Server> ",
        "language_select": "Sprache wählen",
        "available_languages": "Verfügbare Sprachen",
        "current_language": "Aktuelle Sprache",
        "invalid_choice": "Ungültige Auswahl",
        "invalid_ip": "Ungültige IP-Adresse",
    },
    "Italiano": {
        "title": "Server Chat a riga di comando",
        "startup": "Avvio server...",
        "enter_port": "Inserisci porta",
        "select_ip": "Seleziona IP di ascolto",
        "all_interfaces": "Tutte le interfacce (0.0.0.0)",
        "detected_ips": "IP locali rilevati",
        "custom_ip": "Personalizzato",
        "enter_custom_ip": "Inserisci IP personalizzato",
        "port_range": "Intervallo porte 1024-65535",
        "port_must_number": "La porta deve essere un numero",
        "server_started": "Server avviato",
        "listening_on": "In ascolto su",
        "waiting_connections": "In attesa di connessioni...",
        "press_ctrl_c": "Ctrl+C per fermare",
        "commands": "Comandi: /users lista, /kick <utente>, /broadcast <msg>, /help, /quit",
        "help_text": "Comandi:\n  /users - Utenti online\n  /kick <nome> - Espelli utente\n  /broadcast <msg> - Messaggio a tutti\n  /help - Aiuto\n  /quit - Esci",
        "new_connection": "Nuova connessione",
        "from_address": "da",
        "client_disconnected": "Client disconnesso",
        "user_joined": "è entrato",
        "user_left": "ha lasciato la chat",
        "duplicate_username": "Nome utente già in uso",
        "duplicate_rejected": "Nome duplicato, rifiutato",
        "public_message": "[Pubblico]",
        "private_message": "[Privato]",
        "file_transfer": "[Trasferimento file]",
        "file_broadcast": "[Broadcast file]",
        "broadcast_message": "[Messaggio server]",
        "unknown_command": "Comando sconosciuto",
        "usage_kick": "Uso: /kick <nome>",
        "usage_broadcast": "Uso: /broadcast <msg>",
        "user_not_found": "Utente non trovato",
        "user_kicked": "è stato espulso",
        "kick_reason": "Espulso dall'admin",
        "server_stopping": "Arresto server...",
        "server_stopped": "Server arrestato",
        "online_users": "Utenti online",
        "none": "Nessuno",
        "error": "Errore",
        "system": "Sistema",
        "input_prompt": "Server> ",
        "language_select": "Seleziona lingua",
        "available_languages": "Lingue disponibili",
        "current_language": "Lingua corrente",
        "invalid_choice": "Scelta non valida",
        "invalid_ip": "IP non valido",
    },
    "English": {
        "title": "Command Line Chat Server",
        "startup": "Starting server...",
        "enter_port": "Enter port",
        "select_ip": "Select IP address to listen on",
        "all_interfaces": "All interfaces (0.0.0.0)",
        "detected_ips": "Detected local IP addresses",
        "custom_ip": "Custom input",
        "enter_custom_ip": "Enter custom IP address",
        "port_range": "Port range 1024-65535",
        "port_must_number": "Port must be a number",
        "server_started": "Server started",
        "listening_on": "Listening on",
        "waiting_connections": "Waiting for connections...",
        "press_ctrl_c": "Press Ctrl+C to stop",
        "commands": "Commands: /users list, /kick <user>, /broadcast <msg>, /help, /quit",
        "help_text": "Commands:\n  /users - List online users\n  /kick <username> - Kick user\n  /broadcast <msg> - Broadcast message\n  /help - Show help\n  /quit - Stop server",
        "new_connection": "New connection",
        "from_address": "from",
        "client_disconnected": "Client disconnected",
        "user_joined": "joined the chat",
        "user_left": "left the chat",
        "duplicate_username": "Username already in use",
        "duplicate_rejected": "Duplicate username, rejected",
        "public_message": "[Public]",
        "private_message": "[Private]",
        "file_transfer": "[File Transfer]",
        "file_broadcast": "[File Broadcast]",
        "broadcast_message": "[Server Broadcast]",
        "unknown_command": "Unknown command",
        "usage_kick": "Usage: /kick <username>",
        "usage_broadcast": "Usage: /broadcast <msg>",
        "user_not_found": "User not found",
        "user_kicked": "has been kicked",
        "kick_reason": "Kicked by admin",
        "server_stopping": "Stopping server...",
        "server_stopped": "Server stopped",
        "online_users": "Online users",
        "none": "None",
        "error": "Error",
        "system": "System",
        "input_prompt": "Server> ",
        "language_select": "Select language",
        "available_languages": "Available languages",
        "current_language": "Current language",
        "invalid_choice": "Invalid choice",
        "invalid_ip": "Invalid IP address",
    },
    "Français": {
        "title": "Serveur Chat en ligne de commande",
        "startup": "Démarrage du serveur...",
        "enter_port": "Entrez le port",
        "select_ip": "Choisissez l'IP d'écoute",
        "all_interfaces": "Toutes les interfaces (0.0.0.0)",
        "detected_ips": "Adresses IP locales détectées",
        "custom_ip": "Saisie personnalisée",
        "enter_custom_ip": "Entrez une IP personnalisée",
        "port_range": "Plage de ports 1024-65535",
        "port_must_number": "Le port doit être un nombre",
        "server_started": "Serveur démarré",
        "listening_on": "Écoute sur",
        "waiting_connections": "En attente de connexions...",
        "press_ctrl_c": "Ctrl+C pour arrêter",
        "commands": "Commandes: /users liste, /kick <user>, /broadcast <msg>, /help, /quit",
        "help_text": "Commandes:\n  /users - Utilisateurs en ligne\n  /kick <nom> - Expulser\n  /broadcast <msg> - Message général\n  /help - Aide\n  /quit - Arrêter",
        "new_connection": "Nouvelle connexion",
        "from_address": "de",
        "client_disconnected": "Client déconnecté",
        "user_joined": "a rejoint le chat",
        "user_left": "a quitté le chat",
        "duplicate_username": "Nom déjà utilisé",
        "duplicate_rejected": "Nom en double, refusé",
        "public_message": "[Public]",
        "private_message": "[Privé]",
        "file_transfer": "[Transfert fichier]",
        "file_broadcast": "[Diffusion fichier]",
        "broadcast_message": "[Message serveur]",
        "unknown_command": "Commande inconnue",
        "usage_kick": "Usage: /kick <nom>",
        "usage_broadcast": "Usage: /broadcast <msg>",
        "user_not_found": "Utilisateur introuvable",
        "user_kicked": "a été expulsé",
        "kick_reason": "Expulsé par l'admin",
        "server_stopping": "Arrêt du serveur...",
        "server_stopped": "Serveur arrêté",
        "online_users": "Utilisateurs en ligne",
        "none": "Aucun",
        "error": "Erreur",
        "system": "Système",
        "input_prompt": "Serveur> ",
        "language_select": "Choisir la langue",
        "available_languages": "Langues disponibles",
        "current_language": "Langue actuelle",
        "invalid_choice": "Choix invalide",
        "invalid_ip": "Adresse IP invalide",
    },
    "Español": {
        "title": "Servidor Chat de línea de comandos",
        "startup": "Iniciando servidor...",
        "enter_port": "Ingrese puerto",
        "select_ip": "Seleccione IP de escucha",
        "all_interfaces": "Todas las interfaces (0.0.0.0)",
        "detected_ips": "IPs locales detectadas",
        "custom_ip": "Entrada personalizada",
        "enter_custom_ip": "Ingrese IP personalizada",
        "port_range": "Rango de puertos 1024-65535",
        "port_must_number": "El puerto debe ser un número",
        "server_started": "Servidor iniciado",
        "listening_on": "Escuchando en",
        "waiting_connections": "Esperando conexiones...",
        "press_ctrl_c": "Ctrl+C para detener",
        "commands": "Comandos: /users lista, /kick <user>, /broadcast <msg>, /help, /quit",
        "help_text": "Comandos:\n  /users - Usuarios en línea\n  /kick <nombre> - Expulsar\n  /broadcast <msg> - Mensaje general\n  /help - Ayuda\n  /quit - Detener",
        "new_connection": "Nueva conexión",
        "from_address": "desde",
        "client_disconnected": "Cliente desconectado",
        "user_joined": "se unió al chat",
        "user_left": "salió del chat",
        "duplicate_username": "Nombre ya en uso",
        "duplicate_rejected": "Nombre duplicado, rechazado",
        "public_message": "[Público]",
        "private_message": "[Privado]",
        "file_transfer": "[Transferencia]",
        "file_broadcast": "[Difusión archivo]",
        "broadcast_message": "[Mensaje servidor]",
        "unknown_command": "Comando desconocido",
        "usage_kick": "Uso: /kick <nombre>",
        "usage_broadcast": "Uso: /broadcast <msg>",
        "user_not_found": "Usuario no encontrado",
        "user_kicked": "ha sido expulsado",
        "kick_reason": "Expulsado por admin",
        "server_stopping": "Deteniendo servidor...",
        "server_stopped": "Servidor detenido",
        "online_users": "Usuarios en línea",
        "none": "Ninguno",
        "error": "Error",
        "system": "Sistema",
        "input_prompt": "Servidor> ",
        "language_select": "Seleccionar idioma",
        "available_languages": "Idiomas disponibles",
        "current_language": "Idioma actual",
        "invalid_choice": "Selección inválida",
        "invalid_ip": "Dirección IP no válida",
    },
    "Русский": {
        "title": "Консольный чат-сервер",
        "startup": "Запуск сервера...",
        "enter_port": "Введите порт",
        "select_ip": "Выберите IP для прослушивания",
        "all_interfaces": "Все интерфейсы (0.0.0.0)",
        "detected_ips": "Обнаруженные локальные IP",
        "custom_ip": "Свой вариант",
        "enter_custom_ip": "Введите свой IP-адрес",
        "port_range": "Диапазон портов 1024-65535",
        "port_must_number": "Порт должен быть числом",
        "server_started": "Сервер запущен",
        "listening_on": "Прослушивание",
        "waiting_connections": "Ожидание подключений...",
        "press_ctrl_c": "Ctrl+C для остановки",
        "commands": "Команды: /users список, /kick <польз>, /broadcast <сооб>, /help, /quit",
        "help_text": "Команды:\n  /users - Пользователи онлайн\n  /kick <имя> - Отключить\n  /broadcast <сооб> - Сообщение всем\n  /help - Помощь\n  /quit - Остановить",
        "new_connection": "Новое подключение",
        "from_address": "от",
        "client_disconnected": "Клиент отключен",
        "user_joined": "присоединился к чату",
        "user_left": "покинул чат",
        "duplicate_username": "Имя уже используется",
        "duplicate_rejected": "Имя занято, отказ",
        "public_message": "[Общее]",
        "private_message": "[Личное]",
        "file_transfer": "[Передача файла]",
        "file_broadcast": "[Рассылка файла]",
        "broadcast_message": "[Сообщение сервера]",
        "unknown_command": "Неизвестная команда",
        "usage_kick": "Использование: /kick <имя>",
        "usage_broadcast": "Использование: /broadcast <сооб>",
        "user_not_found": "Пользователь не найден",
        "user_kicked": "отключен",
        "kick_reason": "Отключен админом",
        "server_stopping": "Остановка сервера...",
        "server_stopped": "Сервер остановлен",
        "online_users": "Пользователи онлайн",
        "none": "Нет",
        "error": "Ошибка",
        "system": "Система",
        "input_prompt": "Сервер> ",
        "language_select": "Выберите язык",
        "available_languages": "Доступные языки",
        "current_language": "Текущий язык",
        "invalid_choice": "Неверный выбор",
        "invalid_ip": "Неверный IP-адрес",
    }
}

LANGUAGE_LIST = list(TRANSLATIONS.keys())
LANGUAGE_LIST.sort()

class ChatServerCLI:
    def __init__(self):
        self.server = None
        self.clients = {}
        self.buffer_size = 4096
        self.is_running = False
        self.lock = threading.Lock()
        self.current_language = '中文'

    def t(self, key, *args):
        text = TRANSLATIONS.get(self.current_language, {}).get(key, key)
        if args:
            return text.format(*args)
        return text

    def select_language(self):
        """选择语言"""
        print("=" * 50)
        print('Select Language')
        print("-" * 50)
        for i, lang in enumerate(LANGUAGE_LIST, 1):
            print(f"  {i:2d}. {lang}")
        print("-" * 50)
        print("Sorry,the console server does not support arabic.\nIf you're arabic,I recommend you to use the GUI Server")
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

    def get_local_ips(self):
        """获取本地IP地址列表（与GUI版本一致）"""
        ip_list = []
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            if local_ip != '127.0.0.1':
                ip_list.append(local_ip)
            for iface in socket.getaddrinfo(hostname, None):
                ip = iface[4][0]
                if ip not in ip_list and not ip.startswith('127.') and not ':' in ip:
                    ip_list.append(ip)
        except:
            pass
        if not ip_list:
            ip_list = ['127.0.0.1']
        return ip_list

    def select_ip(self):
        """选择监听IP地址（与GUI版本一致）"""
        ip_list = self.get_local_ips()
        
        print("\n" + "=" * 50)
        print(self.t('select_ip'))
        print("-" * 50)
        print(f"  0. {self.t('all_interfaces')}")
        print(f"\n  {self.t('detected_ips')}:")
        for i, ip in enumerate(ip_list, 1):
            print(f"  {i}. {ip}")
        print(f"  {len(ip_list) + 1}. {self.t('custom_ip')}")
        print("-" * 50)

        while True:
            try:
                choice = input(f"[0-{len(ip_list) + 1}]: ").strip()
                if choice == '0':
                    return '0.0.0.0'
                elif choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(ip_list):
                        return ip_list[idx]
                    elif idx == len(ip_list):
                        return self.input_custom_ip()
                print(f"[{self.t('error')}] {self.t('invalid_choice')}")
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)

    def input_custom_ip(self):
        """输入自定义IP"""
        while True:
            ip = input(f"{self.t('enter_custom_ip')}: ").strip()
            if not ip:
                continue
            # 简单验证IP格式
            parts = ip.split('.')
            if len(parts) == 4:
                try:
                    if all(0 <= int(p) <= 255 for p in parts):
                        return ip
                except ValueError:
                    pass
            print(f"[{self.t('error')}] {self.t('invalid_ip')}")

    def start(self):
        """启动服务器"""
        print(self.t('startup'))

        # 选择IP（与GUI版本一致）
        host = self.select_ip()

        # 输入端口
        while True:
            port_str = input(f"\n{self.t('enter_port')} [55555]: ").strip()
            if not port_str:
                port_str = "55555"
            try:
                port = int(port_str)
                if 1024 <= port <= 65535:
                    break
                print(f"[{self.t('error')}] {self.t('port_range')}")
            except ValueError:
                print(f"[{self.t('error')}] {self.t('port_must_number')}")

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((host, port))
            self.server.listen(5)
            self.server.settimeout(1)
            self.is_running = True

            print("\n" + "=" * 50)
            print(f"[{self.t('system')}] {self.t('server_started')}")
            print(f"[{self.t('system')}] {self.t('listening_on')}: {host}:{port}")
            print(f"[{self.t('system')}] {self.t('waiting_connections')}")
            print(f"[{self.t('system')}] {self.t('press_ctrl_c')}")
            print(f"[{self.t('system')}] {self.t('commands')}")
            print("=" * 50)

            # 启动接收线程
            accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
            accept_thread.start()

            # 主循环处理命令
            self.command_loop()

        except Exception as e:
            print(f"[{self.t('error')}] {str(e)}")
            sys.exit(1)

    def accept_clients(self):
        """接受客户端连接"""
        while self.is_running:
            try:
                client_socket, address = self.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True)
                thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.is_running:
                    print(f"\r[{self.t('error')}] {str(e)}")
                    print(self.t('input_prompt'), end='', flush=True)
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
                    print(f"\r[{self.t('system')}] {self.t('duplicate_rejected')}: {username} {address[0]}:{address[1]}")
                    print(self.t('input_prompt'), end='', flush=True)
                    return

                self.clients[client_socket] = {
                    'username': username,
                    'address': f"{address[0]}:{address[1]}",
                    'connect_time': datetime.now().strftime('%H:%M:%S')
                }

            print(f"\r[{self.t('system')}] {self.t('new_connection')}: {username} {self.t('from_address')} {address[0]}:{address[1]}")
            print(self.t('input_prompt'), end='', flush=True)

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
                    print(f"\r{self.t('public_message')} {username}: {md['message'][:50]}")
                    print(self.t('input_prompt'), end='', flush=True)

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
                print(f"\r[{self.t('error')}] {str(e)}")
                print(self.t('input_prompt'), end='', flush=True)
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
                print(f"\r{self.t('file_transfer')}: {username} -> {target}: {data['filename']}")
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
                print(f"\r{self.t('file_broadcast')}: {username}: {data['filename']}")
            print(self.t('input_prompt'), end='', flush=True)
        except Exception as e:
            print(f"\r[{self.t('error')}] {str(e)}")
            print(self.t('input_prompt'), end='', flush=True)

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
                print(f"\r[{self.t('system')}] {self.t('client_disconnected')}: {username}")
                print(self.t('input_prompt'), end='', flush=True)
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
                    print(f"\r[{self.t('system')}] {username} {self.t('user_kicked')}")
                    print(self.t('input_prompt'), end='', flush=True)
                    return True
        return False

    def command_loop(self):
        while self.is_running:
            try:
                cmd = input(self.t('input_prompt')).strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n[{self.t('system')}] {self.t('server_stopping')}")
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
            print(f"[{self.t('system')}] {self.t('server_stopping')}")
            self.stop()
            sys.exit(0)

        elif command == '/help':
            print(self.t('help_text'))

        elif command == '/users':
            with self.lock:
                if self.clients:
                    users = [info['username'] for info in self.clients.values()]
                    print(f"[{self.t('system')}] {self.t('online_users')}: {', '.join(users)}")
                else:
                    print(f"[{self.t('system')}] {self.t('online_users')}: {self.t('none')}")

        elif command == '/kick':
            if len(parts) >= 2:
                if not self.kick_user(parts[1]):
                    print(f"[{self.t('error')}] {self.t('user_not_found')}: {parts[1]}")
            else:
                print(f"[{self.t('error')}] {self.t('usage_kick')}")

        elif command == '/broadcast':
            if len(parts) >= 2:
                msg = json.dumps({
                    'type': 'system',
                    'message': f"{self.t('broadcast_message')}: {parts[1]}",
                    'time': datetime.now().strftime('%H:%M:%S')
                })
                self.broadcast(msg)
                print(f"{self.t('broadcast_message')}: {parts[1]}")
            else:
                print(f"[{self.t('error')}] {self.t('usage_broadcast')}")

        else:
            print(f"[{self.t('error')}] {self.t('unknown_command')}: {command}")

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
        print(f"[{self.t('system')}] {self.t('server_stopped')}")

    def run(self):
        self.select_language()
        self.start()


if __name__ == "__main__":
    ChatServerCLI().run()
