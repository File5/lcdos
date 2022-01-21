from lcdui.views import Text


def paged_layout(layout, h=4):
    new_layout = []
    next_page = []
    for row in layout:
        next_page.append(row)
        if len(next_page) >= h:
            new_layout.append(next_page)
            next_page = []
    if len(next_page) > 0:
        new_layout.append(next_page)
    return new_layout
