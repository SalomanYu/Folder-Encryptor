import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ecnry_decry import *
import sys

# Сохранение вывода консоли в файл, для выявления причин ошибок
sys.stdout = open('output.log', 'w')
sys.stderr = open('output.log', 'a')


# Функция выхода из программы
def close_app(widget):
    Gtk.main_quit()


# создание менеджера файлов для выбора директории
def select_folder(widget):
    dialog = Gtk.FileChooserDialog(
        title='Пожалуйста, выберите папку',
        parent=window, 
        action=Gtk.FileChooserAction.SELECT_FOLDER
    )
    dialog.add_button('Отмена', Gtk.ResponseType.CANCEL)
    dialog.add_button('Выбрать', Gtk.ResponseType.OK)
    dialog.set_default_size(200,100)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        path = dialog.get_filename()
        path_entry.set_text(path)
    dialog.close()


# создание окна для ввода пароля
def show_password_window(widget, title, message):
    dialogWindow = Gtk.MessageDialog(
        window,
        Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
        Gtk.MessageType.QUESTION,
        Gtk.ButtonsType.OK_CANCEL,
        message)

    dialogWindow.set_title(title)
    dialogBox = dialogWindow.get_content_area()
    userEntry = Gtk.Entry()
    userEntry.set_visibility(False)
    userEntry.set_invisible_char("*")
    dialogBox.pack_start(userEntry, False, False, 0)

    unvisible = Gtk.RadioButton.new_with_label_from_widget(None, label='Скрыть пароль')
    visible = Gtk.RadioButton.new_with_label_from_widget(unvisible, label='Показать пароль')    
    unvisible.connect('toggled', lambda x: userEntry.set_visibility(False))
    visible.connect('toggled', lambda x: userEntry.set_visibility(True))
    dialogBox.pack_end(unvisible, False, False, 0)
    dialogBox.pack_end(visible, False, False, 0)

    dialogWindow.show_all()
    response = dialogWindow.run()
    password = userEntry.get_text() 
    dialogWindow.destroy()

    if (response == Gtk.ResponseType.OK) and (password != ''):
        return password
    else:
        return None


# Уведомление о сбое программы
def error_message(widget, message):
    errorDialog = Gtk.MessageDialog(window,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK,
            message
        )
    errorDialog.set_title('Произошла ошибка')
    response = errorDialog.run()
    errorDialog.destroy()


# Уведомление о успешном выполнении задачи
def success_message(widget, message):
    successDialog = Gtk.MessageDialog(window,
        Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
        Gtk.MessageType.INFO,
        Gtk.ButtonsType.OK,
        message
    )
    successDialog.set_title('Операция завершилась успешно')
    successDialog.run()
    successDialog.destroy()


# Шифрование файлов
def encry_clicked(widget):
    if path_entry.get_text() == '':
        error_message(widget, message='Убедитесь, что директория существует')
    else:
        # if widget.get_active():
            # if encry_radio.get_active():
        password = show_password_window(widget, 'Создание пароля','Придумай и запомни пароль')
        if password != None:
            path = path_entry.get_text()

            encrypt_dirs(path, password)
            success_message(widget, message='Файлы успешно зашифрованы')

        # if decry_radio.get_active():


# Дешифрование файлов
def decry_clicked(widget):
    if path_entry.get_text() == '':
        error_message(widget, message='Убедитесь, что директория существует')
    else:
        password = show_password_window(widget, 'Расшифровка файлов', 'Введите пароль')
        if password != None:
            path = path_entry.get_text()

            if str(decrypt_dirs(path, password)) == 'Wrong password (or file is corrupted).':
                error_message(widget, message='Неправильный пароль')
            elif str(decrypt_dirs(path, password)) == 'Input and output files are the same.':
                error_message(widget, message='Ошибка! Зашифрованные файлы не были найдены')
            else:
                print(f'{decrypt_dirs(path, password)}')
                success_message(widget, message='Файлы успешно расшифрованы')
                

# Создание пользовательского интерфейса 
window = Gtk.Window()
window.set_default_geometry(400, 120)
window.set_title('Encryption & Decryption Files')
vi_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
welcome_label = Gtk.Label(label='Mamka ne spalit')
h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
path_entry = Gtk.Entry()
path_btn = Gtk.Button(label='Выбрать папку')

h2_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
encry_btn = Gtk.Button(label='Зашифровать')
decry_btn = Gtk.Button(label='Расшифровать')
close_btn = Gtk.Button(label='Закончить работу')

path_btn.connect('clicked', select_folder)
close_btn.connect('clicked', close_app)
encry_btn.connect('clicked', encry_clicked)
decry_btn.connect('clicked', decry_clicked)


vi_box.pack_start(welcome_label, expand=False, fill=True, padding=5)
vi_box.pack_start(h_box, expand=False, fill=True, padding=5)
h_box.pack_start(path_entry, expand=True, fill=True, padding=0)
h_box.pack_start(path_btn, expand=False, fill=True, padding=0)
vi_box.pack_start(h2_box, expand=False, fill=True, padding=5)
h2_box.pack_start(encry_btn, expand=True, fill=True, padding=0)
h2_box.pack_start(decry_btn, expand=True, fill=True, padding=0)
vi_box.pack_start(close_btn, expand=False, fill=False, padding=0)


window.add(vi_box)
window.show_all()
window.connect('destroy', Gtk.main_quit)
Gtk.main()