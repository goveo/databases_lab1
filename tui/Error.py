import npyscreen


class Error(npyscreen.Form):

    # def __init__(self, *args, **keywords):
    #     print('args : ', args)
    #     super().__init__(*args, **keywords)
    #     self.add_handlers({
    #         "^Q": self.back
    #     })
    #
    # def create(self):
    #     key_of_choice = 'p'
    #     what_to_display = 'Press {} for popup \n Press escape key to quit'.format(key_of_choice)
    #
    #     self.add(npyscreen.FixedText, value="Error")
    #
    # def back(self, *args, **keywords):
    #     self.parentApp.switchForm("MAIN")
    #
    def spawn_notify_popup(self, code_of_key_pressed):
        message_to_display = 'You have a choice, to Cancel and return false, or Ok and return true.'
        notify_result = npyscreen.notify_ok_cancel(message_to_display, title='popup')
        npyscreen.notify_wait('That returned: {}'.format(notify_result), title='results')

    def create(self):
        key_of_choice = 'p'
        what_to_display = 'Press {} for popup \n Press escape key to quit'.format(key_of_choice)

        self.add_handlers({key_of_choice: self.spawn_notify_popup})
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE] = self.back
        self.add(npyscreen.FixedText, value=what_to_display)



    def back(self, *args, **keywords):
        self.parentApp.switchForm("MAIN")