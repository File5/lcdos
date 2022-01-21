from lcdui.views.lineinput import LineInput
from lcdui.display import BufferedRPLCDDisplay, Cursor
from lcdui.event import Event, EventType, InputEvent
from lcdui.views import Window, Button, CheckBox, Radio, Text, LineInput, ListItem
from lcdui.views.pagescroll import PageScrollLayout
from lcdui.utils import getch


class MainWindow(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = PageScrollLayout([
            [
                ListItem('Page 1', 19),
                [Text('Label:'), LineInput(13)],
                [Button('Button'), Text(' '), Radio('Radio')],
                CheckBox('CheckBox'),
            ],
            [
                ListItem('Page 2', 19),
                [Text('Label:'), LineInput(13)],
                [Button('Button'), Text(' '), Radio('Radio')],
                CheckBox('CheckBox'),
            ],
        ], parent=self)


def main():
    ESC = '\033'
    MOVE_SEQ = [ESC, '[']
    display = BufferedRPLCDDisplay()
    w = MainWindow(20, 4)
    display.canvas.position = (0, 0)
    canvas = display.canvas.sub_canvas(20, 4)
    w.print(canvas)
    seq = []

    def update_display():
        w.print(canvas)

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
            w.handle(Event(EventType.UP))
            update_display()
        elif seq == MOVE_SEQ + ['B']:
            if y < canvas.size[1] - 1:
                pass#canvas.position = x, y + 1
            w.handle(Event(EventType.DOWN))
            update_display()
        elif seq == MOVE_SEQ + ['D']:
            if x > 0:
                pass#canvas.position = x - 1, y
            w.handle(Event(EventType.LEFT))
            update_display()
        elif seq == MOVE_SEQ + ['C']:
            if x < canvas.size[0] - 1:
                pass#canvas.position = x + 1, y
            w.handle(Event(EventType.RIGHT))
            update_display()
        elif c in ('\r', '\n', ' '):
            w.handle(Event(EventType.ACTION))
            update_display()
        elif seq[-1] != ESC and seq[-2:] != MOVE_SEQ:
            w.handle(InputEvent(c))
            update_display()


if __name__ == "__main__":
    main()
