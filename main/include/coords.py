import tkinter as tk

root = tk.Tk()

W, H = root.winfo_screenwidth(), root.winfo_screenheight()
root.destroy()

# Card

Card_Title = (round(0.0625*W), round(0.1574*H))
Card_Text = (round(0.264*W), round(0.2315*H))
Card_Answer = (round(0.2656*W), round(0.6574*H))

Card_X1 = round(0.0406*W)
Card_Y1 = round(0.1389*H)
Card_X2 = 0.275*W
Card_Y2 = round(0.7315*H)

# Bar

BarH = round(0.0435*H)
MainMenu_ButtonX = round(0.045*W)
Close_ButtonX = round(0.9635*W)
Timer_TitleX = round(0.095*W)
VolumeUp_ButtonX = round(0.9114*W)
VolumeDown_ButtonX = round(0.8021*W)
Volume_TitleX = round(0.8567*W)

# Gif

GIF_x = round(0.26*W)
GIF_y = round(0.25*H)
ImgBorder = round(0.01041*W)

# DeathBuuton & NewDayButton

DeathButtonX = W - Card_X1 + (Card_X1 - Card_X2)//2
DeathButtonY = Card_Y2 - 2*ImgBorder

NewDayButton = (DeathButtonX, Card_Y1 + ImgBorder)

NewDayImg = (DeathButtonX, Card_Y1 + (Card_Y2 - Card_Y1)//2)

# StartScreen

StartTitleW = round(0.2135*W)
StartTitleH = round(0.5648*H)

StartGifW = round(0.2135*W - 3*ImgBorder)
StartGifH = round(0.38*H - 3*ImgBorder)

StartGifSize = (StartGifW, StartGifH)

StartGifX = DeathButtonX
StartGifY = round(0.533*H)

StartImgCoords = [(Card_X1 + ImgBorder, Card_Y1 + ImgBorder),
                  (W - Card_X2 + ImgBorder, Card_Y1 + ImgBorder)]

# Artefacts

Artefacts = (round(0.2915*W), round(0.3755*H))

ArtefactsW = round(0.2048*W)
ArtefactsH = round(0.3374*H)

GalleryGif_size = (round(0.2*W - 2*ImgBorder),
                   round(0.555*H - 2*ImgBorder))

ArtefactSize = (round(Card_X2 - Card_X1 - 0.5*ImgBorder), round(0.1481*H))

Verse = (Card_X1 + (Card_X2 - Card_X1)//2, round(0.32407*H))

ButOpen = (round(0.42*GIF_x), round(0.18*GIF_x))

OpenButX = W/2 + round(0.0278*GIF_x)
OpenButY = Card_Y1 + round(0.4*(0.57407*GIF_x))

ContinueButY = Card_Y1 + round(0.715*(0.57407*GIF_x))

NotRectanle = (W - Card_X1, Card_Y1,
               W - Card_X1 + (Card_X1 - Card_X2), Card_Y2)

# FontSizes

Font1 = ('Calibri', round(0.020833*W), 'bold')  # 40
Font2 = ('Calibri', round(0.008854*W), 'bold')  # 17
Font3 = ('Calibri', round(0.007812*W), 'bold')  # 15
Font4 = ('Calibri', round(0.01146*W), 'bold')  # 22
Font5 = ('Calibri', round(0.0364*W), 'bold')  # 70
Font6 = ('Calibri', round(0.007291*W), 'bold')  # 14
Font7 = ('Calibri', round(0.0156*W), 'bold')  # 30
Font8 = ('Calibri', round(0.010416*W), 'bold')  # 20
Font9 = ('Calibri', round(0.008333*W), 'bold')  # 16
Font10 = ('Calibri', round(0.006771*W), 'bold')  # 13

# AnswerSection

AnswLabel = [W - Card_X1 - ImgBorder, Card_Y1 + ImgBorder,
             W - Card_X2 + ImgBorder, round(0.465*H)]

AnswText1 = (DeathButtonX, round(0.31*H))
AnswText2 = (W - Card_X2 + 1.5*ImgBorder, round(0.53*H))

AnswEntry = (W - Card_X1 - ImgBorder, round(0.53*H))
AnswButton = (W - Card_X1 - ImgBorder, Card_Y2 - ImgBorder)

# Music Choose

MusicButtons_X = round(0.7135*W)

MusicButtons_Size = (round(0.3338*W), round(0.112*H))

MusicContinue_X = round(0.2805*W)
MusicContinue_Y = round(0.7278*H)

MusicContinue_Size = (round(0.315*W), round(0.1407*H))

# The End

EndTitle_X = round(0.278*W)
EndTitle_Y = round(0.2612*H)

EndVerse_Size = (round(0.225*W), round(0.528*H))

NextButton_X = round(0.46094*W)
NextButton_Y = EndTitle_Y

NextButton_Size = (round(0.3224*W), round(0.529*H))

EndVerse_X = EndTitle_X
EndVerse_Y = round(0.4248*H)

# Video

PauseBut_Size = (round(0.1547*W), round(0.1028*H))

PauseBut_Y = round(0.5648*H)

VideoSize = round(0.3125*W)

Video_Y = round(0.3981*H)

# Age Choose

ChooseClass = (round(0.141*W), round(0.213*H))
ChooseClass_Size = (round(0.2521*W), round(0.4065*H))


MainRect = (round(0.105*W), round(0.166*H))
MainRect_Size = (round(0.7552*W), round(0.7157*H))

NotStudy = (ChooseClass[0], round(0.6426*H))
NotStudy_Size = (ChooseClass_Size[0], round(0.1907*H))

AgeButs_X = round(0.4161*W)
AgeButs_Y = ChooseClass[1]

Xn = round(0.1417*W)
Yn = round(0.2148*H)

AgeButs_Size = (round(0.1245*W), round(0.1917*H))

AgeBg = (-20, H//2)
