import webbrowser
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sound import Sound
import subprocess
import pyautogui
import time


# Словарь
def clean_str(r):
	r = r.lower()
	r = [c for c in r if c in alphabet]
	return ''.join(r)


alphabet = ' 1234567890-йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm'
with open('data-set.txt', encoding='utf-8') as f:
	content = f.read()
blocks = content.split('\n')
dataset = []
for block in blocks:
	replicas = block.split('\\')[:2]
	if len(replicas) == 2:
		pair = [clean_str(replicas[0]), clean_str(replicas[1])]
		if pair[0] and pair[1]:
			dataset.append(pair)
X_text = []
y = []
for question, answer in dataset[:10000]:
	X_text.append(question)
	y += [answer]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X_text)
clf = LogisticRegression()
clf.fit(X, y)


def handle_command(command):  # Отправка запроса на обработку и ответ бота
	command = command.lower()
	reply = get_generative_replica(command)
	say(reply)


def get_generative_replica(text): # Генерирование запроса и ответа
	text_vector = vectorizer.transform([text]).toarray()[0]
	answer = clf.predict([text_vector])[0]
	functions(answer, key_word_clean(text))
	return answer




# Очистка от ключевых слов
def key_word_clean(command):
	arr_comm = [str(word) for word in command.split()]
	key_words = ["открой", "браузер", "яндексе", "яндекс", "аристарх", "на", "youtube", "поищи", "найди",
		     "пожалуйста", 'в']
	for i in arr_comm:
		if any(word in arr_comm for word in key_words):
			for word in key_words:
				try:
					arr_comm.remove(word)
				except:
					pass
	
	no_key_word_comm = ""
	for word in arr_comm:
		no_key_word_comm += word
	return no_key_word_comm


# Поиск цифр в строке
def get_digits(command):
	c = ""
	ch = "1234567890"
	for i in command:
		if i in ch:
			c += i
	return c


# Функционал
def functions(answer, command):  # Определитель функции
	if "уже открываю youtube" in answer:
		search_youtube(command)
	elif "открываю яндекс" in answer:
		search_yandex(command)
	elif "уже ищу" in answer:
		search_yandex(command)
	elif "изменяю громкость" in answer:
		voulme_reg(command)
	elif "выключаю" in answer:
		voulme_reg(command)
	elif "открываю дискорд" in answer:
		open_discord()
	elif "открываю ворд" in answer:
		open_word()
	elif "переключаю" in answer:
		alt_tab(command)
	elif "закрываю" in answer:
		close_window(command)
	elif "пока" in answer:
		stop()
	elif "Ошибка распознания" in answer:
		say(command)
	elif "сворачиваю" in answer:
		minimizing_windows()
	elif "всегда к вашим услугам" in answer:
		start_sleep(True)


def search_yandex(command):  # Открывание яндекса и поиск в нем
	url = "https://yandex.ru/yandsearch?lr=10&amp%3Btext=" + command
	webbrowser.get().open(url)


def search_youtube(command):  # Отрывание ютуба и поиск в нем
	url = "https://www.youtube.com/results?search_query=" + command
	webbrowser.get().open(url)


def voulme_reg(command):  # Регулировка звука
	if "выключи" in command:
		Sound.mute()
	elif "включи" in command:
		Sound.mute()
		Sound.mute()
	else:
		vol = get_digits(command)
		if len(vol) > 0:
			vol = int(vol)
			Sound.volume_set(vol)


def open_discord():  # Открытие дискорда
	subprocess.Popen("C:\\Users\\MaskedMir\\AppData\\Local\Discord\\Update.exe --processStart Discord.exe")


def open_word():  # Открытие ворда
	subprocess.Popen("C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.EXE")


def alt_tab(command):  # Переход между окнами
	tabs = get_digits(command)
	if len(tabs) > 0:
		tabs = int(tabs)
	else:
		tabs = 1
	pyautogui.keyDown('alt')
	time.sleep(.2)
	for i in range(tabs):
		pyautogui.press('tab')
		time.sleep(.2)
	pyautogui.keyUp('alt')


def close_window(command):  # Закрытие окон
	tabs = get_digits(command)
	if len(tabs) > 0:
		tabs = int(tabs)
	else:
		pyautogui.keyDown('alt')
		time.sleep(.2)
		pyautogui.press("F4")
		pyautogui.keyUp('alt')
	
	for i in range(tabs):
		pyautogui.keyUp('alt')
		time.sleep(.2)
		pyautogui.press('tab')
		time.sleep(.2)
	
	pyautogui.press("F4")
	pyautogui.keyDown('alt')
	time.sleep(.2)


def minimizing_windows():  # Сворачивание всех окон
	pyautogui.keyDown('win')
	pyautogui.press("d")
	time.sleep(.2)
	pyautogui.keyUp('win')


def start_sleep(Flag):  # Перевод бота в режим сна и вывод бота из режима сна
	say("всегда к вашим услугам")
	while Flag:
		if "бот" in listen():
			start()
			Flag = False


# Голосовой ассистент
def listen():  # Распознание речи
	voice_recognizer = sr.Recognizer()
	voice_recognizer.dynamic_energy_threshold = False
	voice_recognizer.energy_threshold = 1000
	voice_recognizer.pause_threshold = 0.5
	with sr.Microphone() as source:
		print("Слушаю вас")
		audio = voice_recognizer.listen(source, timeout=None, phrase_time_limit=5)
	try:
		voice_text = voice_recognizer.recognize_google(audio, language="ru")
		print(f"Вы сказали: {voice_text}")
		return voice_text
	except sr.UnknownValueError:
		return "Ошибка распознания"
	except sr.RequestError:
		return "Ошибка соединения"


def say(text):  # Озвучка реплик бота
	voice = gTTS(text, lang="ru")
	unique_file = "audio_" + str(random.randint(0, 10000)) + ".mp3"
	voice.save(unique_file)
	playsound.playsound(unique_file)
	os.remove(unique_file)
	print(f"Бот:  {text}")




def start():  # Запуск бота
	print(f"Запуск бота...")
	say("слушаю вас")
	while True:
		command = listen()
		handle_command(command)


def stop():  # Остановка бота
	say("Пока")
	exit(0)



# if __name__ == '__main__':
# 	start()