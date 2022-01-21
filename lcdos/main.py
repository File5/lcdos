import time

from lcdui.views.lineinput import LineInput
from lcdui.display import BufferedRPLCDDisplay, Cursor
from lcdui.event import Event, EventType, InputEvent
from lcdui.views import Window, Button, CheckBox, Radio, Text, LineInput, ListItem
from lcdui.views.layout import Layout
from lcdui.views.pagescroll import PageScrollLayout
from lcdui.utils import getch

from gamepad import PS4, available as gamepad_available

from lcdos.utils import paged_layout


calendar = ListItem('Calendar', 19)
music = ListItem('Music', 19)
class MainMenu(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = PageScrollLayout(paged_layout([
            calendar,
            ListItem('Calculator', 19),
            ListItem('Terminal', 19),
            ListItem('Settings', 19),
            music,
            ListItem('Notes', 19),
            ListItem('Telegram', 19),
            ListItem('Voice Recorder', 19),
            ListItem('Bluetooth', 19),
            Text(' ' * 19),
            Text(' ' * 19),
            Text(' ' * 19),
        ]), parent=self)


class CalendarWindow(Window):
    layout = [
        Text(' M  T  W  T  F  S  S'),
        Text('10 11 12 13 14 15 16'),
        Text('17 18 19 20[21]22 23'),
        Text('24 25 26 27 28 29 30'),
    ]


class MButton(Button):
    PREFIX = '  '
    SUFFIX = '  '
    FOCUSED_PREFIX = '[ '
    FOCUSED_SUFFIX = ' ]'

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.size = (len(text) + 4, 1)

    def handle(self, event):
        if event.type == EventType.ACTION:
            if self.text == '|>':
                self.text = '||'
                return True
            if self.text == '||':
                self.text = '|>'
                return True
        return False


class MusicWindow(Window):
    def __init__(self, w=None, h=None):
        super().__init__(w, h)
        self.layout = Layout([
            Text('Music               '),
            Text('Title               '),
            Text('01:23####------03:25'),
            [Text(' '), MButton('<<'), MButton('|>'), MButton('>>'), Text('  ')]
        ], parent=self)


def main():
    ESC = '\033'
    MOVE_SEQ = [ESC, '[']
    display = BufferedRPLCDDisplay()
    w = MainMenu(20, 4)
    display.canvas.position = (0, 0)
    canvas = display.canvas.sub_canvas(20, 4)
    w.print(canvas)
    seq = []

    w_stack = [w]

    def update_display():
        w_stack[-1].print(canvas)

    while True:
        c = getch()
        seq.append(c)
        seq = seq[-3:]
        x, y = canvas.position

        if seq[-2:] == [ESC] * 2:
            break
        elif seq == MOVE_SEQ + ['A']:
            if y > 0:
                pass#canvas.position = x, y - 1
            w_stack[-1].handle(Event(EventType.UP))
            update_display()
        elif seq == MOVE_SEQ + ['B']:
            if y < canvas.size[1] - 1:
                pass#canvas.position = x, y + 1
            w_stack[-1].handle(Event(EventType.DOWN))
            update_display()
        elif seq == MOVE_SEQ + ['D']:
            if x > 0:
                pass#canvas.position = x - 1, y
            w_stack[-1].handle(Event(EventType.LEFT))
            if len(w_stack) > 1:
                w_stack.pop(-1)
            update_display()
        elif seq == MOVE_SEQ + ['C']:
            if x < canvas.size[0] - 1:
                pass#canvas.position = x + 1, y
            w_stack[-1].handle(Event(EventType.RIGHT))
            if len(w_stack) == 1:
                if calendar.focused:
                    w_stack.append(CalendarWindow(20, 4))
                elif music.focused:
                    w_stack.append(MusicWindow(20, 4))
            update_display()
        elif c in ('\r', '\n', ' '):
            w_stack[-1].handle(Event(EventType.ACTION))
            update_display()
        elif seq[-1] != ESC and seq[-2:] != MOVE_SEQ:
            w.handle(InputEvent(c))
            update_display()


def main_gamepad():
    while not gamepad_available():
        time.sleep(1)

    gamepad = PS4()

    display = BufferedRPLCDDisplay()
    w = MainMenu(20, 4)
    display.canvas.position = (0, 0)
    canvas = display.canvas.sub_canvas(20, 4)
    w.print(canvas)

    w_stack = [w]

    def update_display():
        w_stack[-1].print(canvas)

    while True:
        event_type, control, value = gamepad.getNextEvent()
        x, y = canvas.position

        if (control, value) == ('PS', True):
            break
        elif (control, value) == ('DPAD-Y', -1.0):
            if y > 0:
                pass#canvas.position = x, y - 1
            w_stack[-1].handle(Event(EventType.UP))
            update_display()
        elif (control, value) == ('DPAD-Y', 1.0):
            if y < canvas.size[1] - 1:
                pass#canvas.position = x, y + 1
            w_stack[-1].handle(Event(EventType.DOWN))
            update_display()
        elif (control, value) == ('DPAD-X', -1.0):
            if x > 0:
                pass#canvas.position = x - 1, y
            w_stack[-1].handle(Event(EventType.LEFT))
            update_display()
        elif (control, value) == ('DPAD-X', 1.0):
            if x < canvas.size[0] - 1:
                pass#canvas.position = x + 1, y
            w_stack[-1].handle(Event(EventType.RIGHT))
            update_display()
        elif (control, value) == ('CROSS', True):
            w_stack[-1].handle(Event(EventType.ACTION))
            if len(w_stack) == 1:
                if calendar.focused:
                    w_stack.append(CalendarWindow(20, 4))
                elif music.focused:
                    w_stack.append(MusicWindow(20, 4))
            update_display()
        elif (control, value) == ('CIRCLE', True):
            if len(w_stack) > 1:
                w_stack.pop(-1)
            update_display()


if __name__ == "__main__":
    main()
