import sys
import os
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
from src.solvers.auto_solver import AutoSolver
from src.solvers.analytic import solve_one_term_cylinder, solve_one_term_slab, solve_one_term_sphere
from src.ui.widgets import ControlPanel, MplCanvas
from src.physics.slab import PlaneWall
from src.physics.cylinder import InfiniteCylinder
from src.physics.sphere import Sphere


class TransientApp(QMainWindow):
    def __init__(self):
        super().__init__() 
        
        self.setWindowTitle("Transient Heat Conduction - Tanta University")
        self.setMinimumSize(1100, 650)
        
        self.controls = ControlPanel()
        self.canvas = MplCanvas()
        
        main_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.controls, 1)
        layout.addWidget(self.canvas, 3)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        
        self.controls.run_btn.clicked.connect(self.update_plot)
        self.controls.export_btn.clicked.connect(self.export_to_excel)
        # Plot only updates when button is clicked, NOT on input changes
        
        try:
            with open("src/ui/styles.qss", "r") as f:
                self.setStyleSheet(f.read())
        except:
            pass

    def update_plot(self):
        try:
            d = {k: float(v.text()) for k, v in self.controls.inputs.items()}
            L_char = d['Characteristic Length (L or r0)']
            time_sec = d['Time (sec)']
            geo_type = self.controls.geo_combo.currentText()

            # Create the heat transfer object
            if geo_type == "Plane Wall":
                geometry_key = 'slab'
                body = PlaneWall(d['Thermal Cond (k)'], d['Density (rho)'], 
                                d['Specific Heat (cp)'], d['Conv Coeff (h)'], 
                                d['Initial Temp (Ti)'], d['Ambient Temp (T_inf)'], 
                                L=L_char)

            elif geo_type == "Infinite Cylinder":
                geometry_key = 'cylinder'
                body = InfiniteCylinder(d['Thermal Cond (k)'], d['Density (rho)'], 
                                    d['Specific Heat (cp)'], d['Conv Coeff (h)'], 
                                    d['Initial Temp (Ti)'], d['Ambient Temp (T_inf)'], 
                                    r0=L_char)

            elif geo_type == "Sphere":
                geometry_key = 'sphere'
                body = Sphere(d['Thermal Cond (k)'], d['Density (rho)'], 
                            d['Specific Heat (cp)'], d['Conv Coeff (h)'], 
                            d['Initial Temp (Ti)'], d['Ambient Temp (T_inf)'], 
                            r0=L_char)

            else:
                raise ValueError("Unknown geometry type")

            # Analysis
            analysis = AutoSolver.get_analysis_info(body,time_sec)

            # Time array
            time_vals = np.linspace(0, time_sec, 200)
            center_pos = 0

            temps = [
                AutoSolver.solve(body, center_pos, t, geometry_key)
                for t in time_vals
            ]

            # Plot
            self.canvas.axes.clear()
            self.canvas.axes.set_facecolor('#2b2b2b')
            self.canvas.axes.grid(True, linestyle='--', alpha=0.3)

            self.canvas.axes.plot(
                time_vals, temps,
                color='#00ff00', marker='o',
                linewidth=2, markersize=3,
                label=f"Position = {center_pos:.4f} m"
            )

            self.canvas.axes.set_title(f"Temperature vs Time: {geo_type}", color='white')
            self.canvas.axes.set_xlabel("Time [s]", color='white')
            self.canvas.axes.set_ylabel("Temperature [°C]", color='white')
            self.canvas.axes.tick_params(colors='white')
            self.canvas.axes.legend()
            self.canvas.draw()

            T_end = AutoSolver.solve(body, 0.0, time_sec, geometry_key)

            # Info
            info_text = (
                f"Bi={analysis['biot']:.4f} ({analysis['system_type']}) | "
                f"Fo={analysis['fourier']:.4f} | "
                f"T(t={time_sec:.0f}s) = {T_end:.1f} °C"
            )
            self.controls.info_label.setText(info_text)

            # Save results
            self.last_results = {
                'time_vals': time_vals,
                'center_pos': center_pos,
                'time_sec': time_sec,
                'body': body,
                'geometry_key': geometry_key,
                'analysis': analysis
            }

        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    def export_to_excel(self):
        """Export temperature data at specified time with 0.001m position intervals"""
        if not hasattr(self, 'last_results'):
            QMessageBox.warning(self, "Warning", "Please run a calculation first.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "", "Excel Files (*.xlsx)"
        )
        
        if file_path:
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'
            
            try:
                results = self.last_results
                body = results['body']
                geometry_key = results['geometry_key']
                final_time = results['time_sec']
                
                # Generate positions with 0.001m intervals from 0 to full characteristic length
                if geometry_key == "Plane Wall":
                    # For plane wall, show positions from 0 to total thickness (2*Lc)
                    total_length = 2 * body.Lc
                else:
                    # For cylinder and sphere, show from 0 to Lc
                    total_length = body.Lc
                
                num_positions = int(total_length / 0.001) + 1
                positions = np.linspace(0, total_length, num_positions)
                
                # Calculate temperatures only at the final time (not full time-series)
                data = []
                for pos in positions:
                    temp = AutoSolver.solve(body, pos, final_time, geometry_key)
                    data.append({
                        'Time (s)': final_time,  # Add time column as requested
                        'Position (m)': round(pos, 6),
                        'Temperature (°C)': round(temp, 4)
                    })
                
                df_data = pd.DataFrame(data)
                
                # Create metadata sheet
                analysis = AutoSolver.get_analysis_info(body, final_time)
                metadata = {
                    'Parameter': [
                        'Geometry', 
                        'Time (s)',
                        'Initial Temp (°C)', 
                        'Ambient Temp (°C)',
                        'Thermal Conductivity (W/m·K)',
                        'Density (kg/m³)',
                        'Specific Heat (J/kg·K)',
                        'Convection Coeff (W/m²·K)',
                        'Characteristic Length (m)',
                        'Thermal Diffusivity (m²/s)',
                        'Biot Number',
                        'Fourier Number',
                        'System Type',
                        'Solving Method',
                        'Time Constant (s)'
                    ],
                    'Value': [
                        geometry_key,
                        final_time,
                        body.Ti,
                        body.T_inf,
                        body.k,
                        body.rho,
                        body.cp,
                        body.h,
                        body.Lc,
                        body.alpha,
                        f"{analysis['biot']:.6f}",
                        f"{analysis['fourier']:.6f}",
                        analysis['system_type'],
                        analysis['method'].upper(),
                        f"{analysis['time_constant']:.2f}"
                    ]
                }
                df_metadata = pd.DataFrame(metadata)
                
                # Write to Excel with multiple sheets
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df_data.to_excel(writer, sheet_name='Temperature Data', index=False)
                    df_metadata.to_excel(writer, sheet_name='Metadata', index=False)
                
                QMessageBox.information(self, "Success", 
                    f"Data exported successfully!\n\n"
                    f"File: {file_path}\n"
                    f"Positions: {len(positions)} (0.001m intervals, 0 to {body.Lc:.3f}m)\n"
                    f"Time: {final_time}s\n"
                    f"Total rows: {len(data)}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransientApp()
    window.show()
    sys.exit(app.exec_())