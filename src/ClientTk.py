# -*- coding: utf-8 -*-
import socket
import threading
import json
import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import subprocess
import sys
from pathlib import Path

# ==================== 语言包 ====================
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

SPECIAL_FONT_KEYS = ["zh-cn","bo-cn", "zh-tw", "ja-jp", "ko-kr", "ar-sa","vi-vn"]
SPECIAL_FONT_VALUES = [
    [
     "Maple Mono NF CN", "Maple Mono NL CN",
     "Cascadia Next SC", 
     "微软雅黑", "Microsoft YaHei", 
     "PingFang SC", 
     "SimHei", "SimSun", 
     "TkDefaultFont" 
    ],
    [
     "Misans Tibetan", 
     "Kailasa","Monlam Bodyig", "Microsoft Himalaya",
     "ཐོན་མིའི་ཕྱག་རྒྱུན-སྣེའུ་བྲིས་འཁྱུག་ཡིག","吞弥恰俊—柳酋体", "TkDefaultFont" 
    ],
    #香港繁中：我一定会回来的！！！！！！！！！
    #澳门繁中：……
    [
     "Noto Sans Mono CJK TC","Cascadia Next TC", "微软正黑体", "微軟正黑體", "Microsoft JhengHei UI", "Microsoft JhengHei",
     "PingFang TC", 
     "MingLiu", 
     "TkDefaultFont" 
    ],
    ["Cica","Myrica","Noto Sans Mono CJK JP","Cascadia Next JP", "Meriyo UI", "MS Gothic UI", "MS Gothic", "MS UI Gothic", "Meiryo UI", "Hiragino Sans", "TkDefaultFont"],
    ["D2CodingLigature Nerd Font","Noto Sans Mono CJK KR","Malgun Gothic", "맑은 고딕", "Gulim", "Apple SD Gothic Neo", "TkDefaultFont"],
    ["Noto Naskh Arabic", "Segoe UI", "SF Arabic", "Geeza Pro", "Al Bayan", "Tahoma", "ليحيى تضامن شعوب العالم إلى الأبد", "TkDefaultFont"], # Did you see the Bonus of this production?
    ["Maple Mono NF CN", "Maple Mono NL CN", "Maple Mono", "SF Pro","Menlo", "DejaVu Sans Mono", "DejaVu Sans", "Segoe UI", "Tahoma", "TkDefaultFont"]
]

MONO_FONTS = [
    # 现代全能
    #   NF
    "Maple Mono NF CN", "Sarasa Mono SC Nerd", # CJK
    'JetBrains Mono Nerd Font', 'Hasklug Nerd Font', #Lig
    'Hack Nerd Font',"Fira Code NF", 'Source Code Pro Nerd Font',#Popular
    "Fira Mono NF",#So do i
    #   没有nf
    "Maple Mono NL CN","Maple Mono", "Sarasa Mono SC",#CJK
    'JetBrains Mono', 'Hasklig',#Lig
    'Hack','Source Code Pro','Fira Code',"Fira Mono"#Popular
    # thinnnnnnnnnnn
    "Iosevka Custom Nerd Font","Iosevka Custom",
    # 0.5 
    "M+ 1m","M+ Nerd Font",
    # Which Editor can come and recongnize your son？
    "Zed Plex Mono", "Cascadia Code NF","Cascadia Code","CaskaydiaCove Nerd Font",
    #Use it and you know why it named 'Envy'
    "Envy Code R","EnvyCodeR Nerd Font"
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


class FontManager:
    """字体管理器"""
    def __init__(self):
        self.available = self._get_available()
        self.default_mono = self._select(MONO_FONTS)
        self.fnt = self._select(self._get_special('zh-cn'))
        self.codefnt = self.fnt if ('Cascadia Next' in self.fnt or self.fnt.startswith('Noto Sans Mono CJK') or "D2CodingLigature Nerd Font" in self.fnt or self.fnt=='Cica' or self.fnt=='Myrica' or 'Maple Mono' in self.fnt) else self.default_mono

    def _get_available(self):
        try:
            import tkinter.font as tkfont
            return list(tkfont.families())
        except:
            return []

    def _get_special(self, code):
        try:
            return SPECIAL_FONT_VALUES[SPECIAL_FONT_KEYS.index(code)]
        except:
            return MONO_FONTS

    def _select(self, fonts):
        return next((f for f in fonts if f in self.available), 'TkDefaultFont')

    def get_font(self, lang):
        code = LANG_KEY_TO_CODE.get(lang)
        if code and code in SPECIAL_FONT_KEYS:
            return self._select(self._get_special(code))
        return self.default_mono

    def get_code_font(self):
        return self.default_mono


def supports_emoji():
    if os.name != 'nt':
        return True
    try:
        return int(os.popen('wmic os get version').read().split()[1].split('.')[0]) >= 10
    except:
        return False


class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("网络聊天室")
        self.root.geometry("1000x650")
        self.root.configure(bg='#DCDAD5')
        self.client = None
        self.username = ""
        self.buffer_size = 4096
        self.current_language = '中文'
        self.emoji_supported = supports_emoji()
        self.font_manager = FontManager()
        self.fnt = self.font_manager.fnt
        self.codefnt = self.font_manager.codefnt
        
        # 初始化 ttk 主题
        self.init_theme()
        
        self.setup_login_ui()
    
    def init_theme(self):
        """初始化 ttk 主题，使按钮支持字体设置"""
        self.style = ttk.Style()
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        elif 'alt' in available_themes:
            self.style.theme_use('alt')
        elif 'default' in available_themes:
            self.style.theme_use('default')
        self._apply_button_style()
    
    def _apply_button_style(self):
        """应用按钮样式"""
        self.style.configure('TButton', font=(self.fnt, 9))
    
    def t(self, key):
        return TRANSLATIONS.get(self.current_language, {}).get(key, key)

    def get_user_icon(self):
        return self.t('user_emoji') if self.emoji_supported else self.t('user_no_emoji')

    def get_file_text(self):
        return self.t('file_emoji') if self.emoji_supported else f"[{self.t('file')}]"

    def update_font(self, lang):
        self.fnt = self.font_manager.get_font(lang)
        if 'Cascadia Next' in self.fnt or self.fnt.startswith('Noto Sans Mono CJK') or "D2CodingLigature Nerd Font" in self.fnt or\
           self.fnt=='Cica' or self.fnt=='Myrica' or 'Maple Mono' in self.fnt:
            self.codefnt = self.fnt
        else:
            self.codefnt = self.font_manager.get_code_font()
        self._apply_button_style()

    def setup_login_ui(self):
        self.login_frame = ttk.Frame(self.root, padding="20")
        self.login_frame.pack(expand=True)
        lf = ttk.Frame(self.login_frame)
        lf.pack(pady=5, anchor=tk.NE)
        self.lang_label = ttk.Label(lf, text=f"{self.t('language_select')}: ", font=(self.fnt, 10))
        self.lang_label.pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value='中文')
        self.lang_combo = ttk.Combobox(lf, textvariable=self.lang_var, values=LANGUAGE_LIST, state='readonly', width=16, font=(self.fnt, 10))
        self.lang_combo.pack(side=tk.LEFT)
        self.lang_combo.bind('<<ComboboxSelected>>', self.change_lang)
        self.welcome_label = ttk.Label(self.login_frame, text=self.t('welcome'), font=(self.fnt, 18, 'bold'))
        self.welcome_label.pack(pady=20)
        self.uname_label = ttk.Label(self.login_frame, text=self.t('username'), font=(self.fnt, 11))
        self.uname_label.pack(pady=5)
        self.uname_entry = ttk.Entry(self.login_frame, width=30, font=(self.fnt, 11))
        self.uname_entry.pack(pady=5)
        self.uname_entry.focus()
        self.host_label = ttk.Label(self.login_frame, text=self.t('server_address'), font=(self.fnt, 11))
        self.host_label.pack(pady=5)
        self.host_entry = ttk.Entry(self.login_frame, width=30, font=(self.codefnt, 11))
        self.host_entry.insert(0, "127.0.0.1")
        self.host_entry.pack(pady=5)
        self.port_label = ttk.Label(self.login_frame, text=self.t('port'), font=(self.fnt, 11))
        self.port_label.pack(pady=5)
        self.port_entry = ttk.Entry(self.login_frame, width=30, font=(self.codefnt, 11))
        self.port_entry.insert(0, "55555")
        self.port_entry.pack(pady=5)
        self.conn_btn = ttk.Button(self.login_frame, text=self.t('connect'), command=self.connect)
        self.conn_btn.pack(pady=20)
        self.root.bind('<Return>', lambda e: self.connect())

    def change_lang(self, event=None):
        old = self.current_language
        self.current_language = self.lang_var.get()
        self.update_font(self.current_language)
        if old != self.current_language:
            self.root.title(self.t('title'))
            self.lang_label.configure(text=f"{self.t('language_select')}: ", font=(self.fnt, 10))
            self.lang_combo.configure(font=(self.fnt, 10))
            self.welcome_label.configure(text=self.t('welcome'), font=(self.fnt, 18, 'bold'))
            self.uname_label.configure(text=self.t('username'), font=(self.fnt, 11))
            self.uname_entry.configure(font=(self.fnt, 11))
            self.host_label.configure(text=self.t('server_address'), font=(self.fnt, 11))
            self.host_entry.configure(font=(self.codefnt, 11))
            self.port_label.configure(text=self.t('port'), font=(self.fnt, 11))
            self.port_entry.configure(font=(self.codefnt, 11))
            self.conn_btn.configure(text=self.t('connect'))

    def setup_chat_ui(self):
        self.login_frame.destroy()
        self.root.unbind('<Return>')
        mc = ttk.Frame(self.root)
        mc.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        lf = ttk.Frame(mc)
        lf.pack(fill=tk.X, pady=(0, 5))
        self.chat_lang_label = ttk.Label(lf, text=f"{self.t('language')}: ", font=(self.fnt, 10))
        self.chat_lang_label.pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value=self.current_language)
        self.chat_lang_combo = ttk.Combobox(lf, textvariable=self.lang_var, values=LANGUAGE_LIST, state='readonly', width=15, font=(self.fnt, 10))
        self.chat_lang_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.chat_lang_combo.bind('<<ComboboxSelected>>', self.change_lang_chat)
        left = ttk.Frame(mc, width=200)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left.pack_propagate(False)
        self.users_label = ttk.Label(left, text=self.t('online_users'), font=(self.fnt, 11, 'bold'))
        self.users_label.pack(pady=5)
        self.user_listbox = tk.Listbox(left, font=(self.fnt, 10))
        self.user_listbox.pack(fill=tk.BOTH, expand=True)
        self.user_listbox.bind('<Double-Button-1>', self.start_private)
        right = ttk.Frame(mc)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.chat_display = scrolledtext.ScrolledText(right, wrap=tk.WORD, font=(self.fnt, 10), state='disabled')
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        for tag, fg in [('system', 'gray'), ('private', 'purple'), ('file', 'blue'), ('own_message', 'black')]:
            self.chat_display.tag_config(tag, foreground=fg)
        self.chat_display.tag_config('username', foreground='dark green', font=(self.fnt, 10, 'bold'))
        bf = ttk.Frame(right)
        bf.pack(fill=tk.X, pady=(5, 0))
        self.msg_entry = ttk.Entry(bf, font=(self.fnt, 10))
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.msg_entry.bind('<Return>', self.send_msg)
        self.send_btn = ttk.Button(bf, text=self.t('send'), command=self.send_msg)
        self.send_btn.pack(side=tk.RIGHT, padx=2)
        self.file_btn = ttk.Button(bf, text=self.get_file_text(), command=self.send_file)
        self.file_btn.pack(side=tk.RIGHT, padx=2)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.msg_entry.focus()
        self.root.title(f"{self.t('title')} - {self.username}")

    def change_lang_chat(self, event=None):
        old = self.current_language
        self.current_language = self.lang_var.get()
        self.update_font(self.current_language)
        if old != self.current_language:
            self.root.title(f"{self.t('title')} - {self.username}")
            self.chat_lang_label.configure(text=f"{self.t('language')}: ", font=(self.fnt, 10))
            self.chat_lang_combo.configure(font=(self.fnt, 10))
            self.users_label.configure(text=self.t('online_users'), font=(self.fnt, 11, 'bold'))
            self.send_btn.configure(text=self.t('send'))
            self.file_btn.configure(text=self.get_file_text())
            self.user_listbox.configure(font=(self.fnt, 10))
            self.chat_display.configure(font=(self.fnt, 10))
            self.chat_display.tag_config('username', font=(self.fnt, 10, 'bold'))
            self.msg_entry.configure(font=(self.fnt, 10))
            self._refresh_user_list()

    def _refresh_user_list(self):
        try:
            users = []
            icon = self.get_user_icon()
            for i in range(self.user_listbox.size()):
                u = self.user_listbox.get(i).replace(f"{icon} ", "")
                for v in TRANSLATIONS.values():
                    if v.get('me'):
                        u = u.replace(f" ({v['me']})", "")
                users.append(u.strip())
            self.user_listbox.delete(0, tk.END)
            for u in users:
                d = f"{icon} {u}"
                if u == self.username:
                    d += f" ({self.t('me')})"
                self.user_listbox.insert(tk.END, d)
        except Exception as e:
            print(f"刷新用户列表错误: {e}")

    def recv_all(self, length):
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
        h = self.recv_all(4)
        return (lambda d: d.decode('utf-8') if d else None)(self.recv_all(int.from_bytes(h, 'big'))) if h else None

    def send_to_server(self, msg):
        d = msg.encode('utf-8')
        h = len(d).to_bytes(4, 'big')
        try:
            self.client.sendall(h + d)
            return True
        except:
            return False

    def connect(self):
        username = self.uname_entry.get().strip()
        host = self.host_entry.get().strip()
        try:
            port = int(self.port_entry.get().strip())
        except:
            messagebox.showerror(self.t('error'), self.t('port'))
            return
        if not username:
            messagebox.showerror(self.t('error'), self.t('username'))
            return
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(10)
            self.client.connect((host, port))
            self.send_to_server(username)
            self.username = username
            self.root.title(f"{self.t('title')} - {username}")
            self.setup_chat_ui()
            self.recv_thread = threading.Thread(target=self.receive_loop)
            self.recv_thread.daemon = True
            self.recv_thread.start()
            self.display(f"{self.t('connecting_success')} {host}:{port}", 'system')
        except socket.timeout:
            messagebox.showerror(self.t('error'), self.t('connecting_timeout'))
        except ConnectionRefusedError:
            messagebox.showerror(self.t('error'), self.t('connection_refused'))
        except Exception as e:
            messagebox.showerror(self.t('error'), f"{self.t('connection_failed')}: {str(e)}")
            if self.client:
                try:
                    self.client.close()
                except:
                    pass
                self.client = None

    def receive_loop(self):
        while True:
            try:
                if not self.client:
                    break
                msg = self.recv_msg()
                if not msg:
                    self.display(self.t('disconnected'), 'system')
                    break
                try:
                    md = json.loads(msg)
                except:
                    continue
                if md['type'] == 'user_list':
                    self.root.after(0, self._update_users, md['users'])
                elif md['type'] == 'system':
                    self.display(md['message'], 'system', md.get('time'))
                elif md['type'] == 'public':
                    self.display(f"{md['username']}: {md['message']}", 'public', md['time'], md['username'])
                elif md['type'] == 'private':
                    self.display(f"{self.t('private_chat_prefix')} {md['from']}: {md['message']}", 'private', md['time'])
                elif md['type'] == 'file':
                    try:
                        sb = self.recv_all(8)
                        if sb and len(sb) == 8:
                            fs = int.from_bytes(sb, 'big')
                            fd = self.recv_all(fs)
                            if fd:
                                self.save_file(md, fd)
                            else:
                                self.display(self.t('file_receive_failed'), 'system')
                        else:
                            self.display(self.t('file_size_error'), 'system')
                    except Exception as e:
                        self.display(f"{self.t('file_receive_error')}: {str(e)}", 'system')
            except Exception as e:
                if self.client:
                    self.display(f"{self.t('connection_error')}: {str(e)}", 'system')
                break

    def display(self, msg, mtype='public', time=None, username=None):
        try:
            self.chat_display.configure(state='normal')
            if time:
                self.chat_display.insert(tk.END, f"[{time}] ", 'system')
            if mtype == 'public' and username:
                self.chat_display.insert(tk.END, self.t('me') if username == self.username else username,
                                        'own_message' if username == self.username else 'username')
                self.chat_display.insert(tk.END, ": ")
                self.chat_display.insert(tk.END, (msg.split(': ', 1)[1] if ': ' in msg else msg) + '\n')
            else:
                self.chat_display.insert(tk.END, msg + '\n', mtype)
            self.chat_display.see(tk.END)
            self.chat_display.configure(state='disabled')
        except Exception as e:
            print(f"显示错误: {e}")

    def _update_users(self, users):
        self.user_listbox.delete(0, tk.END)
        icon = self.get_user_icon()
        for u in users:
            d = f"{icon} {u}"
            if u == self.username:
                d += f" ({self.t('me')})"
            self.user_listbox.insert(tk.END, d)

    def send_msg(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg or not self.client:
            return
        try:
            if msg.startswith('/msg '):
                parts = msg.split(' ', 2)
                if len(parts) >= 3:
                    self._send_private(parts[1], parts[2])
                else:
                    self.display(self.t('usage_hint'), 'system')
            else:
                self.send_to_server(json.dumps({'type': 'public', 'message': msg}))
                self.display(msg, 'public', datetime.now().strftime('%H:%M:%S'), self.username)
            self.msg_entry.delete(0, tk.END)
        except Exception as e:
            self.display(f"{self.t('send_failed')}: {str(e)}", 'system')

    def start_private(self, event=None):
        sel = self.user_listbox.curselection()
        if sel:
            target = self.user_listbox.get(sel[0]).replace(f"{self.get_user_icon()} ", "").replace(f" ({self.t('me')})", "")
            if target != self.username:
                self.msg_entry.delete(0, tk.END)
                self.msg_entry.insert(0, f"/msg {target} ")
                self.msg_entry.focus()

    def _send_private(self, target, msg):
        self.send_to_server(json.dumps({'type': 'private', 'to': target, 'message': msg}))
        self.display(f"{self.t('private_chat_to')} {target}] {msg}", 'private', datetime.now().strftime('%H:%M:%S'))

    def send_file(self):
        sel = self.user_listbox.curselection()
        target = None
        if sel:
            t = self.user_listbox.get(sel[0]).replace(f"{self.get_user_icon()} ", "").replace(f" ({self.t('me')})", "")
            if t != self.username:
                target = t
        fp = filedialog.askopenfilename()
        if not fp:
            return
        try:
            fn = os.path.basename(fp)
            fs = os.path.getsize(fp)
            self.send_to_server(json.dumps({'type': 'file_start', 'filename': fn, 'size': fs, 'to': target}))
            time.sleep(0.1)
            with open(fp, 'rb') as f:
                self.client.sendall(f.read())
            if target:
                self.display(f"{self.t('file_sent_to')} {target}: {fn} ({fs} bytes)", 'file', datetime.now().strftime('%H:%M:%S'))
            else:
                self.display(f"{self.t('file_broadcast')}: {fn} ({fs} bytes)", 'file', datetime.now().strftime('%H:%M:%S'))
        except Exception as e:
            messagebox.showerror(self.t('file_send_failed'), str(e))

    def save_file(self, info, data):
        os.makedirs('received', exist_ok=True)
        fn = f"received/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{info.get('from','unknown')}_{info['filename']}"
        try:
            with open(fn, 'wb') as f:
                f.write(data)
            self.display(f"{self.t('file_saved')}: {fn} ({len(data)} bytes)", 'file')
        except Exception as e:
            self.display(f"{self.t('file_save_failed')}: {str(e)}", 'system')

    def on_close(self):
        if self.client:
            try:
                self.client.close()
            except:
                pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ChatClient().run()
