from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QPushButton, QComboBox, QScrollArea)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure(figsize=(7, 5), dpi=100, facecolor='#2b2b2b')
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('#2b2b2b')
        self.axes.tick_params(colors='white')
        self.axes.xaxis.label.set_color('white')
        self.axes.yaxis.label.set_color('white')
        super(MplCanvas, self).__init__(fig)

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        
        # Create scrollable area for inputs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QGridLayout()
        
        # Geometry Type
        layout.addWidget(QLabel("Geometry Type:"), 0, 0)
        self.geo_combo = QComboBox()
        self.geo_combo.addItems(["Plane Wall", "Infinite Cylinder", "Sphere"])
        layout.addWidget(self.geo_combo, 0, 1)

        self.inputs = {}
        # Input fields
        fields = [
            ('Thermal Cond (k)', ''),
            ('Density (rho)', ''),
            ('Specific Heat (cp)', ''),
            ('Conv Coeff (h)', ''),
            ('Initial Temp (Ti)', ''),
            ('Ambient Temp (T_inf)', ''),
            ('Time (sec)', ''),
            ('Length (L or r0)', ''),
            ('Volume (V) [Optional]', ''),
            ('Surface Area (A) [Optional]', '')
        ]
        
        for i, (label, default) in enumerate(fields, start=1):
            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 11px;")
            edit = QLineEdit(default)
            edit.setMinimumHeight(28)
            layout.addWidget(lbl, i, 0)
            layout.addWidget(edit, i, 1)
            self.inputs[label] = edit
        
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)
        
        main_layout.addWidget(scroll_area)
        
        # Buttons
        button_layout = QGridLayout()
        button_layout.setSpacing(8)
        
        self.run_btn = QPushButton("Calculate and Plot")
        self.run_btn.setMinimumHeight(36)
        self.run_btn.setStyleSheet("font-size: 11px; font-weight: bold;")
        button_layout.addWidget(self.run_btn, 0, 0, 1, 2)
        
        self.export_btn = QPushButton("Export to Excel (Time Series)")
        self.export_btn.setMinimumHeight(36)
        self.export_btn.setStyleSheet("font-size: 11px; font-weight: bold;")
        button_layout.addWidget(self.export_btn, 1, 0, 1, 2)
        
        # Info label for analysis
        self.info_label = QLabel("Analysis Info: N/A")
        self.info_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ff00;")
        self.info_label.setWordWrap(True)
        button_layout.addWidget(self.info_label, 2, 0, 1, 2)
        
        button_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)