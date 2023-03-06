from nltk.stem import WordNetLemmatizer
import nltk
import pyttsx3
import sys
import re
from urllib.request import urlopen
from time import strftime
import webbrowser
import smtplib
import requests
import subprocess
from bs4 import BeautifulSoup
import wikipedia
import wolframalpha
import ctypes
import subprocess
import datetime
import speech_recognition as sr
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
import os
import math
from datetime import datetime, timedelta
import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
nltk.download('popular', quiet=True)


class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


root = tk.Tk()
root.title("Emma Assistant")
lbl = ImageLabel(root)
lbl.pack()
lbl.load(r'\Users\dell\Desktop\jay\Emma.gif')


def mainWin():
    root.destroy()


root.after(9000, mainWin)
root.mainloop()


engine = pyttsx3.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', 170)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

welcomeMessage = 'Hello, I am EMMA, your Assistant. What can I do for you ?'
print(welcomeMessage)
engine.say(welcomeMessage)
engine.runAndWait()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

app_id = 'wolfram_API'


def newCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Your wish is my command...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print('Sorry I can\'t understand')
        command = newCommand()
    return command


def EMMAResponse(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def assistant(command):
    if 'your name' in command:
        EMMAResponse('My name is EMMA. Nice to meet you!')
    elif 'who are you' in command:
        EMMAResponse('I\'m EMMA, your assistant! What can i do for you ?')
    elif 'a joke' in command:
        EMMAResponse(
            'My neighbor has been mad at his wife for sunbathing nude. I personally am on the fence.')
    elif 'old are you' in command:
        EMMAResponse('I was launched in November 2022 by Jayanth Tunk')
    elif 'what can you do' in command:
        EMMAResponse(
            'I can do a lot of things, to help you throughout your day.')
    elif 'help me' in command:
        EMMAResponse('I\'m here to help, you can ask me what I can do.')
    elif 'you single' in command:
        EMMAResponse('I am in a relationship with Harry Potter3')
    elif 'languages do you speak' in command:
        EMMAResponse(
            'I currently speak English but I am also learning a lot of other languages ')
    elif 'love you' in command:
        EMMAResponse(
            'I love myself too...')
    elif 'are you dating someone' in command:
        EMMAResponse(
            'I am currently dating Harsha BRO ! who is also called as daddy ')

    # Greet EMMA
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            EMMAResponse('Hello, Good morning!')
        elif 12 <= day_time < 16:
            EMMAResponse('Hello, Good afternoon!')
        elif 16 <= day_time < 18:
            EMMAResponse('Hello, Good evening!')
        else:
            EMMAResponse('Hello, Good night!')
    elif 'thank you' in command:
        EMMAResponse('You\'re Welcome!')

    # Make EMMA stop
    elif 'exit' in command:
        EMMAResponse('Bye bye. Have a nice day!')
        sys.exit()

    # Open Twitter
    elif 'open twitter' in command:
        reg_ex = re.search('open twitter (.*)', command)
        url = 'https://www.twitter.com/'
        if reg_ex:
            handle = reg_ex.group(1)
            url = url + handle
        webbrowser.open(url)
        EMMAResponse(
            'Opening Twitter.')

    elif 'open instagram' in command:
        reg_ex = re.search('open instagram (.*)', command)
        url = 'https://www.instagram.com/'
        if reg_ex:
            handle = reg_ex.group(1)
            url = url + handle
        webbrowser.open(url)
        EMMAResponse(
            'Opening Instagram.')

    elif 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        EMMAResponse(
            'Opening Reddit.')

    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain + ".com"
            webbrowser.open(url)
            EMMAResponse(
                'Opening ' + domain)

    # Make a search on Google
    elif 'search' in command:
        reg_ex = re.search('search (.+)', command)
        if reg_ex:
            subject = reg_ex.group(1)
            url = 'https://www.google.com/search?q=' + subject
            webbrowser.open(url)
            EMMAResponse(
                'Searching for ' + subject + ' on Google.')

    # Make a type command
    elif 'type' in command:
        with open(r"C:\Users\dell\Desktop\jay\type.txt", encoding='utf8', errors='ignore') as fin:
            raw = fin.read().lower()

        sent_tokens = nltk.sent_tokenize(raw)
        word_tokens = nltk.word_tokenize(raw)

        lemmer = WordNetLemmatizer()

        def LemTokens(tokens):
            return [lemmer.lemmatize(token) for token in tokens]
        remove_punct_dict = dict((ord(punct), None)
                                 for punct in string.punctuation)

        def LemNormalize(text):
            return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

        GREETING_INPUTS = ("hello", "hi", "greetings",
                           "sup", "what's up", "hey",)
        GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there",
                              "hello", "I am glad! You are talking to me"]

        def greeting(sentence):
            """If user's input is a greeting, return a greeting response"""
            for word in sentence.split():
                if word.lower() in GREETING_INPUTS:
                    return random.choice(GREETING_RESPONSES)

        def response(user_response):
            emma_response = ''
            sent_tokens.append(user_response)
            TfidfVec = TfidfVectorizer(
                tokenizer=LemNormalize, stop_words='english')
            tfidf = TfidfVec.fit_transform(sent_tokens)
            vals = cosine_similarity(tfidf[-1], tfidf)
            idx = vals.argsort()[0][-2]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-2]
            if(req_tfidf == 0):
                emma_response = emma_response+"I am sorry! I don't understand you"
                return emma_response
            else:
                emma_response = emma_response+sent_tokens[idx]
                return emma_response

        flag = True
        print("emma: My name is emma. I will answer your queries about Chatbots. If you want to exit, type Bye!")
        while(flag == True):
            user_response = input()
            user_response = user_response.lower()
            if(user_response != 'bye'):
                if(user_response == 'thanks' or user_response == 'thank you'):
                    flag = False
                    print("emma: You are welcome..")
                else:
                    if(greeting(user_response) != None):
                        print("emma: "+greeting(user_response))
                    else:
                        print("emma: ", end="")
                        print(response(user_response))
                        sent_tokens.remove(user_response)
            else:
                flag = False
                print("emma: Bye! take care..")

    # Play a song on Youtube
    elif 'play' in command:
        reg_ex = re.search('play (.+)', command)
        if reg_ex:
            searchedSong = reg_ex.group(1)
            url = 'https://www.youtube.com/results?q=' + searchedSong
            try:
                source_code = requests.get(url, headers=headers, timeout=15)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, "html.parser")
                songs = soup.findAll('div', {'class': 'yt-lockup-video'})
                song = songs[0].contents[0].contents[0].contents[0]
                hit = song['href']
                webbrowser.open('https://www.youtube.com' + hit)
                EMMAResponse('Playing ' + searchedSong + ' on Youtube.')
            except Exception as e:
                webbrowser.open(url)
                EMMAResponse('Searching for ' +
                             searchedSong + ' on Youtube.')

    # Send Email
    elif 'email' in command:
        EMMAResponse('Who is the recipient?')
        recipient = newCommand()
        if 'someone' in recipient:
            EMMAResponse('What should I say to him?')
            content = newCommand()
            try:
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('sender_email', 'sender_password')
                mail.sendmail('sender_email', 'receiver_email', content)
                mail.close()
                EMMAResponse(
                    'Email has been sent successfuly.')
            except Exception as e:
                print(e)
        else:
            EMMAResponse('I don\'t know anyone named ' + recipient + '.')

    # Launch apps
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".exe"
            subprocess.call([appname1])
            EMMAResponse('Launching ' + appname + '.')

    # Get current time
    elif 'time' in command:
        now = datetime.datetime.now()
        EMMAResponse('Current time is %d:%d.' %
                     (now.hour, now.minute))

    # Get recent news
    elif 'news' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = BeautifulSoup(xml_page, "html.parser")
            news_list = soup_page.findAll("item")
            for news in news_list[:5]:
                EMMAResponse(news.title.text)
        except Exception as e:
            print(e)

    # Lock the device
    elif 'lock' in command:
        try:
            EMMAResponse("Locking the device.")
            ctypes.windll.user32.LockWorkStation()
        except Exception as e:
            print(str(e))

    elif "alarm" in command:
        from kivy.app import App
        from kivy.clock import Clock
        from kivy.core.audio import SoundLoader
        from kivy.properties import BooleanProperty, NumericProperty
        from kivy.properties import ObjectProperty, StringProperty
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.label import Label
        from kivy.uix.pagelayout import PageLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.widget import Widget

        class ClockLayout(FloatLayout):
            """FloatLayout for displaying the clock."""

        class ClockTimeBgLayout(FloatLayout):
            """FloatLayout for the first screen, where there are the clock and the time."""

        class InputLayout(FloatLayout):
            """FloatLayout for placing the text-input box used for setting an alarm."""

        class NoAlarmLabel(Label):
            """Label displayed when there is no alarm set."""

        class SetAlarmLayout(FloatLayout):
            """FloatLayout for displaying the page where the alarms are set."""

        class TimeLayout(FloatLayout):
            "FloatLayout for displaying the time."

        class TimeWid(Widget):
            """The time display widget."""

        class GeneralLayout(PageLayout):
            "PageLayout for the scheduled alarms and for the set alarm pages."
            time = ObjectProperty(datetime.now())

            def __init__(self, **kwargs):
                Clock.schedule_interval(
                    self.update_time, 1
                )
                super().__init__(**kwargs)

            def update_time(self, dt):
                """Update the time every second."""
                self.time = datetime.now()
                return True

        class Alarm(Widget):
            """An alarm widget. It is created upon setting an alarm.
            It has a label displaying the time set and a button to cancel it.
            """
            alarm_time = StringProperty()
            playing = BooleanProperty(False)
            sound = ObjectProperty(
                SoundLoader.load(
                    os.path.join('alarm-sounds', 'sound1.wav'),
                )
            )

            def __init__(self, **kwargs):
                self.check = Clock.schedule_interval(self.time_check, 1)
                self.sound.loop = True
                super().__init__(**kwargs)

            def to_datetime(self, value):
                """Convert H:M:S string time-format to datetime object."""
                time = self.parent.parent.time
                x = datetime.strptime(value, r'%H:%M:%S')
                x = datetime(time.year, time.month, time.day,
                             x.hour, x.minute, x.second)
                return x

            def time_check(self, dt):
                """Check whether the alarm time is equal to the current time."""
                alarm_time_dt = self.to_datetime(self.alarm_time)
                if (alarm_time_dt - timedelta(seconds=1) <=
                    self.parent.parent.time <= alarm_time_dt +
                        timedelta(seconds=1)) and not self.playing:
                    self.playing = True
                    self.sound.play()
                    Clock.schedule_once(
                        self.remove, 60
                    )

            def remove(self, *args):
                """Cancel and remove the alarm from the list of set alarms."""
                if self.playing:
                    self.sound.stop()
                self.check.cancel()
                self.parent.remove_widget(self)

        class AlarmInput(TextInput):
            """The text-input box for setting an alarm."""

            def __init__(self, **kwargs):
                self.h_patt = re.compile(r'^(([0-1][0-9])|(2[0-3]))$')
                self.m_patt = re.compile(r'^([0-5][0-9])$')
                self.s_patt = self.m_patt
                super().__init__(**kwargs)

            def clear_text(self):
                """Clear the text inside the text-input box."""
                Clock.schedule_once(
                    lambda _: setattr(
                        self, 'text', ''
                    )
                )

            def add_colon(self):
                """Add a colon after the hour or minute part has been input."""
                Clock.schedule_once(
                    lambda _: setattr(
                        self, 'text', str(self.text) + ':'
                    )
                )

            def move_cursor_colon(self):
                """Move cursor one slot to the right after a colon has been put."""
                Clock.schedule_once(
                    lambda _: setattr(
                        self, 'cursor', (self.cursor[0]+1, self.cursor[1])
                    )
                )

            def keyboard_on_key_down(self, window, keycode, text, modifiers):

                if len(self.text) == 8:
                    if keycode[1] == 'enter':
                        alarms_lay = self.parent.parent.parent.children[1]
                        try:
                            if len(alarms_lay.children) < 8:
                                alarms_lay.add_widget(
                                    Alarm(alarm_time=self.text)
                                )
                        except IndexError:
                            alarms_lay.add_widget(Alarm(alarm_time=self.text))
                        self.clear_text()
                        Clock.schedule_once(
                            lambda _: setattr(
                                self, 'focus', False
                            )
                        )
                    elif keycode[1] == 'backspace':
                        self.clear_text()
                    Clock.schedule_once(
                        lambda _: setattr(
                            self, 'text', self.text[:-1]
                        )
                    )
                    return True
                for c in keycode[1]:
                    if c.isdigit():
                        return super().keyboard_on_key_down(window, keycode, text, modifiers)
                self.clear_text()
                return True

            def on_text(self, instance, value):
                """Listen to text changes."""
                length = len(self.text)
                if length == 2:
                    if self.h_patt.match(self.text):
                        self.add_colon()
                        self.move_cursor_colon()
                        return True
                    self.clear_text()
                    return True
                elif length == 5:
                    mins = self.text[-2:]
                    if self.m_patt.match(mins):
                        self.add_colon()
                        self.move_cursor_colon()
                        return True
                    self.clear_text()
                    return True
                elif length == 8:
                    secs = self.text[-2:]
                    if self.m_patt.match(secs):
                        return True
                    self.clear_text()
                    return True

        class AlarmsLayout(BoxLayout):
            """BoxLayout for displaying all the set alarms. Each alarm created
            will stack on top of each other."""
            label = ObjectProperty()

            def __init__(self, **kwargs):
                Clock.schedule_interval(self.check_if_alarms, 0.05)
                super().__init__(**kwargs)

            def check_if_alarms(self, dt):
                """Check whether there is at least one alarm set. If there is
                none, add a label saying 'NO ALARMS'."""
                if not self.label and not self.children:
                    self.label = NoAlarmLabel()
                    self.add_widget(self.label)
                elif self.label and len(self.children) > 1:
                    self.remove_widget(self.label)
                    self.label = ''

        class ClockWid(Widget):
            """The clock widget."""
            h_degrees = NumericProperty()
            m_degrees = NumericProperty()
            s_degrees = NumericProperty()

            def __init__(self, **kwargs):
                self.clock = Clock.schedule_interval(self.set_degrees, 1)
                super().__init__(**kwargs)

            def angle(self, pointer: str):
                """Calculate the degrees of the clock pointers (hours, minutes and seconds)."""
                now = self.parent.parent.parent.time
                if pointer == 'hour':
                    segs = (now.hour % 12)*60*60 + now.minute*60 + now.second
                    return math.radians((360/(12*60*60))*segs)
                elif pointer == 'minute':
                    segs = now.minute*60 + now.second
                    return math.radians((360/(60*60))*segs)
                elif pointer == 'second':
                    return math.radians((360/60)*now.second)

            def set_degrees(self, dt):
                """Set the clock's degrees properties."""
                self.h_degrees = self.angle('hour')
                self.m_degrees = self.angle('minute')
                self.s_degrees = self.angle('second')
                return True

        class AlarmClockApp(App):
            """The main application."""

            def build(self):
                return GeneralLayout()

        if __name__ == '__main__':
            AlarmClockApp().run()

    # Ask general questions
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                EMMAResponse(wikipedia.summary(topic, sentences=3))
        except Exception as e:
            EMMAResponse(e)
    elif any(c in command for c in ("what is", "what\'s")):
        reg_ex = re.search(' (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                EMMAResponse(wikipedia.summary(topic, sentences=2))
        except Exception as e:
            EMMAResponse(e)

    # printing commands using various languages
    elif 'addition of matrix' in command:
        print("""
        #include<stdio.h>
        int main()
        {
        int a, b, c, d;
        int m1[10][10], m2[10][10], sum[10][10];
        scanf("%d",&a);
        scanf("%d",&b);
        for ( c = 0; c < a ; c++ )
        {
        for ( d = 0 ; d < b ; d++ )
        {
        scanf("%d",&m1[c][d]);
        }
        }
        for ( c = 0 ; c < a ; c++ )
        {
        for ( d = 0 ; d < b ; d++ )
        {
        scanf("%d",&m2[c][d]);
        }
        }
        for ( c = 0 ; c < a ; c++ )
        {
        for ( d = 0 ; d < b ; d++ )
        {
        sum[c][d] = m1[c][d] + m2[c][d];
        }
        }
        for ( c = 0 ; c < a ; c++ )
        {
        for ( d = 0 ; d < b ; d++ )
        printf("%d\n",sum[c][d]);
        }
        return 0;
        }
        """)

    elif 'addition using function' in command:
        print(""" #include <stdio.h>
int addition(int num1, int num2)
{
int sum;
sum = num1 + num2;
return sum;
}
int main()
{
int number1, number2, result;
scanf("%d %d", &number1, &number2);
result = addition(number1, number2);
printf("%d\n", result);
return 0;
} """)

    elif 'area of circle' in command:
        print(""" #include<stdio.h>
float diameter(int radius)
{
float dia=2*radius;
return dia;
}
float circumference(int radius)
{
float cir=2*3.14*radius;
return cir;
}
float area(int radius)
{
float a=3.14*radius*radius;
return a;
}
int main()
{
int radius;
scanf("%d",&radius);
printf("Diameter Of a Circle = %.2lf\n\n",diameter(radius));
printf(" Circumference Of a Circle = %.2lf\n\n",circumference(radius));
printf(" Area Of a Circle = %.2lf\n\n",area(radius));
return 0;
} """)

    elif 'arithmetic operations' in command:
        print(""" #include <stdio.h>
int main()
{
int num1, num2;
int sum, sub, mult, mod;
float div;
/*
* Input two numbers from user
*/
scanf("%d%d", &num1, &num2);
/*
* Perform all arithmetic operations
*/
sum = num1 + num2;
sub = num1 - num2;
mult = num1 * num2;
div =(float) num1 / num2;
mod = num1 % num2;
/*
* Print result of all arithmetic operations
*/
printf("%d\n", sum);
printf("%d\n", sub);
printf("%d\n", mult);
printf("%.2f\n", div);
printf("%d\n", mod);
return 0;
} """)

    elif 'convert decimal to roman' in command:
        print(""" #include <stdio.h>
int main(void)
{
int num;
scanf("%d", &num);
while(num != 0)
{
if (num >= 1000) // 1000 - m
{
printf("m");
num -= 1000;
}
else if (num >= 900) // 900 - cm
{
printf("cm");
num -= 900;
}
else if (num >= 500) // 500 - d
{
printf("d");
num -= 500;
}
else if (num >= 400) // 400 - cd
{
printf("cd");
num -= 400;
}
else if (num >= 100) // 100 - c
{
printf("c");
num -= 100;
}
else if (num >= 90) // 90 - xc
{
printf("xc");
num -= 90;
}
else if (num >= 50) // 50 - l
{
printf("l");
num -= 50;
}
else if (num >= 40) // 40 - xl
{
printf("xl");
num -= 40;
}
else if (num >= 10) // 10 - x
{
printf("x");
num -= 10;
}
else if (num >= 9) // 9 - ix
{
printf("ix");
num -= 9;
}
else if (num >= 5) // 5 - v
{
printf("v");
num -= 5;
}
else if (num >= 4) // 4 - iv
{
printf("iv");
num -= 4;
}
else if (num >= 1) // 1 - i
{
printf("i");
num -= 1;
}
}
return 0;
} """)

    elif 'fibonacci series' in command:
        print(""" #include <stdio.h>
                void fib(int a, int b, int sum, int N)
                {
                if (N != 0) {
                printf("%d\n", a);
                sum = a + b;
                a = b;
                b = sum;
                N--;
                fib(a, b, sum, N);
                }
                }
                int main()
                {
                int N = 3;
                fib(0, 1, 0, N);
                return 0;
                } """)

    elif 'GCD' in command:
        print(""" #include<stdio.h>
                int main()
                {
                int n1, n2, i, gcd;
                printf("Enter two numbers: ");
                scanf("%d, %d",&n1, &n2);
                for(i=1; i <= n1, i <= n2; ++i)
                {if(n1%i==0 && n2%i==0) gcd = i;
                }
                printf("G.C.D of %d and %d is %d", n1, n2, gcd);
                return 0;
                } """)
    elif 'perimeter of rectangle' in command:
        print(""" #include <stdio.h>
int main()
{
float l, w, p;
scanf("%f", &l);
scanf("%f", &w);
/* Calculate perimeter of rectangle */
p = 2 * (l + w);
/* Print output */
printf("%f ", p);
return 0;
} """)

    elif 'prime number' in command:
        print(""" #include<stdio.h>
int check_prime(int);
int main()
{
int n, result;
scanf("%d",&n);
result = check_prime(n);
if ( result == 1 )
printf("Prime\n");
else
printf("Not Prime\n");
return 0;
}
int check_prime(int a)
{
int c;
for ( c = 2 ; c <= a - 1 ; c++ )
{
if ( a%c == 0 )
return 0;
}
return 1;
} """)

    elif 'sum of matrices' in command:
        print(""" #include<stdio.h>
int main()
{
int a, b, c, d;
int m1[10][10], m2[10][10], sum[10][10];
scanf("%d",&a);
scanf("%d",&b);
for ( c = 0; c < a ; c++ )
{
for ( d = 0 ; d < b ; d++ )
{
scanf("%d",&m1[c][d]);
}
}
for ( c = 0 ; c < a ; c++ )
{
for ( d = 0 ; d < b ; d++ )
{
scanf("%d",&m2[c][d]);
}
}
for ( c = 0 ; c < a ; c++ )
{
for ( d = 0 ; d < b ; d++ )
{
sum[c][d] = m1[c][d] + m2[c][d];
}
}
for ( c = 0 ; c < a ; c++ )
{
for ( d = 0 ; d < b ; d++ )
printf("%d\n",sum[c][d]);
}
return 0;
} """)

    elif 'swapping' in command:
        print(""" include<stdio.h>
void swap(int, int);
int main()
{
int a, b;
scanf("%d%d", &a, &b);
swap(a, b);
return 0;
}
void swap(int x, int y)
{
int temp;
temp = x;
x = y;
y = temp;
printf("%d\n%d\n", x, y);
} """)

    elif 'ascending and descending order' in command:
        print(""" using namespace std;
#include <iostream>
class sort{
int a[15],n;
public:
void init();
void ascend();
void descend();
void display();
};
void sort::init(){
cin>>n;
for(int i=0;i<n;i++)
cin>>a[i];
}
void sort::ascend(){
for(int i=0;i<n-1;i++){
int min=i;
for(int j=i+1;j<n;j++){
if(a[min]>a[j])
min=j;
}
if(min!=i){
int temp;
temp=a[min];
a[min]=a[i];
a[i]=temp;
}
}
}
void sort::descend(){
for(int i=0;i<n-1;i++){
int min=i;
for(int j=i+1;j<n;j++){
if(a[min]<a[j])
min=j;
}
if(min!=i){
int temp;
temp=a[min];
a[min]=a[i];
a[i]=temp;
}
}
}
void sort::display(){
for(int i=0;i<n;i++)
cout<<a[i]<<endl;
}
int main(){
sort s;
s.init();
s.ascend();
s.display();
s.descend();
s.display();
return 0;
} """)
    elif 'factorial' in command:
        print(""" #include<iostream>
using namespace std;
class factorial
{
public:
int n,n1,f=1;
void inti()
{
cin>>n;
}
void calc()
{
while(n!=0)
{
f=f*n;
n=n-1;
}
}
void dispay()
{
cout<<f;
}
};
int main()
{
factorial obj;
obj.inti();
obj.calc();
obj.dispay();
} """)
    elif 'linear search' in command:
        print("""#include <iostream>
using namespace std;
class LS
{
public:
void LinearSearch(int arr[], int value, int i, int n)
{ int found = 0;
for (i = 0; i < n ; i++)
{
if (value == arr[i] )
{
found = 1;
break;
}
}
if (found == 1)
{
cout<<i;
}
else
{
cout<<"Element is not present in the array.";
}
}
};
int main()
{ int num;
int i,keynum;
cin>>num;
int array[num];
for (i = 0; i < num; i++)
{
cin>> array[i];
}
cin>>keynum;
LS l1;
l1.LinearSearch(array,keynum,i,num);
return 0;
}""")
    elif 'palindrome' in command:
        print("""using namespace std;
#include<iostream>
class sample{
int n=0,pow=0,res=0;
public:
void init();
void compute();
void display();
};
void sample::init(){
cin>>n>>pow;
}
void sample::compute(){
int pro,pseq,p;
pro=1;
pseq=n;
p=pow;
while(p>0){
if(p%2)
pro *= pseq;
p/=2;
pseq*=pseq;
}
res=pro;
}
void sample::display(){
cout<<res;
}
int main(){
sample s;
s.init();
s.compute();
s.display();
return 1;
}""")
    elif 'Python Program to find whether the given number is palindrome or not' in command:
        print("""n=int(input(""))
temp=n
rev=0
while(n>0):
    dig=n%10
    rev=rev*10+dig
    n=n//10
print(rev)
""")

    elif 'Python program to reverse a number using recursive function' in command:
        print("""n=int(input())
temp=n
rev=0
while(n>0):
    dig=n%10
    rev=rev*10+dig
    n=n//10
if(temp==rev):
    print(rev)
else:
    print(rev)
""")
    elif 'Python Program to print the Fibonacci Series' in command:
        print("""n = int(input(""))
a = 0
b = 1
sum = 0
count = 1
print(end = "")
while(count <= n):
  print(sum, end = " ")
  count += 1
  a = b
  b = sum
  sum = a + b
""")
    elif 'Python program to sort the elements of list in ascending order' in command:
        print("""arr = [int(x) for x in input().split()]    
temp = 0;    
  
#Sort the array in ascending order    
for i in range(0, len(arr)):    
    for j in range(i+1, len(arr)):    
        if(arr[i] > arr[j]):    
            temp = arr[i];    
            arr[i] = arr[j];    
            arr[j] = temp;    

for i in range(0, len(arr)):    
    print(arr[i], end=" ");
""")
    elif 'Python program to check whether an alphabet is vowel or consonant' in command:
        print("""str = input("")
 
if str in ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U', 'A', 'E'):
	print("Consonant")
	print("Vowel")
else:
	print("Consonant")
	print("Vowel")
""")
    elif 'Python Program to Check Prime Number' in command:
        print(""" A = 11
if A > 1:
    for i in range(2, A//2):
        if (A % i) == 0:
            print(A, "is not a prime number")
    else:
        print(A, "is a prime number")
else:
    print(A, "is not a prime number")
""")
    elif 'Python Program to Create Pyramid Patterns' in command:
        print("""rows = 5

k = 0

for i in range(1, rows+1):
    for space in range(1, (rows-i)+1):
        print(end="  ")
   
    while k!=(2*i-1):
        print("* ", end="")
        k += 1
   
    k = 0
    print()
 """)
    elif 'MergeSort' in command:
        print("""def mergeSort(arr):
	if len(arr) > 1:
		mid = len(arr)//2
		L = arr[:mid]
		R = arr[mid:]
		mergeSort(L)
		mergeSort(R)
		i = j = k = 0
		while i < len(L) and j < len(R):
			if L[i] < R[j]:
				arr[k] = L[i]
				i += 1
			else:
				arr[k] = R[j]
				j += 1
			k += 1
		while i < len(L):
			arr[k] = L[i]
			i += 1
			k += 1
		while j < len(R):
			arr[k] = R[j]
			j += 1
			k += 1
def printList(arr):
	for i in range(len(arr)):
		print(arr[i], end=" ")
	print()
if __name__ == '__main__':
	arr = [12, 11, 13, 5, 6, 7]
	print("Given array is", end="\n")
	printList(arr)
	mergeSort(arr)
	print("Sorted array is: ", end="\n")
	printList(arr)
 """)
    elif 'timSort' in command:
        print("""MINIMUM= 32
  
def find_minrun(n): 
  
    r = 0
    while n >= MINIMUM: 
        r |= n & 1
        n >>= 1
    return n + r 
  
def insertion_sort(array, left, right): 
    for i in range(left+1,right+1):
        element = array[i]
        j = i-1
        while element<array[j] and j>=left :
            array[j+1] = array[j]
            j -= 1
        array[j+1] = element
    return array
              
def merge(array, l, m, r): 
  
    array_length1= m - l + 1
    array_length2 = r - m 
    left = []
    right = []
    for i in range(0, array_length1): 
        left.append(array[l + i]) 
    for i in range(0, array_length2): 
        right.append(array[m + 1 + i]) 
  
    i=0
    j=0
    k=l
   
    while j < array_length2 and  i < array_length1: 
        if left[i] <= right[j]: 
            array[k] = left[i] 
            i += 1
  
        else: 
            array[k] = right[j] 
            j += 1
  
        k += 1
  
    while i < array_length1: 
        array[k] = left[i] 
        k += 1
        i += 1
  
    while j < array_length2: 
        array[k] = right[j] 
        k += 1
        j += 1
  
def tim_sort(array): 
    n = len(array) 
    minrun = find_minrun(n) 
  
    for start in range(0, n, minrun): 
        end = min(start + minrun - 1, n - 1) 
        insertion_sort(array, start, end) 
   
    size = minrun 
    while size < n: 
  
        for left in range(0, n, 2 * size): 
  
            mid = min(n - 1, left + size - 1) 
            right = min((left + 2 * size - 1), (n - 1)) 
            merge(array, left, mid, right) 
  
        size = 2 * size 
  
  
  
  
array = [-2, 7, 15, -14, 0, 15, 0, 7, -7, -4, -13, 5, 8, -14, 12] 
  

print("Given Array is") 
print(array) 
  
tim_sort(array) 
  
print("After Sorting Array is") 
print(array)
 """)
    elif 'Linear Search' in command:
        print("""def linear_Search(list1, n, key):  
  
    # Searching list1 sequentially  
    for i in range(0, n):  
        if (list1[i] == key):  
            return i  
    return -1  
  
  
list1 = [1 ,3, 5, 4, 7, 9]  
key = 7  
  
n = len(list1)  
res = linear_Search(list1, n, key)  
if(res == -1):  
    print("Element not found")  
else:  
    print("Element found at index: ", res)   """)
    elif 'heap sort' in command:
        print("""def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2

    if l < n and arr[i] < arr[l]:
        largest = l

    if r < n and arr[largest] < arr[r]:
        largest = r

    if largest != i:
        arr[i],arr[largest] = arr[largest],arr[i]  # swap

        heapify(arr, n, largest)

def heapSort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
  
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]   # swap
        heapify(arr, i, 0)
  
arr = [ 12, 11, 13, 5, 6, 7]
heapSort(arr)
n = len(arr)
print ("Sorted array is")
for i in range(n):
    print ("%d" %arr[i]),
 """)
    elif 'ShellSort' in command:
        print("""def shellSort(array, a):

    gap = a // 2
    while gap > 0:
        for i in range(gap, a):
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap

            array[j] = temp
        gap //= 2
array = [9, 1, 8, 7, 3, 6, 4, 5]

size = len(array)
shellSort(array, size)
print('Sorted Array in Ascending Order:')
print(array)
 """)
    elif 'Bubble Sort' in command:
        print("""def bubbleSort(array):
  for a in range(len(array)):
    for b in range(0, len(array) - a - 1):
      if array[b] > array[b + 1]:
        temp = array[b]
        array[b] = array[b+1]
        array[b+1] = temp
array = [-2, 45, 0, 11, -9]
bubbleSort(array)
print('Sorted Array in Ascending Order: ')
print(array)
 """)
    elif 'Merge Sort' in command:
        print(""" def Merge_Sort(array):
    if len(array) > 1:
        mid = len(array)//2
        Left = array[:mid]
        Right = array[mid:]
        Merge_Sort(Left)
        Merge_Sort(Right)
        i = j = k = 0
        while i < len(Left) and j < len(Right):
            if Left[i] < Right[j]:
                array[k] = Left[i]
                i += 1
            else:
                array[k] = Right[j]
                j += 1
            k += 1
        while i < len(Left):
            array[k] = Left[i]
            i += 1
            k += 1
        while j < len(Right):
            array[k] = Right[j]
            j += 1
            k += 1
def printarray(array):
    for i in range(len(array)):
        print(array[i], end=" ")
    print()
if __name__ == '__main__':
    array = [12, 11, 13, 5, 6, 7]
    Merge_Sort(array)
    print("Sorted array is: ")
    printarray(array)
 """)

    elif 'Radix Sort' in command:
        print("""def countingSort(arr, exp1):  

    

    n = len(arr)  

    

    # The output array elements that will have sorted arr  

    output = [0] * (n)  

    

    # initialize count array as 0  

    count = [0] * (10)  

    

    # Store count of occurrences in count[]  

    for i in range(0, n):  

        index = (arr[i]/exp1)  

        count[int((index)%10)] += 1

    

    # Change count[i] so that count[i] now contains actual  

    #  position of this digit in output array  

    for i in range(1,10):  

        count[i] += count[i-1]  

    

    # Build the output array  

    i = n-1

    while i>=0:  

        index = (arr[i]/exp1)  

        output[ count[ int((index)%10) ] - 1] = arr[i]  

        count[int((index)%10)] -= 1

        i -= 1

    

    # Copying the output array to arr[],  

    # so that arr now contains sorted numbers  

    i = 0

    for i in range(0,len(arr)):  

        arr[i] = output[i]  

  
# Method to do Radix Sort 

def radixSort(arr): 

  

    # Find the maximum number to know number of digits 

    max1 = max(arr) 

 
    exp = 1

    while max1/exp > 0: 

        countingSort(arr,exp) 

        exp *= 10
arr = [ 170, 45, 75, 90, 802, 24, 2, 66] 
radixSort(arr) 

 
for i in range(len(arr)): 

    print(arr[i]),
 """)
    elif 'print a statement' in command:
        print(""" print('Hello World ! My name is Emma')  """)
    # All other cases
    else:
        try:
            # wolframalpha
            client = wolframalpha.Client(app_id)
            res = client.query(command)
            answer = next(res.results).text
            EMMAResponse(answer)
        except:
            try:
                # wikipedia
                EMMAResponse(wikipedia.summary(command, sentences=2))
            except Exception as e:
                EMMAResponse(e)

    ######

    ######
while True:
    assistant(newCommand())
