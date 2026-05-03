from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, 
                             QPushButton, QComboBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='#2b2b2b')
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('#2b2b2b')
        self.axes.tick_params(colors='white')
        self.axes.xaxis.label.set_color('white')
        self.axes.yaxis.label.set_color('white')
        super(MplCanvas, self).__init__(fig)

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
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
            ('Characteristic Length (L or r0)', '')
        ]
        
        for i, (label, default) in enumerate(fields, start=1):
            lbl = QLabel(label)
            edit = QLineEdit(default)
            layout.addWidget(lbl, i, 0)
            layout.addWidget(edit, i, 1)
            self.inputs[label] = edit
            
        self.run_btn = QPushButton("Calculate and Plot")
        layout.addWidget(self.run_btn, len(fields) + 2, 0, 1, 2)
        
        self.export_btn = QPushButton("Export to Excel (Time Series)")
        layout.addWidget(self.export_btn, len(fields) + 3, 0, 1, 2)
        
        # Info label for analysis
        self.info_label = QLabel("Analysis Info: N/A")
        layout.addWidget(self.info_label, len(fields) + 4, 0, 1, 2)
        
        self.setLayout(layout)