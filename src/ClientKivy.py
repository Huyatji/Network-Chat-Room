# -*- coding: utf-8 -*-
"""
网络聊天室 - Kivy 移动版
可在 Android/iOS 上运行，桌面端也可用
"""
import socket
import threading
import json
import os
import time
from datetime import datetime
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ListProperty, BooleanProperty, ObjectProperty
from kivy.clock import Clock, mainthread
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform

# ==================== 语言包（与原版完全一致） ====================
TRANSLATIONS = {
    "中文": {"title":"网络聊天室","welcome":"欢迎来到聊天室","username":"用户名:","server_address":"服务器地址:","port":"端口:","connect":"连接","online_users":"在线用户","send":"发送","file":"文件","file_emoji":"📎 文件","me":"我","connecting_success":"成功连接到服务器","connecting_timeout":"连接服务器超时，请检查服务器地址和端口","connection_refused":"服务器拒绝连接，请检查服务器是否启动","connection_failed":"无法连接到服务器","disconnected":"与服务器断开连接","send_failed":"发送失败","file_receive_failed":"文件接收失败","file_size_error":"文件大小信息错误","file_receive_error":"文件接收错误","connection_error":"连接错误","file_sent_to":"文件已发送给","file_broadcast":"文件已广播","file_save_failed":"文件保存失败","file_saved":"文件已保存","send_file_title":"发送文件","send_file_prompt":"未选择用户，发送给所有人?","language_select":"选择语言 / Select Language","usage_hint":"用法: /msg 用户名 消息内容","file_send_failed":"文件发送失败","error":"错误","private_chat_prefix":"[私聊]","private_chat_to":"私聊 →","language":"语言","user_emoji":"👤","user_no_emoji":"*"},
    "བོད་སྐད།": {"title": "དྲ་རྒྱའི་སྐད་ཕྲིན་ཁང་།", "welcome": "སྐད་ཕྲིན་ཁང་ལ་ཕེབས་པར་དགའ་བསུ་ཞུ།", "username": "བེད་སྤྱོད་པའི་མིང་།:", "server_address": "སེར་བར་གྱི་ས་གནས།:", "port": "སྒོ་ཨང་།:", "connect": "མཐུད།", "online_users": "དྲ་ཐོག་བེད་སྤྱོད་པ།", "send": "གཏོང་།", "file": "ཡིག་ཆ།", "file_emoji": "📎 ཡིག་ཆ།", "me": "ང།", "connecting_success": "སེར་བར་ལ་མཐུད་ཐུབ་སོང་།", "connecting_timeout": "སེར་བར་མཐུད་དུས་ཚོད་འགོར་སོང་། སེར་བར་ས་གནས་དང་སྒོ་ཨང་ཞིབ་བཤེར་གནང་།", "connection_refused": "སེར་བར་གྱིས་མཐུད་སྦྲེལ་ཁས་མི་ལེན། སེར་བར་འགོ་ཚུགས་མེད་པ་ཞིབ་བཤེར་གནང་།", "connection_failed": "སེར་བར་ལ་མཐུད་མ་ཐུབ།", "disconnected": "སེར་བར་དང་མཐུད་སྦྲེལ་ཆད་སོང་།", "send_failed": "གཏོང་སྐྱེལ་མ་ཐུབ།", "file_receive_failed": "ཡིག་ཆ་དང་ལེན་མ་ཐུབ།", "file_size_error": "ཡིག་ཆའི་ཆེ་ཆུང་གནས་ཚུལ་ནོར་འཁྲུལ།", "file_receive_error": "ཡིག་ཆ་དང་ལེན་ནོར་འཁྲུལ།", "connection_error": "མཐུད་སྦྲེལ་ནོར་འཁྲུལ།", "file_sent_to": "ཡིག་ཆ་གཏོང་ས་", "file_broadcast": "ཡིག་ཆ་ཚང་མར་བརྒྱུད་སྤེལ་བྱས་ཟིན།", "file_save_failed": "ཡིག་ཆ་ཉར་ཚགས་མ་ཐུབ།", "file_saved": "ཡིག་ཆ་ཉར་ཚགས་བྱས་ཟིན།", "send_file_title": "ཡིག་ཆ་གཏོང་།", "send_file_prompt": "བེད་སྤྱོད་པ་འདེམས་མེད། ཚང་མར་གཏོང་དགོས་སམ།", "language_select": "སྐད་ཡིག་འདེམས། / Select Language", "usage_hint": "བེད་སྤྱོད་ཐབས།: /msg བེད་སྤྱོད་མིང་། སྐད་ཕྲིན་ནང་དོན།", "file_send_failed": "ཡིག་ཆ་གཏོང་སྐྱེལ་མ་ཐུབ།", "error": "ནོར་འཁྲུལ།", "private_chat_prefix": "[སྒེར་གྱི་སྐད་ཕྲིན]", "private_chat_to": "སྒེར་གྱི་སྐད་ཕྲིན →", "language": "སྐད་ཡིག", "user_emoji": "👤", "user_no_emoji": "*"},
    "繁體中文": {"title":"網路聊天室","welcome":"歡迎來到聊天室","username":"使用者名稱:","server_address":"伺服器位址:","port":"連接埠:","connect":"連線","online_users":"線上使用者","send":"傳送","file":"檔案","file_emoji":"📎 檔案","me":"我","connecting_success":"成功連線到伺服器","connecting_timeout":"連線伺服器逾時，請檢查伺服器位址和連接埠","connection_refused":"伺服器拒絕連線，請檢查伺服器是否啟動","connection_failed":"無法連線到伺服器","disconnected":"與伺服器中斷連線","send_failed":"傳送失敗","file_receive_failed":"檔案接收失敗","file_size_error":"檔案大小資訊錯誤","file_receive_error":"檔案接收錯誤","connection_error":"連線錯誤","file_sent_to":"檔案已傳送給","file_broadcast":"檔案已廣播","file_save_failed":"檔案儲存失敗","file_saved":"檔案已儲存","send_file_title":"傳送檔案","send_file_prompt":"未選擇使用者，傳送給所有人?","language_select":"選擇語言 / Select Language","usage_hint":"用法: /msg 使用者名稱 訊息內容","file_send_failed":"檔案傳送失敗","error":"錯誤","private_chat_prefix":"[私聊]","private_chat_to":"私聊 →","language":"語言","user_emoji":"👤","user_no_emoji":"*"},
    "日本語": {"title":"ネットワークチャットルーム","welcome":"チャットルームへようこそ","username":"ユーザー名:","server_address":"サーバーアドレス:","port":"ポート:","connect":"接続","online_users":"オンラインユーザー","send":"送信","file":"ファイル","file_emoji":"📎 ファイル","me":"自分","connecting_success":"サーバーに正常に接続しました","connecting_timeout":"接続がタイムアウトしました","connection_refused":"接続が拒否されました","connection_failed":"サーバーに接続できません","disconnected":"サーバーから切断されました","send_failed":"送信失敗","file_receive_failed":"ファイル受信失敗","file_size_error":"ファイルサイズ情報エラー","file_receive_error":"ファイル受信エラー","connection_error":"接続エラー","file_sent_to":"ファイルを送信しました","file_broadcast":"ファイルをブロードキャストしました","file_save_failed":"ファイル保存失敗","file_saved":"ファイルを保存しました","send_file_title":"ファイル送信","send_file_prompt":"ユーザーが選択されていません。全員に送信しますか？","language_select":"言語選択 / Select Language","usage_hint":"使用法: /msg ユーザー名 メッセージ","file_send_failed":"ファイル送信失敗","error":"エラー","private_chat_prefix":"[プライベート]","private_chat_to":"プライベート →","language":"言語","user_emoji":"👤","user_no_emoji":"*"},
    "한국어": {"title":"네트워크 채팅방","welcome":"채팅방에 오신 것을 환영합니다","username":"사용자 이름:","server_address":"서버 주소:","port":"포트:","connect":"연결","online_users":"온라인 사용자","send":"보내기","file":"파일","file_emoji":"📎 파일","me":"나","connecting_success":"서버에 성공적으로 연결되었습니다","connecting_timeout":"연결 시간 초과","connection_refused":"연결이 거부되었습니다","connection_failed":"서버에 연결할 수 없습니다","disconnected":"서버와 연결이 끊어졌습니다","send_failed":"전송 실패","file_receive_failed":"파일 수신 실패","file_size_error":"파일 크기 정보 오류","file_receive_error":"파일 수신 오류","connection_error":"연결 오류","file_sent_to":"파일을 보냈습니다","file_broadcast":"파일을 방송했습니다","file_save_failed":"파일 저장 실패","file_saved":"파일이 저장되었습니다","send_file_title":"파일 보내기","send_file_prompt":"사용자가 선택되지 않았습니다. 모두에게 보내시겠습니까?","language_select":"언어 선택 / Select Language","usage_hint":"사용법: /msg 사용자이름 메시지","file_send_failed":"파일 전송 실패","error":"오류","private_chat_prefix":"[비공개]","private_chat_to":"비공개 →","language":"언어","user_emoji":"👤","user_no_emoji":"*"},
    "Deutsch": {"title":"Netzwerk-Chatraum","welcome":"Willkommen im Chatraum","username":"Benutzername:","server_address":"Serveradresse:","port":"Port:","connect":"Verbinden","online_users":"Online-Benutzer","send":"Senden","file":"Datei","file_emoji":"📎 Datei","me":"Ich","connecting_success":"Erfolgreich mit dem Server verbunden","connecting_timeout":"Verbindungszeitüberschreitung","connection_refused":"Verbindung abgelehnt","connection_failed":"Keine Verbindung zum Server möglich","disconnected":"Vom Server getrennt","send_failed":"Senden fehlgeschlagen","file_receive_failed":"Dateiempfang fehlgeschlagen","file_size_error":"Dateigrößeninformationen fehlerhaft","file_receive_error":"Dateiempfangsfehler","connection_error":"Verbindungsfehler","file_sent_to":"Datei gesendet an","file_broadcast":"Datei an alle gesendet","file_save_failed":"Datei speichern fehlgeschlagen","file_saved":"Datei gespeichert","send_file_title":"Datei senden","send_file_prompt":"Kein Benutzer ausgewählt, an alle senden?","language_select":"Sprache wählen / Select Language","usage_hint":"Verwendung: /msg Benutzername Nachricht","file_send_failed":"Datei senden fehlgeschlagen","error":"Fehler","private_chat_prefix":"[Privat]","private_chat_to":"Privat →","language":"Sprache","user_emoji":"👤","user_no_emoji":"*"},
    "Italiano": {"title":"Chat Room di Rete","welcome":"Benvenuto nella Chat Room","username":"Nome utente:","server_address":"Indirizzo server:","port":"Porta:","connect":"Connetti","online_users":"Utenti online","send":"Invia","file":"File","file_emoji":"📎 File","me":"Io","connecting_success":"Connesso al server con successo","connecting_timeout":"Timeout connessione","connection_refused":"Connessione rifiutata","connection_failed":"Impossibile connettersi al server","disconnected":"Disconnesso dal server","send_failed":"Invio fallito","file_receive_failed":"Ricezione file fallita","file_size_error":"Errore informazioni dimensione file","file_receive_error":"Errore ricezione file","connection_error":"Errore di connessione","file_sent_to":"File inviato a","file_broadcast":"File trasmesso a tutti","file_save_failed":"Salvataggio file fallito","file_saved":"File salvato","send_file_title":"Invia file","send_file_prompt":"Nessun utente selezionato, inviare a tutti?","language_select":"Seleziona lingua / Select Language","usage_hint":"Uso: /msg nomeutente messaggio","file_send_failed":"Invio file fallito","error":"Errore","private_chat_prefix":"[Privato]","private_chat_to":"Privato →","language":"Lingua","user_emoji":"👤","user_no_emoji":"*"},
    "English": {"title":"Network Chat Room","welcome":"Welcome to the Chat Room","username":"Username:","server_address":"Server Address:","port":"Port:","connect":"Connect","online_users":"Online Users","send":"Send","file":"File","file_emoji":"📎 File","me":"Me","connecting_success":"Successfully connected to server","connecting_timeout":"Connection timeout, please check server address and port","connection_refused":"Connection refused, please check if server is running","connection_failed":"Cannot connect to server","disconnected":"Disconnected from server","send_failed":"Send failed","file_receive_failed":"File receive failed","file_size_error":"File size information error","file_receive_error":"File receive error","connection_error":"Connection error","file_sent_to":"File sent to","file_broadcast":"File broadcast","file_save_failed":"File save failed","file_saved":"File saved","send_file_title":"Send File","send_file_prompt":"No user selected, send to everyone?","language_select":"选择语言 / Select Language","usage_hint":"Usage: /msg username message","file_send_failed":"File send failed","error":"Error","private_chat_prefix":"[Private]","private_chat_to":"Private →","language":"Language","user_emoji":"👤","user_no_emoji":"*"},
    "Français": {"title":"Chat Room Réseau","welcome":"Bienvenue dans le Chat Room","username":"Nom d'utilisateur:","server_address":"Adresse du serveur:","port":"Port:","connect":"Connecter","online_users":"Utilisateurs en ligne","send":"Envoyer","file":"Fichier","file_emoji":"📎 Fichier","me":"Moi","connecting_success":"Connecté au serveur avec succès","connecting_timeout":"Délai de connexion dépassé","connection_refused":"Connexion refusée","connection_failed":"Impossible de se connecter au serveur","disconnected":"Déconnecté du serveur","send_failed":"Échec de l'envoi","file_receive_failed":"Échec de la réception du fichier","file_size_error":"Erreur de taille de fichier","file_receive_error":"Erreur de réception du fichier","connection_error":"Erreur de connexion","file_sent_to":"Fichier envoyé à","file_broadcast":"Fichier diffusé","file_save_failed":"Échec de la sauvegarde du fichier","file_saved":"Fichier sauvegardé","send_file_title":"Envoyer un fichier","send_file_prompt":"Aucun utilisateur sélectionné, envoyer à tout le monde?","language_select":"Sélectionner la langue / Select Language","usage_hint":"Utilisation: /msg utilisateur message","file_send_failed":"Échec de l'envoi du fichier","error":"Erreur","private_chat_prefix":"[Privé]","private_chat_to":"Privé →","language":"Langue","user_emoji":"👤","user_no_emoji":"*"},
    "Español": {"title":"Sala de Chat en Red","welcome":"Bienvenido a la Sala de Chat","username":"Usuario:","server_address":"Dirección del servidor:","port":"Puerto:","connect":"Conectar","online_users":"Usuarios en línea","send":"Enviar","file":"Archivo","file_emoji":"📎 Archivo","me":"Yo","connecting_success":"Conectado al servidor exitosamente","connecting_timeout":"Tiempo de conexión agotado","connection_refused":"Conexión rechazada","connection_failed":"No se puede conectar al servidor","disconnected":"Desconectado del servidor","send_failed":"Envío fallido","file_receive_failed":"Recepción de archivo fallida","file_size_error":"Error de información de tamaño de archivo","file_receive_error":"Error de recepción de archivo","connection_error":"Error de conexión","file_sent_to":"Archivo enviado a","file_broadcast":"Archivo transmitido","file_save_failed":"Error al guardar el archivo","file_saved":"Archivo guardado","send_file_title":"Enviar archivo","send_file_prompt":"¿No se seleccionó usuario, enviar a todos?","language_select":"Seleccionar idioma / Select Language","usage_hint":"Uso: /msg usuario mensaje","file_send_failed":"Error al enviar archivo","error":"Error","private_chat_prefix":"[Privado]","private_chat_to":"Privado →","language":"Idioma","user_emoji":"👤","user_no_emoji":"*"},
    "Русский": {"title":"Сетевой чат","welcome":"Добро пожаловать в чат","username":"Имя пользователя:","server_address":"Адрес сервера:","port":"Порт:","connect":"Подключиться","online_users":"Пользователи онлайн","send":"Отправить","file":"Файл","file_emoji":"📎 Файл","me":"Я","connecting_success":"Успешно подключено к серверу","connecting_timeout":"Время подключения истекло","connection_refused":"Подключение отклонено","connection_failed":"Не удается подключиться к серверу","disconnected":"Отключено от сервера","send_failed":"Ошибка отправки","file_receive_failed":"Ошибка получения файла","file_size_error":"Ошибка информации о размере файла","file_receive_error":"Ошибка приема файла","connection_error":"Ошибка подключения","file_sent_to":"Файл отправлен","file_broadcast":"Файл транслирован","file_save_failed":"Ошибка сохранения файла","file_saved":"Файл сохранен","send_file_title":"Отправить файл","send_file_prompt":"Пользователь не выбран, отправить всем?","language_select":"Выберите язык / Select Language","usage_hint":"Использование: /msg пользователь сообщение","file_send_failed":"Ошибка отправки файла","error":"Ошибка","private_chat_prefix":"[Личное]","private_chat_to":"Личное →","language":"Язык","user_emoji":"👤","user_no_emoji":"*"},
    "Polski": {"title": "Czat internetowy","welcome": "Witamy na czacie","username": "Nazwa użytkownika:","server_address": "Adres serwera:","port": "Port:","connect": "Połącz","online_users": "Użytkownicy online","send": "Wyślij","file": "Plik","file_emoji": "📎 Plik","me": "Ja","connecting_success": "Pomyślnie połączono z serwerem","connecting_timeout": "Przekroczono czas połączenia z serwerem, sprawdź adres serwera i port","connection_refused": "Serwer odrzucił połączenie, sprawdź czy serwer jest uruchomiony","connection_failed": "Nie można połączyć się z serwerem","disconnected": "Rozłączono z serwerem","send_failed": "Wysyłanie nie powiodło się","file_receive_failed": "Odbiór pliku nie powiódł się","file_size_error": "Błąd informacji o rozmiarze pliku","file_receive_error": "Błąd odbioru pliku","connection_error": "Błąd połączenia","file_sent_to": "Plik wysłany do","file_broadcast": "Plik został rozesłany","file_save_failed": "Zapisywanie pliku nie powiodło się","file_saved": "Plik zapisany","send_file_title": "Wyślij plik","send_file_prompt": "Nie wybrano użytkownika, wysłać do wszystkich?","language_select": "Wybierz język / Select Language","usage_hint": "Użycie: /msg nazwa_użytkownika treść_wiadomości","file_send_failed": "Wysyłanie pliku nie powiodło się","error": "Błąd","private_chat_prefix": "[Prywatnie]","private_chat_to": "Prywatna wiadomość →","language": "Język","user_emoji": "👤","user_no_emoji": "*"},
    "Tiếng Việt": {"title": "Phòng chat trực tuyến", "welcome": "Chào mừng đến phòng chat", "username": "Tên người dùng:", "server_address": "Địa chỉ máy chủ:", "port": "Cổng:", "connect": "Kết nối", "online_users": "Người dùng trực tuyến", "send": "Gửi", "file": "Tệp", "file_emoji": "📎 Tệp", "me": "Tôi", "connecting_success": "Kết nối máy chủ thành công", "connecting_timeout": "Kết nối máy chủ quá thời gian, vui lòng kiểm tra địa chỉ máy chủ và cổng", "connection_refused": "Máy chủ từ chối kết nối, vui lòng kiểm tra máy chủ đã khởi động chưa", "connection_failed": "Không thể kết nối máy chủ", "disconnected": "Đã ngắt kết nối với máy chủ", "send_failed": "Gửi thất bại", "file_receive_failed": "Nhận tệp thất bại", "file_size_error": "Lỗi thông tin kích thước tệp", "file_receive_error": "Lỗi nhận tệp", "connection_error": "Lỗi kết nối", "file_sent_to": "Tệp đã gửi cho", "file_broadcast": "Tệp đã phát toàn bộ", "file_save_failed": "Lưu tệp thất bại", "file_saved": "Tệp đã lưu", "send_file_title": "Gửi tệp", "send_file_prompt": "Chưa chọn người dùng, gửi cho tất cả?", "language_select": "Chọn ngôn ngữ / Select Language", "usage_hint": "Cách dùng: /msg tên_người_dùng nội_dung", "file_send_failed": "Gửi tệp thất bại", "error": "Lỗi", "private_chat_prefix": "[Riêng tư]", "private_chat_to": "Nhắn riêng →", "language": "Ngôn ngữ", "user_emoji": "👤", "user_no_emoji": "*"}, 
    "Türkçe": {"title": "İnternet Sohbet Odası", "welcome": "Sohbet odasına hoş geldiniz", "username": "Kullanıcı adı:", "server_address": "Sunucu adresi:", "port": "Port:", "connect": "Bağlan", "online_users": "Çevrimiçi kullanıcılar", "send": "Gönder", "file": "Dosya", "file_emoji": "📎 Dosya", "me": "Ben", "connecting_success": "Sunucuya başarıyla bağlanıldı", "connecting_timeout": "Sunucu bağlantısı zaman aşımına uğradı, lütfen sunucu adresini ve portu kontrol edin", "connection_refused": "Sunucu bağlantıyı reddetti, lütfen sunucunun başlatıldığını kontrol edin", "connection_failed": "Sunucuya bağlanılamadı", "disconnected": "Sunucuyla bağlantı kesildi", "send_failed": "Gönderme başarısız", "file_receive_failed": "Dosya alımı başarısız", "file_size_error": "Dosya boyutu bilgisi hatası", "file_receive_error": "Dosya alma hatası", "connection_error": "Bağlantı hatası", "file_sent_to": "Dosya gönderildi:", "file_broadcast": "Dosya herkese gönderildi", "file_save_failed": "Dosya kaydedilemedi", "file_saved": "Dosya kaydedildi", "send_file_title": "Dosya gönder", "send_file_prompt": "Kullanıcı seçilmedi, herkese gönderilsin mi?", "language_select": "Dil seçin / Select Language", "usage_hint": "Kullanım: /msg kullanıcı_adı mesaj_içeriği", "file_send_failed": "Dosya gönderme başarısız", "error": "Hata", "private_chat_prefix": "[Özel]", "private_chat_to": "Özel sohbet →", "language": "Dil", "user_emoji": "👤", "user_no_emoji": "*"},
    "Bahasa Indonesia": {"title": "Ruang Obrolan Daring", "welcome": "Selamat datang di ruang obrolan", "username": "Nama pengguna:", "server_address": "Alamat server:", "port": "Port:", "connect": "Hubungkan", "online_users": "Pengguna daring", "send": "Kirim", "file": "Berkas", "file_emoji": "📎 Berkas", "me": "Saya", "connecting_success": "Berhasil terhubung ke server", "connecting_timeout": "Koneksi server waktu habis, silakan periksa alamat server dan port", "connection_refused": "Server menolak koneksi, silakan periksa apakah server sudah berjalan", "connection_failed": "Tidak dapat terhubung ke server", "disconnected": "Terputus dari server", "send_failed": "Pengiriman gagal", "file_receive_failed": "Penerimaan berkas gagal", "file_size_error": "Kesalahan informasi ukuran berkas", "file_receive_error": "Kesalahan penerimaan berkas", "connection_error": "Kesalahan koneksi", "file_sent_to": "Berkas dikirim ke", "file_broadcast": "Berkas disiarkan ke semua", "file_save_failed": "Penyimpanan berkas gagal", "file_saved": "Berkas tersimpan", "send_file_title": "Kirim berkas", "send_file_prompt": "Tidak ada pengguna dipilih, kirim ke semua?", "language_select": "Pilih bahasa / Select Language", "usage_hint": "Penggunaan: /msg nama_pengguna isi_pesan", "file_send_failed": "Pengiriman berkas gagal", "error": "Kesalahan", "private_chat_prefix": "[Pribadi]", "private_chat_to": "Obrolan pribadi →", "language": "Bahasa", "user_emoji": "👤", "user_no_emoji": "*"},
    "العربية": {"title":"غرفة الدردشة الشبكية","welcome":"مرحباً بك في غرفة الدردشة","username":"اسم المستخدم:","server_address":"عنوان الخادم:","port":"المنفذ:","connect":"اتصال","online_users":"المستخدمون المتصلون","send":"إرسال","file":"ملف","file_emoji":"📎 ملف","me":"أنا","connecting_success":"تم الاتصال بالخادم بنجاح","connecting_timeout":"انتهت مهلة الاتصال","connection_refused":"تم رفض الاتصال","connection_failed":"لا يمكن الاتصال بالخادم","disconnected":"تم قطع الاتصال بالخادم","send_failed":"فشل الإرسال","file_receive_failed":"فشل استلام الملف","file_size_error":"خطأ في معلومات حجم الملف","file_receive_error":"خطأ في استلام الملف","connection_error":"خطأ في الاتصال","file_sent_to":"تم إرسال الملف إلى","file_broadcast":"تم بث الملف","file_save_failed":"فشل حفظ الملف","file_saved":"تم حفظ الملف","send_file_title":"إرسال ملف","send_file_prompt":"لم يتم تحديد مستخدم، إرسال للجميع؟","language_select":"اختيار اللغة / Select Language","usage_hint":"الاستخدام: /msg اسم المستخدم الرسالة","file_send_failed":"فشل إرسال الملف","error":"خطأ","private_chat_prefix":"[خاص]","private_chat_to":"خاص ←","language":"اللغة","user_emoji":"👤","user_no_emoji":"*"},
    "Ελληνικά": {"title": "Δωμάτιο Συνομιλίας Δικτύου", "welcome": "Καλώς ήρθατε στο δωμάτιο συνομιλίας", "username": "Όνομα χρήστη:", "server_address": "Διεύθυνση διακομιστή:", "port": "Θύρα:", "connect": "Σύνδεση", "online_users": "Συνδεδεμένοι χρήστες", "send": "Αποστολή", "file": "Αρχείο", "file_emoji": "📎 Αρχείο", "me": "Εγώ", "connecting_success": "Επιτυχής σύνδεση με τον διακομιστή", "connecting_timeout": "Λήξη χρονικού ορίου σύνδεσης, ελέγξτε τη διεύθυνση και τη θύρα", "connection_refused": "Ο διακομιστής απέρριψε τη σύνδεση, ελέγξτε αν ο διακομιστής λειτουργεί", "connection_failed": "Αδυναμία σύνδεσης με τον διακομιστή", "disconnected": "Αποσυνδεθήκατε από τον διακομιστή", "send_failed": "Η αποστολή απέτυχε", "file_receive_failed": "Η λήψη αρχείου απέτυχε", "file_size_error": "Σφάλμα πληροφοριών μεγέθους αρχείου", "file_receive_error": "Σφάλμα λήψης αρχείου", "connection_error": "Σφάλμα σύνδεσης", "file_sent_to": "Το αρχείο στάλθηκε στον", "file_broadcast": "Το αρχείο μεταδόθηκε σε όλους", "file_save_failed": "Η αποθήκευση αρχείου απέτυχε", "file_saved": "Το αρχείο αποθηκεύτηκε", "send_file_title": "Αποστολή αρχείου", "send_file_prompt": "Δεν επιλέχθηκε χρήστης, αποστολή σε όλους;", "language_select": "Επιλογή Γλώσσας / Select Language", "usage_hint": "Χρήση: /msg όνομα_χρήστη περιεχόμενο_μηνύματος", "file_send_failed": "Η αποστολή αρχείου απέτυχε", "error": "Σφάλμα", "private_chat_prefix": "[Ιδιωτικό]", "private_chat_to": "Ιδιωτική συνομιλία →", "language": "Γλώσσα", "user_emoji": "👤", "user_no_emoji": "*"}
}

LANGUAGE_LIST = list(TRANSLATIONS.keys())
LANGUAGE_LIST.sort()


class LoginScreen(BoxLayout):
    """登录界面"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(10)
        
        # 语言选择
        lang_box = BoxLayout(size_hint_y=None, height=dp(40))
        lang_box.add_widget(Label(text=self.t('language_select') + ':', size_hint_x=0.4))
        self.lang_spinner = Spinner(
            text='中文',
            values=LANGUAGE_LIST,
            size_hint_x=0.6
        )
        self.lang_spinner.bind(text=self.on_lang_change)
        lang_box.add_widget(self.lang_spinner)
        self.add_widget(lang_box)
        
        # 欢迎标题
        self.welcome_label = Label(
            text=self.t('welcome'),
            font_size=dp(24),
            size_hint_y=None,
            height=dp(60)
        )
        self.add_widget(self.welcome_label)
        
        # 用户名
        self.add_widget(Label(text=self.t('username'), size_hint_y=None, height=dp(30)))
        self.username_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(self.username_input)
        
        # 服务器地址
        self.add_widget(Label(text=self.t('server_address'), size_hint_y=None, height=dp(30)))
        self.host_input = TextInput(
            text='127.0.0.1',
            multiline=False,
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(self.host_input)
        
        # 端口
        self.add_widget(Label(text=self.t('port'), size_hint_y=None, height=dp(30)))
        self.port_input = TextInput(
            text='55555',
            multiline=False,
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(self.port_input)
        
        # 连接按钮
        self.connect_btn = Button(
            text=self.t('connect'),
            size_hint_y=None,
            height=dp(50)
        )
        self.connect_btn.bind(on_press=self.do_connect)
        self.add_widget(self.connect_btn)
        
        # 空白填充
        self.add_widget(Label())
    
    def t(self, key):
        return TRANSLATIONS.get(self.app.current_language, {}).get(key, key)
    
    def on_lang_change(self, instance, value):
        self.app.current_language = value
        self.refresh_ui()
    
    def refresh_ui(self):
        self.welcome_label.text = self.t('welcome')
        self.connect_btn.text = self.t('connect')
        # 更新所有label...（简化处理）
        children = self.children[:]
        for child in children:
            if isinstance(child, Label) and child != self.welcome_label:
                if '用户名' in child.text or 'Username' in child.text:
                    child.text = self.t('username')
                elif '地址' in child.text or 'Address' in child.text:
                    child.text = self.t('server_address')
                elif '端口' in child.text or 'Port' in child.text:
                    child.text = self.t('port')
    
    def do_connect(self, instance):
        username = self.username_input.text.strip()
        host = self.host_input.text.strip()
        try:
            port = int(self.port_input.text.strip())
        except:
            self.show_error(self.t('error'), '端口必须是数字')
            return
        
        if not username:
            self.show_error(self.t('error'), '请输入用户名')
            return
        
        self.app.connect_to_server(username, host, port)
    
    def show_error(self, title, msg):
        popup = Popup(
            title=title,
            content=Label(text=msg),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class UserListItem(RecycleDataViewBehavior, BoxLayout):
    """用户列表项"""
    text = StringProperty()
    index = None
    
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.text = data.get('text', '')
        return super().refresh_view_attrs(rv, index, data)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                # 双击发起私聊
                app = App.get_running_app()
                target = self.text.split(' ', 1)[-1] if ' ' in self.text else self.text
                # 移除" (我)"标记
                target = target.replace(f" ({app.t('me')})", "")
                if target != app.username:
                    app.chat_screen.msg_input.text = f"/msg {target} "
                    app.chat_screen.msg_input.focus = True
        return super().on_touch_down(touch)


class ChatMessage(BoxLayout):
    """聊天消息气泡"""
    message = StringProperty()
    msg_type = StringProperty()  # system, public, private, file, own
    
    def __init__(self, msg_type='public', **kwargs):
        super().__init__(**kwargs)
        self.msg_type = msg_type
        self.size_hint_y = None
        self.padding = dp(5)
        
        if msg_type == 'system':
            self.color = (0.5, 0.5, 0.5, 0.3)
        elif msg_type == 'private':
            self.color = (0.6, 0.2, 0.6, 0.3)
        elif msg_type == 'file':
            self.color = (0.2, 0.4, 0.8, 0.3)
        else:
            self.color = (0.9, 0.9, 0.9, 1)


class ChatScreen(BoxLayout):
    """聊天主界面"""
    
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = dp(5)
        self.spacing = dp(5)
        
        # 顶部语言选择
        top_bar = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
        top_bar.add_widget(Label(text=self.t('language') + ':', size_hint_x=0.3))
        self.lang_spinner = Spinner(
            text=app.current_language,
            values=LANGUAGE_LIST,
            size_hint_x=0.7
        )
        self.lang_spinner.bind(text=self.on_lang_change)
        top_bar.add_widget(self.lang_spinner)
        self.add_widget(top_bar)
        
        # 主体区域：用户列表 + 聊天区
        main_area = BoxLayout(spacing=dp(5))
        
        # 左侧用户列表
        user_panel = BoxLayout(orientation='vertical', size_hint_x=0.3)
        user_panel.add_widget(Label(
            text=self.t('online_users'),
            size_hint_y=None,
            height=dp(30),
            bold=True
        ))
        self.user_rv = RecycleView()
        self.user_rv.data = []
        self.user_rv.viewclass = 'UserListItem'
        self.user_rv.add_widget(RecycleBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            default_size_hint=(1, None)
        ))
        self.user_rv.children[0].bind(minimum_height=self.user_rv.children[0].setter('height'))
        user_panel.add_widget(self.user_rv)
        main_area.add_widget(user_panel)
        
        # 右侧聊天区
        chat_panel = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        # 消息显示
        self.msg_scroll = ScrollView()
        self.msg_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(2),
            padding=dp(5)
        )
        self.msg_layout.bind(minimum_height=self.msg_layout.setter('height'))
        self.msg_scroll.add_widget(self.msg_layout)
        chat_panel.add_widget(self.msg_scroll)
        
        # 输入区
        input_area = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(5))
        
        self.file_btn = Button(
            text=self.t('file_emoji') if '📎' in self.t('file_emoji') else f"[{self.t('file')}]",
            size_hint_x=0.15
        )
        self.file_btn.bind(on_press=self.send_file)
        input_area.add_widget(self.file_btn)
        
        self.msg_input = TextInput(
            multiline=False,
            size_hint_x=0.65
        )
        self.msg_input.bind(on_text_validate=self.send_msg)
        input_area.add_widget(self.msg_input)
        
        send_btn = Button(
            text=self.t('send'),
            size_hint_x=0.2
        )
        send_btn.bind(on_press=self.send_msg)
        input_area.add_widget(send_btn)
        
        chat_panel.add_widget(input_area)
        main_area.add_widget(chat_panel)
        
        self.add_widget(main_area)
    
    def t(self, key):
        return TRANSLATIONS.get(self.app.current_language, {}).get(key, key)
    
    def on_lang_change(self, instance, value):
        self.app.current_language = value
        self.file_btn.text = self.t('file_emoji') if '📎' in self.t('file_emoji') else f"[{self.t('file')}]"
    
    @mainthread
    def display(self, msg, msg_type='public', time_str=None, username=None):
        """在主线程中显示消息"""
        if time_str:
            full_msg = f"[{time_str}] "
        else:
            full_msg = ""
        
        if msg_type == 'public' and username:
            if username == self.app.username:
                full_msg += f"{self.t('me')}: {msg}"
                msg_type = 'own'
            else:
                full_msg += f"{username}: {msg}"
        else:
            full_msg += msg
        
        msg_widget = Label(
            text=full_msg,
            size_hint_y=None,
            text_size=(self.msg_layout.width - dp(20), None),
            halign='left',
            valign='top',
            padding=dp(5)
        )
        
        # 设置颜色
        colors = {
            'system': (0.3, 0.3, 0.3, 1),
            'private': (0.5, 0.1, 0.5, 1),
            'file': (0.1, 0.3, 0.7, 1),
            'own': (0, 0, 0, 1),
            'public': (0.1, 0.1, 0.1, 1)
        }
        msg_widget.color = colors.get(msg_type, (0.1, 0.1, 0.1, 1))
        
        # 设置背景色
        bg_colors = {
            'system': (0.85, 0.85, 0.85, 1),
            'private': (0.9, 0.8, 0.95, 1),
            'file': (0.8, 0.85, 0.95, 1),
            'own': (0.95, 0.95, 1, 1),
            'public': (0.95, 0.95, 0.95, 1)
        }
        
        # 计算高度
        msg_widget.bind(texture_size=msg_widget.setter('size'))
        msg_widget.bind(width=lambda w, v: setattr(w, 'text_size', (v - dp(20), None)))
        
        self.msg_layout.add_widget(msg_widget)
        
        # 自动滚动到底部
        Clock.schedule_once(lambda dt: setattr(self.msg_scroll, 'scroll_y', 0), 0.1)
    
    @mainthread
    def update_user_list(self, users):
        """更新用户列表"""
        self.user_rv.data = []
        for u in users:
            display_name = f"👤 {u}"
            if u == self.app.username:
                display_name += f" ({self.t('me')})"
            self.user_rv.data.append({'text': display_name})
    
    def send_msg(self, instance=None):
        msg = self.msg_input.text.strip()
        if not msg:
            return
        
        if msg.startswith('/msg '):
            parts = msg.split(' ', 2)
            if len(parts) >= 3:
                self.app.send_to_server(json.dumps({
                    'type': 'private',
                    'to': parts[1],
                    'message': parts[2]
                }))
                self.display(
                    f"{self.t('private_chat_to')} {parts[1]}] {parts[2]}",
                    'private',
                    datetime.now().strftime('%H:%M:%S')
                )
            else:
                self.display(self.t('usage_hint'), 'system')
        else:
            self.app.send_to_server(json.dumps({
                'type': 'public',
                'message': msg
            }))
            self.display(msg, 'public', datetime.now().strftime('%H:%M:%S'), self.app.username)
        
        self.msg_input.text = ''
    
    def send_file(self, instance=None):
        """发送文件（移动端使用原生文件选择器）"""
        if platform in ('android', 'ios'):
            # 移动端使用 plyer 或原生选择器
            try:
                from plyer import filechooser
                filechooser.open_file(on_selection=self._on_file_selected)
            except ImportError:
                self.display("文件选择器不可用，请安装 plyer", 'system')
        else:
            # 桌面端使用内置文件选择器
            content = FileChooserListView()
            popup = Popup(
                title=self.t('send_file_title'),
                content=content,
                size_hint=(0.9, 0.9)
            )
            
            def on_select(instance, selection, touch):
                if selection:
                    popup.dismiss()
                    self._send_file_data(selection[0])
            
            content.bind(on_submit=on_select)
            popup.open()
    
    def _on_file_selected(self, selection):
        if selection:
            self._send_file_data(selection[0])
    
    def _send_file_data(self, filepath):
        try:
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            
            self.app.send_to_server(json.dumps({
                'type': 'file_start',
                'filename': filename,
                'size': filesize,
                'to': None
            }))
            
            time.sleep(0.1)
            
            with open(filepath, 'rb') as f:
                self.app.client.sendall(f.read())
            
            self.display(
                f"{self.t('file_broadcast')}: {filename} ({filesize} bytes)",
                'file',
                datetime.now().strftime('%H:%M:%S')
            )
        except Exception as e:
            self.display(f"{self.t('file_send_failed')}: {str(e)}", 'system')


class ChatApp(App):
    """主应用"""
    
    current_language = StringProperty('中文')
    username = StringProperty('')
    client = ObjectProperty(None)
    buffer_size = 4096
    
    def build(self):
        self.title = TRANSLATIONS[self.current_language]['title']
        self.chat_screen = ChatScreen(self)
        return LoginScreen(self)
    
    def t(self, key):
        return TRANSLATIONS.get(self.current_language, {}).get(key, key)
    
    def connect_to_server(self, username, host, port):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(10)
            self.client.connect((host, port))
            
            # 发送用户名
            msg = username.encode('utf-8')
            self.client.sendall(len(msg).to_bytes(4, 'big') + msg)
            
            self.username = username
            self.title = f"{self.t('title')} - {username}"
            
            # 切换到聊天界面
            self.root.clear_widgets()
            self.root.add_widget(self.chat_screen)
            
            # 启动接收线程
            self.recv_thread = threading.Thread(target=self.receive_loop, daemon=True)
            self.recv_thread.start()
            
            self.chat_screen.display(
                f"{self.t('connecting_success')} {host}:{port}",
                'system'
            )
        except socket.timeout:
            self.show_error(self.t('connecting_timeout'))
        except ConnectionRefusedError:
            self.show_error(self.t('connection_refused'))
        except Exception as e:
            self.show_error(f"{self.t('connection_failed')}: {str(e)}")
            if self.client:
                self.client.close()
                self.client = None
    
    def show_error(self, msg):
        popup = Popup(
            title=self.t('error'),
            content=Label(text=msg),
            size_hint=(0.8, 0.3)
        )
        popup.open()
    
    def send_to_server(self, msg):
        """发送消息到服务器"""
        if not self.client:
            return False
        try:
            data = msg.encode('utf-8')
            self.client.sendall(len(data).to_bytes(4, 'big') + data)
            return True
        except:
            return False
    
    def recv_all(self, length):
        """接收指定长度的数据"""
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
        """接收一条消息"""
        header = self.recv_all(4)
        if not header:
            return None
        length = int.from_bytes(header, 'big')
        data = self.recv_all(length)
        return data.decode('utf-8') if data else None
    
    def receive_loop(self):
        """消息接收循环"""
        while True:
            try:
                if not self.client:
                    break
                
                msg = self.recv_msg()
                if not msg:
                    self.chat_screen.display(self.t('disconnected'), 'system')
                    break
                
                try:
                    md = json.loads(msg)
                except:
                    continue
                
                if md['type'] == 'user_list':
                    self.chat_screen.update_user_list(md['users'])
                elif md['type'] == 'system':
                    self.chat_screen.display(md['message'], 'system', md.get('time'))
                elif md['type'] == 'public':
                    self.chat_screen.display(
                        md['message'], 'public', md.get('time'), md['username']
                    )
                elif md['type'] == 'private':
                    self.chat_screen.display(
                        f"{self.t('private_chat_prefix')} {md['from']}: {md['message']}",
                        'private',
                        md.get('time')
                    )
                elif md['type'] == 'file':
                    try:
                        size_bytes = self.recv_all(8)
                        if size_bytes and len(size_bytes) == 8:
                            file_size = int.from_bytes(size_bytes, 'big')
                            file_data = self.recv_all(file_size)
                            if file_data:
                                self.save_file(md, file_data)
                            else:
                                self.chat_screen.display(
                                    self.t('file_receive_failed'), 'system'
                                )
                        else:
                            self.chat_screen.display(
                                self.t('file_size_error'), 'system'
                            )
                    except Exception as e:
                        self.chat_screen.display(
                            f"{self.t('file_receive_error')}: {str(e)}", 'system'
                        )
            except Exception as e:
                if self.client:
                    self.chat_screen.display(
                        f"{self.t('connection_error')}: {str(e)}", 'system'
                    )
                break
    
    def save_file(self, info, data):
        """保存接收到的文件"""
        save_dir = Path('received')
        save_dir.mkdir(exist_ok=True)
        
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{info.get('from', 'unknown')}_{info['filename']}"
        filepath = save_dir / filename
        
        try:
            filepath.write_bytes(data)
            self.chat_screen.display(
                f"{self.t('file_saved')}: {filepath} ({len(data)} bytes)",
                'file'
            )
        except Exception as e:
            self.chat_screen.display(
                f"{self.t('file_save_failed')}: {str(e)}", 'system'
            )
    
    def on_stop(self):
        """应用关闭时清理"""
        if self.client:
            try:
                self.client.close()
            except:
                pass


if __name__ == '__main__':
    ChatApp().run()
