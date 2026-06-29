# -*- coding: utf-8 -*-
import socket
import threading
import json
import os
import time
import sys
import locale
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QTextEdit,
    QLineEdit, QComboBox, QFrame, QSplitter, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QFontDatabase

# ==================== 语言包 ====================
TRANSLATIONS = {
    "简体中文": {"title":"网络聊天室","welcome":"欢迎来到聊天室","username":"用户名:","server_address":"服务器地址:","port":"端口:","connect":"连接","online_users":"在线用户","send":"发送","file":"文件","file_emoji":"📎 文件","me":"我","connecting_success":"成功连接到服务器","connecting_timeout":"连接服务器超时，请检查服务器地址和端口","connection_refused":"服务器拒绝连接，请检查服务器是否启动","connection_failed":"无法连接到服务器","disconnected":"与服务器断开连接","send_failed":"发送失败","file_receive_failed":"文件接收失败","file_size_error":"文件大小信息错误","file_receive_error":"文件接收错误","connection_error":"连接错误","file_sent_to":"文件已发送给","file_broadcast":"文件已广播","file_save_failed":"文件保存失败","file_saved":"文件已保存","send_file_title":"发送文件","send_file_prompt":"未选择用户，发送给所有人?","language_select":"选择语言","usage_hint":"用法: /msg 用户名 消息内容","file_send_failed":"文件发送失败","error":"错误","private_chat_prefix":"[私聊]","private_chat_to":"私聊 →","language":"语言","user_emoji":"👤","user_no_emoji":"*","placeholder":"输入消息..."},
    "བོད་སྐད།": {"title": "དྲ་རྒྱའི་སྐད་ཕྲིན་ཁང་།", "welcome": "སྐད་ཕྲིན་ཁང་ལ་ཕེབས་པར་དགའ་བསུ་ཞུ།", "username": "བེད་སྤྱོད་པའི་མིང་།:", "server_address": "སེར་བར་གྱི་ས་གནས།:", "port": "སྒོ་ཨང་།:", "connect": "མཐུད།", "online_users": "དྲ་ཐོག་བེད་སྤྱོད་པ།", "send": "གཏོང་།", "file": "ཡིག་ཆ།", "file_emoji": "📎 ཡིག་ཆ།", "me": "ང།", "connecting_success": "སེར་བར་ལ་མཐུད་ཐུབ་སོང་།", "connecting_timeout": "སེར་བར་མཐུད་དུས་ཚོད་འགོར་སོང་། སེར་བར་ས་གནས་དང་སྒོ་ཨང་ཞིབ་བཤེར་གནང་།", "connection_refused": "སེར་བར་གྱིས་མཐུད་སྦྲེལ་ཁས་མི་ལེན། སེར་བར་འགོ་ཚུགས་མེད་པ་ཞིབ་བཤེར་གནང་།", "connection_failed": "སེར་བར་ལ་མཐུད་མ་ཐུབ།", "disconnected": "སེར་བར་དང་མཐུད་སྦྲེལ་ཆད་སོང་།", "send_failed": "གཏོང་སྐྱེལ་མ་ཐུབ།", "file_receive_failed": "ཡིག་ཆ་དང་ལེན་མ་ཐུབ།", "file_size_error": "ཡིག་ཆའི་ཆེ་ཆུང་གནས་ཚུལ་ནོར་འཁྲུལ།", "file_receive_error": "ཡིག་ཆ་དང་ལེན་ནོར་འཁྲུལ།", "connection_error": "མཐུད་སྦྲེལ་ནོར་འཁྲུལ།", "file_sent_to": "ཡིག་ཆ་གཏོང་ས་", "file_broadcast": "ཡིག་ཆ་ཚང་མར་བརྒྱུད་སྤེལ་བྱས་ཟིན།", "file_save_failed": "ཡིག་ཆ་ཉར་ཚགས་མ་ཐུབ།", "file_saved": "ཡིག་ཆ་ཉར་ཚགས་བྱས་ཟིན།", "send_file_title": "ཡིག་ཆ་གཏོང་།", "send_file_prompt": "བེད་སྤྱོད་པ་འདེམས་མེད། ཚང་མར་གཏོང་དགོས་སམ།", "language_select": "སྐད་ཡིག་འདེམས།", "usage_hint": "བེད་སྤྱོད་ཐབས།: /msg བེད་སྤྱོད་མིང་། སྐད་ཕྲིན་ནང་དོན།", "file_send_failed": "ཡིག་ཆ་གཏོང་སྐྱེལ་མ་ཐུབ།", "error": "ནོར་འཁྲུལ།", "private_chat_prefix": "[སྒེར་གྱི་སྐད་ཕྲིན]", "private_chat_to": "སྒེར་གྱི་སྐད་ཕྲིན →", "language": "སྐད་ཡིག", "user_emoji": "👤", "user_no_emoji": "*", "placeholder":"ཡིག་ཟམ་ནང་དུ་འཇུག་རོགས།"},
    "繁體中文": {"title":"網路聊天室","welcome":"歡迎來到聊天室","username":"使用者名稱:","server_address":"伺服器位址:","port":"連接埠:","connect":"連線","online_users":"線上使用者","send":"傳送","file":"檔案","file_emoji":"📎 檔案","me":"我","connecting_success":"成功連線到伺服器","connecting_timeout":"連線伺服器逾時，請檢查伺服器位址和連接埠","connection_refused":"伺服器拒絕連線，請檢查伺服器是否啟動","connection_failed":"無法連線到伺服器","disconnected":"與伺服器中斷連線","send_failed":"傳送失敗","file_receive_failed":"檔案接收失敗","file_size_error":"檔案大小資訊錯誤","file_receive_error":"檔案接收錯誤","connection_error":"連線錯誤","file_sent_to":"檔案已傳送給","file_broadcast":"檔案已廣播","file_save_failed":"檔案儲存失敗","file_saved":"檔案已儲存","send_file_title":"傳送檔案","send_file_prompt":"未選擇使用者，傳送給所有人?","language_select":"選擇語言","usage_hint":"用法: /msg 使用者名稱 訊息內容","file_send_failed":"檔案傳送失敗","error":"錯誤","private_chat_prefix":"[私聊]","private_chat_to":"私聊 →","language":"語言","user_emoji":"👤","user_no_emoji":"*","placeholder":"輸入訊息..."},
    "日本語": {"title":"ネットワークチャットルーム","welcome":"チャットルームへようこそ","username":"ユーザー名:","server_address":"サーバーアドレス:","port":"ポート:","connect":"接続","online_users":"オンラインユーザー","send":"送信","file":"ファイル","file_emoji":"📎 ファイル","me":"自分","connecting_success":"サーバーに正常に接続しました","connecting_timeout":"接続がタイムアウトしました","connection_refused":"接続が拒否されました","connection_failed":"サーバーに接続できません","disconnected":"サーバーから切断されました","send_failed":"送信失敗","file_receive_failed":"ファイル受信失敗","file_size_error":"ファイルサイズ情報エラー","file_receive_error":"ファイル受信エラー","connection_error":"接続エラー","file_sent_to":"ファイルを送信しました","file_broadcast":"ファイルをブロードキャストしました","file_save_failed":"ファイル保存失敗","file_saved":"ファイルを保存しました","send_file_title":"ファイル送信","send_file_prompt":"ユーザーが選択されていません。全員に送信しますか？","language_select":"言語選択","usage_hint":"使用法: /msg ユーザー名 メッセージ","file_send_failed":"ファイル送信失敗","error":"エラー","private_chat_prefix":"[プライベート]","private_chat_to":"プライベート →","language":"言語","user_emoji":"👤","user_no_emoji":"*","placeholder":"メッセージを入力..."},
    "한국어": {"title":"네트워크 채팅방","welcome":"채팅방에 오신 것을 환영합니다","username":"사용자 이름:","server_address":"서버 주소:","port":"포트:","connect":"연결","online_users":"온라인 사용자","send":"보내기","file":"파일","file_emoji":"📎 파일","me":"나","connecting_success":"서버에 성공적으로 연결되었습니다","connecting_timeout":"연결 시간 초과","connection_refused":"연결이 거부되었습니다","connection_failed":"서버에 연결할 수 없습니다","disconnected":"서버와 연결이 끊어졌습니다","send_failed":"전송 실패","file_receive_failed":"파일 수신 실패","file_size_error":"파일 크기 정보 오류","file_receive_error":"파일 수신 오류","connection_error":"연결 오류","file_sent_to":"파일을 보냈습니다","file_broadcast":"파일을 방송했습니다","file_save_failed":"파일 저장 실패","file_saved":"파일이 저장되었습니다","send_file_title":"파일 보내기","send_file_prompt":"사용자가 선택되지 않았습니다. 모두에게 보내시겠습니까?","language_select":"언어 선택","usage_hint":"사용법: /msg 사용자이름 메시지","file_send_failed":"파일 전송 실패","error":"오류","private_chat_prefix":"[비공개]","private_chat_to":"비공개 →","language":"언어","user_emoji":"👤","user_no_emoji":"*","placeholder":"메시지 입력..."},
    "Deutsch": {"title":"Netzwerk-Chatraum","welcome":"Willkommen im Chatraum","username":"Benutzername:","server_address":"Serveradresse:","port":"Port:","connect":"Verbinden","online_users":"Online-Benutzer","send":"Senden","file":"Datei","file_emoji":"📎 Datei","me":"Ich","connecting_success":"Erfolgreich mit dem Server verbunden","connecting_timeout":"Verbindungszeitüberschreitung","connection_refused":"Verbindung abgelehnt","connection_failed":"Keine Verbindung zum Server möglich","disconnected":"Vom Server getrennt","send_failed":"Senden fehlgeschlagen","file_receive_failed":"Dateiempfang fehlgeschlagen","file_size_error":"Dateigrößeninformationen fehlerhaft","file_receive_error":"Dateiempfangsfehler","connection_error":"Verbindungsfehler","file_sent_to":"Datei gesendet an","file_broadcast":"Datei an alle gesendet","file_save_failed":"Datei speichern fehlgeschlagen","file_saved":"Datei gespeichert","send_file_title":"Datei senden","send_file_prompt":"Kein Benutzer ausgewählt, an alle senden?","language_select":"Sprache wählen","usage_hint":"Verwendung: /msg Benutzername Nachricht","file_send_failed":"Datei senden fehlgeschlagen","error":"Fehler","private_chat_prefix":"[Privat]","private_chat_to":"Privat →","language":"Sprache","user_emoji":"👤","user_no_emoji":"*","placeholder":"Nachricht eingeben..."},
    "Italiano": {"title":"Chat Room di Rete","welcome":"Benvenuto nella Chat Room","username":"Nome utente:","server_address":"Indirizzo server:","port":"Porta:","connect":"Connetti","online_users":"Utenti online","send":"Invia","file":"File","file_emoji":"📎 File","me":"Io","connecting_success":"Connesso al server con successo","connecting_timeout":"Timeout connessione","connection_refused":"Connessione rifiutata","connection_failed":"Impossibile connettersi al server","disconnected":"Disconnesso dal server","send_failed":"Invio fallito","file_receive_failed":"Ricezione file fallita","file_size_error":"Errore informazioni dimensione file","file_receive_error":"Errore ricezione file","connection_error":"Errore di connessione","file_sent_to":"File inviato a","file_broadcast":"File trasmesso a tutti","file_save_failed":"Salvataggio file fallito","file_saved":"File salvato","send_file_title":"Invia file","send_file_prompt":"Nessun utente selezionato, inviare a tutti?","language_select":"Seleziona lingua","usage_hint":"Uso: /msg nomeutente messaggio","file_send_failed":"Invio file fallito","error":"Errore","private_chat_prefix":"[Privato]","private_chat_to":"Privato →","language":"Lingua","user_emoji":"👤","user_no_emoji":"*","placeholder":"Inserisci messaggio..."},
    "English": {"title":"Network Chat Room","welcome":"Welcome to the Chat Room","username":"Username:","server_address":"Server Address:","port":"Port:","connect":"Connect","online_users":"Online Users","send":"Send","file":"File","file_emoji":"📎 File","me":"Me","connecting_success":"Successfully connected to server","connecting_timeout":"Connection timeout, please check server address and port","connection_refused":"Connection refused, please check if server is running","connection_failed":"Cannot connect to server","disconnected":"Disconnected from server","send_failed":"Send failed","file_receive_failed":"File receive failed","file_size_error":"File size information error","file_receive_error":"File receive error","connection_error":"Connection error","file_sent_to":"File sent to","file_broadcast":"File broadcast","file_save_failed":"File save failed","file_saved":"File saved","send_file_title":"Send File","send_file_prompt":"No user selected, send to everyone?","language_select":"Select Language","usage_hint":"Usage: /msg username message","file_send_failed":"File send failed","error":"Error","private_chat_prefix":"[Private]","private_chat_to":"Private →","language":"Language","user_emoji":"👤","user_no_emoji":"*","placeholder":"Type a message..."},
    "Français": {"title":"Chat Room Réseau","welcome":"Bienvenue dans le Chat Room","username":"Nom d'utilisateur:","server_address":"Adresse du serveur:","port":"Port:","connect":"Connecter","online_users":"Utilisateurs en ligne","send":"Envoyer","file":"Fichier","file_emoji":"📎 Fichier","me":"Moi","connecting_success":"Connecté au serveur avec succès","connecting_timeout":"Délai de connexion dépassé","connection_refused":"Connexion refusée","connection_failed":"Impossible de se connecter au serveur","disconnected":"Déconnecté du serveur","send_failed":"Échec de l'envoi","file_receive_failed":"Échec de la réception du fichier","file_size_error":"Erreur de taille de fichier","file_receive_error":"Erreur de réception du fichier","connection_error":"Erreur de connexion","file_sent_to":"Fichier envoyé à","file_broadcast":"Fichier diffusé","file_save_failed":"Échec de la sauvegarde du fichier","file_saved":"Fichier sauvegardé","send_file_title":"Envoyer un fichier","send_file_prompt":"Aucun utilisateur sélectionné, envoyer à tout le monde?","language_select":"Sélectionner la langue","usage_hint":"Utilisation: /msg utilisateur message","file_send_failed":"Échec de l'envoi du fichier","error":"Erreur","private_chat_prefix":"[Privé]","private_chat_to":"Privé →","language":"Langue","user_emoji":"👤","user_no_emoji":"*","placeholder":"Saisir un message..."},
    "Español": {"title":"Sala de Chat en Red","welcome":"Bienvenido a la Sala de Chat","username":"Usuario:","server_address":"Dirección del servidor:","port":"Puerto:","connect":"Conectar","online_users":"Usuarios en línea","send":"Enviar","file":"Archivo","file_emoji":"📎 Archivo","me":"Yo","connecting_success":"Conectado al servidor exitosamente","connecting_timeout":"Tiempo de conexión agotado","connection_refused":"Conexión rechazada","connection_failed":"No se puede conectar al servidor","disconnected":"Desconectado del servidor","send_failed":"Envío fallido","file_receive_failed":"Recepción de archivo fallida","file_size_error":"Error de información de tamaño de archivo","file_receive_error":"Error de recepción de archivo","connection_error":"Error de conexión","file_sent_to":"Archivo enviado a","file_broadcast":"Archivo transmitido","file_save_failed":"Error al guardar el archivo","file_saved":"Archivo guardado","send_file_title":"Enviar archivo","send_file_prompt":"¿No se seleccionó usuario, enviar a todos?","language_select":"Seleccionar idioma","usage_hint":"Uso: /msg usuario mensaje","file_send_failed":"Error al enviar archivo","error":"Error","private_chat_prefix":"[Privado]","private_chat_to":"Privado →","language":"Idioma","user_emoji":"👤","user_no_emoji":"*","placeholder":"Escribir mensaje..."},
    "Русский": {"title":"Сетевой чат","welcome":"Добро пожаловать в чат","username":"Имя пользователя:","server_address":"Адрес сервера:","port":"Порт:","connect":"Подключиться","online_users":"Пользователи онлайн","send":"Отправить","file":"Файл","file_emoji":"📎 Файл","me":"Я","connecting_success":"Успешно подключено к серверу","connecting_timeout":"Время подключения истекло","connection_refused":"Подключение отклонено","connection_failed":"Не удается подключиться к серверу","disconnected":"Отключено от сервера","send_failed":"Ошибка отправки","file_receive_failed":"Ошибка получения файла","file_size_error":"Ошибка информации о размере файла","file_receive_error":"Ошибка приема файла","connection_error":"Ошибка подключения","file_sent_to":"Файл отправлен","file_broadcast":"Файл транслирован","file_save_failed":"Ошибка сохранения файла","file_saved":"Файл сохранен","send_file_title":"Отправить файл","send_file_prompt":"Пользователь не выбран, отправить всем?","language_select":"Выберите язык","usage_hint":"Использование: /msg пользователь сообщение","file_send_failed":"Ошибка отправки файла","error":"Ошибка","private_chat_prefix":"[Личное]","private_chat_to":"Личное →","language":"Язык","user_emoji":"👤","user_no_emoji":"*","placeholder":"Введите сообщение..."},
    "Polski": {"title":"Czat internetowy","welcome":"Witamy na czacie","username":"Nazwa użytkownika:","server_address":"Adres serwera:","port":"Port:","connect":"Połącz","online_users":"Użytkownicy online","send":"Wyślij","file":"Plik","file_emoji":"📎 Plik","me":"Ja","connecting_success":"Pomyślnie połączono z serwerem","connecting_timeout":"Przekroczono czas połączenia z serwerem, sprawdź adres serwera i port","connection_refused":"Serwer odrzucił połączenie, sprawdź czy serwer jest uruchomiony","connection_failed":"Nie można połączyć się z serwerem","disconnected":"Rozłączono z serwerem","send_failed":"Wysyłanie nie powiodło się","file_receive_failed":"Odbiór pliku nie powiódł się","file_size_error":"Błąd informacji o rozmiarze pliku","file_receive_error":"Błąd odbioru pliku","connection_error":"Błąd połączenia","file_sent_to":"Plik wysłany do","file_broadcast":"Plik został rozesłany","file_save_failed":"Zapisywanie pliku nie powiodło się","file_saved":"Plik zapisany","send_file_title":"Wyślij plik","send_file_prompt":"Nie wybrano użytkownika, wysłać do wszystkich?","language_select":"Wybierz język","usage_hint":"Użycie: /msg nazwa_użytkownika treść_wiadomości","file_send_failed":"Wysyłanie pliku nie powiodło się","error":"Błąd","private_chat_prefix":"[Prywatnie]","private_chat_to":"Prywatna wiadomość →","language":"Język","user_emoji":"👤","user_no_emoji":"*","placeholder":"Wpisz wiadomość..."},
    "Tiếng Việt": {"title":"Phòng chat trực tuyến","welcome":"Chào mừng đến phòng chat","username":"Tên người dùng:","server_address":"Địa chỉ máy chủ:","port":"Cổng:","connect":"Kết nối","online_users":"Người dùng trực tuyến","send":"Gửi","file":"Tệp","file_emoji":"📎 Tệp","me":"Tôi","connecting_success":"Kết nối máy chủ thành công","connecting_timeout":"Kết nối máy chủ quá thời gian, vui lòng kiểm tra địa chỉ máy chủ và cổng","connection_refused":"Máy chủ từ chối kết nối, vui lòng kiểm tra máy chủ đã khởi động chưa","connection_failed":"Không thể kết nối máy chủ","disconnected":"Đã ngắt kết nối với máy chủ","send_failed":"Gửi thất bại","file_receive_failed":"Nhận tệp thất bại","file_size_error":"Lỗi thông tin kích thước tệp","file_receive_error":"Lỗi nhận tệp","connection_error":"Lỗi kết nối","file_sent_to":"Tệp đã gửi cho","file_broadcast":"Tệp đã phát toàn bộ","file_save_failed":"Lưu tệp thất bại","file_saved":"Tệp đã lưu","send_file_title":"Gửi tệp","send_file_prompt":"Chưa chọn người dùng, gửi cho tất cả?","language_select":"Chọn ngôn ngữ","usage_hint":"Cách dùng: /msg tên_người_dùng nội_dung","file_send_failed":"Gửi tệp thất bại","error":"Lỗi","private_chat_prefix":"[Riêng tư]","private_chat_to":"Nhắn riêng →","language":"Ngôn ngữ","user_emoji":"👤","user_no_emoji":"*","placeholder":"Nhập tin nhắn..."},
    "Türkçe": {"title":"İnternet Sohbet Odası","welcome":"Sohbet odasına hoş geldiniz","username":"Kullanıcı adı:","server_address":"Sunucu adresi:","port":"Port:","connect":"Bağlan","online_users":"Çevrimiçi kullanıcılar","send":"Gönder","file":"Dosya","file_emoji":"📎 Dosya","me":"Ben","connecting_success":"Sunucuya başarıyla bağlanıldı","connecting_timeout":"Sunucu bağlantısı zaman aşımına uğradı, lütfen sunucu adresini ve portu kontrol edin","connection_refused":"Sunucu bağlantıyı reddetti, lütfen sunucunun başlatıldığını kontrol edin","connection_failed":"Sunucuya bağlanılamadı","disconnected":"Sunucuyla bağlantı kesildi","send_failed":"Gönderme başarısız","file_receive_failed":"Dosya alımı başarısız","file_size_error":"Dosya boyutu bilgisi hatası","file_receive_error":"Dosya alma hatası","connection_error":"Bağlantı hatası","file_sent_to":"Dosya gönderildi:","file_broadcast":"Dosya herkese gönderildi","file_save_failed":"Dosya kaydedilemedi","file_saved":"Dosya kaydedildi","send_file_title":"Dosya gönder","send_file_prompt":"Kullanıcı seçilmedi, herkese gönderilsin mi?","language_select":"Dil seçin","usage_hint":"Kullanım: /msg kullanıcı_adı mesaj_içeriği","file_send_failed":"Dosya gönderme başarısız","error":"Hata","private_chat_prefix":"[Özel]","private_chat_to":"Özel sohbet →","language":"Dil","user_emoji":"👤","user_no_emoji":"*","placeholder":"Mesajınızı yazın..."},
    "Bahasa Indonesia": {"title":"Ruang Obrolan Daring","welcome":"Selamat datang di ruang obrolan","username":"Nama pengguna:","server_address":"Alamat server:","port":"Port:","connect":"Hubungkan","online_users":"Pengguna daring","send":"Kirim","file":"Berkas","file_emoji":"📎 Berkas","me":"Saya","connecting_success":"Berhasil terhubung ke server","connecting_timeout":"Koneksi server waktu habis, silakan periksa alamat server dan port","connection_refused":"Server menolak koneksi, silakan periksa apakah server sudah berjalan","connection_failed":"Tidak dapat terhubung ke server","disconnected":"Terputus dari server","send_failed":"Pengiriman gagal","file_receive_failed":"Penerimaan berkas gagal","file_size_error":"Kesalahan informasi ukuran berkas","file_receive_error":"Kesalahan penerimaan berkas","connection_error":"Kesalahan koneksi","file_sent_to":"Berkas dikirim ke","file_broadcast":"Berkas disiarkan ke semua","file_save_failed":"Penyimpanan berkas gagal","file_saved":"Berkas tersimpan","send_file_title":"Kirim berkas","send_file_prompt":"Tidak ada pengguna dipilih, kirim ke semua?","language_select":"Pilih bahasa","usage_hint":"Penggunaan: /msg nama_pengguna isi_pesan","file_send_failed":"Pengiriman berkas gagal","error":"Kesalahan","private_chat_prefix":"[Pribadi]","private_chat_to":"Obrolan pribadi →","language":"Bahasa","user_emoji":"👤","user_no_emoji":"*","placeholder":"Ketik pesan..."},
    "العربية": {"title":"غرفة الدردشة الشبكية","welcome":"مرحباً بك في غرفة الدردشة","username":"اسم المستخدم:","server_address":"عنوان الخادم:","port":"المنفذ:","connect":"اتصال","online_users":"المستخدمون المتصلون","send":"إرسال","file":"ملف","file_emoji":"📎 ملف","me":"أنا","connecting_success":"تم الاتصال بالخادم بنجاح","connecting_timeout":"انتهت مهلة الاتصال","connection_refused":"تم رفض الاتصال","connection_failed":"لا يمكن الاتصال بالخادم","disconnected":"تم قطع الاتصال بالخادم","send_failed":"فشل الإرسال","file_receive_failed":"فشل استلام الملف","file_size_error":"خطأ في معلومات حجم الملف","file_receive_error":"خطأ في استلام الملف","connection_error":"خطأ في الاتصال","file_sent_to":"تم إرسال الملف إلى","file_broadcast":"تم بث الملف","file_save_failed":"فشل حفظ الملف","file_saved":"تم حفظ الملف","send_file_title":"إرسال ملف","send_file_prompt":"لم يتم تحديد مستخدم، إرسال للجميع؟","language_select":"اختيار اللغة","usage_hint":"الاستخدام: /msg اسم المستخدم الرسالة","file_send_failed":"فشل إرسال الملف","error":"خطأ","private_chat_prefix":"[خاص]","private_chat_to":"خاص ←","language":"اللغة","user_emoji":"👤","user_no_emoji":"*","placeholder":"أدخل رسالة..."},
    "Ελληνικά": {"title":"Δωμάτιο Συνομιλίας Δικτύου","welcome":"Καλώς ήρθατε στο δωμάτιο συνομιλίας","username":"Όνομα χρήστη:","server_address":"Διεύθυνση διακομιστή:","port":"Θύρα:","connect":"Σύνδεση","online_users":"Συνδεδεμένοι χρήστες","send":"Αποστολή","file":"Αρχείο","file_emoji":"📎 Αρχείο","me":"Εγώ","connecting_success":"Επιτυχής σύνδεση με τον διακομιστή","connecting_timeout":"Λήξη χρονικού ορίου σύνδεσης, ελέγξτε τη διεύθυνση και τη θύρα","connection_refused":"Ο διακομιστής απέρριψε τη σύνδεση, ελέγξτε αν ο διακομιστής λειτουργεί","connection_failed":"Αδυναμία σύνδεσης με τον διακομιστή","disconnected":"Αποσυνδεθήκατε από τον διακομιστή","send_failed":"Η αποστολή απέτυχε","file_receive_failed":"Η λήψη αρχείου απέτυχε","file_size_error":"Σφάλμα πληροφοριών μεγέθους αρχείου","file_receive_error":"Σφάλμα λήψης αρχείου","connection_error":"Σφάλμα σύνδεσης","file_sent_to":"Το αρχείο στάλθηκε στον","file_broadcast":"Το αρχείο μεταδόθηκε σε όλους","file_save_failed":"Η αποθήκευση αρχείου απέτυχε","file_saved":"Το αρχείο αποθηκεύτηκε","send_file_title":"Αποστολή αρχείου","send_file_prompt":"Δεν επιλέχθηκε χρήστης, αποστολή σε όλους;","language_select":"Επιλογή Γλώσσας","usage_hint":"Χρήση: /msg όνομα_χρήστη περιεχόμενο_μηνύματος","file_send_failed":"Η αποστολή αρχείου απέτυχε","error":"Σφάλμα","private_chat_prefix":"[Ιδιωτικό]","private_chat_to":"Ιδιωτική συνομιλία →","language":"Γλώσσα","user_emoji":"👤","user_no_emoji":"*","placeholder":"Εισάγετε μήνυμα..."},
}

LANGUAGE_LIST = list(TRANSLATIONS.keys())
LANGUAGE_LIST.sort()

# ==================== 字体配置 ====================
NERD_FONT_FALLBACKS = [
    # 现代全能
    #   NF
    "Maple Mono NF CN", "Sarasa Mono SC Nerd", # CJK
    'JetBrains Mono Nerd Font', 'Hasklug Nerd Font', #Lig
    'Hack Nerd Font',"Fira Code NF", 'Source Code Pro Nerd Font',#Popular
    "Fira Mono NF",
    # thinnnnnnnnnnn
    "Iosevka Custom Nerd Font",
    # 0.5 
    "M+ Nerd Font",
    # Which Editor can come and recongnize your son？
    "Cascadia Code NF","CaskaydiaCove Nerd Font",
    #Use it and you know why it named 'Envy'
    "EnvyCodeR Nerd Font"
]
LANG_CODE_MAP = {
    'zh-cn': '中文', 'zh-tw': '繁體中文', 'ja-jp': '日本語', 'ko-kr': '한국어',
    'ar-sa': 'العربية', 'en-us': 'English', 'de-de': 'Deutsch', 'it-it': 'Italiano',
    'fr-fr': 'Français', 'es-es': 'Español', 'ru-ru': 'Русский','pl-pl': 'Polski',
    'vi-vn': 'Tiếng Việt','tr-tr':'Türkçe','id-id':'Bahasa Indonesia','bo-cn':'བོད་སྐད།',
    'el-gr':"Ελληνικά"
}
LANG_KEY_TO_CODE = {v: k for k, v in LANG_CODE_MAP.items()}


SPECIAL_FONT_KEYS = ["zh-cn","bo-cn","zh-tw","ja-jp","ko-kr","ar-sa","vi-vn"]
SPECIAL_FONT_VALUES = [
    ["Maple Mono NF CN","Maple Mono NL CN","Cascadia Next SC","Microsoft YaHei UI","Microsoft YaHei","PingFang SC","SimHei","SimSun"],
    ["Misans Tibetan","Kailasa","Monlam Bodyig","Microsoft Himalaya"],
    ["Noto Sans Mono CJK TC","Cascadia Next TC","Microsoft JhengHei UI","Microsoft JhengHei","PingFang TC","MingLiu"],
    ["Cica","Myrica","Noto Sans Mono CJK JP","Cascadia Next JP","MS Gothic UI","Meiryo UI","Hiragino Sans"],
    ["D2CodingLigature Nerd Font","Noto Sans Mono CJK KR","Malgun Gothic","맑은 고딕","Gulim","Apple SD Gothic Neo"],
    ["Noto Naskh Arabic","Segoe UI","SF Arabic","Geeza Pro","Al Bayan","Tahoma"],
    ["Maple Mono NF CN","Maple Mono NL CN","Maple Mono","SF Pro","Menlo","DejaVu Sans Mono","Segoe UI","Tahoma"],
]


LANG_CODE_MAP = {
    'zh-cn': '中文', 'zh-tw': '繁體中文', 'ja-jp': '日本語', 'ko-kr': '한국어',
    'ar-sa': 'العربية', 'en-us': 'English', 'de-de': 'Deutsch', 'it-it': 'Italiano',
    'fr-fr': 'Français', 'es-es': 'Español', 'ru-ru': 'Русский','pl-pl': 'Polski',
    'vi-vn': 'Tiếng Việt','tr-tr':'Türkçe','id-id':'Bahasa Indonesia','bo-cn':'བོད་སྐད།',
    'el-gr':"Ελληνικά"
}
LANG_KEY_TO_CODE = {v: k for k, v in LANG_CODE_MAP.items()}


MONO_FONTS = [
    #   没有nf
    "Maple Mono NL CN","Maple Mono", "Sarasa Mono SC",#CJK
    'JetBrains Mono', 'Hasklig',#Lig
    'Hack','Source Code Pro','Fira Code',"Fira Mono"#Popular
    # thinnnnnnnnnnn
    "Iosevka Custom",
    # 0.5 
    "M+ 1m",
    # Which Editor can come and recongnize your son？
    "Zed Plex Mono","Cascadia Code",
    #Use it and you know why it named 'Envy'
    "Envy Code R"
    #System Font
    "SF Mono", "Menlo","Andale Mono","Monaco",#Mac 
    "Ubuntu Mono","DejaVu Sans Mono","LiberationMono", #Linux
    "Consolas","Lucida Console","Terminal", #Windows
    "Courier",#all
    "Courier New", #i2
    "TkDefaultFont" #-A- 
]
LANG_CODE_MAP = {
    'zh-cn': '中文', 'zh-tw': '繁體中文', 'ja-jp': '日本語', 'ko-kr': '한국어',
    'ar-sa': 'العربية', 'en-us': 'English', 'de-de': 'Deutsch', 'it-it': 'Italiano',
    'fr-fr': 'Français', 'es-es': 'Español', 'ru-ru': 'Русский','pl-pl': 'Polski',
    'vi-vn': 'Tiếng Việt','tr-tr':'Türkçe','id-id':'Bahasa Indonesia','bo-cn':'བོད་སྐད།',
    'el-gr':"Ελληνικά"
}
LANG_KEY_TO_CODE = {v: k for k, v in LANG_CODE_MAP.items()}

def get_best_font(lang):
    all_fonts = QFontDatabase.families()
    code = LANG_KEY_TO_CODE.get(lang)
    if code and code in SPECIAL_FONT_KEYS:
        for f in SPECIAL_FONT_VALUES[SPECIAL_FONT_KEYS.index(code)]:
            if f in all_fonts: return f
    for nf in NERD_FONT_FALLBACKS:
        if nf in all_fonts: return nf
    for mf in MONO_FONTS:
        if mf in all_fonts: return mf
    for f in ["Consolas","Courier New","DejaVu Sans Mono","Noto Sans Mono","Microsoft YaHei UI","Segoe UI","SimSun"]:
        if f in all_fonts: return f
    return "monospace"

# ==================== 系统检测 ====================
def is_system_dark_mode():
    if os.name == 'nt':
        try:
            import winreg
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            v, _ = winreg.QueryValueEx(k, "AppsUseLightTheme")
            return v == 0
        except: pass
    elif sys.platform == 'darwin':
        try:
            import subprocess as sp
            r = sp.run(['defaults','read','-g','AppleInterfaceStyle'], capture_output=True, text=True)
            return 'Dark' in r.stdout
        except: pass
    else:
        for cmd in [['gsettings','get','org.gnome.desktop.interface','color-scheme'],['gsettings','get','org.gnome.desktop.interface','gtk-theme']]:
            try:
                import subprocess as sp
                r = sp.run(cmd, capture_output=True, text=True)
                if 'dark' in r.stdout.lower(): return True
            except: pass
        try:
            kg = os.path.expanduser('~/.config/kdeglobals')
            if os.path.exists(kg):
                for l in open(kg):
                    if 'ColorScheme' in l and 'Dark' in l: return True
        except: pass
    return False

def get_system_accent_color():
    if os.name == 'nt':
        try:
            import winreg
            try:
                k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Accent")
                pal, _ = winreg.QueryValueEx(k, "AccentPalette")
                if len(pal) >= 4:
                    r, g, b = pal[1], pal[2], pal[3]
                    if r + g + b < 30: r, g, b = pal[3], pal[2], pal[1]
                    if r + g + b > 30:
                        accent = f"#{r:02x}{g:02x}{b:02x}"
                        return accent, accent + "33", accent + "cc"
            except: pass
            try:
                k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
                c, _ = winreg.QueryValueEx(k, "ColorizationColor")
                r, g, b = (c>>16)&0xFF, (c>>8)&0xFF, c&0xFF
                if r + g + b > 30:
                    accent = f"#{r:02x}{g:02x}{b:02x}"
                    return accent, accent + "33", accent + "cc"
            except: pass
        except: pass
    elif sys.platform == 'darwin':
        try:
            import subprocess as sp
            r = sp.run(['defaults','read','-g','AppleAccentColor'], capture_output=True, text=True)
            i = int(r.stdout.strip() or 0)
            colors = ["#007aff","#ff3b30","#ff9500","#ffcc00","#34c759","#af52de","#5856d6","#8e8e93"]
            a = colors[i] if i<len(colors) else colors[0]
            return a, a+"33", a+"cc"
        except: pass
    else:
        try:
            import subprocess as sp, re
            r = sp.run(['gsettings','get','org.gnome.desktop.interface','accent-color'], capture_output=True, text=True)
            if 'rgb' in r.stdout:
                n = re.findall(r'\d+', r.stdout)
                if len(n)>=3:
                    a = f"#{int(n[0]):02x}{int(n[1]):02x}{int(n[2]):02x}"
                    return a, a+"33", a+"cc"
        except: pass
    return "#0078d4", "#e8f3ff", "#106ebe"

# ==================== OpenType locl ====================
LOCL_MAP = {'ja':0x0411,'ko':0x0412,'pl':0x0415,'bg':0x0402,'ro':0x0418,'no':0x0414,'zh':0x0804}

def set_thread_locale(lt):
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.kernel32.SetThreadLocale(LOCL_MAP.get(lt,0x0409))
        except: pass
    else:
        try:
            lm = {'ja':'ja_JP.UTF-8','ko':'ko_KR.UTF-8','zh':'zh_CN.UTF-8','pl':'pl_PL.UTF-8','bg':'bg_BG.UTF-8','ro':'ro_RO.UTF-8','no':'nb_NO.UTF-8'}
            lc = lm.get(lt)
            if lc: locale.setlocale(locale.LC_ALL, lc)
        except: pass

# ==================== 样式表 ====================
LIGHT_STYLE = """
QMainWindow{{background:#f3f3f3}}
QFrame#card{{background:#fff;border:none;border-radius:12px}}
QLabel{{color:#1a1a1a;font-size:13px}}
QLabel#title{{font-size:26px;color:#1a1a1a;padding:12px 16px}}
QLabel#section{{font-size:13px;font-weight:bold;color:#666}}
QLineEdit{{background:#fafafa;border:1px solid #d1d1d1;border-radius:6px;padding:10px;font-size:14px;color:#1a1a1a}}
QLineEdit:focus{{border:2px solid {accent};background:#fff}}
QPushButton#primary{{background:{accent};color:#fff;border:none;padding:10px 28px;border-radius:6px;font-size:14px;font-weight:500}}
QPushButton#primary:hover{{background:{accent_hover}}}
QPushButton#file{{background:transparent;color:{accent};border:1px solid {accent};padding:10px 20px;border-radius:6px;font-size:14px}}
QPushButton#file:hover{{background:{accent_bg}}}
QComboBox{{background:#fafafa;border:1px solid #d1d1d1;border-radius:6px;padding:8px;font-size:13px;color:#1a1a1a}}
QComboBox QAbstractItemView{{background:#fff;color:#1a1a1a;selection-background-color:{accent_bg};selection-color:{accent}}}
QListWidget#users{{background:#fff;border:1px solid #e8e8e8;border-radius:8px;font-size:13px;padding:4px;color:#1a1a1a}}
QListWidget#users::item{{padding:10px 14px;margin:1px 4px;border-radius:6px;color:#333}}
QListWidget#users::item:selected{{background:{accent_bg};color:{accent}}}
QListWidget#users::item:hover:!selected{{background:#f5f5f5}}
QTextEdit#chat{{background:#fff;border:1px solid #e8e8e8;border-radius:8px;padding:16px;font-size:14px;color:#1a1a1a}}
QFrame#input{{background:#fff;border:1px solid #e8e8e8;border-radius:8px}}
QScrollBar:vertical{{background:#f0f0f0;width:10px;border-radius:5px;margin:2px}}
QScrollBar::handle:vertical{{background:#c0c0c0;border-radius:5px;min-height:30px}}
QScrollBar::handle:vertical:hover{{background:#a0a0a0}}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0px}}
QScrollBar:horizontal{{background:#f0f0f0;height:10px;border-radius:5px;margin:2px}}
QScrollBar::handle:horizontal{{background:#c0c0c0;border-radius:5px;min-width:30px}}
QScrollBar::handle:horizontal:hover{{background:#a0a0a0}}
QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{{width:0px}}
"""

DARK_STYLE = """
QMainWindow{{background:#1e1e1e}}
QFrame#card{{background:#2d2d2d;border:none;border-radius:12px}}
QLabel{{color:#e0e0e0;font-size:13px}}
QLabel#title{{font-size:26px;color:#fff;padding:12px 16px}}
QLabel#section{{font-size:13px;font-weight:bold;color:#aaa}}
QLineEdit{{background:#3c3c3c;border:1px solid #555;border-radius:6px;padding:10px;font-size:14px;color:#e0e0e0}}
QLineEdit:focus{{border:2px solid {accent};background:#3c3c3c}}
QPushButton#primary{{background:{accent};color:#fff;border:none;padding:10px 28px;border-radius:6px;font-size:14px;font-weight:500}}
QPushButton#primary:hover{{background:{accent_hover}}}
QPushButton#file{{background:transparent;color:{accent};border:1px solid {accent};padding:10px 20px;border-radius:6px;font-size:14px}}
QPushButton#file:hover{{background:{accent_bg}44}}
QComboBox{{background:#3c3c3c;border:1px solid #555;border-radius:6px;padding:8px;font-size:13px;color:#e0e0e0}}
QComboBox QAbstractItemView{{background:#2d2d2d;color:#e0e0e0;selection-background-color:{accent};selection-color:#fff}}
QListWidget#users{{background:#2d2d2d;border:1px solid #3e3e3e;border-radius:8px;font-size:13px;padding:4px;color:#e0e0e0}}
QListWidget#users::item{{padding:10px 14px;margin:1px 4px;border-radius:6px;color:#ccc}}
QListWidget#users::item:selected{{background:{accent_bg}44;color:{accent}}}
QListWidget#users::item:hover:!selected{{background:#353535}}
QTextEdit#chat{{background:#2d2d2d;border:1px solid #3e3e3e;border-radius:8px;padding:16px;font-size:14px;color:#e0e0e0}}
QFrame#input{{background:#2d2d2d;border:1px solid #3e3e3e;border-radius:8px}}
QScrollBar:vertical{{background:#2d2d2d;width:10px;border-radius:5px;margin:2px}}
QScrollBar::handle:vertical{{background:#555;border-radius:5px;min-height:30px}}
QScrollBar::handle:vertical:hover{{background:#777}}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0px}}
QScrollBar:horizontal{{background:#2d2d2d;height:10px;border-radius:5px;margin:2px}}
QScrollBar::handle:horizontal{{background:#555;border-radius:5px;min-width:30px}}
QScrollBar::handle:horizontal:hover{{background:#777}}
QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{{width:0px}}
"""

class Emitter(QObject):
    display = Signal(str, str, str, str)
    users = Signal(list)
    login_ok = Signal()
    login_err = Signal(str)

class Chat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("聊天室")
        self.resize(1050, 700)
        self.client = None
        self.username = ""
        self.lang = 'zh-cn'
        self.buf = 4096
        
        self.accent, self.accent_bg, self.accent_hover = get_system_accent_color()
        self.dark = is_system_dark_mode()
        
        self.current_font = get_best_font(self.lang)
        self.chat_font = QFont(self.current_font, 11)
        QApplication.setFont(QFont(self.current_font, 10))
        
        self._apply_style()

        self.em = Emitter()
        self.em.display.connect(self._show)
        self.em.users.connect(self._users)
        self.em.login_ok.connect(self._chat_ui)
        self.em.login_err.connect(lambda m: QMessageBox.critical(self, self.t('error'), m))

        self._login_ui()

    def _apply_style(self):
        base = DARK_STYLE if self.dark else LIGHT_STYLE
        styled = (base
            .replace("{accent}", self.accent)
            .replace("{accent_bg}", self.accent_bg)
            .replace("{accent_hover}", self.accent_hover)
        )
        self.setStyleSheet(styled)
        self.style().unpolish(self); self.style().polish(self); self.update()
        for c in self.findChildren(QWidget):
            c.style().unpolish(c); c.style().polish(c); c.update()

    def t(self, k): return TRANSLATIONS.get(self.lang, {}).get(k, k)

    def _chg_lang(self, lang):
        self.lang=lang
        code=LANG_KEY_TO_CODE.get(lang,'zh-cn'); iso=code.split('-')[0]
        set_thread_locale(iso)
        self.current_font=get_best_font(self.lang)
        self.chat_font=QFont(self.current_font,11)
        QApplication.setFont(QFont(self.current_font,10))
        if hasattr(self,'chat'): self.chat.setFont(self.chat_font,10)
        if hasattr(self,'wl'):
            self.wl.setFont(QFont(self.current_font, 20, QFont.Bold)) 
            self.wl.setText(self.t('welcome'))
        if hasattr(self,'ue'):
            self.ue.setPlaceholderText(self.t('username').rstrip(':'))
            self.ue.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'cb'):
            self.cb.setText(self.t('connect'))
            self.cb.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'uname_label'):
            self.uname_label.setText(self.t('username'))
            self.uname_label.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'host_label'):
            self.host_label.setText(self.t('server_address'))
            self.host_label.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'port_label'):
            self.port_label.setText(self.t('port'))
            self.port_label.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'lang_label'):
            self.lang_label.setText(self.t('language_select')+":")
            self.lang_label.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'sb'):
            self.sb.setText(self.t('send'))
            self.sb.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'fb'):
            self.fb.setText(self.t('file_emoji'))
            self.fb.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'ul'):
            self.ul.setText(self.t('online_users'))
            self.ul.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'chat_lang_label'):
            self.chat_lang_label.setText(self.t('language')+":")
            self.chat_lang_label.setFont(QFont(self.current_font, 11)) 
        if hasattr(self,'me'):
            self.me.setFont(QFont(self.current_font, 11))
        if hasattr(self,'lang_cb'):
            self.lang_cb.setCurrentText(lang)
            self.lang_cb.setFont(QFont(self.current_font, 11)) 
        self.setWindowTitle(f"{self.t('title')} - {self.username}" if self.username else self.t('title'))

    def _login_ui(self):
        c=QWidget(); self.setCentralWidget(c)
        v=QVBoxLayout(c); v.setAlignment(Qt.AlignCenter)
        card=QFrame(); card.setObjectName("card")
        card.setMinimumWidth(420); card.setMaximumWidth(700)
        l=QVBoxLayout(card); l.setSpacing(12); l.setContentsMargins(30,30,30,30)

        h=QHBoxLayout(); h.addStretch()
        self.lang_label=QLabel(self.t('language_select')+":")
        h.addWidget(self.lang_label)
        self.lang_cb=QComboBox(); self.lang_cb.addItems(LANGUAGE_LIST)
        self.lang_cb.setFixedWidth(200)
        self.lang_cb.currentTextChanged.connect(self._chg_lang)
        h.addWidget(self.lang_cb); l.addLayout(h)

        self.wl=QLabel(self.t('welcome'))
        self.wl.setObjectName('title')
        self.wl.setFont(QFont(self.current_font, 20, QFont.Bold)) 
        self.wl.setAlignment(Qt.AlignCenter)
        l.addWidget(self.wl); l.addSpacing(8)

        self.uname_label=QLabel(self.t('username')); l.addWidget(self.uname_label)
        self.ue=QLineEdit(); self.ue.setPlaceholderText(self.t('username').rstrip(':')); l.addWidget(self.ue)
        self.host_label=QLabel(self.t('server_address')); l.addWidget(self.host_label)
        self.he=QLineEdit("127.0.0.1"); l.addWidget(self.he)
        self.port_label=QLabel(self.t('port')); l.addWidget(self.port_label)
        self.pe=QLineEdit("55555"); l.addWidget(self.pe)
        l.addSpacing(8)
        self.cb=QPushButton(self.t('connect')); self.cb.setObjectName("primary")
        self.cb.setFixedHeight(44); self.cb.clicked.connect(self._connect); l.addWidget(self.cb)
        v.addWidget(card)
        for w in[self.ue,self.he,self.pe]: w.returnPressed.connect(self._connect)
        self.ue.setFocus()

    def _chat_ui(self):
        c=QWidget(); self.setCentralWidget(c)
        m=QVBoxLayout(c); m.setContentsMargins(8,8,8,8); m.setSpacing(6)

        tb=QHBoxLayout(); tb.addStretch()
        self.chat_lang_label=QLabel(self.t('language')+":")
        tb.addWidget(self.chat_lang_label)
        self.lcb=QComboBox(); self.lcb.addItems(LANGUAGE_LIST)
        self.lcb.setCurrentText(self.lang); self.lcb.setFixedWidth(120)
        self.lcb.currentTextChanged.connect(self._chg_lang)
        tb.addWidget(self.lcb); m.addLayout(tb)

        sp=QSplitter(Qt.Horizontal)

        lp=QWidget(); ll=QVBoxLayout(lp); ll.setContentsMargins(0,0,0,0)
        self.ul=QLabel(self.t('online_users')); self.ul.setObjectName("section")
        ll.addWidget(self.ul)
        self.ulb=QListWidget(); self.ulb.setObjectName("users")
        self.ulb.setFixedWidth(200); self.ulb.itemDoubleClicked.connect(self._priv)
        ll.addWidget(self.ulb); sp.addWidget(lp)

        rp=QWidget(); rl=QVBoxLayout(rp); rl.setContentsMargins(4,0,0,0); rl.setSpacing(6)
        self.chat=QTextEdit(); self.chat.setObjectName("chat"); self.chat.setReadOnly(True)
        self.chat.document().setDocumentMargin(10)
        self.chat.setFont(self.chat_font); rl.addWidget(self.chat)

        ib=QFrame(); ib.setObjectName("input")
        il=QHBoxLayout(ib); il.setContentsMargins(8,6,8,6)
        self.me=QLineEdit(); self.me.setPlaceholderText(self.t('placeholder'))
        self.me.returnPressed.connect(self._send); il.addWidget(self.me)
        self.fb=QPushButton(self.t('file_emoji')); self.fb.setObjectName("file")
        self.fb.clicked.connect(self._file); il.addWidget(self.fb)
        self.sb=QPushButton(self.t('send')); self.sb.setObjectName("primary")
        self.sb.clicked.connect(self._send); il.addWidget(self.sb)
        rl.addWidget(ib); sp.addWidget(rp); m.addWidget(sp)

        self.me.setFocus()
        self.setWindowTitle(f"{self.t('title')} - {self.username}")

    def _show(self, msg, mtype, ts, user):
        c=self.chat; c.moveCursor(QTextCursor.End); cur=c.textCursor()
        tc=QColor("#e0e0e0") if self.dark else QColor("#1a1a1a")
        gc=QColor("#888") if self.dark else QColor("#999")
        pc=QColor("#c39bdb") if self.dark else QColor("#9b59b6")
        bc=QColor("#5dade2") if self.dark else QColor("#2980b9")
        grc=QColor("#58d68d") if self.dark else QColor("#27ae60")
        fmt=QTextCharFormat(); fmt.setForeground(tc); fmt.setFont(self.chat_font)
        if ts:
            tf=QTextCharFormat(fmt); tf.setForeground(gc); cur.insertText(f"[{ts}] ", tf)
        if mtype=='system':
            f=QTextCharFormat(fmt); f.setForeground(gc); cur.insertText(msg+"\n", f)
        elif mtype=='private':
            f=QTextCharFormat(fmt); f.setForeground(pc); cur.insertText(msg+"\n", f)
        elif mtype=='file':
            f=QTextCharFormat(fmt); f.setForeground(bc); cur.insertText("📦 "+msg+"\n", f)
        elif mtype=='public' and user:
            uf=QTextCharFormat(fmt); uf.setFontWeight(QFont.Bold)
            uf.setForeground(tc if user==self.username else grc)
            cur.insertText(user, uf); cur.insertText(": "+msg+"\n", fmt)
        else: cur.insertText(msg+"\n", fmt)
        c.setTextCursor(cur); c.ensureCursorVisible()

    def _users(self, users):
        self.ulb.clear(); icon=self.t('user_emoji')
        for u in users:
            d=f"{icon} {u}"
            if u==self.username: d+=f" ({self.t('me')})"
            self.ulb.addItem(QListWidgetItem(d))

    def _recv(self, n):
        d=b''
        while len(d)<n:
            try:
                c=self.client.recv(min(self.buf,n-len(d)))
                if not c: return None
                d+=c
            except socket.timeout: continue
        return d

    def _rmsg(self):
        h=self._recv(4)
        return self._recv(int.from_bytes(h,'big')).decode() if h else None

    def _snd(self, m):
        d=m.encode()
        try: self.client.sendall(len(d).to_bytes(4,'big')+d); return True
        except: return False

    def _connect(self):
        u=self.ue.text().strip(); h=self.he.text().strip()
        try: p=int(self.pe.text().strip())
        except: self.em.login_err.emit(self.t('port')); return
        if not u: self.em.login_err.emit(self.t('username')); return
        try:
            self.client=socket.socket(); self.client.settimeout(10)
            self.client.connect((h,p)); self._snd(u); self.username=u
            self.em.login_ok.emit()
            threading.Thread(target=self._loop, daemon=True).start()
            self.em.display.emit(f"{self.t('connecting_success')} {h}:{p}",'system','','')
        except socket.timeout: self.em.login_err.emit(self.t('connecting_timeout'))
        except ConnectionRefusedError: self.em.login_err.emit(self.t('connection_refused'))
        except Exception as e:
            self.em.login_err.emit(f"{self.t('connection_failed')}: {e}")
            if self.client:
                try: self.client.close()
                except: pass
                self.client=None

    def _loop(self):
        while True:
            try:
                if not self.client: break
                m=self._rmsg()
                if not m: self.em.display.emit(self.t('disconnected'),'system','',''); break
                md=json.loads(m)
                if md['type']=='user_list': self.em.users.emit(md['users'])
                elif md['type']=='system': self.em.display.emit(md['message'],'system',md.get('time',''),'')
                elif md['type']=='public': self.em.display.emit(md['message'],'public',md.get('time',''),md.get('username',''))
                elif md['type']=='private': self.em.display.emit(f"{self.t('private_chat_prefix')} {md['from']}: {md['message']}",'private',md.get('time',''),'')
                elif md['type']=='file':
                    try:
                        sb=self._recv(8)
                        if sb and len(sb)==8:
                            fd=self._recv(int.from_bytes(sb,'big'))
                            if fd: self._save(md,fd)
                            else: self.em.display.emit(self.t('file_receive_failed'),'system','','')
                        else: self.em.display.emit(self.t('file_size_error'),'system','','')
                    except Exception as e: self.em.display.emit(f"{self.t('file_receive_error')}: {e}",'system','','')
            except Exception as e:
                if self.client: self.em.display.emit(f"{self.t('connection_error')}: {e}",'system','','')
                break

    def _send(self):
        m=self.me.text().strip()
        if not m or not self.client: return
        try:
            if m.startswith('/msg '):
                p=m.split(' ',2)
                if len(p)>=3:
                    self._snd(json.dumps({'type':'private','to':p[1],'message':p[2]}))
                    self.em.display.emit(f"{self.t('private_chat_to')} {p[1]}] {p[2]}",'private',datetime.now().strftime('%H:%M:%S'),'')
                else: self.em.display.emit(self.t('usage_hint'),'system','','')
            else:
                self._snd(json.dumps({'type':'public','message':m}))
                self.em.display.emit(m,'public',datetime.now().strftime('%H:%M:%S'),self.username)
            self.me.clear()
        except Exception as e: self.em.display.emit(f"{self.t('send_failed')}: {e}",'system','','')

    def _priv(self, item):
        t=item.text().replace(f"{self.t('user_emoji')} ","").replace(f" ({self.t('me')})","")
        if t!=self.username: self.me.setText(f"/msg {t} "); self.me.setFocus()

    def _file(self):
        target=None
        sel=self.ulb.currentItem()
        if sel:
            t=sel.text().replace(f"{self.t('user_emoji')} ","").replace(f" ({self.t('me')})","")
            if t!=self.username: target=t
        fp,_=QFileDialog.getOpenFileName(self,self.t('send_file_title'))
        if not fp: return
        try:
            fn,fs=os.path.basename(fp),os.path.getsize(fp)
            self._snd(json.dumps({'type':'file_start','filename':fn,'size':fs,'to':target}))
            time.sleep(0.1)
            with open(fp,'rb') as f: self.client.sendall(f.read())
            msg=f"{self.t('file_sent_to')} {target}: {fn} ({fs}B)" if target else f"{self.t('file_broadcast')}: {fn} ({fs}B)"
            self.em.display.emit(msg,'file',datetime.now().strftime('%H:%M:%S'),'')
        except Exception as e: QMessageBox.critical(self,self.t('file_send_failed'),str(e))

    def _save(self, info, data):
        os.makedirs('received',exist_ok=True)
        fn=f"received/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{info.get('from','?')}_{info['filename']}"
        try:
            with open(fn,'wb') as f: f.write(data)
            self.em.display.emit(f"{self.t('file_saved')}: {fn}",'file','','')
        except Exception as e: self.em.display.emit(f"{self.t('file_save_failed')}: {e}",'system','','')

    def closeEvent(self, e):
        if self.client:
            try: self.client.close()
            except: pass
        e.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    k=Chat()
    k._chg_lang('English')
    k.show()
    sys.exit(app.exec())
