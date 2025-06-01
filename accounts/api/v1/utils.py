import threading


class EmailThread(threading.Thread):
    """
        A thread class to send emails asynchronously.

        This class takes an email object (with a send_email method)
        and sends the email in a separate thread to avoid blocking the main process.
        """
    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send_email()
