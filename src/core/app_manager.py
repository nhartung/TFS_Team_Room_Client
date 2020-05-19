class App_Manager():
    """
    This base class defines the set of methods that should be defined by
    a front end. It is passed to the core back end and it used to provide 
    callbacks to the front end and for the front end to send messages to the
    back end to communicate user events.
    """

    def __init__(self):
        raise NotImplementedError

    def rooms_callback(self, rooms):
        """
        This function is called when the list of available rooms is updated.

        Inputs:
        rooms - list of Room objects.
        """
        raise NotImplementedError

    def users_callback(self, users):
        """
        This function is called when the list of users is updated.

        Inputs:
        users - list of users objects.
        """
        raise NotImplementedError

    def get_room_function(self):
        """
        This function should return the room id.
        """
        raise NotImplementedError

    def messages_callback(self, messages):
        """
        This function is called when the list of messages is updated.

        Inputs:
        messages - The list of messages to be displayed.
        """
        raise NotImplementedError

    def login_success_callback(self):
        """
        This function is called by the back end when login succeeds.
        """
        raise NotImplementedError

    def login_failure_callback(self, reason):
        """
        This function is called by the back end when login fails.

        Inputs:
        reason - A string stating the reason for the login failure.
        """
        raise NotImplementedError

    def set_message_queue(self, queue):
        """
        The back end provides a queue to the front end through this fucntion.
        The front end should put messages that it wants to send to the current
        chat room into this queue.
        """
        raise NotImplementedError

    def set_login_queue(self, queue):
        """
        The back end provides a queue to the front end through this fucntion.
        The front end should put tuples of (username, password) that it wants
        the back end to attempt a login with.
        """
        raise NotImplementedError
