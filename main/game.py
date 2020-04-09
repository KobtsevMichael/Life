# coding : utf-8
# PEP-8

from tkinter import Tk, Canvas, Frame, TclError
from tkinter import Button, Label, Entry
from tkinter import ttk, messagebox

from PIL import ImageTk, Image
from threading import Thread
from random import randint

import os
import time
import cv2
import pygame

import include.cards as Cards
import include.gallery as Gallery
import include.theme as Theme
import include.coords as Coords
import include.format as Format

from include.ways import Ways


class Life:

    def __init__(self, master, W, H):

        self.master = master
        self.W = W
        self.H = H

        self.canv = Canvas(master, width=W, height=H, bg='#232426',
                           highlightthickness=0, borderwidth=0)
        self.canv.pack(side="left")

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)

        master.protocol("WM_DELETE_WINDOW", self.Destroy)

        self.Path = 'packages/'

        self.K = 1
        self.CountGifs = 0

        self.PlayVideo = False

        self.VideoW = Coords.VideoSize
        self.VideoH = round(0.57*Coords.VideoSize)

        Thread(target=self.Resizing).start()
        self.SetValues()

    def Resizing(self):

        AllGifs = self.GIF_names(self.Path + 'GIF', [])
        self.CountGifs = len(AllGifs)

        if not self.Exists(self.Path + 'video/Resized/End.avi'):
            Thread(target=self.ResizeVideo).start()

        for gif in AllGifs:
            way_to_file = self.Path + 'temp/' + gif[1]
            self.K += 1
            if not self.Exists(way_to_file):
                if gif[2]:
                    ResizeGif(gif[0], save_as=way_to_file, resize_to=gif[2])
                else:
                    ResizeGif(gif[0], save_as=way_to_file)

    def ResizeVideo(self):

        cap = cv2.VideoCapture(self.Path + 'video/End Video.mp4')
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        out = cv2.VideoWriter(self.Path + 'video/Resized/End.avi',
                              fourcc, 30.0, (self.VideoW, self.VideoH))

        while cap.isOpened():
            ret, frame = cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
                break
            frame_temp = cv2.resize(frame, (self.VideoW, self.VideoH),
                                    interpolation=cv2.INTER_CUBIC)
            out.write(frame_temp)

        out.release()
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def Exists(path):

        try:
            os.stat(path)
        except OSError:
            return False

        return True

    def GIF_names(self, di, files):

        for name in os.listdir(di):
            path = os.path.join(di, name)
            if os.path.isfile(path):

                if name[:-5] == 'YouDied':
                    resize_to = (Coords.StartTitleW, Coords.StartTitleH)
                    files.append([path, name, resize_to])

                elif name == 'Gallery.gif':
                    resize_to = Coords.GalleryGif_size
                    files.append([path, name, resize_to])

                else:
                    files.append([path, name, False])

            else:
                self.GIF_names(path, files)

        return files

    def LoadGif(self, way, x=None, y=None):

        im = Image.open(way)

        pic_w, pic_h = im.size

        if not x:
            x = self.W/2
        if not y:
            y = Coords.Card_Y1 + pic_h/2 + Coords.ImgBorder

        x1 = x - (pic_w/2 + Coords.ImgBorder)
        y1 = y - (pic_h/2 + Coords.ImgBorder)
        x2 = x + (pic_w/2 + Coords.ImgBorder)
        y2 = y + (pic_h/2 + Coords.ImgBorder)

        ImgRect = self.canv.create_rectangle(x1, y1, x2, y2,
                                             fill=self.BG,
                                             outline=self.BG)

        self.ImgRects.append(ImgRect)

        lbl = Label(self.canv, image=ImageTk.PhotoImage(im),
                    borderwidth=0)
        self.canv.create_window((x, y), anchor="center", window=lbl)

        self.PhotoGif.append(im)
        self.LabelGif.append(lbl)

        self.GIF_play = True

        self.PlayGif(-1, self.PhotoGif.index(im))

    def PlayGif(self, frame, i):

        while self.GIF_play:

            frame += 1

            try:
                self.PhotoGif[i].seek(frame)
                img = ImageTk.PhotoImage(self.PhotoGif[i])
                self.LabelGif[i].config(image=img)

            except EOFError:
                frame = 0

            self.canv.update()

            self.master.after(68)

    def Destroy(self):

        StopVideo = False

        if self.PlayVideo:
            self.Snapshot()
            StopVideo = True

        if messagebox.askyesno('', 'Are you sure you want to quit ?'):

            self.GIF_play = False

            for lbl in self.LabelGif:
                lbl.destroy()

            pygame.mixer.music.stop()

            self.master.after(400, self.master.destroy)

        else:
            if StopVideo:
                self.Snapshot()

    def Clear(self):

        self.GIF_play = False

        for lbl in self.LabelGif:
            lbl.destroy()

        for rectangle in self.ImgRects:
            self.canv.delete(rectangle)

        for element in self.Elements:
            element.destroy()

        for but in self.CardButtons:
            but.destroy()

        self.CardButtons = []

    @staticmethod
    def Play(music):

        pygame.mixer.music.load(music + '.ogg')
        pygame.mixer.music.play(-1)

    def ChangeTheme(self, day):

        self.BG = Theme.colors[day][0]
        self.FG_1 = Theme.colors[day][1]
        self.FG_2 = Theme.colors[day][2]
        self.HG = Theme.colors[day][3]

    def VolumeUp(self):

        vol = pygame.mixer.music.get_volume()

        if vol > 1.0:
            pass
        else:
            pygame.mixer.music.set_volume(round(vol + 0.1, 1))
            self.VolumeTitle.config(text='VOLUME: ' +
                                    str(round(vol + 0.1, 1)))

    def VolumeDown(self):

        vol = pygame.mixer.music.get_volume()

        if vol < 0.05:
            pass
        else:
            pygame.mixer.music.set_volume(abs(round(vol - 0.1, 1)))
            self.VolumeTitle.config(text='VOLUME: ' +
                                    str(abs(round(vol - 0.1, 1))))

    def ChangeBgColor(self):

        for but in self.FrameButtons:
            but.config(bg=self.BG, activebackground=self.BG)
        self.VolumeTitle.config(bg=self.BG)
        self.TimerTitle.config(bg=self.BG)
        self.Bar.config(bg=self.BG)
        self.Card_Text.config(bg=self.BG, fg=self.FG_1)
        self.Card_Title.config(bg=self.BG, fg=self.FG_2)

    def SetValues(self):

        self.Elements = []
        self.ImgRects = []
        self.PhotoGif = []
        self.LabelGif = []

        self.CardButtons = []

        self.sec = 0
        self.min = 0
        self.hour = 0

        self.EndGame = False
        self.StartLoad = True
        self.BackToDay = False

        self.StartGif = False

        PlaylistName = open(self.Path + 'info/Playlist.txt').read()
        self.Music = PlaylistName

        self.master.after(70)

        if self.K != self.CountGifs+1:
            self.Play(self.Path + 'music/Load')
            self.Loading1(0, LOADING_GIFS=True, NEW_DAY=True)
        else:
            self.K = 0
            self.Play(self.Path + self.Music + 'main0')
            self.MainMenu()

    def MusicChoose(self, settings=None):

        self.ChangeTheme(0)
        self.ClearList()
        self.ButtonMAIN.config(state="disabled", text='SETTINGS')

        self.StartGif = False
        self.FirstTap = False

        if settings:
            self.NewImage(self.Path + 'images/MusicChange.jpg')
            ButName = 'SettingsBut'
            self.StartLoad = True
            self.FirstTap = True
        else:
            self.NewImage(self.Path + 'images/MusicChoose.jpg')
            ButName = 'ContinueBut'
            self.FirstTap = False

        self.MusicButs = []
        self.MusicButsImages = []

        names = ['Hip Hop', 'Rock', 'Hotline Miami', 'Author choice']

        for i in range(4):

            im = Image.open(self.Path + 'images/Music/Playlist' +
                            str(i+1) + '.jpg')
            im = im.resize(Coords.MusicButtons_Size, Image.ANTIALIAS)
            self.MusicButsImages.append(ImageTk.PhotoImage(im))

            MusicBut = Button(self.canv, bg=self.BG, relief="flat",
                              borderwidth=0, cursor="hand2",
                              highlightthickness=0,
                              activebackground=self.BG,
                              image=self.MusicButsImages[i],
                              command=lambda i=i:
                              self.Playlist(i, names[i], ButName))

            self.MusicButs.append(MusicBut)

            Y = round(0.2963*self.H) + round(0.1436*self.H)*i

            self.canv.create_window(Coords.MusicButtons_X, Y, anchor="n",
                                    window=MusicBut)

        if settings:
            self.CreateMusicBut(ButName)

    def Playlist(self, i, name, ButName):

        for but in self.MusicButs:
            but['relief'] = 'flat'

        self.MusicButs[i]['relief'] = 'sunken'

        self.Music = 'music/' + name + '/'

        file = open(self.Path + 'info/Playlist.txt', 'w')
        file.write(self.Music)
        file.close()

        self.Play(self.Path + self.Music + 'main0')

        if not self.FirstTap:
            self.CreateMusicBut(ButName)
            self.FirstTap = True

    def CreateMusicBut(self, ButName):

        im = Image.open(self.Path + 'images/Music/' + ButName + '.jpg')
        im = im.resize(Coords.MusicContinue_Size, Image.ANTIALIAS)
        self.ContinueButImg = ImageTk.PhotoImage(im)

        ContinueBut = Button(self.canv, bg=self.BG, relief="flat",
                             borderwidth=0, cursor="hand2",
                             highlightthickness=0,
                             activebackground=self.BG,
                             image=self.ContinueButImg,
                             command=self.MainMenu)

        self.canv.create_window(Coords.MusicContinue_X,
                                Coords.MusicContinue_Y,
                                anchor="center", window=ContinueBut)

    def MainMenu(self):

        self.ChangeTheme(1)
        self.ClearList()

        self.ButtonMAIN.config(state="normal", text='SETTINGS',
                               command=lambda: self.MusicChoose(True))

        if not self.StartLoad:
            self.Play(self.Path + self.Music + 'main0')
            self.EndGame = True
            if self.hour:
                self.TimerTitle.config(text='YOUR PLAY TIME:  ' +
                                       '{:>02d}:{:>02d}:{:02d}'
                                       .format(self.hour, self.min, self.sec))
            else:
                self.TimerTitle.config(text='YOUR PLAY TIME:  ' +
                                       '{:>02d}:{:02d}'
                                       .format(self.min, self.sec))

        self.StartLoad = False

        self.NewImage(self.Path + 'images/start.png')

        self.CreateCard()
        self.CreateCard2()

        self.DeleteDayButtons = []
        self.Modes()
        self.ArtefactsButton('artefacts', 'Gallery')

        self.StartImages = []
        names = ['start.png', 'rule.png']

        self.i = -1
        for i in range(2):
            self.CreateStartImages('StartPage/' + names[i],
                                   Coords.StartImgCoords[i])

        self.DefaultWays(0)

        if not self.StartGif:

            self.StartGif = True
            self.SlideShow(randint(1, 8))

    def SlideShow(self, iter):

        if iter == 9:
            iter = 1

        pic_way = self.Path + 'images/StartPage/Gif/' + str(iter) + '.png'

        if self.StartGif:

            im = Image.open(pic_way)
            im = im.resize(Coords.StartGifSize, Image.ANTIALIAS)

            self.SlideImg = ImageTk.PhotoImage(im)

            self.canv.create_image(Coords.StartGifX,
                                   Coords.StartGifY,
                                   anchor="center",
                                   image=self.SlideImg)

            self.master.after(1700, self.SlideShow, iter + 1)

    def Modes(self):

        for but in self.DeleteDayButtons:
            self.canv.delete(but)

        self.ArtefactsButton('artefacts', 'Gallery')

        self.ModeImages = []
        self.ModeButtons = []

        self.CreateModeButs('hardcore', 0)
        self.CreateModeButs('arcade', 1)

    def CreateDayButtons(self):

        for but in self.ModeButtons:
            but.destroy()

        self.ButImages = []
        self.DeleteDayButtons = []

        for i in range(6):
            self.DayButtons(i+1, round((0.33+i*0.059)*self.H))

    def ArtefactsButton(self, name, func, verse=None):

        im = Image.open(self.Path + 'images/StartPage/' + name + '.png')
        im = im.resize((Coords.ArtefactsW, Coords.ArtefactsH), Image.ANTIALIAS)
        self.Artefacts = ImageTk.PhotoImage(im)

        self.ButtonArtefacts = Button(self.canv, bg=self.BG,
                                      relief="flat",
                                      cursor="hand2", bd=0,
                                      highlightthickness=0,
                                      activebackground=self.BG,
                                      image=self.Artefacts)

        if verse:
            self.ButtonArtefacts.\
                config(command=lambda: self.Loading1(int(self.Way[0]),
                                                     NEW_DAY=True))
        else:
            self.ButtonArtefacts.config(command=getattr(self, func))

        self.canv.create_window(Coords.Artefacts, anchor="nw",
                                window=self.ButtonArtefacts)

    def CreateStartImages(self, way, coords):

        self.i += 1

        im = Image.open(self.Path + 'images/' + way)
        im.thumbnail((Coords.StartTitleW, Coords.StartTitleH), Image.ANTIALIAS)
        self.StartImages.append(ImageTk.PhotoImage(im))
        self.canv.create_image(coords[0], coords[1],
                               image=self.StartImages[self.i], anchor="nw")

    def CreateModeButs(self, name, num):

        im = Image.open(self.Path + 'images/StartPage/' + name + '.png')
        im.thumbnail((Coords.StartTitleW, Coords.StartTitleH), Image.ANTIALIAS)

        self.ModeImages.append(ImageTk.PhotoImage(im))

        ModeButton = Button(self.canv, bg=self.BG,
                            relief="flat",
                            activebackground=self.BG,
                            image=self.ModeImages[num])

        self.SetBind(ModeButton, "SetMode", name)

        if name == 'hardcore':
            Y = round(0.33*self.H)
        else:
            Y = round(0.507*self.H)

        self.ModeButtons.append(ModeButton)

        self.canv.create_window((Coords.Card_X1 + Coords.Card_X2)//2, Y,
                                anchor="n", window=ModeButton)

    def SetBind(self, widget, func, *args):

        widget.config(cursor="hand2")

        widget.bind("<Enter>", lambda event:
                    self.ChangeButColor(widget, self.HG))
        widget.bind("<Leave>", lambda event:
                    self.ChangeButColor(widget, self.BG))
        widget.bind("<Button-1>", lambda event:
                    getattr(self, func)(*args))

    @staticmethod
    def DeleteBind(widget):

        widget.unbind("<Enter>")
        widget.unbind("<Leave>")
        widget.unbind("<Button-1>")

        widget['state'] = 'disabled'

    @staticmethod
    def ChangeButColor(widget, color):

        try:
            widget.config(bg=color)
        except TclError:
            pass

    def SetMode(self, name):

        self.Mode = name

        if name == 'hardcore':
            self.Loading1(1, '1_1')
        else:
            self.CreateDayButtons()
            self.ArtefactsButton('lobby', 'Modes')

    def DayButtons(self, day, coord_Y):

        line = open(self.Path + 'info/GameInfo.txt').readlines()

        Start = line[day-1].strip()

        im = Image.open(self.Path + 'images/StartPage/day' + str(day) + '.png')
        im.thumbnail((Coords.StartTitleW, Coords.StartTitleH), Image.ANTIALIAS)

        self.ButImages.append(ImageTk.PhotoImage(im))

        DayButton = Button(self.canv, bg=self.BG,
                           relief="flat",
                           activebackground=self.BG,
                           image=self.ButImages[day-1])

        self.SetBind(DayButton, "Loading1", day, Start)

        if line[day-1].strip() == '0':

            def_im = Image.open(self.Path + 'images/StartPage/day0.png')
            def_im.thumbnail((Coords.StartTitleW, Coords.StartTitleH),
                             Image.ANTIALIAS)

            DayButton.config(state="disabled",
                             image=ImageTk.PhotoImage(def_im))

        window = self.canv.create_window((Coords.Card_X1 + Coords.Card_X2)//2,
                                         coord_Y, anchor="n",
                                         window=DayButton)

        self.DeleteDayButtons.append(window)

    def Loading1(self, day, Start=None, LOADING_GIFS=None, NEW_DAY=None):

        self.GIF_play = False
        self.StartGif = False

        if Start:
            self.sec = 0
            self.min = 0

        self.ChangeTheme(day)
        self.ClearList()
        self.ButtonMAIN.config(state="disabled")

        self.NewImage(self.Path + 'images/main' + str(day) + '.jpg')

        if not NEW_DAY:
            self.Play(self.Path + self.Music + 'main' + str(day))

        self.load_sec = 0
        self.canv.create_rectangle(round(0.078*self.W), round(0.26*self.H),
                                   round(0.922*self.W), round(0.444*self.H),
                                   fill=self.BG, width=2)

        if LOADING_GIFS:
            self.load_line = round((0.84375*self.W) / self.CountGifs)
            LoadTitleText = "INSTALLATION"
            self.ButtonMAIN.config(text='VERSION 2.1')
        else:
            self.load_line = round((0.84375*self.W) / 50)
            LoadTitleText = 'Loading... Wait a few seconds'

        self.LoadTitle = Label(self.canv,
                               text=LoadTitleText,
                               bg=self.BG,
                               fg='white',
                               font=Coords.Font5)
        self.canv.create_window((round(0.4167*self.W), round(0.3472*self.H)),
                                anchor="center",
                                window=self.LoadTitle)

        self.Procents = Label(self.canv, text='{:^3.1f}%'.format(0),
                              bg=self.BG,
                              fg='white',
                              font=Coords.Font5)
        self.canv.create_window((0.8125*self.W, round(0.3472*self.H)),
                                anchor="center",
                                window=self.Procents)

        if LOADING_GIFS:
            self.LoadTitle.config(fg=self.FG_1)
            self.Procents.config(fg=self.FG_1)

        self.canv.create_rectangle(round(0.078*self.W), round(0.4815*self.H),
                                   round(0.922*self.W), round(0.5185*self.H),
                                   fill=self.BG, width=2)

        self.master.after(280, self.Loading2, day, Start, LOADING_GIFS)

    def CreatingLastLine(self):

        self.canv.create_rectangle(round(0.078*self.W) +
                                   self.load_sec * self.load_line,
                                   round(0.4815*self.H),
                                   round(0.9219*self.W) - 1,
                                   round(0.5185*self.H),
                                   fill=self.FG_2, width=0)

    def Loading2(self, day, Start=None, LOADING_GIFS=None):

        if LOADING_GIFS:
            self.load_sec = self.K
        else:
            self.load_sec += 1

        self.canv.create_rectangle(round(0.078*self.W),
                                   round(0.4815*self.H),
                                   round(0.078*self.W) +
                                   self.load_sec*self.load_line,
                                   round(0.5185*self.H),
                                   fill=self.FG_2, width=0)

        if round(0.078*self.W) + (self.load_sec + 1)*self.load_line > \
           round(0.9219*self.W) or self.K == self.CountGifs + 1:

            self.K = 0
            self.CreatingLastLine()
            self.Procents.config(text='{:^3.1f}%'.format(100))

            if LOADING_GIFS:
                self.master.after(220, self.MusicChoose)
            else:
                self.master.after(45, self.StartDay, day, Start)

        else:
            if LOADING_GIFS:
                self.Procents.config(text='{:^3.1f}%'
                                     .format((self.K-1)*(100/self.CountGifs)))
                self.master.after(72, self.Loading2, day, Start, LOADING_GIFS)
            else:
                self.Procents.config(text='{:^3.1f}%'
                                     .format(self.load_sec*1.9))
                self.master.after(72, self.Loading2, day, Start)

    def StartDay(self, day, Start=None):

        self.ClearList()

        self.NewImage(self.Path + 'images/main' + str(day) + '.jpg')

        self.LoadTitle.destroy()

        self.ButtonMAIN.config(state="normal")

        if Start:
            self.DAY_START = Start
            self.EndGame = False
            self.Timer()

        if self.BackToDay:
            self.CreateCard()
            self.CreateCard2()

            self.Game(self.Way)
            self.BackToDay = False

        elif self.DAY_START in ['7_1', '7_2']:
            self.GameEnd()

        else:
            self.CreateCard()
            self.CreateCard2()

            self.Game(self.DAY_START)

    def ClearList(self):

        self.canv.delete('all')

        self.Bar = Frame(self.canv, width=self.W, height=Coords.BarH,
                         bg=self.BG, colormap="new")
        self.canv.create_window((0, 0),  anchor="nw", window=self.Bar)

        self.FrameButtons = []

        k = round(self.H/self.W, 4)

        if (k > 0.56 and self.H < 900) or (k > 0.7):
            Main_W = round(0.011*self.W)
            Close_W = round(0.008*self.W)
        else:
            Main_W = round(0.008*self.W)
            Close_W = round(0.00625*self.W)

        self.BarButton('CLOSE', Coords.Close_ButtonX, Close_W, 'Destroy')

        self.ButtonMAIN = Button(self.canv, width=Main_W,
                                 relief="raised", cursor="hand2",
                                 bg=self.BG, fg='white',
                                 activebackground=self.BG,
                                 activeforeground='white',
                                 font=Coords.Font6, text='MAIN MENU',
                                 command=self.MainMenu)

        self.canv.create_window(Coords.MainMenu_ButtonX,
                                (Coords.BarH - 1)/2,
                                anchor="center",
                                window=self.ButtonMAIN)

        self.FrameButtons.append(self.ButtonMAIN)

        self.BarButton('+', Coords.VolumeUp_ButtonX,
                       round(0.002083*self.W), 'VolumeUp')

        self.BarButton('-', Coords.VolumeDown_ButtonX,
                       round(0.002083*self.W), 'VolumeDown')

        if self.hour:
            timer_text = 'TIME:  {:>02d}{:>02d}:{:02d}'\
                         .format(self.hour, self.min, self.sec)
        else:
            timer_text = 'TIME:  {:>02d}:{:02d}'.format(self.min, self.sec)

        self.TimerTitle = Label(self.canv, text=timer_text,
                                bg=self.BG, fg='white',
                                font=Coords.Font2)
        self.canv.create_window(Coords.Timer_TitleX, (Coords.BarH - 3)/2,
                                anchor="w", window=self.TimerTitle)

        vol = pygame.mixer.music.get_volume()

        self.VolumeTitle = Label(self.canv, text='VOLUME: ' +
                                 str(abs(round(vol, 1))),
                                 bg=self.BG, fg='white',
                                 font=Coords.Font2)
        self.canv.create_window(Coords.Volume_TitleX, (Coords.BarH - 3)/2,
                                anchor="center", window=self.VolumeTitle)

    def Gallery(self, OpenVerse=None):

        scroll_color = '#6d6a6a'

        if OpenVerse:
            self.BackToDay = True
            self.ArtefactsButton('lobby', 'Loading1', True)
        else:
            self.Clear()
            self.min = 0
            self.sec = 0
            self.ArtefactsButton('lobby', 'MainMenu')
            self.StartLoad = True
            self.StartGif = False
            self.ButtonMAIN.config(state="normal", text='SETTINGS',
                                   command=lambda: self.MusicChoose(True))
            for but in self.ModeButtons:
                but.destroy()

        self.NewImage(self.Path + 'images/gallery.png')

        self.CreateCard()
        self.CreateCard2()

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("My.Vertical.TScrollbar",
                        gripcount=0,
                        background=scroll_color,
                        darkcolor=scroll_color,
                        lightcolor=scroll_color,
                        troughcolor=self.BG,
                        bordercolor=self.BG,
                        arrowcolor=scroll_color)

        PoemFrame = Frame(self.canv)
        self.canv.create_window(self.W - Coords.Card_X2, Coords.Card_Y1,
                                anchor="nw", window=PoemFrame)

        self.PoemCanv = Canvas(PoemFrame, bd=0, highlightthicknes=0,
                               height=Coords.Card_Y2 - Coords.Card_Y1,
                               bg=self.BG)

        self.Vscrollbar = ttk.Scrollbar(PoemFrame, orient="vertical",
                                        style="My.Vertical.TScrollbar",
                                        command=self.PoemCanv.yview)

        self.PoemCanv.config(yscrollcommand=self.Vscrollbar.set)
        self.Vscrollbar.pack(fill="y", side="right")

        self.interior = Frame(self.PoemCanv)

        self.PoemCanv.pack()
        self.PoemCanv.create_window((0, 0), anchor="nw",
                                    window=self.interior)

        self.Verse = False

        self.interior.bind('<Configure>',
                           lambda event: self.ConfigureInterior())

        self.interior.bind_all("<MouseWheel>",  self.OnMouseWheel)

        self.PoemButtons = []
        self.PoemImages = []

        t = -1
        self.Disabled = []

        self.Scrolls = []

        for i in range(1, 11):

            im = Image.open(self.Path + 'images/StartPage/Gallery/' +
                            str(i) + '.png')
            im = im.resize(Coords.ArtefactSize, Image.ANTIALIAS)
            self.PoemImages.append(ImageTk.PhotoImage(im))

            but = Button(self.interior, bg=self.BG,
                         relief="flat", bd=0, highlightthicknes=0,
                         image=self.PoemImages[i-1],
                         activebackground=self.BG,
                         cursor="hand2",
                         command=lambda i=i: self.Poem(i))

            self.PoemButtons.append(but)

            line = open(self.Path + 'info/Verse.txt').readlines()

            if line[i-1].strip() == '0':

                t += 1

                def_im = Image.open(self.Path +
                                    'images/StartPage/Gallery/0.png')

                def_im = def_im.resize(Coords.ArtefactSize, Image.ANTIALIAS)

                self.Disabled.append(ImageTk.PhotoImage(def_im))

                self.PoemButtons[i-1].config(state="disabled",
                                             image=self.Disabled[t])

            self.PoemButtons[-1].pack()

        if not OpenVerse:
            self.LoadGif(self.Path + 'temp/Gallery.gif',
                         self.W - Coords.StartGifX, Coords.NewDayImg[1])

    def ConfigureInterior(self):

        size = (self.interior.winfo_reqwidth(),
                self.interior.winfo_reqheight())

        self.PoemCanv.config(scrollregion="0 0 %s %s" % size)

        if self.interior.winfo_reqwidth() != self.PoemCanv.winfo_width():

            self.PoemCanv.config(width=self.interior.winfo_reqwidth())

    def OnMouseWheel(self, event):

        if self.Verse:

            x = self.canv.winfo_pointerx()
            if x > self.W/2:
                self.PoemCanv.yview_scroll(-1*(event.delta//120), "units")
            else:
                self.VerseCanv.yview_scroll(-1*(event.delta//120), "units")
        else:
            self.PoemCanv.yview_scroll(-1*(event.delta//120), "units")

    def Poem(self, num):

        for Scroll in self.Scrolls:
            Scroll.destroy()

        self.GIF_play = False

        for lbl in self.LabelGif:
            lbl.destroy()

        self.CreateCard()

        self.CreateStartImages('StartPage/Gallery/Title' + str(num) + '.png',
                               Coords.StartImgCoords[0])

        VerseFrame = Frame(self.canv)
        self.canv.create_window(Coords.Verse, anchor="n",
                                window=VerseFrame)

        self.VerseCanv = Canvas(VerseFrame, bd=0, highlightthicknes=0,
                                width=round(0.198 * self.W),
                                height=round(0.36 * self.H), bg=self.BG)

        self.VerseBar = ttk.Scrollbar(VerseFrame, orient="vertical",
                                      style="My.Vertical.TScrollbar",
                                      command=self.VerseCanv.yview)

        self.VerseCanv.config(yscrollcommand=self.VerseBar.set)
        self.VerseBar.pack(fill="y", side="right")

        self.Scrolls.append(self.VerseBar)
        self.Scrolls.append(VerseFrame)

        self.interior2 = Frame(self.VerseCanv, bg=self.BG)

        self.VerseCanv.pack()
        self.VerseCanv.create_window((0, 0), anchor="nw",
                                     window=self.interior2)

        self.Verse = True

        self.interior2.bind('<Configure>',
                            lambda event: self.ConfigureInterior2())

        self.interior2.bind_all("<MouseWheel>", self.OnMouseWheel)

        self.VerseWrite(num)

    def VerseWrite(self, num):

        FG = '#d6d6d6'
        txt = getattr(Gallery, 'Artefact' + str(num))

        font = Format.text_font(txt)
        height = Format.text_height(txt, font)

        Temp = Canvas(self.interior2, bg=self.BG,
                      width=round(0.198 * self.W),
                      height=height,
                      highlightthicknes=0, bd=0)

        label = Label(Temp, text=txt, justify="left",
                      font=font, bg=self.BG, fg=FG)

        Temp.create_window((0, 0), anchor="nw", window=label)
        Temp.pack()

    def ConfigureInterior2(self):

        size = (self.interior2.winfo_reqwidth(),
                self.interior2.winfo_reqheight())

        self.VerseCanv.config(scrollregion="0 0 %s %s" % size)

        if self.interior2.winfo_reqwidth() != self.VerseCanv.winfo_width():

            self.VerseCanv.config(width=self.interior2.winfo_reqwidth())

    def Timer(self):

        if self.sec == 59 and self.min == 59:
            self.sec = 0
            self.min = 0
            self.hour += 1
        elif self.sec == 59:
            self.sec = 0
            self.min += 1
        else:
            self.sec += 1

        if not self.EndGame:

            if self.hour:
                self.TimerTitle.config(text='TIME:  ' +
                                       '{:>02d}:{:>02d}:{:02d}'
                                       .format(self.hour, self.min, self.sec))
            else:
                self.TimerTitle.config(text='TIME:  ' +
                                       '{:>02d}:{:02d}'.format(self.min,
                                                               self.sec))
            self.master.after(1000, self.Timer)

    def NewImage(self, way):

        self.pic = ImageTk.PhotoImage(Image.open(way)
                                      .resize((round(1.001*self.W),
                                               round(0.958*self.H)),
                                              Image.ANTIALIAS))

        pic_window = self.canv.create_image(-2, Coords.BarH - 2,
                                            image=self.pic, anchor="nw")

        self.canv.tag_lower(pic_window)

    def CreateCard(self):

        self.Rect = self.canv.create_rectangle(Coords.Card_X1, Coords.Card_Y1,
                                               Coords.Card_X2, Coords.Card_Y2,
                                               fill=self.BG,
                                               outline=self.BG)

    def CreateCard2(self):

        self.Rect2 = self.canv.create_rectangle(self.W - Coords.Card_X1,
                                                Coords.Card_Y1,
                                                self.W - Coords.Card_X2,
                                                Coords.Card_Y2,
                                                fill=self.BG,
                                                outline=self.BG)

    def BarButton(self, text, x, w, func_name):

        self.Button0 = Button(self.canv, width=w, relief="raised",
                              bg=self.BG, fg='white',
                              activebackground=self.BG,
                              activeforeground='white',
                              cursor="hand2",
                              font=Coords.Font6, text=text,
                              command=getattr(self, func_name))

        self.canv.create_window(x, (Coords.BarH - 1)/2, anchor="center",
                                window=self.Button0)

        self.FrameButtons.append(self.Button0)

    def PrintText(self, a, coords):

        self.Card_Text = Label(self.canv, text=a, justify="left",
                               font=Coords.Font3,
                               bg=self.BG, fg=self.FG_1)

        self.canv.create_window(coords,  anchor="ne", window=self.Card_Text)

        self.Elements.append(self.Card_Text)

    def PrintTitle(self, a, coords):

        self.Card_Title = Label(self.canv, text=a,
                                bg=self.BG, fg=self.FG_2,
                                font=Coords.Font7)

        self.canv.create_window(coords,  anchor="nw", window=self.Card_Title)

        self.Elements.append(self.Card_Title)

    def CreateButton(self, i, num, a, font, width, height, k, func_name):

        card_center = round(0.4352*self.H)

        if i == 0:
            if num % 2:
                Y = card_center
            else:
                if num == 4:
                    Y = round(card_center - 0.43*self.H//(num + 2))
                else:
                    Y = round(card_center - round(0.58*self.H//(num + 2)))
        else:
            if i % 2:
                Y = round(card_center + k*i*(round(0.58*self.H)//(num + 2)))
            else:
                if num % 2:
                    i -= 1
                else:
                    i += 1
                Y = round(card_center - k*i*(round(0.58*self.H)//(num + 2)))

        ButtonPlay = Button(self.canv, width=width,
                            height=round(0.5555*self.H)//num//height - 1,
                            bg=self.BG, fg=self.FG_2,
                            cursor="hand2",
                            relief="groove", overrelief="ridge",
                            highlightthickness=1,
                            highlightcolor=self.HG,
                            font=('Calibri', font, 'bold'),
                            activebackground=self.FG_2,
                            activeforeground=self.BG, text=a.upper())

        if func_name == 'Last':
            self.SetBind(ButtonPlay, "Game", self.DAY_START)
        elif func_name == 'AnswerSection':
            self.SetBind(ButtonPlay, "AnswerSection")
        else:
            self.SetBind(ButtonPlay, "Game", func_name)

        self.canv.create_window(self.W - Coords.Card_X2 +
                                (Coords.Card_X2 - Coords.Card_X1)/2, Y,
                                anchor="center", window=ButtonPlay)

        self.CardButtons.append(ButtonPlay)

    def DEATH(self, day, way):

        try:
            self.Play(self.Path + self.Music + 'die' + str(day))
        except pygame.error:
            self.Play(self.Path + 'music/Hotline Miami/die1')

        self.NewImage(self.Path + 'images/end' + str(day) + '.png')

        self.CreateCard2()

        im = Image.open(self.Path + 'images/GameOver/GameOver' +
                        str(day) + '.png')

        im.thumbnail((Coords.StartTitleW, Coords.StartTitleH), Image.ANTIALIAS)
        self.GameOver = ImageTk.PhotoImage(im)

        self.canv.create_image(Coords.DeathButtonX, Coords.Card_Y1 +
                               Coords.ImgBorder,
                               image=self.GameOver, anchor="n")

        self.DefaultWays(day)

        self.DeathButton(day)

        self.LoadGif(self.Path + 'temp/' + way + '.gif',)

    def NEW_DAY(self, day):

        if day != 7:
            self.Play(self.Path + self.Music + 'main' + str(day))
        else:
            self.Play(self.Path + 'music/End')

        self.ChangeTheme(day)

        self.canv.delete(self.Rect)
        self.canv.delete(self.Rect2)

        self.ChangeBgColor()
        self.CreateCard()
        self.CreateCard2()

        self.NewImage(self.Path + 'images/main' + str(day) + '.jpg')

        self.NewDayButton(day)

        info = open(self.Path + 'info/GameInfo.txt').readlines()
        info[day-1] = self.DAY_START

        f = open(self.Path + 'info/GameInfo.txt', 'w')

        for item in info:
            f.write("%s\n" % item.strip())

        f.close()

        self.LoadGif(self.Path + 'temp/New' + self.DAY_START + '.gif')

    def DeathButton(self, day):

        im = Image.open(self.Path + 'images/GameOver/TryAgain' +
                        str(day) + '.png')

        im.thumbnail((Coords.StartTitleW - 5*Coords.ImgBorder,
                      Coords.StartTitleH), Image.ANTIALIAS)
        self.TryAgain = ImageTk.PhotoImage(im)

        if self.Mode == 'hardcore':
            day = 1
            self.DAY_START = '1_1'

        self.ButtonRestart = Button(self.canv, bg=self.BG,
                                    relief="flat", cursor="hand2",
                                    bd=0, highlightthickness=0,
                                    activebackground=self.BG,
                                    image=self.TryAgain,
                                    command=lambda: self.Loading1(day))

        self.canv.create_window(
            Coords.DeathButtonX,
            round(Coords.DeathButtonY - 1.5*Coords.ImgBorder),
            anchor="s", window=self.ButtonRestart)

    def NewDayButton(self, day):

        im = Image.open(self.Path + 'images/NewDay/' + str(day) + '.png')
        im.thumbnail((Coords.StartTitleW, Coords.StartTitleH), Image.ANTIALIAS)

        self.NDim = ImageTk.PhotoImage(im)

        self.ButtonDayStart = Button(self.canv, relief="flat", bg=self.BG,
                                     activebackground=self.BG,
                                     image=self.NDim,
                                     cursor="hand2",
                                     command=lambda:
                                     self.Loading1(day, NEW_DAY=True))

        self.canv.create_window(Coords.NewDayButton, anchor="n",
                                window=self.ButtonDayStart)

    def AnswerSection(self):

        Answer = getattr(Cards, 'Question' + self.Way)

        self.Clear()

        self.PrintTitle(getattr(Cards, 'Title' + self.Way), Coords.Card_Title)

        self.PrintText(Format.text(getattr(Cards, 'Text' + self.Way)),
                       Coords.Card_Text)

        Card_Text = Label(self.canv, text=Answer, justify="center",
                          font=Coords.Font4,
                          bg=self.BG, fg=self.FG_2)
        self.canv.create_window(Coords.AnswText1,  anchor="center",
                                window=Card_Text)

        self.canv.create_rectangle(Coords.AnswLabel[0],
                                   Coords.AnswLabel[1],
                                   Coords.AnswLabel[2],
                                   Coords.AnswLabel[3],
                                   outline=self.FG_2)

        Card_Text2 = Label(self.canv, text='Ответ:', justify="right",
                           font=Coords.Font4,
                           bg=self.BG, fg=self.FG_1)
        self.canv.create_window(Coords.AnswText2, anchor="w",
                                window=Card_Text2)

        enter = Entry(self.canv, width=20, font=Coords.Font8)

        self.canv.create_window(Coords.AnswEntry, anchor="e", window=enter)

        enter.insert(0, ' '*2)
        enter.focus_set()

        ButtonAnswer = Button(self.canv, width=33, height=4,
                              relief="groove",
                              bg=self.BG, fg=self.FG_1,
                              activebackground=self.FG_1,
                              activeforeground=self.BG,
                              cursor="hand2",
                              font=Coords.Font2, text='ANSWER',
                              command=lambda:
                              self.AnswerSection2(enter.get()))

        self.canv.create_window(Coords.AnswButton, anchor="se",
                                window=ButtonAnswer)

        enter.bind("<Return>", lambda event: self.AnswerSection2(enter.get()))

        self.LoadGif(self.Path + 'temp/AnswerSection' + self.Way + '.gif')

    def AnswerSection2(self, answ):

        if answ.lower().strip() == getattr(Cards, 'RightAnswer' + self.Way):

            self.ClearList()
            self.NewImage(self.Path + 'images/main' + self.Way[0] + '.jpg')
            self.CreateCard()
            self.CreateCard2()
            self.Game(Ways[self.Way][2])

        elif answ.lower().strip() == '':

            messagebox.showinfo('', 'Напишите ответ')

        else:

            self.ClearList()
            self.NewImage(self.Path + 'images/main' + self.Way[0] + '.jpg')
            self.CreateCard()
            self.CreateCard2()
            self.Game(Ways[self.Way][3])

    def ChallengeComplete1(self, num):

        for but in self.CardButtons:
            self.DeleteBind(but)

        im = Image.open(self.Path + 'images/Challenge/' + str(num) + '.png')
        im.thumbnail((Coords.GIF_x + 2*Coords.ImgBorder,
                      Coords.GIF_y + 2*Coords.ImgBorder), Image.ANTIALIAS)

        self.ChallengePic = ImageTk.PhotoImage(im)

        self.Nameplate = self.canv.create_image((self.W/2, -Coords.GIF_y),
                                                anchor="n",
                                                image=self.ChallengePic)

        info = open(self.Path + 'info/Verse.txt').readlines()
        info[num-1] = '1'

        f = open(self.Path + 'info/Verse.txt', 'w')

        for item in info:
            f.write("%s\n" % item.strip())

        f.close()

        setattr(Cards, 'Challenge' + self.Way, 'Done')

        day = int(self.Way[0])
        Thread(target=self.ChallengeComplete2, args=(num, day)).start()

    def ChallengeComplete2(self, num, day):

        if self.canv.coords(self.Nameplate)[1] < Coords.Card_Y1:
            self.canv.move(self.Nameplate, 0, 6)
            self.master.after(30, self.ChallengeComplete2, num, day)
        else:
            self.Num = num
            self.OpenImg = []
            self.OpenBut = []
            self.OpenContinueButs(day, 1, Coords.OpenButY, 'OpenArtefact')
            self.OpenContinueButs(day, 2, Coords.ContinueButY, 'ContinuePlay')

    def OpenContinueButs(self, day, num, Y, func):

        im = Image.open(self.Path + 'images/Challenge/Buts/But' + str(day) +
                        '_' + str(num) + '.png')
        im.thumbnail(Coords.ButOpen, Image.ANTIALIAS)
        self.OpenImg.append(ImageTk.PhotoImage(im))

        But = Button(self.canv, relief="flat",
                     image=self.OpenImg[num-1],
                     borderwidth=0,
                     cursor="hand2",
                     highlightthickness=0,
                     bg=self.BG,
                     activebackground=self.BG,
                     command=getattr(self, func))

        self.OpenBut.append(But)

        self.canv.create_window(Coords.OpenButX, Y, anchor="nw", window=But)

    def ContinuePlay(self):

        for but in self.CardButtons:
            but.destroy()

        buttons = getattr(Cards, 'Buttons' + self.Way)
        info = Format.buttons_info(buttons)

        for i in range(info[0]):
            self.CreateButton(i, info[0], info[1][i], info[2], info[3],
                              info[4], info[5], Ways[self.Way][i])

        self.canv.delete(self.Nameplate)

        for But in self.OpenBut:
            But.destroy()

        self.LoadGif(self.Path + 'temp/' + self.Way + '.gif')

    def OpenArtefact(self):

        self.canv.delete(self.Nameplate)

        for But in self.OpenBut:
            But.destroy()

        self.ChangeTheme(1)
        self.ClearList()

        self.Gallery(True)
        self.Poem(self.Num)

    def Pass(self):
        pass

    @staticmethod
    def DefaultWays(day):

        if day == 1:
            Ways['2_4'][1] = '2_15'

        Ways['4_41'][1] = '4_43'

    def Game(self, way):

        self.Clear()
        Start_Gif = True

        self.PrintTitle(getattr(Cards, 'Title' + way), Coords.Card_Title)

        if way in ['6_14', '6_26']:
            lines = getattr(Cards, 'Text' + way)
            Text_END = '\n'.join(map(lambda a: a.strip(), lines.split('\n')))
            self.PrintText(Text_END, Coords.Card_Text)
        else:
            self.PrintText(Format.text(getattr(Cards, 'Text' + way)),
                           Coords.Card_Text)

        if way == '1_18':
            Ways['2_4'][1] = '2_26'

        if way == '4_38':
            Ways['4_41'][1] = '4_44'

        try:
            answer = getattr(Cards, 'Answer' + way).upper()
            self.PrintText(answer, Coords.Card_Answer)

        except AttributeError:
            pass

        try:
            buttons = getattr(Cards, 'Buttons' + way)
            info = Format.buttons_info(buttons)
            for i in range(info[0]):
                self.CreateButton(i, info[0], info[1][i], info[2], info[3],
                                  info[4], info[5], Ways[way][i])
        except AttributeError:
            pass

        try:
            self.DEATH(getattr(Cards, 'Death' + way), way)
            Start_Gif = False

        except AttributeError:
            pass

        try:
            self.DAY_START = getattr(Cards, 'NewDay' + way)
            self.NEW_DAY(int(self.DAY_START[0]))
            Start_Gif = False

        except AttributeError:
            pass

        self.Way = way

        try:
            ChallengeNum = getattr(Cards, 'Challenge' + way)
            info = open(self.Path + 'info/Verse.txt').readlines()

            if ChallengeNum != 'Done' and info[ChallengeNum-1].strip() != '1':
                self.ChallengeComplete1(ChallengeNum)
                Start_Gif = False

        except AttributeError:
            pass

        if Start_Gif:
            self.LoadGif(self.Path + 'temp/' + way + '.gif')

    def GameEnd(self):

        self.NewImage(self.Path + 'images/End/VerseBackground.jpg')

        im = Image.open(self.Path + 'images/End/VerseTitle.png')
        im = im.resize(Coords.EndVerse_Size, Image.ANTIALIAS)
        self.EndTitleImg = ImageTk.PhotoImage(im)

        self.canv.create_image(Coords.EndTitle_X, Coords.EndTitle_Y,
                               image=self.EndTitleImg, anchor="n")

        BG_color = '#452e24'
        scroll_color = '#a69d7f'

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("My.Vertical.TScrollbar",
                        gripcount=0,
                        background=scroll_color,
                        darkcolor=scroll_color,
                        lightcolor=scroll_color,
                        troughcolor=BG_color,
                        bordercolor=BG_color,
                        arrowcolor=scroll_color)

        self.EndFrame = Frame(self.canv)
        self.canv.create_window(Coords.EndVerse_X, Coords.EndVerse_Y,
                                anchor="n", window=self.EndFrame)

        self.EndBar = ttk.Scrollbar(self.EndFrame, orient="vertical",
                                    style="My.Vertical.TScrollbar")
        self.EndBar.pack(fill="y", side="right", expand="false")

        self.EndCanv = Canvas(self.EndFrame, bd=0, highlightthicknes=0,
                              height=round(0.33*self.H), bg=BG_color,
                              yscrollcommand=self.EndBar.set)

        self.EndCanv.pack(side="left", fill="both", expand="true")

        self.EndBar.config(command=self.EndCanv.yview)

        self.interior_end = Frame(self.EndCanv, bg=BG_color)
        self.interior_end_id = self.EndCanv.create_window(
            (0, 0),
            window=self.interior_end,
            anchor="nw")

        self.interior_end.bind('<Configure>',
                               lambda event: self.ConfigureInterior_end())

        self.interior_end.bind_all("<MouseWheel>", self.OnMouseWheel_end)

        info = open(self.Path + 'info/Verse.txt').readlines()
        info[9] = '1'

        f = open(self.Path + 'info/Verse.txt', 'w')

        for item in info:
            f.write("%s\n" % item.strip())

        f.close()

        self.EndWrite(10, BG_color)

        self.NextButton()

    def EndWrite(self, num, color):

        FG = '#d6d6d6'
        txt = getattr(Gallery, 'Artefact' + str(num))

        font = Format.text_font(txt)

        Temp = Canvas(self.interior_end, bg=color,
                      width=round(0.198 * self.W),
                      height=round(0.332 * self.H),
                      highlightthicknes=0, bd=0)

        label = Label(Temp, text=txt, justify="left",
                      font=font, bg=color, fg=FG)

        Temp.create_window((0, 0), anchor="nw", window=label)
        Temp.pack()

        Temp.grid(row=0, column=0, sticky="w")

    def ConfigureInterior_end(self):

        size = (self.interior_end.winfo_reqwidth(),
                self.interior_end.winfo_reqheight())

        self.EndCanv.config(scrollregion="0 0 %s %s" % size)

        if self.interior_end.winfo_reqwidth() != self.EndCanv.winfo_width():

            self.EndCanv.config(width=self.interior_end.winfo_reqwidth())

    def OnMouseWheel_end(self, event):

        self.EndCanv.yview_scroll(-1*(event.delta//120), "units")

    def NextButton(self):

        im = Image.open(self.Path + 'images/End/NextButton.png')
        im = im.resize(Coords.NextButton_Size, Image.ANTIALIAS)
        self.NextImg = ImageTk.PhotoImage(im)

        self.NextBut = Button(self.canv, bg=self.BG, relief="flat",
                              borderwidth=0, cursor="hand2",
                              highlightthickness=0,
                              activebackground=self.BG,
                              image=self.NextImg,
                              command=self.Age)

        self.canv.create_window(Coords.NextButton_X, Coords.NextButton_Y,
                                anchor="nw", window=self.NextBut)

    def CreateAgeImages(self, name, size, coord):

        self.ImgN += 1

        Im1 = Image.open(self.Path + 'images/Age/' + name)
        self.AgeImg.append(ImageTk.PhotoImage(Im1.resize(size,
                                                         Image.ANTIALIAS)))

        self.canv.create_image(coord, image=self.AgeImg[self.ImgN],
                               anchor="nw")

    def Age(self):

        self.ChangeTheme(0)
        self.ClearList()

        self.NewImage(self.Path + 'images/main7.jpg')

        self.AgeImg = []
        self.ImgN = -1

        self.AgeBg = self.canv.create_rectangle(-10, 0, self.W + 10, -self.H,
                                                fill=self.BG,
                                                outline=self.BG)
        self.canv.tag_raise(self.AgeBg)

        self.master.after(100, self.MoveBg2)

    def MoveBg2(self):

        if self.canv.coords(self.AgeBg)[3] <= self.H:
            self.canv.move(self.AgeBg, 0, 9)
            self.master.after(26, self.MoveBg2)
        else:
            self.master.after(70, self.Video)

    def Video(self):

        self.ChangeTheme(0)
        self.ClearList()

        self.ButtonMAIN.config(state="disabled", text='VERSION 2.1')

        self.EndGame = True

        if self.hour:
            self.TimerTitle.config(text='YOUR PLAY TIME:  ' +
                                   '{:>02d}:{:>02d}:{:02d}'
                                   .format(self.hour, self.min, self.sec))
        else:
            self.TimerTitle.config(text='YOUR PLAY TIME:  ' +
                                   '{:>02d}:{:02d}'.format(self.min, self.sec))

        self.NewImage(self.Path + 'images/End/VideoBackground.png')

        Im1 = Image.open(self.Path + 'images/End/Play.png')
        Im2 = Image.open(self.Path + 'images/End/Pause.png')

        Im1 = Im1.resize(Coords.PauseBut_Size, Image.ANTIALIAS)
        Im2 = Im2.resize(Coords.PauseBut_Size, Image.ANTIALIAS)

        self.PlayImg = ImageTk.PhotoImage(Im1)
        self.PauseImg = ImageTk.PhotoImage(Im2)

        self.CreateButImg(self.PlayImg)

        way_to_video = self.Path + 'video/Resized/End.avi'
        way_to_music = self.Path + 'video/End Audio.ogg'

        pygame.mixer.music.stop()

        x1 = self.W/2 - self.VideoW//2
        y1 = Coords.Video_Y - self.VideoH//2
        x2 = self.W/2 + self.VideoW//2
        y2 = Coords.Video_Y + self.VideoH//2

        self.VideoR = self.canv.create_rectangle(x1, y1, x2, y2,
                                                 fill=self.BG,
                                                 outline="black",
                                                 width=2)

        self.master.after(200, self.CreateVideo, way_to_video, way_to_music)

    def CreateButImg(self, img):

        self.VidBut = self.canv.create_image(self.W/2, Coords.PauseBut_Y,
                                             image=img,
                                             anchor="n")

    def CreateVideo(self, video_source, music_source):

        self.vid = MyVideoCapture(video_source)

        self.VideoCloseBut = True
        self.CaptionsStart = False

        self.PlayVideo = True
        self.IsPaused = False

        self.delay = 40

        self.master.after(20, self.VideoMusic(music_source))
        self.Update()

    @staticmethod
    def VideoMusic(music_source):

        pygame.mixer.music.load(music_source)
        pygame.mixer.music.play(1)

    def Snapshot(self):

        if not self.CaptionsStart:

            self.Pause()
            self.canv.delete(self.VidBut)

            if self.PlayVideo:
                self.PlayVideo = False
                self.CreateButImg(self.PauseImg)
            else:
                self.PlayVideo = True
                self.CreateButImg(self.PlayImg)
                self.Update()

    def Update(self):

        before_read = time.time()

        ret, frame = self.vid.GetFrame()

        self.canv.focus_set()

        if ret:
            image = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image)
            self.canv.create_image(self.W/2, Coords.Video_Y,
                                   image=self.photo, anchor="center")
        else:
            self.PlayVideo = False
            self.canv.delete(self.VidBut)
            self.MainMenu()

        self.canv.bind("<space>", lambda event: self.Snapshot())

        after_read = time.time()

        k = round((after_read - before_read)*1000)

        if self.PlayVideo:
            self.master.after(self.delay - k, self.Update)

    def Pause(self):

        if self.IsPaused:
            pygame.mixer.music.unpause()
            self.IsPaused = False
        else:
            pygame.mixer.music.pause()
            self.IsPaused = True


class MyVideoCapture:

    def __init__(self, video_source):

        self.vid = cv2.VideoCapture(video_source)

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def GetFrame(self):

        ret = None

        if self.vid.isOpened():

            ret, frame = self.vid.read()

            if ret:
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return ret, None

    def __del__(self):

        if self.vid.isOpened():
            pygame.mixer.music.stop()
            self.vid.release()


class ResizeGif:

    def __init__(self, path, save_as=None, resize_to=None):

        all_frames = self.ExtractAndResizeFrames(path, resize_to)

        if not save_as:
            save_as = path

        if len(all_frames) == 1:
            all_frames[0].save(save_as, optimize=True)
        else:
            all_frames[0].save(save_as, optimize=True, save_all=True,
                               append_images=all_frames[1:], loop=1000)

    @staticmethod
    def AnalyseImage(path):

        img = Image.open(path)
        results = {'size': img.size, 'mode': 'full'}

        try:
            while True:
                if img.tile:
                    tile = img.tile[0]
                    update_region = tile[1]
                    update_region_dimensions = update_region[2:]
                    if update_region_dimensions != img.size:
                        results['mode'] = 'partial'
                        break
                img.seek(img.tell() + 1)

        except EOFError:
            pass

        return results

    def ExtractAndResizeFrames(self, path, resize_to=None):

        mode = self.AnalyseImage(path)['mode']

        img = Image.open(path)

        if not resize_to:
            resize_to = (Coords.GIF_x, Coords.GIF_y)

        i = 0
        p = img.getpalette()
        last_frame = img.convert('RGBA')

        all_frames = []

        try:
            while True:

                if not img.getpalette():
                    img.putpalette(p)

                new_frame = Image.new('RGBA', img.size)

                if mode == 'partial':
                    new_frame.paste(last_frame)

                new_frame.paste(img, (0, 0), img.convert('RGBA'))

                new_frame.thumbnail(resize_to, Image.ANTIALIAS)
                all_frames.append(new_frame)

                i += 1
                last_frame = new_frame
                img.seek(img.tell() + 1)

        except EOFError:
            pass

        return all_frames


if __name__ == "__main__":

    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(True)
    root.config(cursor="plus")

    game = Life(root, w, h)
    root.mainloop()
