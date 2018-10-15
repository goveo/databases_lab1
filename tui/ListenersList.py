import npyscreen
import sys


class ListenersList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(ListenersList, self).__init__(*args, **keywords)
        self.name = "Musicians"
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return "%s \t| %s \t| %s" % (vl['id'], vl['name'], vl['services'])

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('LISTENEREDIT').value = act_on_this["id"]
        self.parent.parentApp.switchForm('LISTENEREDIT')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('LISTENEREDIT').value = None
        self.parent.parentApp.switchForm('LISTENEREDIT')

    def when_delete_record(self, *args, **keywords):
        try:
            cur_id = self.values[self.cursor_line]["id"]
            self.parent.parentApp.database.delete_listener_by_id(cur_id)
        except Exception as e:
            self.parent.wMain.values = []
            self.parent.wMain.display()
        self.parent.update_list()


class ListenersListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = ListenersList

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        to_display = self.parentApp.database.get_all_listeners()
        self.wMain.values = to_display
        if len(to_display) == 0:
            self.parentApp.switchForm("MAIN")
        self.wMain.display()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
