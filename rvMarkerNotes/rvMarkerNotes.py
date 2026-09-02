from rv.rvtypes import *
from rv.commands import *
from rv.extra_commands import *
from PySide6.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QDialog,
    QCheckBox,
    QLabel,
    QPushButton,
    QHBoxLayout,
)


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
        checkbox_state = False
        if propertyExists(property_info):
            stored_values = getStringProperty(property_info)
            checkbox_state = stored_values[1] == "True"
            existing_text = stored_values[2]

        # change pop up to custom pop up:
        # pop up title
        dialog_box = QDialog(None)
        dialog_box.setWindowTitle(f"frame: {current_frame}")
        # pop up body
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Notes: "))
        # text box
        text_box = QLineEdit()
        text_box.setText(existing_text)
        layout.addWidget(text_box)  # adding text box to the pop up body
        # checkbox
        checkbox = QCheckBox("Resolved")
        checkbox.setChecked(checkbox_state)
        layout.addWidget(checkbox)
        # buttons
        cancel_button = QPushButton("Cancel")  # creating layout
        ok_button = QPushButton("OK")
        button_row = QHBoxLayout()
        button_row.addWidget(cancel_button)
        button_row.addWidget(ok_button)
        cancel_button.clicked.connect(dialog_box.reject)  # adding connection
        ok_button.clicked.connect(dialog_box.accept)
        layout.addLayout(button_row)  # adding buttons to popup
        # size of pop up
        dialog_box.setLayout(layout)
        dialog_box.resize(400, 150)  # length, height

        ok = dialog_box.exec()
        text_input = text_box.text()
        checkbox_state = checkbox.isChecked()

        if ok == QDialog.Accepted and text_input:
            # mark the timeline on frame current_frame
            markFrame(current_frame, True)
            print(f"Note captured on frame {current_frame}: {text_input}")

            # if property does not exist yet, create
            if not propertyExists(property_info):
                newProperty(property_info, StringType, 3)

            # set the property
            setStringProperty(
                property_info,
                [str(current_frame), str(checkbox_state), text_input],
                True,
            )

            # read back value in the terminal
            print(getStringProperty(property_info))

        print(f"session file name: {sessionFileName()}")
        saveSession(sessionFileName())


def createMode():
    return rvMarkerNotes()
