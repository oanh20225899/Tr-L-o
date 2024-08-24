import os
import playsound
import speech_recognition as sr
import time
import sys
import subprocess
import ctypes 
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from youtubesearchpython import VideosSearch
from deep_translator import GoogleTranslator
import pytesseract
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import face_recognition
import cv2
import matplotlib.pyplot as plt
import webbrowser
import requests
from bs4 import BeautifulSoup



wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()
# chuyen van ban thanh giong noi va phat am thanh cho nguoi dung
def speak(text):
    print("Bot: {}".format(text)) #in van ban bot muon noi
    tts = gTTS(text=text, lang=language, slow=False) #su dung gTTS de chuyen doi van ban thanh giong noi
    tts.save("sound.mp3")#luu duoi dang mp3
    playsound.playsound("sound.mp3", False)#su dung thu vien de phat am thanh ko dong bo
    os.remove("sound.mp3")#xoa
# ghi âm giọng nói từ microphone, chuyển giọng nói thành văn bản và trả về văn bản đó.
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0
  #ham stop          
def stop():
    speak("Hẹn gặp lại bạn sau!")
    time.sleep(5)
# co gang nghe hieu 3 lan neu sau 3 lan van ko hieu thi stop
def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak("Bot không nghe rõ. Bạn nói lại được không!")
            time.sleep(5)
    stop()
    return 0
# chao hoi
def hello(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(name))
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn {}.".format(name))
    else:
        speak("Chào buổi tối bạn {}. ".format(name))
    time.sleep(5)
# Hàm lấy thời gian 
def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d" %
              (now.day, now.month, now.year))
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")
# Hàm mở ứng dụng 
def open_application(text):
    if "google" in text:
        speak("Mở Google Chrome")
        time.sleep(3)
        subprocess.run(["open", "-a", "Google Chrome"])
    elif "safari" in text:
        speak("Mở Safari")
        subprocess.run(["open", "-a", "Safari"])
    elif "excel" in text:
        speak("Mở Microsoft Excel")
        subprocess.run(["open", "-a", "Microsoft Excel"])
    else:
        speak("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")

# mở webside
def open_website(text):
    reg_ex = re.search('mở (.+)', text)#timkiemphanten mien
    if reg_ex:
        domain = reg_ex.group(1)
        url = 'https://www.' + domain # Tạo URL từ tên miền
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đã được mở.")
        time.sleep(5)
        return True
    else:
        return False

# Tìm kiếm từ khoa
def open_google_and_search(text):
    
    search_for = text.split("kiếm", 1)[1]
    speak('Okay!')
    
    # Khởi tạo WebDriver cho Firefox
    browser = webdriver.Firefox()

    # Mở trang Google
    browser.get('http://www.google.com')
    assert 'Google' in browser.title

    # Tìm hộp tìm kiếm và nhập từ khóa
    elem = browser.find_element(By.NAME, 'q')  # Tìm hộp tìm kiếm của Google
    elem.send_keys(search_for + Keys.RETURN)  # Nhập từ khóa và nhấn Enter

    


# Dự báo thời tiết
def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    time.sleep(3)
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute, 
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        speak(content)
        time.sleep(30)
    else:
        speak("Không tìm thấy địa chỉ của bạn")
#phát nhạc trên youtube
def play_song():
    speak('Xin mời bạn chọn tên bài hát')
    time.sleep(3)
    mysong = get_text()
    videosSearch = VideosSearch(mysong, limit=1)
    result = videosSearch.result()
    if result and 'result' in result:
        for video in result['result']:
            link = video.get('link')
            if link:
                webbrowser.open(link)

    speak("Bài hát bạn yêu cầu đã được mở.")
    time.sleep(5)
# Thay đổi nền trên máy tính
def change_wallpaper():
    api_key = 'RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
    url = f'https://api.unsplash.com/photos/random?client_id={api_key}'

    response = requests.get(url)
    parsed_json = response.json()
    photo_url = parsed_json['urls']['full']

    # Generate a unique file name for each image using timestamp
    timestamp = int(time.time())
    image_path = os.path.join(os.path.expanduser('~'), 'Downloads', f'wallpaper_{timestamp}.png')

    # Download the image
    img_data = requests.get(photo_url).content
    with open(image_path, 'wb') as handler:
        handler.write(img_data)

    # Set the wallpaper using AppleScript
    script = f"""
    tell application "System Events"
        set desktopCount to count of desktops
        repeat with desktopNumber from 1 to desktopCount
            tell desktop desktopNumber
                set picture to "{image_path}"
            end tell
        end repeat
    end tell
    """
    subprocess.run(["osascript", "-e", script])

# Đọc báo ngày hom nay
def read_news():
    speak("Bạn muốn đọc báo về gì?")
    time.sleep(3)
    queue = get_text()

    params = {
        'apiKey': '30d02d187f7140faacf9ccd27a1441ad',
        "q": queue,
    }

    try:
        api_result = requests.get('http://newsapi.org/v2/top-headlines', params=params)
        api_result.raise_for_status()  # Kiểm tra lỗi HTTP
    except requests.exceptions.RequestException as e:
        speak("Đã xảy ra lỗi khi kết nối đến API tin tức.")
        print(e)
        return

    api_response = api_result.json()

    speak("Dưới đây là các tin tức hàng đầu:")
    for number, result in enumerate(api_response['articles'], start=1):
        print(f"""Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}
        """)
        if number <= 3:
            webbrowser.open(result['url'])
# tìm kiếm từ điển wikipidia
def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        time.sleep(4)
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(40)
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không")
            time.sleep(4)
            ans = get_text()
            if "có" not in ans:
                break    
            speak(content)
            time.sleep(10)

        speak('Cảm ơn bạn đã lắng nghe!!!')
        time.sleep(4)

    except:
        speak("Bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")
        time.sleep(4)
#Dịch từ anh sang việt
def translate_text(text, src_lang='en', dest_lang='vi'):
    try:
        translated = GoogleTranslator(source=src_lang, target=dest_lang).translate(text)
    except Exception as e:
        return f"Error: {e}"
    print(f"Translated text: {translated}")
 # Chuyển ảnh sang văn bản 
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  

def select_image():
    # Tạo một cửa sổ ẩn để mở hộp thoại chọn tệp
    Tk().withdraw()
    file_path = askopenfilename(filetypes=[
        ("Image files", "*.png"),
        ("Image files", "*.jpg"),
        ("Image files", "*.jpeg"),
        ("Image files", "*.tiff"),
        ("Image files", "*.bmp")
    ])
    return file_path

def extract_text_from_image(image_path):
    # Đọc ảnh và sử dụng Tesseract OCR để trích xuất văn bản
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def save_text_to_file(text, file_path):
    # Lưu văn bản vào tệp
    with open(file_path, 'w') as file:
        file.write(text)

def main_select_image():
    # Chọn ảnh từ Finder
    image_path = select_image()
    
    if not image_path:
        print("No file selected. Exiting.")
        return

    # Trích xuất văn bản từ ảnh
    text = extract_text_from_image(image_path)
    
    # Lưu văn bản vào tệp
    text_file_path = os.path.splitext(image_path)[0] + '_extracted_text.txt'
    save_text_to_file(text, text_file_path)
    
    print(f"Text extracted and saved to {text_file_path}")
    print(f"Translated text: {text}")
#nhan dien khuon mat
def detect_faces_in_image(image_path,output_path) :
    # Đọc ảnh từ tệp
    image = face_recognition.load_image_file(image_path)
    
    # Tìm các khuôn mặt trong ảnh
    face_locations = face_recognition.face_locations(image)
    
    print(f"Found {len(face_locations)} face(s) in this image.")

    # Hiển thị ảnh với các khuôn mặt được đánh dấu
    image_with_boxes = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(image_with_boxes, (left, top), (right, bottom), (0, 255, 0), 2)
    
    plt.imshow(cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    cv2.imwrite(output_path, image_with_boxes)
    print(f"Image saved to {output_path}")  

#call 
def call_bot():
    speak("Xin chào, bạn tên là gì?")
    time.sleep(3)
    name = get_text()
    if name:
        speak("Chào bạn {}".format(name))
        time.sleep(2)
        speak("Bot có thể giúp bạn làm gì?")
        time.sleep(5)
        while True:
            text = get_text()
            if not text:
                break
            elif "thôi" in text or "tạm biệt" in text or "dừng" in text:
                stop()
                break
            elif "nói chuyện" in text:
                hello(name)#ok
            elif "giờ" in text:
                get_time(text)#ok
                time.sleep(5)
            elif "mở " in text:
                if "." in text:
                    open_website(text)#ok
                elif "tìm kiếm" in text:
                    open_google_and_search(text)#ok
                else:
                    open_application(text)#ok
            
            elif "thời tiết" in text:
                current_weather()#ok
            elif "nhạc" in text or "bài hát" in text:
                play_song()#ok
            elif "hình nền" in text:
                change_wallpaper()#ok
            elif "đọc" in text or "báo" in text:
                read_news()#ok
            elif "định nghĩa" in text or "giải thích" in text:
                tell_me_about()#ok
            elif "dịch" in text:
                text_to_translate = input("Enter text to translate: ")
                translate_text(text_to_translate)#ok
            elif "chuyển" in text or "ảnh" in text:
                main_select_image()#ok
            elif "đếm" in text or "khuôn mặt" in text:
                image_path =  select_image()  
                output_path = '/Users/kieuoanh/Downloads/detected_faces_image.png'
                detect_faces_in_image(image_path,output_path)    
            else:
                speak("Bạn cần  giúp gì thêm ạ?")
                time.sleep(2)
        
call_bot()  