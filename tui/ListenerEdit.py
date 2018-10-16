import npyscreen
from models.listener import Listener


class ListenerEdit(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgName = self.add(npyscreen.TitleText, name="Name:")
        self.wgServices = self.add(npyscreen.TitleText, name="Services:")
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        if self.value:
            listener = self.parentApp.database.get_listener_by_id(self.value)
            self.name = "Edit"
            self.record_id = listener["id"]
            self.wgName.value = listener["name"]
            self.wgServices.value = ','.join(map(str, listener["services"]))
            # f = open("log.txt", "w")
            # f.write(f'record : {record}')
        else:
            self.name = "New Listener"
            self.record_id = ''
            self.wgName.value = ''
            self.wgServices.value = ''

    def on_ok(self):
        listener = Listener(self.wgName.value, self.wgServices.value.split(','))
        if self.record_id: # We are editing an existing record
            self.parentApp.database.update_listener_by_id(self.record_id, listener)
        else: # We are adding a new record.
            self.parentApp.database.create_new_listener(listener)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()