from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import json
directory = 'notes.json'

notes = {}


if os.path.exists(directory):
    with open(directory, 'r', encoding='utf-8')as file:
        notes = json.load(file)
else:
    notes = {
        'Welcome': {'text': 'Добро пожаловать!!!', 'tags': ['Приветствие']}
    }

    with open(directory, 'w', encoding='utf-8')as file:
        json.dump(notes, file, indent=4)

def show_notes():
    filenames = list(notes.keys())
    list_notes.clear()
    list_notes.addItems(filenames)

def choose_file():
    filename = list_notes.selectedItems()[0].text()
    text = notes[filename]['text']
    text_edit.setText(text)

    tags = get_tags(filename)
    list_tags.clear()
    list_tags.addItems(tags)


def get_tags(filename):
    return notes[filename]['tags']






def add_note():
    name, ok = QInputDialog.getText(window, 'Добавить заметку', 'Название заметки')
    if ok and name != '':
        notes[name] = {'text':'', 'tags':[]}
        show_notes()
        with open(directory, 'w', encoding='utf-8') as file:
            json.dump(notes, file, indent=4)

def delet_note():
    filename = list_notes.selectedItems()[0].text()
    del notes[filename]
    show_notes()
    with open(directory, 'w', encoding='utf-8')as file:
        json.dump(notes, file, indent=4)


def save():
    text = text_edit.toPlainText()
    filename = list_notes.selectedItems()[0].text()
    notes[filename]['text'] =text
    with open(directory, 'w', encoding='utf-8') as file:
        json.dump(notes, file, indent=4)

def add_tag():
    if line_edit.text() == '':
        return
    filename = list_notes.selectedItems()[0].text()
    notes[filename]['tags'].append(line_edit.text())
    with open(directory, 'w', encoding='utf-8') as file:
        json.dump(notes, file, indent=4)
    choose_file()
    list_tags.clear()
    list_tags.addItems(get_tags(filename))
app = QApplication([])
window = QWidget()

def remove_tag():
    filename = list_notes.selectedItems()[0].text()

    tag = list_tags.selectedItems()[0].text()
    if tag in notes[filename]['tags']:
        notes[filename]['tags'].remove(tag)
    with open(directory, 'w', encoding='utf-8') as file:
        json.dump(notes, file, indent=4)

    list_tags.clear()
    list_tags.addItems(get_tags(filename))

def search():

    if search_tag.text() == 'Искать по тегу':

        tag = line_edit.text()
        filtred = []

        for file in list(notes.keys()):
            tags = get_tags(file)
            if tag in tags:
                filtred.append(file)
        list_notes.clear()
        list_notes.addItems(filtred)
        search_tag.setText('Сбросить поиск')
    else:
        show_notes()
        search_tag.setText('Искать по тегу')

#виджеты
text_edit = QTextEdit()
l_notes = QLabel('список заметок')
list_notes  = QListWidget()
creat_note = QPushButton('Создать заметку')
delete_note  = QPushButton('Удалить заметку')
save_note = QPushButton('Сохранить заметку')
l_tags = QLabel('Список тегов')
list_tags  = QListWidget()
line_edit = QLineEdit()
line_edit.setPlaceholderText('Введите тег...')
creat_tag = QPushButton('Добавить тег')
delete_tag  = QPushButton('Удалить тег')
search_tag = QPushButton('Искать по тегу')

#лэйаут
main_box = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

btn_row1 = QHBoxLayout()
btn_row2 = QHBoxLayout()

col1.addWidget(text_edit)
col2.addWidget(l_notes)
col2.addWidget(list_notes)
btn_row1.addWidget(creat_note)
btn_row1.addWidget(delete_note)
col2.addLayout(btn_row1)
col2.addWidget(save_note)

col2.addWidget(l_tags)
col2.addWidget(list_tags)
col2.addWidget(line_edit)
btn_row2.addWidget(creat_tag)
btn_row2.addWidget(delete_tag)
col2.addLayout(btn_row2)
col2.addWidget(search_tag)

main_box.addLayout(col1)
main_box.addLayout(col2)

window.setLayout(main_box)

list_notes.itemClicked.connect(choose_file)
creat_note.clicked.connect(add_note)
delete_note.clicked.connect(delet_note)
save_note.clicked.connect(save)
creat_tag.clicked.connect(add_tag)
delete_tag.clicked.connect(remove_tag)
search_tag.clicked.connect(search)

show_notes()
window.show()

app.exec_()
