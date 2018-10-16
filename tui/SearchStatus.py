import npyscreen
from models.musician import Musician, Status


class SearchStatus(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgStatus = self.add(npyscreen.TitleSelectOne,
                                 name="Status:",
                                 values=Status.get_all(),
                                 max_height=5,
                                 value=None)
        self.wgResult = self.add(npyscreen.TitleMultiLine,
                                 name="Result:",
                                 values=[],
                                 max_height=4)
        self.add_handlers({
            "^Q": self.exit
        })

    def beforeEditing(self):
        self.name = "Search status"

    def on_ok(self):
        if len(self.wgStatus.value) == 0:
            ...
        else:
            status = self.wgStatus.values[self.wgStatus.value[0]]
            self.wgResult.values = self.parentApp.database.search_status(status)
        #
        # if self.wgRelease.value:
        #
        #     self.parentApp.switchFormPrevious()
        # else:
        #     # TODO make popup
        #     self.is_error = True


    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()