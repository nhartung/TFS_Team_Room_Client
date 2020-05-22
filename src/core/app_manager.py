class App_Manager():
    """
    This base class defines the set of methods that should be defined by
    a front end. It is passed to the core back end and it used to provide 
    callbacks to the front end and for the front end to send messages to the
    back end to communicate user events.
    """

    def __init__(self):
        raise NotImplementedError

    def room_provider_callback(self, rooms):
        """
        The backend calls this function when the list of available rooms is 
        updated.

        Inputs:
        rooms - list of Room objects.
        """
        raise NotImplementedError

    def user_provider_callback(self, users):
        """
        The backend calls this function when the list of available users is
        updated.

        Inputs:
        users - list of users objects.
        """
        raise NotImplementedError

    def message_provider_callback(self, messages):
        """
        The backend calls this function when the list of chat messages is 
        updated.

        Inputs:
        messages - The list of messages to be displayed.
        """
        raise NotImplementedError

    def login_success_callback(self):
        """
        This function is called by the backend when login succeeds.
        """
        raise NotImplementedError

    def login_failure_callback(self, reason):
        """
        This function is called by the backend when login fails.

        Inputs:
        reason - A string stating the reason for the login failure.
        """
        raise NotImplementedError

    def get_selected_room(self):
        """
        The backend calls this fucntion to query the frontend for the currently
        selected room.
        """
        raise NotImplementedError

    def set_message_queue(self, queue):
        """
        The backend provides a queue to the frontend through this fucntion.
        The frontend should put messages that it wants to send to the current
        chat room into this queue.
        """
        raise NotImplementedError

    def set_login_queue(self, queue):
        """
        The backend provides a queue to the frontend through this fucntion.
        The frontend should put tuples of (username, password) that it wants
        the back end to attempt a login with.
        """
        raise NotImplementedError
