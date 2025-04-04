import backend as be
import FreeSimpleGUI as FSG
import time
import os

if not os.path.exists(be.TODO_FILE):
    with open(be.TODO_FILE, "w") as file:
        pass

FSG.theme("Black")

clock = FSG.Text('', key="clock")

label = FSG.Text("Type in a todo")
input_box = FSG.InputText(tooltip="Enter todo", key="todo")
add_button = FSG.Button("Add")
list_box = FSG.Listbox(values=be.get_todos(), key="todos",
                       enable_events=True, size=(45, 10))
edit_button = FSG.Button("Edit")
done_button = FSG.Button("Done")
exit_button = FSG.Button("Exit")


window = FSG.Window("ToDo List",
                    layout=[
                        [clock],
                        [label],
                        [input_box, add_button],
                        [list_box, edit_button, done_button],
                        [exit_button]],
                    font=("Helvetica",20))

while True:
    event, values = window.read(timeout=200)
    window["clock"].update(value=time.strftime("%b %d, %Y %H:%M:%S"))
    match event:
        case "Add":
            new_todo = values["todo"]
            todos = be.add_todo(new_todo)
            window['todos'].update(values=todos)
            window['todo'].update("")

        case "Edit":
            try:
                todo_to_edit = values['todos'][0]
                new_todo = values["todo"]
                todos = be.get_todos()
                index = todos.index(todo_to_edit)
                todos = be.update_todo(index,new_todo)
                window['todos'].update(values=todos)
            except IndexError:
                FSG.popup("Please select an item first.", font=("helvetica", 20))

        case "Done":
            try:
                todo_to_complete = values['todos'][0]
                todos = be.get_todos()
                index = todos.index(todo_to_complete)
                todos = be.drop_todo(index)
                window['todos'].update(values=todos)
                window['todo'].update(value='')
            except IndexError:
                FSG.popup("Please select an item first.", font=("Helvetica", 20))

        case "todos":
            # NOTE: The \n has to be stripped for the edit logic to work.
            #       Otherwise, extra \n get added unexpectedly and new blank
            #       lines get created. This is a dependency on the underlying
            #       data structure, which should not exist. Just leaving
            #       it alone for now 3/31/2025 mikebstudy.
            window['todo'].update(value=values["todos"][0].strip('\n'))

        case "Exit":
            print("Window closed")
            break

        case FSG.WIN_CLOSED:
            print("WINDOW closed")
            break

window.close()

