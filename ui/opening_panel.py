from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QRadioButton,
    QPushButton,
)

from PySide6.QtCore import Signal


class OpeningPanel(QWidget):

    training_started = Signal(
        str,
        str,
        str
    )


    def __init__(
        self,
        opening_manager,
        parent=None
    ):

        super().__init__(parent)

        self.opening_manager = opening_manager


        layout = QVBoxLayout(self)


        title = QLabel(
            "Opening Trainer"
        )

        layout.addWidget(title)


        #
        # Opening selection
        #

        layout.addWidget(
            QLabel("Opening:")
        )


        self.opening_combo = QComboBox()


        self.opening_combo.addItems(
            self.opening_manager.get_openings()
        )


        self.opening_combo.currentTextChanged.connect(
            self.update_variations
        )


        layout.addWidget(
            self.opening_combo
        )


        #
        # Variation selection
        #

        layout.addWidget(
            QLabel("Variation:")
        )


        self.variation_combo = QComboBox()


        layout.addWidget(
            self.variation_combo
        )


        self.update_variations(
            self.opening_combo.currentText()
        )


        #
        # Side selection
        #

        layout.addWidget(
            QLabel("Play As:")
        )


        self.white_radio = QRadioButton(
            "White"
        )

        self.black_radio = QRadioButton(
            "Black"
        )


        self.white_radio.setChecked(
            True
        )


        layout.addWidget(
            self.white_radio
        )

        layout.addWidget(
            self.black_radio
        )


        #
        # Start button
        #

        self.start_button = QPushButton(
            "Start Training"
        )


        self.start_button.clicked.connect(
            self.start_training
        )


        layout.addWidget(
            self.start_button
        )


        layout.addStretch()



    def update_variations(
        self,
        opening_name
    ):

        self.variation_combo.clear()


        variations = self.opening_manager.get_variations(
            opening_name
        )


        self.variation_combo.addItems(
            variations
        )



    def start_training(self):

        opening = (
            self.opening_combo.currentText()
        )


        variation = (
            self.variation_combo.currentText()
        )


        color = (
            "White"
            if self.white_radio.isChecked()
            else "Black"
        )


        self.training_started.emit(
            opening,
            variation,
            color
        )