# source: http://code.activestate.com/recipes/464635-call-a-callback-when-a-tkintertext-is-modified/
# this script has be modified to be compatible with Python 3.


class ModifiedMixin:
    """
    Class to allow a Tkinter Text widget to notice when it's modified.

    To use this mixin, subclass from Tkinter.Text and the mixin, then write
    an __init__() method for the new class that calls _init().

    Then override the beenModified() method to implement the behavior that
    you want to happen when the Text is modified.
    """

    def _init(self):
        """
        Prepare the Text for modification notification.
        """

        # Clear the modified flag, as a side effect this also gives the
        # instance a _resetting_modified_flag attribute.
        self.clear_modified_flag()

        # Bind the <<Modified>> virtual event to the internal callback.
        self.bind_all('<<Modified>>', self._been_modified)

    def _been_modified(self, event=None):
        """
        Call the user callback. Clear the Tk 'modified' variable of the Text.
        """

        # If this is being called recursively as a result of the call to
        # clearModifiedFlag() immediately below, then we do nothing.
        if self._resetting_modified_flag: return

        # Clear the Tk 'modified' variable.
        self.clear_modified_flag()

        # Call the user-defined callback.
        self.been_modified(event)

    def been_modified(self, event=None):
        """
        Override this method in your class to do what you want when the Text
        is modified.
        """
        pass

    def clear_modified_flag(self):
        """
        Clear the Tk 'modified' variable of the Text.

        Uses the _resetting_modified_flag attribute as a sentinel against
        triggering _beenModified() recursively when setting 'modified' to 0.
        """

        # Set the sentinel.
        self._resetting_modified_flag = True

        try:

            # Set 'modified' to 0.  This will also trigger the <<Modified>>
            # virtual event which is why we need the sentinel.
            self.tk.call(self._w, 'edit', 'modified', 0)

        finally:
            # Clean the sentinel.
            self._resetting_modified_flag = False


if __name__ == '__main__':
    from tkinter import Text, BOTH


    class T(ModifiedMixin, Text):
        """
        Subclass both ModifiedMixin and Tkinter.Text.
        """

        def __init__(self, *a, **b):
            # Create self as a Text.
            Text.__init__(self, *a, **b)

            # Initialize the ModifiedMixin.
            self._init()

        def been_modified(self, event=None):
            """
            Override this method do do work when the Text is modified.
            """
            print('Hi there.')


    t = T()
    t.pack(expand=1, fill=BOTH)
    t.mainloop()
