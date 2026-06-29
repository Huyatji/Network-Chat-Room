# -*- coding: utf-8 -*-
import socket
import threading
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from locale import getlocale

# ==================== 语言包 ====================
TRANSLATIONS = {
    "中文":{"title":"聊天室服务器","server_config":"服务器配置","ip_address":"IP地址:","refresh":"刷新","port":"端口:","start_server":"▶ 启动服务器","stop_server":"■ 停止服务器","server_stopped":"● 服务器未启动","server_running":"● 服务器运行中","online_clients":"在线客户端","username_col":"用户名","ip_col":"IP地址","connect_time_col":"连接时间","server_log":"服务器日志","online_count":"当前在线: {}","kick_hint":"双击客户端可踢出","detected_ips":"检测到本地IP地址","port_error":"端口错误","port_range":"端口范围: 1024-65535","server_start_success":"服务器启动成功","start_failed":"启动失败","closing_server":"正在关闭服务器...","server_stopped_msg":"服务器已停止","accept_error":"接受连接时出错","new_client":"新客户端连接","client_disconnected":"客户端断开","duplicate_username":"用户名已被使用，请更换用户名重试","duplicate_rejected":"用户名重复，拒绝连接","welcome_msg":"欢迎 {} 加入聊天室！","leave_msg":"{} 离开了聊天室","public_msg_tag":"[公共消息]","private_msg_tag":"[私聊]","file_transfer_tag":"[文件传输]","file_broadcast_tag":"[文件广播]","file_tag":"[文件]","private_fail":"私聊失败: 用户 {} 不存在","user_not_exist":"用户 {} 不存在或已离线","file_receive_fail":"文件接收失败","file_transfer_error":"文件传输错误","process_error":"处理消息时出错","client_error":"客户端处理错误","kick_reason":"被管理员踢出","send_fail":"消息发送失败","private_send_fail":"发送私聊消息失败","update_list_fail":"更新用户列表失败","you_kicked":"你已被管理员踢出聊天室","kick_confirm":"确定要踢出 {} 吗？","kick_title":"踢出客户端","close_confirm":"服务器正在运行，确定要关闭吗？","close_title":"关闭服务器","server_shutdown":"服务器关闭","error":"错误","info":"信息","warning":"警告","success":"成功","language_select":"选择语言 / Select Language","current_language":"语言","stats_online":"当前在线","file_sending":"正在发送文件"},
    "繁體中文":{"title":"聊天室伺服器","server_config":"伺服器設定","ip_address":"IP位址:","refresh":"重新整理","port":"連接埠:","start_server":"▶ 啟動伺服器","stop_server":"■ 停止伺服器","server_stopped":"● 伺服器未啟動","server_running":"● 伺服器執行中","online_clients":"線上客戶端","username_col":"使用者名稱","ip_col":"IP位址","connect_time_col":"連線時間","server_log":"伺服器記錄","online_count":"目前線上: {}","kick_hint":"按兩下客戶端可踢出","detected_ips":"偵測到本地IP位址","port_error":"連接埠錯誤","port_range":"連接埠範圍: 1024-65535","server_start_success":"伺服器啟動成功","start_failed":"啟動失敗","closing_server":"正在關閉伺服器...","server_stopped_msg":"伺服器已停止","accept_error":"接受連線時出錯","new_client":"新客戶端連線","client_disconnected":"客戶端中斷連線","duplicate_username":"使用者名稱已被使用","duplicate_rejected":"使用者名稱重複，拒絕連線","welcome_msg":"歡迎 {} 加入聊天室！","leave_msg":"{} 離開了聊天室","public_msg_tag":"[公開訊息]","private_msg_tag":"[私聊]","file_transfer_tag":"[檔案傳輸]","file_broadcast_tag":"[檔案廣播]","file_tag":"[檔案]","private_fail":"私聊失敗: 使用者 {} 不存在","user_not_exist":"使用者 {} 不存在或已離線","file_receive_fail":"檔案接收失敗","file_transfer_error":"檔案傳輸錯誤","process_error":"處理訊息時出錯","client_error":"客戶端處理錯誤","kick_reason":"被管理員踢出","send_fail":"訊息傳送失敗","private_send_fail":"傳送私聊訊息失敗","update_list_fail":"更新使用者列表失敗","you_kicked":"你已被管理員踢出聊天室","kick_confirm":"確定要踢出 {} 嗎？","kick_title":"踢出客戶端","close_confirm":"伺服器正在執行，確定要關閉嗎？","close_title":"關閉伺服器","server_shutdown":"伺服器關閉","error":"錯誤","info":"資訊","warning":"警告","success":"成功","language_select":"選擇語言 / Select Language","current_language":"語言","stats_online":"目前線上","file_sending":"正在傳送檔案"},
    "日本語":{"title":"チャットサーバー","server_config":"サーバー設定","ip_address":"IPアドレス:","refresh":"更新","port":"ポート:","start_server":"▶ サーバー起動","stop_server":"■ サーバー停止","server_stopped":"● サーバー停止中","server_running":"● サーバー実行中","online_clients":"オンラインクライアント","username_col":"ユーザー名","ip_col":"IPアドレス","connect_time_col":"接続時間","server_log":"サーバーログ","online_count":"オンライン: {}","kick_hint":"ダブルクリックでキック","detected_ips":"検出されたローカルIP","port_error":"ポートエラー","port_range":"ポート範囲: 1024-65535","server_start_success":"サーバーが起動しました","start_failed":"起動失敗","closing_server":"サーバーを停止中...","server_stopped_msg":"サーバーが停止しました","accept_error":"接続受付エラー","new_client":"新しいクライアントが接続","client_disconnected":"クライアント切断","duplicate_username":"ユーザー名は既に使用されています","duplicate_rejected":"ユーザー名重複、接続拒否","welcome_msg":"{} さんがチャットルームに参加しました！","leave_msg":"{} さんがチャットルームを退出しました","public_msg_tag":"[公開]","private_msg_tag":"[プライベート]","file_transfer_tag":"[ファイル転送]","file_broadcast_tag":"[ファイルブロードキャスト]","file_tag":"[ファイル]","private_fail":"プライベートメッセージ失敗: {} が見つかりません","user_not_exist":"ユーザー {} は存在しないかオフラインです","file_receive_fail":"ファイル受信失敗","file_transfer_error":"ファイル転送エラー","process_error":"メッセージ処理エラー","client_error":"クライアント処理エラー","kick_reason":"管理者によりキックされました","send_fail":"メッセージ送信失敗","private_send_fail":"プライベートメッセージ送信失敗","update_list_fail":"ユーザーリスト更新失敗","you_kicked":"管理者によりキックされました","kick_confirm":"{} をキックしますか？","kick_title":"クライアントキック","close_confirm":"サーバーが実行中です。終了しますか？","close_title":"サーバー終了","server_shutdown":"サーバーシャットダウン","error":"エラー","info":"情報","warning":"警告","success":"成功","language_select":"言語選択 / Select Language","current_language":"言語","stats_online":"オンライン","file_sending":"ファイル送信中"},
    "한국어":{"title":"채팅 서버","server_config":"서버 설정","ip_address":"IP 주소:","refresh":"새로고침","port":"포트:","start_server":"▶ 서버 시작","stop_server":"■ 서버 중지","server_stopped":"● 서버 중지됨","server_running":"● 서버 실행 중","online_clients":"온라인 클라이언트","username_col":"사용자 이름","ip_col":"IP 주소","connect_time_col":"연결 시간","server_log":"서버 로그","online_count":"온라인: {}","kick_hint":"더블 클릭으로 강제 퇴장","detected_ips":"감지된 로컬 IP","port_error":"포트 오류","port_range":"포트 범위: 1024-65535","server_start_success":"서버가 시작되었습니다","start_failed":"시작 실패","closing_server":"서버 종료 중...","server_stopped_msg":"서버가 중지되었습니다","accept_error":"연결 수락 오류","new_client":"새 클라이언트 연결","client_disconnected":"클라이언트 연결 해제","duplicate_username":"이미 사용 중인 사용자 이름입니다","duplicate_rejected":"중복 사용자 이름, 연결 거부","welcome_msg":"{} 님이 채팅방에 참여했습니다!","leave_msg":"{} 님이 채팅방을 나갔습니다","public_msg_tag":"[공개]","private_msg_tag":"[비공개]","file_transfer_tag":"[파일 전송]","file_broadcast_tag":"[파일 브로드캐스트]","file_tag":"[파일]","private_fail":"비공개 메시지 실패: {} 없음","user_not_exist":"사용자 {} 이(가) 존재하지 않거나 오프라인입니다","file_receive_fail":"파일 수신 실패","file_transfer_error":"파일 전송 오류","process_error":"메시지 처리 오류","client_error":"클라이언트 처리 오류","kick_reason":"관리자에 의해 강제 퇴장","send_fail":"메시지 전송 실패","private_send_fail":"비공개 메시지 전송 실패","update_list_fail":"사용자 목록 업데이트 실패","you_kicked":"관리자에 의해 강제 퇴장되었습니다","kick_confirm":"{} 님을 강제 퇴장시키겠습니까?","kick_title":"클라이언트 강제 퇴장","close_confirm":"서버가 실행 중입니다. 종료하시겠습니까?","close_title":"서버 종료","server_shutdown":"서버 종료됨","error":"오류","info":"정보","warning":"경고","success":"성공","language_select":"언어 선택 / Select Language","current_language":"언어","stats_online":"온라인","file_sending":"파일 전송 중"},
    "Deutsch":{"title":"Chat-Server","server_config":"Serverkonfiguration","ip_address":"IP-Adresse:","refresh":"Aktualisieren","port":"Port:","start_server":"▶ Server starten","stop_server":"■ Server stoppen","server_stopped":"● Server gestoppt","server_running":"● Server läuft","online_clients":"Online-Clients","username_col":"Benutzername","ip_col":"IP-Adresse","connect_time_col":"Verbindungszeit","server_log":"Serverprotokoll","online_count":"Online: {}","kick_hint":"Doppelklick zum Kicken","detected_ips":"Erkannte lokale IPs","port_error":"Portfehler","port_range":"Portbereich: 1024-65535","server_start_success":"Server erfolgreich gestartet","start_failed":"Start fehlgeschlagen","closing_server":"Server wird heruntergefahren...","server_stopped_msg":"Server gestoppt","accept_error":"Fehler beim Annehmen der Verbindung","new_client":"Neuer Client verbunden","client_disconnected":"Client getrennt","duplicate_username":"Benutzername bereits vergeben","duplicate_rejected":"Doppelter Benutzername, Verbindung abgelehnt","welcome_msg":"Willkommen {} im Chatraum!","leave_msg":"{} hat den Chatraum verlassen","public_msg_tag":"[Öffentlich]","private_msg_tag":"[Privat]","file_transfer_tag":"[Dateiübertragung]","file_broadcast_tag":"[Datei-Broadcast]","file_tag":"[Datei]","private_fail":"Private Nachricht fehlgeschlagen: {} nicht gefunden","user_not_exist":"Benutzer {} existiert nicht oder ist offline","file_receive_fail":"Dateiempfang fehlgeschlagen","file_transfer_error":"Dateiübertragungsfehler","process_error":"Fehler bei Nachrichtenverarbeitung","client_error":"Client-Verarbeitungsfehler","kick_reason":"Vom Administrator gekickt","send_fail":"Nachricht senden fehlgeschlagen","private_send_fail":"Private Nachricht senden fehlgeschlagen","update_list_fail":"Aktualisierung der Benutzerliste fehlgeschlagen","you_kicked":"Sie wurden vom Administrator gekickt","kick_confirm":"{} wirklich kicken?","kick_title":"Client kicken","close_confirm":"Server läuft, wirklich schließen?","close_title":"Server schließen","server_shutdown":"Server heruntergefahren","error":"Fehler","info":"Info","warning":"Warnung","success":"Erfolg","language_select":"Sprache wählen / Select Language","current_language":"Sprache","stats_online":"Online","file_sending":"Datei wird gesendet"},
    "Italiano":{"title":"Server Chat","server_config":"Configurazione Server","ip_address":"Indirizzo IP:","refresh":"Aggiorna","port":"Porta:","start_server":"▶ Avvia Server","stop_server":"■ Ferma Server","server_stopped":"● Server fermo","server_running":"● Server in esecuzione","online_clients":"Client online","username_col":"Nome utente","ip_col":"Indirizzo IP","connect_time_col":"Ora connessione","server_log":"Log Server","online_count":"Online: {}","kick_hint":"Doppio clic per espellere","detected_ips":"IP locali rilevati","port_error":"Errore porta","port_range":"Intervallo porte: 1024-65535","server_start_success":"Server avviato con successo","start_failed":"Avvio fallito","closing_server":"Arresto del server...","server_stopped_msg":"Server arrestato","accept_error":"Errore nell'accettare la connessione","new_client":"Nuovo client connesso","client_disconnected":"Client disconnesso","duplicate_username":"Nome utente già in uso","duplicate_rejected":"Nome utente duplicato, connessione rifiutata","welcome_msg":"Benvenuto {} nella chat!","leave_msg":"{} ha lasciato la chat","public_msg_tag":"[Pubblico]","private_msg_tag":"[Privato]","file_transfer_tag":"[Trasferimento file]","file_broadcast_tag":"[Broadcast file]","file_tag":"[File]","private_fail":"Messaggio privato fallito: {} non trovato","user_not_exist":"L'utente {} non esiste o è offline","file_receive_fail":"Ricezione file fallita","file_transfer_error":"Errore trasferimento file","process_error":"Errore elaborazione messaggio","client_error":"Errore elaborazione client","kick_reason":"Espulso dall'amministratore","send_fail":"Invio messaggio fallito","private_send_fail":"Invio messaggio privato fallito","update_list_fail":"Aggiornamento lista utenti fallito","you_kicked":"Sei stato espulso dall'amministratore","kick_confirm":"Espellere {}?","kick_title":"Espelli client","close_confirm":"Il server è in esecuzione, chiudere?","close_title":"Chiudi server","server_shutdown":"Server arrestato","error":"Errore","info":"Info","warning":"Attenzione","success":"Successo","language_select":"Seleziona lingua / Select Language","current_language":"Lingua","stats_online":"Online","file_sending":"Invio file in corso"},
    "English":{"title":"Chat Room Server","server_config":"Server Configuration","ip_address":"IP Address:","refresh":"Refresh","port":"Port:","start_server":"▶ Start Server","stop_server":"■ Stop Server","server_stopped":"● Server Stopped","server_running":"● Server Running","online_clients":"Online Clients","username_col":"Username","ip_col":"IP Address","connect_time_col":"Connect Time","server_log":"Server Log","online_count":"Online: {}","kick_hint":"Double-click to kick client","detected_ips":"Detected local IP addresses","port_error":"Port Error","port_range":"Port range: 1024-65535","server_start_success":"Server started successfully","start_failed":"Start failed","closing_server":"Shutting down server...","server_stopped_msg":"Server stopped","accept_error":"Error accepting connection","new_client":"New client connected","client_disconnected":"Client disconnected","duplicate_username":"Username already in use","duplicate_rejected":"Duplicate username, connection rejected","welcome_msg":"Welcome {} to the chat room!","leave_msg":"{} left the chat room","public_msg_tag":"[Public]","private_msg_tag":"[Private]","file_transfer_tag":"[File Transfer]","file_broadcast_tag":"[File Broadcast]","file_tag":"[File]","private_fail":"Private message failed: user {} not found","user_not_exist":"User {} does not exist or is offline","file_receive_fail":"File receive failed","file_transfer_error":"File transfer error","process_error":"Error processing message","client_error":"Client processing error","kick_reason":"Kicked by administrator","send_fail":"Message send failed","private_send_fail":"Private message send failed","update_list_fail":"User list update failed","you_kicked":"You have been kicked by the administrator","kick_confirm":"Are you sure you want to kick {}?","kick_title":"Kick Client","close_confirm":"Server is running, are you sure you want to close?","close_title":"Close Server","server_shutdown":"Server shutdown","error":"Error","info":"Info","warning":"Warning","success":"Success","language_select":"选择语言 / Select Language","current_language":"Language","stats_online":"Online","file_sending":"Sending file"},
    "Français":{"title":"Serveur de Chat","server_config":"Configuration du serveur","ip_address":"Adresse IP:","refresh":"Actualiser","port":"Port:","start_server":"▶ Démarrer","stop_server":"■ Arrêter","server_stopped":"● Serveur arrêté","server_running":"● Serveur en cours","online_clients":"Clients en ligne","username_col":"Utilisateur","ip_col":"Adresse IP","connect_time_col":"Heure de connexion","server_log":"Journal du serveur","online_count":"En ligne: {}","kick_hint":"Double-clic pour expulser","detected_ips":"Adresses IP détectées","port_error":"Erreur de port","port_range":"Plage de ports: 1024-65535","server_start_success":"Serveur démarré avec succès","start_failed":"Échec du démarrage","closing_server":"Arrêt du serveur...","server_stopped_msg":"Serveur arrêté","accept_error":"Erreur lors de l'acceptation","new_client":"Nouveau client connecté","client_disconnected":"Client déconnecté","duplicate_username":"Nom d'utilisateur déjà utilisé","duplicate_rejected":"Nom en double, connexion refusée","welcome_msg":"Bienvenue {} dans le chat!","leave_msg":"{} a quitté le chat","public_msg_tag":"[Public]","private_msg_tag":"[Privé]","file_transfer_tag":"[Transfert]","file_broadcast_tag":"[Diffusion]","file_tag":"[Fichier]","private_fail":"Message privé échoué: {} introuvable","user_not_exist":"Utilisateur {} inexistant ou hors ligne","file_receive_fail":"Échec de réception","file_transfer_error":"Erreur de transfert","process_error":"Erreur de traitement","client_error":"Erreur client","kick_reason":"Expulsé par l'administrateur","send_fail":"Échec d'envoi","private_send_fail":"Échec d'envoi privé","update_list_fail":"Échec de mise à jour","you_kicked":"Vous avez été expulsé","kick_confirm":"Expulser {}?","kick_title":"Expulser","close_confirm":"Serveur en cours, fermer?","close_title":"Fermer le serveur","server_shutdown":"Arrêt du serveur","error":"Erreur","info":"Info","warning":"Attention","success":"Succès","language_select":"Sélectionner la langue / Select Language","current_language":"Langue","stats_online":"En ligne","file_sending":"Envoi de fichier"},
    "Español":{"title":"Servidor de Chat","server_config":"Configuración","ip_address":"Dirección IP:","refresh":"Actualizar","port":"Puerto:","start_server":"▶ Iniciar","stop_server":"■ Detener","server_stopped":"● Servidor detenido","server_running":"● Servidor activo","online_clients":"Clientes en línea","username_col":"Usuario","ip_col":"Dirección IP","connect_time_col":"Hora de conexión","server_log":"Registro","online_count":"En línea: {}","kick_hint":"Doble clic para expulsar","detected_ips":"IPs detectadas","port_error":"Error de puerto","port_range":"Rango: 1024-65535","server_start_success":"Servidor iniciado","start_failed":"Inicio fallido","closing_server":"Cerrando servidor...","server_stopped_msg":"Servidor detenido","accept_error":"Error de aceptación","new_client":"Nuevo cliente conectado","client_disconnected":"Cliente desconectado","duplicate_username":"Nombre ya en uso","duplicate_rejected":"Nombre duplicado, rechazado","welcome_msg":"¡Bienvenido {}!","leave_msg":"{} salió del chat","public_msg_tag":"[Público]","private_msg_tag":"[Privado]","file_transfer_tag":"[Transferencia]","file_broadcast_tag":"[Difusión]","file_tag":"[Archivo]","private_fail":"Privado fallido: {} no encontrado","user_not_exist":"Usuario {} no existe","file_receive_fail":"Recepción fallida","file_transfer_error":"Error de transferencia","process_error":"Error de procesamiento","client_error":"Error de cliente","kick_reason":"Expulsado por admin","send_fail":"Envío fallido","private_send_fail":"Envío privado fallido","update_list_fail":"Actualización fallida","you_kicked":"Has sido expulsado","kick_confirm":"¿Expulsar a {}?","kick_title":"Expulsar","close_confirm":"¿Cerrar servidor?","close_title":"Cerrar","server_shutdown":"Servidor cerrado","error":"Error","info":"Info","warning":"Aviso","success":"Éxito","language_select":"Seleccionar idioma / Select Language","current_language":"Idioma","stats_online":"En línea","file_sending":"Enviando archivo"},
    "Русский":{"title":"Сервер чата","server_config":"Настройки","ip_address":"IP-адрес:","refresh":"Обновить","port":"Порт:","start_server":"▶ Запустить","stop_server":"■ Остановить","server_stopped":"● Сервер остановлен","server_running":"● Сервер работает","online_clients":"Клиенты онлайн","username_col":"Пользователь","ip_col":"IP-адрес","connect_time_col":"Время подключения","server_log":"Журнал","online_count":"Онлайн: {}","kick_hint":"Двойной клик для кика","detected_ips":"Обнаруженные IP","port_error":"Ошибка порта","port_range":"Диапазон: 1024-65535","server_start_success":"Сервер запущен","start_failed":"Ошибка запуска","closing_server":"Остановка сервера...","server_stopped_msg":"Сервер остановлен","accept_error":"Ошибка подключения","new_client":"Новый клиент","client_disconnected":"Клиент отключен","duplicate_username":"Имя уже используется","duplicate_rejected":"Имя занято, отказ","welcome_msg":"Добро пожаловать {}!","leave_msg":"{} покинул чат","public_msg_tag":"[Общее]","private_msg_tag":"[Личное]","file_transfer_tag":"[Передача]","file_broadcast_tag":"[Расслка]","file_tag":"[Файл]","private_fail":"Ошибка: {} не найден","user_not_exist":"Пользователь {} не существует","file_receive_fail":"Ошибка получения","file_transfer_error":"Ошибка передачи","process_error":"Ошибка обработки","client_error":"Ошибка клиента","kick_reason":"Отключен админом","send_fail":"Ошибка отправки","private_send_fail":"Ошибка личного сообщения","update_list_fail":"Ошибка обновления","you_kicked":"Вы отключены администратором","kick_confirm":"Отключить {}?","kick_title":"Кик","close_confirm":"Закрыть сервер?","close_title":"Закрытие","server_shutdown":"Сервер закрыт","error":"Ошибка","info":"Инфо","warning":"Внимание","success":"Успех","language_select":"Выберите язык / Select Language","current_language":"Язык","stats_online":"Онлайн","file_sending":"Отправка файла"},
    "العربية":{"title":"خادم الدردشة","server_config":"إعدادات الخادم","ip_address":"عنوان IP:","refresh":"تحديث","port":"المنفذ:","start_server":"▶ بدء","stop_server":"■ إيقاف","server_stopped":"● الخادم متوقف","server_running":"● الخادم يعمل","online_clients":"العملاء المتصلون","username_col":"المستخدم","ip_col":"عنوان IP","connect_time_col":"وقت الاتصال","server_log":"السجل","online_count":"متصل: {}","kick_hint":"نقر مزدوج للطرد","detected_ips":"عناوين IP المكتشفة","port_error":"خطأ في المنفذ","port_range":"النطاق: 1024-65535","server_start_success":"تم بدء الخادم","start_failed":"فشل البدء","closing_server":"جاري إيقاف الخادم...","server_stopped_msg":"تم إيقاف الخادم","accept_error":"خطأ في القبول","new_client":"عميل جديد متصل","client_disconnected":"تم قطع اتصال العميل","duplicate_username":"اسم المستخدم مستخدم","duplicate_rejected":"اسم مكرر، تم الرفض","welcome_msg":"!{} مرحباً","leave_msg":"{} غادر الدردشة","public_msg_tag":"[عام]","private_msg_tag":"[خاص]","file_transfer_tag":"[نقل ملف]","file_broadcast_tag":"[بث]","file_tag":"[ملف]","private_fail":"{} فشل: غير موجود","user_not_exist":"{} المستخدم غير موجود","file_receive_fail":"فشل الاستلام","file_transfer_error":"خطأ في النقل","process_error":"خطأ في المعالجة","client_error":"خطأ في العميل","kick_reason":"تم الطرد","send_fail":"فشل الإرسال","private_send_fail":"فشل الرسالة الخاصة","update_list_fail":"فشل التحديث","you_kicked":"تم طردك من قبل المشرف","kick_confirm":"?{} طرد","kick_title":"طرد","close_confirm":"إغلاق الخادم؟","close_title":"إغلاق","server_shutdown":"تم إغلاق الخادم","error":"خطأ","info":"معلومات","warning":"تحذير","success":"نجاح","language_select":"اختيار اللغة / Select Language","current_language":"اللغة","stats_online":"متصل","file_sending":"جاري الإرسال"},
    "Tiếng Việt": {"title": "Máy chủ phòng chat", "server_config": "Cấu hình máy chủ", "ip_address": "Địa chỉ IP:", "refresh": "Làm mới", "port": "Cổng:", "start_server": "▶ Khởi động máy chủ", "stop_server": "■ Dừng máy chủ", "server_stopped": "● Máy chủ chưa khởi động", "server_running": "● Máy chủ đang chạy", "online_clients": "Máy khách trực tuyến", "username_col": "Tên người dùng", "ip_col": "Địa chỉ IP", "connect_time_col": "Thời gian kết nối", "server_log": "Nhật ký máy chủ", "online_count": "Đang trực tuyến: {}", "kick_hint": "Nhấp đúp để đá máy khách", "detected_ips": "Đã phát hiện địa chỉ IP cục bộ", "port_error": "Lỗi cổng", "port_range": "Phạm vi cổng: 1024-65535", "server_start_success": "Khởi động máy chủ thành công", "start_failed": "Khởi động thất bại", "closing_server": "Đang đóng máy chủ...", "server_stopped_msg": "Máy chủ đã dừng", "accept_error": "Lỗi khi chấp nhận kết nối", "new_client": "Máy khách mới kết nối", "client_disconnected": "Máy khách ngắt kết nối", "duplicate_username": "Tên người dùng đã được sử dụng, vui lòng đổi tên khác", "duplicate_rejected": "Tên người dùng trùng lặp, từ chối kết nối", "welcome_msg": "Chào mừng {} đã vào phòng chat!", "leave_msg": "{} đã rời phòng chat", "public_msg_tag": "[Tin công khai]", "private_msg_tag": "[Nhắn riêng]", "file_transfer_tag": "[Truyền tệp]", "file_broadcast_tag": "[Phát tệp]", "file_tag": "[Tệp]", "private_fail": "Nhắn riêng thất bại: người dùng {} không tồn tại", "user_not_exist": "Người dùng {} không tồn tại hoặc đã ngoại tuyến", "file_receive_fail": "Nhận tệp thất bại", "file_transfer_error": "Lỗi truyền tệp", "process_error": "Lỗi khi xử lý tin nhắn", "client_error": "Lỗi xử lý máy khách", "kick_reason": "Bị quản trị viên đá", "send_fail": "Gửi tin nhắn thất bại", "private_send_fail": "Gửi tin nhắn riêng thất bại", "update_list_fail": "Cập nhật danh sách người dùng thất bại", "you_kicked": "Bạn đã bị quản trị viên đá khỏi phòng chat", "kick_confirm": "Xác nhận đá {}?", "kick_title": "Đá máy khách", "close_confirm": "Máy chủ đang chạy, xác nhận đóng?", "close_title": "Đóng máy chủ", "server_shutdown": "Máy chủ đã tắt", "error": "Lỗi", "info": "Thông tin", "warning": "Cảnh báo", "success": "Thành công", "language_select": "Chọn ngôn ngữ / Select Language", "current_language": "Ngôn ngữ", "stats_online": "Đang trực tuyến", "file_sending": "Đang gửi tệp"}, 
    "Türkçe": {"title": "Sohbet Odası Sunucusu", "server_config": "Sunucu Yapılandırması", "ip_address": "IP adresi:", "refresh": "Yenile", "port": "Port:", "start_server": "▶ Sunucuyu Başlat", "stop_server": "■ Sunucuyu Durdur", "server_stopped": "● Sunucu başlatılmadı", "server_running": "● Sunucu çalışıyor", "online_clients": "Çevrimiçi İstemciler", "username_col": "Kullanıcı Adı", "ip_col": "IP Adresi", "connect_time_col": "Bağlantı Zamanı", "server_log": "Sunucu Günlüğü", "online_count": "Çevrimiçi: {}", "kick_hint": "İstemciyi atmak için çift tıklayın", "detected_ips": "Yerel IP adresleri algılandı", "port_error": "Port hatası", "port_range": "Port aralığı: 1024-65535", "server_start_success": "Sunucu başarıyla başlatıldı", "start_failed": "Başlatma başarısız", "closing_server": "Sunucu kapatılıyor...", "server_stopped_msg": "Sunucu durduruldu", "accept_error": "Bağlantı kabul edilirken hata oluştu", "new_client": "Yeni istemci bağlandı", "client_disconnected": "İstemci bağlantısı kesildi", "duplicate_username": "Kullanıcı adı zaten kullanımda, lütfen başka bir ad deneyin", "duplicate_rejected": "Kullanıcı adı tekrarı, bağlantı reddedildi", "welcome_msg": "{} sohbet odasına hoş geldiniz!", "leave_msg": "{} sohbet odasından ayrıldı", "public_msg_tag": "[Herkese Açık]", "private_msg_tag": "[Özel]", "file_transfer_tag": "[Dosya Transferi]", "file_broadcast_tag": "[Dosya Yayını]", "file_tag": "[Dosya]", "private_fail": "Özel mesaj başarısız: {} kullanıcısı mevcut değil", "user_not_exist": "{} kullanıcısı mevcut değil veya çevrimdışı", "file_receive_fail": "Dosya alımı başarısız", "file_transfer_error": "Dosya transfer hatası", "process_error": "Mesaj işlenirken hata oluştu", "client_error": "İstemci işleme hatası", "kick_reason": "Yönetici tarafından atıldı", "send_fail": "Mesaj gönderimi başarısız", "private_send_fail": "Özel mesaj gönderimi başarısız", "update_list_fail": "Kullanıcı listesi güncellemesi başarısız", "you_kicked": "Yönetici tarafından sohbet odasından atıldınız", "kick_confirm": "{} atılsın mı?", "kick_title": "İstemciyi At", "close_confirm": "Sunucu çalışıyor, kapatmak istediğinize emin misiniz?", "close_title": "Sunucuyu Kapat", "server_shutdown": "Sunucu kapatıldı", "error": "Hata", "info": "Bilgi", "warning": "Uyarı", "success": "Başarılı", "language_select": "Dil Seçin / Select Language", "current_language": "Dil", "stats_online": "Çevrimiçi", "file_sending": "Dosya gönderiliyor"}, 
    "Polski": {"title": "Serwer czatu", "server_config": "Konfiguracja serwera", "ip_address": "Adres IP:", "refresh": "Odśwież", "port": "Port:", "start_server": "▶ Uruchom serwer", "stop_server": "■ Zatrzymaj serwer", "server_stopped": "● Serwer nieuruchomiony", "server_running": "● Serwer działa", "online_clients": "Klienci online", "username_col": "Nazwa użytkownika", "ip_col": "Adres IP", "connect_time_col": "Czas połączenia", "server_log": "Dziennik serwera", "online_count": "Online: {}", "kick_hint": "Kliknij dwukrotnie, aby wyrzucić klienta", "detected_ips": "Wykryto lokalne adresy IP", "port_error": "Błąd portu", "port_range": "Zakres portów: 1024-65535", "server_start_success": "Serwer uruchomiony pomyślnie", "start_failed": "Uruchomienie nie powiodło się", "closing_server": "Zamykanie serwera...", "server_stopped_msg": "Serwer zatrzymany", "accept_error": "Błąd podczas akceptowania połączenia", "new_client": "Nowy klient połączony", "client_disconnected": "Klient rozłączony", "duplicate_username": "Nazwa użytkownika jest już zajęta, wybierz inną", "duplicate_rejected": "Duplikat nazwy, połączenie odrzucone", "welcome_msg": "Witaj {} na czacie!", "leave_msg": "{} opuścił czat", "public_msg_tag": "[Publiczne]", "private_msg_tag": "[Prywatne]", "file_transfer_tag": "[Transfer pliku]", "file_broadcast_tag": "[Rozgłaszanie pliku]", "file_tag": "[Plik]", "private_fail": "Prywatna wiadomość nie powiodła się: użytkownik {} nie istnieje", "user_not_exist": "Użytkownik {} nie istnieje lub jest offline", "file_receive_fail": "Odbiór pliku nie powiódł się", "file_transfer_error": "Błąd transferu pliku", "process_error": "Błąd przetwarzania wiadomości", "client_error": "Błąd przetwarzania klienta", "kick_reason": "Wyrzucony przez administratora", "send_fail": "Wysyłanie wiadomości nie powiodło się", "private_send_fail": "Wysyłanie prywatnej wiadomości nie powiodło się", "update_list_fail": "Aktualizacja listy użytkowników nie powiodła się", "you_kicked": "Zostałeś wyrzucony z czatu przez administratora", "kick_confirm": "Na pewno wyrzucić {}?", "kick_title": "Wyrzuć klienta", "close_confirm": "Serwer jest uruchomiony, na pewno zamknąć?", "close_title": "Zamknij serwer", "server_shutdown": "Serwer wyłączony", "error": "Błąd", "info": "Informacja", "warning": "Ostrzeżenie", "success": "Sukces", "language_select": "Wybierz język / Select Language", "current_language": "Język", "stats_online": "Online", "file_sending": "Wysyłanie pliku"}, 
    "Bahasa Indonesia": {"title": "Server Ruang Obrolan", "server_config": "Konfigurasi Server", "ip_address": "Alamat IP:", "refresh": "Segarkan", "port": "Port:", "start_server": "▶ Mulai Server", "stop_server": "■ Hentikan Server", "server_stopped": "● Server belum dimulai", "server_running": "● Server berjalan", "online_clients": "Klien Daring", "username_col": "Nama Pengguna", "ip_col": "Alamat IP", "connect_time_col": "Waktu Koneksi", "server_log": "Log Server", "online_count": "Daring: {}", "kick_hint": "Klik dua kali untuk menendang klien", "detected_ips": "Alamat IP lokal terdeteksi", "port_error": "Kesalahan port", "port_range": "Rentang port: 1024-65535", "server_start_success": "Server berhasil dimulai", "start_failed": "Gagal memulai", "closing_server": "Menutup server...", "server_stopped_msg": "Server dihentikan", "accept_error": "Kesalahan saat menerima koneksi", "new_client": "Klien baru terhubung", "client_disconnected": "Klien terputus", "duplicate_username": "Nama pengguna sudah digunakan, silakan ganti nama lain", "duplicate_rejected": "Nama pengguna ganda, koneksi ditolak", "welcome_msg": "Selamat datang {} di ruang obrolan!", "leave_msg": "{} meninggalkan ruang obrolan", "public_msg_tag": "[Pesan Umum]", "private_msg_tag": "[Pribadi]", "file_transfer_tag": "[Transfer Berkas]", "file_broadcast_tag": "[Siaran Berkas]", "file_tag": "[Berkas]", "private_fail": "Pesan pribadi gagal: pengguna {} tidak ada", "user_not_exist": "Pengguna {} tidak ada atau sedang luring", "file_receive_fail": "Penerimaan berkas gagal", "file_transfer_error": "Kesalahan transfer berkas", "process_error": "Kesalahan saat memproses pesan", "client_error": "Kesalahan pemrosesan klien", "kick_reason": "Ditendang oleh administrator", "send_fail": "Pengiriman pesan gagal", "private_send_fail": "Pengiriman pesan pribadi gagal", "update_list_fail": "Pembaruan daftar pengguna gagal", "you_kicked": "Anda telah ditendang dari ruang obrolan oleh administrator", "kick_confirm": "Yakin menendang {}?", "kick_title": "Tendang Klien", "close_confirm": "Server sedang berjalan, yakin ingin menutup?", "close_title": "Tutup Server", "server_shutdown": "Server dimatikan", "error": "Kesalahan", "info": "Informasi", "warning": "Peringatan", "success": "Berhasil", "language_select": "Pilih Bahasa / Select Language", "current_language": "Bahasa", "stats_online": "Daring", "file_sending": "Mengirim berkas"},
    "Ελληνικά": {"title": "Διακομιστής Δωματίου Συνομιλίας", "server_config": "Ρυθμίσεις Διακομιστή", "ip_address": "Διεύθυνση IP:", "refresh": "Ανανέωση", "port": "Θύρα:", "start_server": "▶ Εκκίνηση Διακομιστή", "stop_server": "■ Διακοπή Διακομιστή", "server_stopped": "● Ο διακομιστής δεν εκκινήθηκε", "server_running": "● Ο διακομιστής λειτουργεί", "online_clients": "Συνδεδεμένοι Χρήστες", "username_col": "Όνομα Χρήστη", "ip_col": "Διεύθυνση IP", "connect_time_col": "Ώρα Σύνδεσης", "server_log": "Αρχείο Καταγραφής", "online_count": "Συνδεδεμένοι: {}", "kick_hint": "Διπλό κλικ για αποβολή χρήστη", "detected_ips": "Εντοπίστηκαν τοπικές διευθύνσεις IP", "port_error": "Σφάλμα θύρας", "port_range": "Εύρος θυρών: 1024-65535", "server_start_success": "Ο διακομιστής εκκινήθηκε με επιτυχία", "start_failed": "Η εκκίνηση απέτυχε", "closing_server": "Κλείσιμο διακομιστή...", "server_stopped_msg": "Ο διακομιστής διακόπηκε", "accept_error": "Σφάλμα αποδοχής σύνδεσης", "new_client": "Νέα σύνδεση χρήστη", "client_disconnected": "Ο χρήστης αποσυνδέθηκε", "duplicate_username": "Το όνομα χρήστη χρησιμοποιείται ήδη, παρακαλώ επιλέξτε άλλο", "duplicate_rejected": "Διπλότυπο όνομα χρήστη, η σύνδεση απορρίφθηκε", "welcome_msg": "Καλώς ήρθες {} στο δωμάτιο συνομιλίας!", "leave_msg": "Ο {} αποχώρησε από το δωμάτιο", "public_msg_tag": "[Δημόσιο Μήνυμα]", "private_msg_tag": "[Ιδιωτικό]", "file_transfer_tag": "[Μεταφορά Αρχείου]", "file_broadcast_tag": "[Μετάδοση Αρχείου]", "file_tag": "[Αρχείο]", "private_fail": "Το ιδιωτικό μήνυμα απέτυχε: ο χρήστης {} δεν υπάρχει", "user_not_exist": "Ο χρήστης {} δεν υπάρχει ή είναι εκτός σύνδεσης", "file_receive_fail": "Η λήψη αρχείου απέτυχε", "file_transfer_error": "Σφάλμα μεταφοράς αρχείου", "process_error": "Σφάλμα επεξεργασίας μηνύματος", "client_error": "Σφάλμα επεξεργασίας χρήστη", "kick_reason": "Αποβλήθηκε από τον διαχειριστή", "send_fail": "Η αποστολή μηνύματος απέτυχε", "private_send_fail": "Η αποστολή ιδιωτικού μηνύματος απέτυχε", "update_list_fail": "Η ενημέρωση λίστας χρηστών απέτυχε", "you_kicked": "Αποβληθήκατε από το δωμάτιο συνομιλίας από τον διαχειριστή", "kick_confirm": "Είστε βέβαιοι για την αποβολή του {};", "kick_title": "Αποβολή Χρήστη", "close_confirm": "Ο διακομιστής λειτουργεί, είστε βέβαιοι ότι θέλετε να τον κλείσετε;", "close_title": "Κλείσιμο Διακομιστή", "server_shutdown": "Ο διακομιστής τερματίστηκε", "error": "Σφάλμα", "info": "Πληροφορία", "warning": "Προειδοποίηση", "success": "Επιτυχία", "language_select": "Επιλογή Γλώσσας / Select Language", "current_language": "Γλώσσα", "stats_online": "Συνδεδεμένοι", "file_sending": "Αποστολή αρχείου"},
    "བོད་སྐད།": {"title": "སྐད་ཕྲིན་ཁང་སེར་བར།", "server_config": "སེར་བར་སྒྲིག་འཛུགས།", "ip_address": "IP ཁ་བྱང་།:", "refresh": "གསར་བསྐྱར།", "port": "སྒོ་ཨང་།:", "start_server": "▶ སེར་བར་འགོ་འཛུགས།", "stop_server": "■ སེར་བར་མཚམས་འཇོག", "server_stopped": "● སེར་བར་འགོ་མ་འཛུགས།", "server_running": "● སེར་བར་བཀོལ་སྤྱོད་བྱེད་བཞིན་ཡོད།", "online_clients": "དྲ་ཐོག་བེད་སྤྱོད་པ།", "username_col": "བེད་སྤྱོད་མིང་།", "ip_col": "IP ཁ་བྱང་།", "connect_time_col": "མཐུད་སྦྲེལ་དུས་ཚོད།", "server_log": "སེར་བར་དྲན་དེབ།", "online_count": "དྲ་ཐོག་ཁ་གྲངས།: {}", "kick_hint": "བེད་སྤྱོད་པ་ཕྱིར་འབུད་བྱེད་པར་གཉིས་རྡེབ་གནང་།", "detected_ips": "ས་གནས་IP ཁ་བྱང་ཚོར་ཟིན།", "port_error": "སྒོ་ཨང་ནོར་འཁྲུལ།", "port_range": "སྒོ་ཨང་ཁྱོན།: 1024-65535", "server_start_success": "སེར་བར་འགོ་འཛུགས་ལེགས་འགྲུབ་བྱུང་།", "start_failed": "འགོ་འཛུགས་མ་ཐུབ།", "closing_server": "སེར་བར་ཁ་བརྒྱབ་བཞིན་ཡོད།...", "server_stopped_msg": "སེར་བར་མཚམས་འཇོག་བྱས་ཟིན།", "accept_error": "མཐུད་སྦྲེལ་དང་ལེན་སྐབས་ནོར་འཁྲུལ་བྱུང་།", "new_client": "བེད་སྤྱོད་པ་གསར་པ་མཐུད་སྦྲེལ་བྱས་ཡོད།", "client_disconnected": "བེད་སྤྱོད་པའི་མཐུད་སྦྲེལ་ཆད་སོང་།", "duplicate_username": "བེད་སྤྱོད་མིང་དེ་བེད་སྤྱོད་བྱས་ཟིན། མིང་གཞན་བརྗེ་རོགས་གནང་།", "duplicate_rejected": "བེད་སྤྱོད་མིང་བསྐྱར་ཟློས་ཡོད། མཐུད་སྦྲེལ་ཁས་མི་ལེན།", "welcome_msg": "{} སྐད་ཕྲིན་ཁང་ལ་ཕེབས་པར་དགའ་བསུ་ཞུ།", "leave_msg": "{} སྐད་ཕྲིན་ཁང་ནས་ཕྱིར་ཐོན་སོང་།", "public_msg_tag": "[མང་སྤྱོད་སྐད་ཕྲིན]", "private_msg_tag": "[སྒེར་གྱི་སྐད་ཕྲིན]", "file_transfer_tag": "[ཡིག་ཆ་སྤྲོད་ལེན]", "file_broadcast_tag": "[ཡིག་ཆ་ཁྱབ་བསྒྲགས]", "file_tag": "[ཡིག་ཆ]", "private_fail": "སྒེར་སྐད་ཕྲིན་མ་ཐུབ།: བེད་སྤྱོད་པ {} མེད།", "user_not_exist": "བེད་སྤྱོད་པ {} མེད་པའམ་དྲ་ཐོག་ནས་ཕྱིར་ཐོན་ཟིན།", "file_receive_fail": "ཡིག་ཆ་དང་ལེན་མ་ཐུབ།", "file_transfer_error": "ཡིག་ཆ་སྤྲོད་ལེན་ནོར་འཁྲུལ།", "process_error": "སྐད་ཕྲིན་བཟོ་སྒྲིག་སྐབས་ནོར་འཁྲུལ་བྱུང་།", "client_error": "བེད་སྤྱོད་པའི་བཟོ་སྒྲིག་ནོར་འཁྲུལ།", "kick_reason": "དོ་དམ་པས་ཕྱིར་འབུད་བྱས་ཟིན།", "send_fail": "སྐད་ཕྲིན་གཏོང་སྐྱེལ་མ་ཐུབ།", "private_send_fail": "སྒེར་སྐད་ཕྲིན་གཏོང་སྐྱེལ་མ་ཐུབ།", "update_list_fail": "བེད་སྤྱོད་པའི་ཐོ་གཞུང་གསར་བསྐྱར་མ་ཐུབ།", "you_kicked": "ཁྱེད་རང་དོ་དམ་པས་སྐད་ཕྲིན་ཁང་ནས་ཕྱིར་འབུད་བྱས་ཟིན།", "kick_confirm": "{} ཕྱིར་འབུད་བྱེད་རྒྱུར་གཏན་འབེབས་བྱས་ཟིན་ནམ།", "kick_title": "བེད་སྤྱོད་པ་ཕྱིར་འབུད།", "close_confirm": "སེར་བར་བཀོལ་སྤྱོད་བྱེད་བཞིན་ཡོད། ཁ་བརྒྱབ་རྒྱུར་གཏན་འབེབས་བྱས་ཟིན་ནམ།", "close_title": "སེར་བར་ཁ་རྒྱག", "server_shutdown": "སེར་བར་ཁ་བརྒྱབ་ཟིན།", "error": "ནོར་འཁྲུལ།", "info": "གནས་ཚུལ།", "warning": "ཉེན་བརྡ།", "success": "ལེགས་འགྲུབ།", "language_select": "སྐད་ཡིག་འདེམས། / Select Language", "current_language": "སྐད་ཡིག", "stats_online": "དྲ་ཐོག་ཁ་གྲངས།", "file_sending": "ཡིག་ཆ་གཏོང་བཞིན་ཡོད།"}
}

LANGUAGE_LIST = list(TRANSLATIONS.keys())
LANGUAGE_LIST.sort()

# ==================== 字体配置 ====================
SPECIAL_FONT_KEYS = ["zh-cn","bo-cn", "zh-tw", "ja-jp", "ko-kr", "ar-sa","vi-vn"]
SPECIAL_FONT_VALUES = [
    ["Maple Mono NF CN","Maple Mono NL CN","Cascadia Next SC", "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", "SimHei", "SimSun", "TkDefaultFont"],
    ["Monlam Bodyig","Microsoft Himalaya","TkDefaultFont"],
    ["Cica","Myrica","Noto Sans Mono CJK TC","Cascadia Next TC", "Microsoft JhengHei UI", "Microsoft JhengHei", "PingFang TC", "TkDefaultFont"],
    ["Noto Sans Mono CJK JP","Cascadia Next JP", "MS Gothic UI", "MS Gothic", "MS UI Gothic", "Meiryo UI", "Hiragino Sans", "TkDefaultFont"],
    ["D2CodingLigature Nerd Font","Noto Sans Mono CJK KR","Malgun Gothic", "맑은 고딕", "Gulim", "Apple SD Gothic Neo", "TkDefaultFont"],
    ["Segoe UI", "Tahoma", "TkDefaultFont"],
    ["Maple Mono NF CN","Maple Mono NL CN","Maple Mono","Segoe UI","Tahoma","TkDefaultFont"]
]
MONO_FONTS = ["Maple Mono NF CN","Maple Mono NL CN","Maple Mono","Cascadia Mono", "Cascadia Code", "Consolas", "Courier New", "TkDefaultFont"]

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
        self.fnt = self._select(self._get_special('en-us'))
        self.codefnt = self.fnt if 'Cascadia Next' in self.fnt or self.fnt.startswith('Noto Sans Mono CJK') or "D2CodingLigature Nerd Font" in self.fnt or self.fnt=='Cica' or self.fnt=='Myrica' or 'Maple Mono' in self.fnt else self.default_mono

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


class ChatServerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("聊天室服务器")
        self.root.geometry("1000x700")
        self.root.minsize(600, 400)

        self.server = None
        self.clients = {}
        self.buffer_size = 4096
        self.is_running = False
        self.lock = threading.Lock()
        self.current_language = 'English'
        self.emoji_supported = supports_emoji()

        self.font_manager = FontManager()
        self.fnt = self.font_manager.fnt
        self.codefnt = self.font_manager.codefnt

        # 初始化 ttk 主题
        self.init_theme()

        self.setup_ui()
        self.get_local_ip()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # print(f"服务器启动 - UI字体: {self.fnt}, 等宽字体: {self.codefnt}")

    def init_theme(self):
        """初始化 ttk 主题"""
        self.style = ttk.Style()
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        elif 'alt' in available_themes:
            self.style.theme_use('alt')
        elif 'default' in available_themes:
            self.style.theme_use('default')
        self._apply_styles()

    def _apply_styles(self):
        """应用全局样式"""
        self.style.configure('TButton', font=(self.fnt, 9))
        self.style.configure('TLabel', font=(self.fnt, 9))
        self.style.configure('Bold.TLabel', font=(self.fnt, 10, 'bold'))
        # LabelFrame 标题字体
        self.style.configure('TLabelframe.Label', font=(self.fnt, 9))
        # Treeview 列标题字体
        self.style.configure('Treeview.Heading', font=(self.fnt, 9))

    def t(self, key, *args):
        text = TRANSLATIONS.get(self.current_language, {}).get(key, key)
        return text.format(*args) if args else text

    def get_emoji(self, ek, tk=None):
        return ek if self.emoji_supported else (self.t(tk) if tk else '')

    def update_font(self, lang):
        """根据语言更新字体"""
        old_codefnt = self.codefnt
        self.fnt = self.font_manager.get_font(lang)

        if 'Cascadia Next' in self.fnt or self.fnt.startswith('Noto Sans Mono CJK') or "D2CodingLigature Nerd Font" in self.fnt or self.fnt=='Cica' or self.fnt=='Myrica' or 'Maple Mono' in self.fnt:
            self.codefnt = self.fnt
        else:
            self.codefnt = self.font_manager.get_code_font()

        # 更新全局样式
        self._apply_styles()

        # 更新日志显示区域字体
        if hasattr(self, 'log_disp') and self.codefnt != old_codefnt:
            self.log_disp.configure(font=(self.codefnt, 9))

        # 更新服务器状态标签字体
        if hasattr(self, 'status_label'):
            self.status_label.configure(font=(self.fnt, 10, 'bold'))

        # print(f"字体切换 - 语言: {lang}, UI: {self.fnt}, 等宽: {self.codefnt}")

    def setup_ui(self):
        mf = ttk.Frame(self.root, padding="10")
        mf.pack(fill=tk.BOTH, expand=True)

        # 语言选择框架
        lf = ttk.Frame(mf)
        lf.pack(fill=tk.X, pady=(0, 5))
        self.lang_label = ttk.Label(lf, text=f"{self.t('language_select')}: ", font=(self.fnt, 9))
        self.lang_label.pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value='English')
        self.lang_combo = ttk.Combobox(lf, textvariable=self.lang_var, values=LANGUAGE_LIST, state='readonly', width=16, font=(self.fnt, 9))
        self.lang_combo.pack(side=tk.LEFT)
        self.lang_combo.bind('<<ComboboxSelected>>', self.change_lang)

        # 服务器配置框架
        self.cfg_frame = ttk.LabelFrame(mf, text=self.t('server_config'), padding="10")
        self.cfg_frame.pack(fill=tk.X, pady=(0, 10))

        self.ip_label = ttk.Label(self.cfg_frame, text=self.t('ip_address'), font=(self.fnt, 10))
        self.ip_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ip_var = tk.StringVar()
        self.ip_combo = ttk.Combobox(self.cfg_frame, textvariable=self.ip_var, state='readonly', width=20, font=(self.codefnt, 10))
        self.ip_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.ref_btn = ttk.Button(self.cfg_frame, text=self.t('refresh'), command=self.get_local_ip, width=8)
        self.ref_btn.grid(row=0, column=2, padx=5, pady=5)
        self.port_label = ttk.Label(self.cfg_frame, text=self.t('port'), font=(self.fnt, 10))
        self.port_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.port_var = tk.StringVar(value="55555")
        self.port_spin = ttk.Spinbox(self.cfg_frame, from_=1024, to=65535, textvariable=self.port_var, width=10, font=(self.codefnt, 10))
        self.port_spin.grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.start_btn = ttk.Button(self.cfg_frame, text=self.get_emoji('▶ ', 'start_server') or self.t('start_server'), command=self.toggle, width=15)
        self.start_btn.grid(row=0, column=5, padx=10, pady=5)
        self.status_var = tk.StringVar(value=self.t('server_stopped'))
        self.status_label = ttk.Label(self.cfg_frame, textvariable=self.status_var, font=(self.fnt, 10, 'bold'))
        self.status_label.grid(row=0, column=6, padx=20, pady=5)

        # 中间框架
        mid = ttk.Frame(mf)
        mid.pack(fill=tk.BOTH, expand=True)

        # 在线客户端框架
        self.cli_frame = ttk.LabelFrame(mid, text=self.t('online_clients'), padding="5")
        self.cli_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        self.tree = ttk.Treeview(self.cli_frame, columns=('u', 'i', 't'), show='headings', height=8)
        self.tree.heading('u', text=self.t('username_col'))
        self.tree.heading('i', text=self.t('ip_col'))
        self.tree.heading('t', text=self.t('connect_time_col'))
        self.tree.column('u', width=120)
        self.tree.column('i', width=150)
        self.tree.column('t', width=120)
        ts = ttk.Scrollbar(self.cli_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=ts.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ts.pack(side=tk.RIGHT, fill=tk.Y)

        # 服务器日志框架
        self.log_frame = ttk.LabelFrame(mid, text=self.t('server_log'), padding="5")
        self.log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.log_disp = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, font=(self.codefnt, 9), state='disabled')
        self.log_disp.pack(fill=tk.BOTH, expand=True)
        for t, f in [('info', 'blue'), ('warning', 'orange'), ('error', 'red'), ('success', 'green'), ('timestamp', 'gray')]:
            self.log_disp.tag_config(t, foreground=f)

        # 统计框架
        sf = ttk.Frame(mf)
        sf.pack(fill=tk.X, pady=(10, 0))
        self.stats_var = tk.StringVar(value=self.t('online_count', 0))
        self.stats_label = ttk.Label(sf, textvariable=self.stats_var, font=(self.fnt, 9))
        self.stats_label.pack(side=tk.LEFT)
        self.kick_label = ttk.Label(sf, text=self.t('kick_hint'), font=(self.fnt, 9))
        self.kick_label.pack(side=tk.RIGHT)
        self.tree.bind('<Double-Button-1>', self.kick)

    def change_lang(self, event=None):
        old = self.current_language
        self.current_language = self.lang_var.get()
        self.update_font(self.current_language)
        if old != self.current_language:
            # 窗口标题
            self.root.title(self.t('title'))
            # 语言选择
            self.lang_label.configure(text=f"{self.t('language_select')}: ", font=(self.fnt, 9))
            self.lang_combo.configure(font=(self.fnt, 9))
            # 服务器配置框架
            self.cfg_frame.configure(text=self.t('server_config'))
            # IP地址
            self.ip_label.configure(text=self.t('ip_address'), font=(self.fnt, 10))
            self.ip_combo.configure(font=(self.codefnt, 10))
            # 刷新按钮
            self.ref_btn.configure(text=self.t('refresh'))
            # 端口
            self.port_label.configure(text=self.t('port'), font=(self.fnt, 10))
            self.port_spin.configure(font=(self.codefnt, 10))
            # 启停按钮
            btn_text = self.get_emoji('■ ', 'stop_server') or self.t('stop_server') if self.is_running else self.get_emoji('▶ ', 'start_server') or self.t('start_server')
            self.start_btn.configure(text=btn_text)
            # 服务器状态标签
            self.status_var.set(self.t('server_running') if self.is_running else self.t('server_stopped'))
            self.status_label.configure(font=(self.fnt, 10, 'bold'))
            # 在线客户端框架
            self.cli_frame.configure(text=self.t('online_clients'))
            self.tree.heading('u', text=self.t('username_col'))
            self.tree.heading('i', text=self.t('ip_col'))
            self.tree.heading('t', text=self.t('connect_time_col'))
            # 服务器日志框架
            self.log_frame.configure(text=self.t('server_log'))
            self.log_disp.configure(font=(self.codefnt, 9))
            # 统计标签
            self.stats_var.set(self.t('online_count', len(self.clients)))
            self.stats_label.configure(font=(self.fnt, 9))
            # 踢出提示标签
            self.kick_label.configure(text=self.t('kick_hint'), font=(self.fnt, 9))

    def get_local_ip(self):
        ips = []
        try:
            hn = socket.gethostname()
            lip = socket.gethostbyname(hn)
            if lip != '127.0.0.1':
                ips.append(lip)
            for iface in socket.getaddrinfo(hn, None):
                ip = iface[4][0]
                if ip not in ips and not ip.startswith('127.'):
                    ips.append(ip)
        except:
            pass
        if not ips:
            ips = ['127.0.0.1']
        ips.insert(0, '0.0.0.0')
        if ips:
            self.ip_combo.set(ips[0])
        del_tag = []
        for i in range(len(ips)):
            if ':' in ips[i] or len(ips[i]) > 16:
                del_tag.append(ips[i])
        
        for i in del_tag:
            ips.remove(i)
        del del_tag
        self.ip_combo['values'] = ips
        self.log(f"{self.t('detected_ips')}: {', '.join(ips[1:] if len(ips) > 1 else ips)}", 'info')

    def toggle(self):
        self.start() if not self.is_running else self.stop()

    def start(self):
        h, ps = self.ip_var.get(), self.port_var.get()
        try:
            p = int(ps)
            if p < 1024 or p > 65535:
                raise ValueError(self.t('port_range'))
        except ValueError as e:
            messagebox.showerror(self.t('port_error'), str(e))
            return
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((h, p))
            self.server.listen(5)
            self.server.settimeout(1)
            self.is_running = True
            self._update_ui(True)
            self.log(f"{self.t('server_start_success')} - {h}:{p}", 'success')
            self.status_var.set(self.t('server_running'))
            threading.Thread(target=self.accept, daemon=True).start()
        except Exception as e:
            self.log(f"{self.t('start_failed')}: {str(e)}", 'error')
            messagebox.showerror(self.t('start_failed'), str(e))
            if self.server:
                self.server.close()
                self.server = None

    def stop(self):
        self.log(self.t('closing_server'), 'warning')
        self.is_running = False
        with self.lock:
            for cs in list(self.clients.keys()):
                self._remove(cs, self.t('server_shutdown'))
        if self.server:
            try:
                self.server.close()
            except:
                pass
            self.server = None
        self._update_ui(False)
        self.status_var.set(self.t('server_stopped'))
        self.log(self.t('server_stopped_msg'), 'info')

    def _update_ui(self, running):
        btn_text = self.get_emoji('■ ', 'stop_server') or self.t('stop_server') if running else self.get_emoji('▶ ', 'start_server') or self.t('start_server')
        self.start_btn.configure(text=btn_text)
        self.status_label.configure(font=(self.fnt, 10, 'bold'))
        self.ip_combo.configure(state='disabled' if running else 'readonly')
        self.port_spin.configure(state='disabled' if running else '!disabled')

    def accept(self):
        while self.is_running:
            try:
                cs, addr = self.server.accept()
                threading.Thread(target=self.handle, args=(cs, addr), daemon=True).start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.is_running:
                    self.log(f"{self.t('accept_error')}: {str(e)}", 'error')
                break

    def recv_all(self, cs, length):
        data = b''
        while len(data) < length:
            try:
                chunk = cs.recv(min(self.buffer_size, length - len(data)))
                if not chunk:
                    return None
                data += chunk
            except socket.timeout:
                continue
        return data

    def recv_msg(self, cs):
        h = self.recv_all(cs, 4)
        if not h:
            return None
        msg_len = int.from_bytes(h, 'big')
        d = self.recv_all(cs, msg_len)
        return d.decode('utf-8') if d else None

    def send_to(self, cs, msg):
        d = msg.encode('utf-8')
        h = len(d).to_bytes(4, 'big')
        try:
            cs.sendall(h + d)
            return True
        except:
            return False

    def handle(self, cs, addr):
        username = None
        try:
            username = self.recv_msg(cs)
            if not username:
                return
            with self.lock:
                if any(info['username'] == username for info in self.clients.values()):
                    self.send_to(cs, json.dumps({'type': 'system', 'message': self.t('duplicate_username')}))
                    cs.close()
                    self.log(f"{self.t('duplicate_rejected')}: {username}", 'warning')
                    return
                ct = datetime.now().strftime('%H:%M:%S')
                self.clients[cs] = {'username': username, 'address': f"{addr[0]}:{addr[1]}", 'connect_time': ct}
            self.root.after(0, self._add_client, username, addr[0], ct)
            self.log(f"{self.t('new_client')}: {username} {addr[0]}:{addr[1]}", 'success')
            self.broadcast(json.dumps({'type': 'system', 'message': self.t('welcome_msg', username), 'time': datetime.now().strftime('%H:%M:%S')}), cs)
            self._update_list()
            while self.is_running:
                msg = self.recv_msg(cs)
                if not msg:
                    break
                try:
                    md = json.loads(msg)
                except:
                    continue
                if md['type'] == 'public':
                    self.broadcast(json.dumps({'type': 'public', 'username': username, 'message': md['message'], 'time': datetime.now().strftime('%H:%M:%S')}), cs)
                    self.log(f"{self.t('public_msg_tag')} {username}: {md['message'][:50]}", 'info')
                elif md['type'] == 'private':
                    pm = json.dumps({'type': 'private', 'from': username, 'message': md['message'], 'time': datetime.now().strftime('%H:%M:%S')})
                    if not self._send_private(pm, md['to']):
                        self.send_to(cs, json.dumps({'type': 'system', 'message': self.t('user_not_exist', md['to'])}))
                elif md['type'] == 'file_start':
                    self._handle_file(cs, username, md)
        except Exception as e:
            self.log(f"{self.t('client_error')}: {str(e)}", 'error')
        finally:
            if username:
                self._remove(cs, self.t('client_disconnected'))
            else:
                try:
                    cs.close()
                except:
                    pass

    def _handle_file(self, cs, username, data):
        try:
            fd = self.recv_all(cs, data['size'])
            if not fd:
                return
            fm = json.dumps({'type': 'file', 'from': username, 'filename': data['filename'], 'size': data['size'], 'time': datetime.now().strftime('%H:%M:%S')})
            if data.get('to'):
                with self.lock:
                    for c, info in self.clients.items():
                        if info['username'] == data['to']:
                            if self.send_to(c, fm):
                                c.send(data['size'].to_bytes(8, 'big'))
                                c.sendall(fd)
                            break
            else:
                with self.lock:
                    for c in list(self.clients.keys()):
                        if c != cs:
                            try:
                                self.send_to(c, fm)
                                c.send(data['size'].to_bytes(8, 'big'))
                                c.sendall(fd)
                            except:
                                self._remove(c, self.t('send_fail'))
        except Exception as e:
            self.log(f"{self.t('file_transfer_error')}: {str(e)}", 'error')

    def broadcast(self, msg, sender=None):
        failed = []
        with self.lock:
            for c in list(self.clients.keys()):
                if c != sender and not self.send_to(c, msg):
                    failed.append(c)
        for c in failed:
            self._remove(c, self.t('send_fail'))

    def _send_private(self, msg, target):
        with self.lock:
            for c, info in self.clients.items():
                if info['username'] == target:
                    if self.send_to(c, msg):
                        return True
                    self._remove(c, self.t('private_send_fail'))
                    return False
        return False

    def _update_list(self):
        with self.lock:
            users = [info['username'] for info in self.clients.values()]
            msg = json.dumps({'type': 'user_list', 'users': users})
            failed = [c for c in list(self.clients.keys()) if not self.send_to(c, msg)]
        for c in failed:
            self._remove(c, self.t('update_list_fail'))

    def _remove(self, cs, reason=""):
        with self.lock:
            if cs in self.clients:
                username = self.clients[cs]['username']
                address = self.clients[cs]['address']
                del self.clients[cs]
                try:
                    cs.close()
                except:
                    pass
                self.root.after(0, self._del_client, username)
                self.broadcast(json.dumps({'type': 'system', 'message': self.t('leave_msg', username), 'time': datetime.now().strftime('%H:%M:%S')}))
                log_msg = f"{self.t('client_disconnected')}: {username} ({address})"
                if reason:
                    log_msg += f" - {reason}"
                self.log(log_msg, 'warning' if reason else 'info')
                self._update_list()

    def _add_client(self, u, ip, t):
        self.tree.insert('', 'end', values=(u, ip, t))
        self._update_stats()

    def _del_client(self, u):
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == u:
                self.tree.delete(item)
                break
        self._update_stats()

    def kick(self, event):
        sel = self.tree.selection()
        if sel:
            u = self.tree.item(sel[0])['values'][0]
            if messagebox.askyesno(self.t('kick_title'), self.t('kick_confirm', u)):
                with self.lock:
                    for cs, info in list(self.clients.items()):
                        if info['username'] == u:
                            try:
                                self.send_to(cs, json.dumps({'type': 'system', 'message': self.t('you_kicked')}))
                            except:
                                pass
                            self._remove(cs, self.t('kick_reason'))
                            break

    def _update_stats(self):
        self.stats_var.set(self.t('online_count', len(self.clients)))

    def log(self, msg, tag=''):
        self.log_disp.configure(state='normal')
        self.log_disp.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] ", 'timestamp')
        self.log_disp.insert(tk.END, f"{msg}\n", tag if tag else '')
        self.log_disp.see(tk.END)
        self.log_disp.configure(state='disabled')

    def on_closing(self):
        if self.is_running:
            if messagebox.askyesno(self.t('close_title'), self.t('close_confirm')):
                self.stop()
                self.root.destroy()
        else:
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ChatServerGUI().run()
