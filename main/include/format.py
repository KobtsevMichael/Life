import tkinter as tk
from tkinter.font import Font


def button_resize(a, width):

    str_ = text(a, width)
    if str_[1] <= 2:
        return [str_[0], width]

    return button_resize(a, width + 1)


def text(text, width=None):

    words = text.split()

    if not width:
        width = 37

    text_lines = []
    r = ''

    i = 0
    text_end = None

    while i < len(words):

        leng = len(r)

        while leng < width:

            if i == len(words)-1:
                if len(r + words[i] + ' ') > width:
                    r += '\n' + words[i] + ' '
                else:
                    r += words[i] + ' '
                leng = width
                text_end = True
            else:
                r += words[i] + ' '
                leng += len(words[i] + ' ')
                i += 1
                text_end = False

        if not text_end:
            text_lines.append(r[:-len(words[i-1])-1])
            r = ''
            i -= 1
        else:
            text_lines.append(r)
            i += 1

    if width != 37:
        return ['\n'.join(map(lambda a: a.strip(), text_lines)),
                len(text_lines)]
    else:
        return '\n'.join(map(lambda a: a.strip(), text_lines))


def buttons_info(buttons):

    num = len(buttons)

    text_button = []
    font_button = []
    width_button = []
    height_button = []

    for i in range(num):

        if len(list(buttons[i])) > 7:
            text, width = button_resize(buttons[i], 12)
            text_button.append(text)
        else:
            width = len(list(buttons[i]))
            text_button.append(buttons[i])

        size = round(0.0354 * W) // num
        wid = round(0.1667*W)//width + 1
        hei = None

        while wid > round(0.1667*W)//width:
            font = Font(family='Calibri', size=size, weight='bold')
            wid, hei = (font.measure('A'), font.metrics("linespace"))
            size -= 1

        font_button.append(size)
        width_button.append(wid)
        height_button.append(hei)

    if num == 2:
        k = 1
    elif num == 3:
        k = 1.5
    elif num == 4:
        k = 0.7
    else:
        k = 0

    return (num, text_button, min(font_button),
            round(0.21875*W)//min(width_button), min(height_button), k)


def text_font(text):

    max_line = max([len(a) for a in text.split("\n")])

    size = 0.0085
    font = Font(family='Calibri', weight='bold',
                size=round(size * W))

    while font.measure('a') * max_line > round(0.21 * W):
        size -= 0.0005
        font["size"] = round(size * W)

    return font


def text_height(text, font):

    lines = len(text.split("\n"))
    height = font.metrics("linespace") * lines

    return height if height > round(0.361 * H) else round(0.361 * H)


root = tk.Tk()

W, H = root.winfo_screenwidth(), root.winfo_screenheight()
root.destroy()
