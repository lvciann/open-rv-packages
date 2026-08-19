from rv.rvtypes import *
from rv.commands import *
from rv.extra_commands import *
from PySide6.QtWidgets import QInputDialog, QLineEdit, QDialog


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

        # get the session node
        session_node = nodesOfType("RVSession")[0]

        # take the frame and note information
        property_info = f"{session_node}.rvMarkerNotes.frame_{current_frame}"

        # frame had text in it previously, make it show up
        existing_text = ""
        if propertyExists(property_info):
            existing_text = getStringProperty(property_info)[1]

        # popup set up
        dialog_box = QInputDialog(None)
        dialog_box.setWindowTitle(f"Marker Note frame {current_frame}")
        dialog_box.setLabelText("Notes:")
        dialog_box.setTextEchoMode(QLineEdit.Normal)
        dialog_box.setTextValue(
            existing_text
        )  # text box shows existing text, will be empty if it does not have
        dialog_box.resize(400, 300)  # length, height

        ok = dialog_box.exec()
        text_input = dialog_box.textValue()

        if ok == QDialog.Accepted and text_input:
            # mark the timeline on frame current_frame
            markFrame(current_frame, True)
            print(f"Note captured on frame {current_frame}: {text_input}")

            # if property does not exist yet, create
            if not propertyExists(property_info):
                newProperty(property_info, StringType, 2)

            # set the property
            setStringProperty(property_info, [str(current_frame), text_input], True)

            # read back value in the terminal
            print(getStringProperty(property_info))

        print(f"session file name: {sessionFileName()}")
        saveSession(sessionFileName())


def createMode():
    return rvMarkerNotes()
