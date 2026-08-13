from rv.rvtypes import *
from rv.commands import *
from rv.extra_commands import *
from PySide6.QtWidgets import QInputDialog, QLineEdit


class rvMarkerNotes(MinorMode):
    def __init__(self):
        # class inheriting from MinorMode
        MinorMode.__init__(self)
        # registration call -- tells RV that this object is a real mode
        # using letter J bc "jotting down notes" and it was a free letter
        self.init(
            "rv-marker-notes",
            [("key-down--j", self.openPopUp, "pop up appeears")],
            None,
            None,
        )

    # function calls the function that puts a marker on timeline and pop
    def openPopUp(self, event):
        current_frame = frame()
        markFrame(current_frame, True)

        text_input, ok = QInputDialog.getText(
            None, f"Marker Note frame {current_frame}", "Notes:", QLineEdit.Normal, ""
        )

        if ok and text_input:
            print(f"Note captured on frame {current_frame}: {text_input}")


def createMode():
    return rvMarkerNotes()
