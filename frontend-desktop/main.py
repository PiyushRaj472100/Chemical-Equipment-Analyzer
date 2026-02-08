import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QLabel, 
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QGroupBox, QGridLayout, QSplitter, QDialog,
                             QLineEdit, QFormLayout, QTabWidget, QHeaderView)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class AuthDialog(QDialog):
    def __init__(self, api_base_url, session, parent=None):
        super().__init__(parent)
        self.api_base_url = api_base_url
        self.session = session
        self.access_token = None
        self.username = None

        self.setWindowTitle('Authentication')
        self.setModal(True)
        self.setFixedSize(420, 320)

        root_layout = QVBoxLayout(self)
        tabs = QTabWidget()

        login_widget = QWidget()
        login_layout = QFormLayout(login_widget)
        self.login_email = QLineEdit()
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.do_login)
        login_layout.addRow('Email', self.login_email)
        login_layout.addRow('Password', self.login_password)
        login_layout.addRow(self.login_btn)

        register_widget = QWidget()
        register_layout = QFormLayout(register_widget)
        self.reg_username = QLineEdit()
        self.reg_email = QLineEdit()
        self.reg_password = QLineEdit()
        self.reg_password.setEchoMode(QLineEdit.Password)
        self.reg_btn = QPushButton('Register')
        self.reg_btn.clicked.connect(self.do_register)
        register_layout.addRow('Username', self.reg_username)
        register_layout.addRow('Email', self.reg_email)
        register_layout.addRow('Password', self.reg_password)
        register_layout.addRow(self.reg_btn)

        tabs.addTab(login_widget, 'Login')
        tabs.addTab(register_widget, 'Register')

        root_layout.addWidget(tabs)

    def do_login(self):
        email = self.login_email.text().strip()
        password = self.login_password.text()
        if not email or not password:
            QMessageBox.warning(self, 'Error', 'Email and password are required')
            return

        try:
            resp = self.session.post(
                f'{self.api_base_url}/login/',
                json={'email': email, 'password': password},
                timeout=15,
            )
            if resp.status_code != 200:
                msg = resp.json().get('error', 'Login failed') if resp.headers.get('content-type', '').startswith('application/json') else 'Login failed'
                QMessageBox.warning(self, 'Login failed', msg)
                return

            data = resp.json()
            self.access_token = data.get('access')
            self.username = data.get('username')
            if not self.access_token:
                QMessageBox.warning(self, 'Login failed', 'No access token returned')
                return
            self.accept()
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Connection Error', 'Cannot connect to backend at http://localhost:8000')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def do_register(self):
        username = self.reg_username.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_password.text()
        if not email or not password:
            QMessageBox.warning(self, 'Error', 'Email and password are required')
            return

        try:
            resp = self.session.post(
                f'{self.api_base_url}/register/',
                json={'username': username, 'password': password, 'email': email},
                timeout=15,
            )
            if resp.status_code != 201:
                msg = resp.json().get('error', 'Registration failed') if resp.headers.get('content-type', '').startswith('application/json') else 'Registration failed'
                QMessageBox.warning(self, 'Registration failed', msg)
                return
            QMessageBox.information(self, 'Success', 'Registration successful. Please login.')
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Connection Error', 'Cannot connect to backend at http://localhost:8000')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))


class HistoryDialog(QDialog):
    def __init__(self, api_base_url, session, parent=None):
        super().__init__(parent)
        self.api_base_url = api_base_url
        self.session = session

        self.setWindowTitle('Upload History')
        self.setModal(True)
        self.resize(900, 520)

        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'ID',
            'Name',
            'Uploaded',
            'Total',
            'Avg Flowrate',
            'Avg Pressure',
            'Avg Temperature',
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.clicked.connect(self.load_history)
        self.pdf_btn = QPushButton('Download PDF')
        self.pdf_btn.clicked.connect(self.download_selected_pdf)
        btn_row.addWidget(self.refresh_btn)
        btn_row.addWidget(self.pdf_btn)
        layout.addLayout(btn_row)

        self.load_history()

    def load_history(self):
        try:
            resp = self.session.get(f'{self.api_base_url}/history/', timeout=15)
            if resp.status_code == 401:
                QMessageBox.warning(self, 'Unauthorized', 'Please login again.')
                self.close()
                return
            data = resp.json()
            datasets = data.get('datasets', [])

            self.table.setRowCount(len(datasets))
            for r, d in enumerate(datasets):
                self.table.setItem(r, 0, QTableWidgetItem(str(d.get('id'))))
                self.table.setItem(r, 1, QTableWidgetItem(str(d.get('name', ''))))
                self.table.setItem(r, 2, QTableWidgetItem(str(d.get('upload_timestamp', ''))))
                self.table.setItem(r, 3, QTableWidgetItem(str(d.get('total_equipment', ''))))
                self.table.setItem(r, 4, QTableWidgetItem(f"{float(d.get('average_flowrate', 0.0)):.2f}"))
                self.table.setItem(r, 5, QTableWidgetItem(f"{float(d.get('average_pressure', 0.0)):.2f}"))
                self.table.setItem(r, 6, QTableWidgetItem(f"{float(d.get('average_temperature', 0.0)):.2f}"))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load history: {e}')

    def _selected_dataset_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        if not item:
            return None
        try:
            return int(item.text())
        except Exception:
            return None

    def download_selected_pdf(self):
        dataset_id = self._selected_dataset_id()
        if not dataset_id:
            QMessageBox.information(self, 'Select Dataset', 'Please select a dataset row first.')
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            'Save PDF',
            f'equipment_report_{dataset_id}.pdf',
            'PDF Files (*.pdf)'
        )
        if not save_path:
            return

        try:
            resp = self.session.get(f'{self.api_base_url}/generate-pdf/{dataset_id}/', timeout=30)
            if resp.status_code == 401:
                QMessageBox.warning(self, 'Unauthorized', 'Please login again.')
                self.close()
                return
            if resp.status_code != 200:
                msg = resp.json().get('error', 'Failed to generate PDF') if resp.headers.get('content-type', '').startswith('application/json') else 'Failed to generate PDF'
                QMessageBox.warning(self, 'Error', msg)
                return
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            QMessageBox.information(self, 'Saved', f'PDF saved to:\n{save_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to download PDF: {e}')


class ChemicalEquipmentAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_base_url = 'http://localhost:8000/api'
        self.current_data = None
        self.session = requests.Session()
        self.access_token = None
        self.username = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Parameter Visualizer - Desktop')
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel('Chemical Equipment Parameter Visualizer')
        header_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                padding: 20px;
                border-radius: 10px;
            }
        """)
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        auth_row = QHBoxLayout()
        self.user_label = QLabel('Not logged in')
        self.user_label.setStyleSheet('padding: 6px; font-weight: bold; color: #333;')
        self.login_btn = QPushButton('Login / Register')
        self.login_btn.clicked.connect(self.open_auth)
        self.logout_btn = QPushButton('Logout')
        self.logout_btn.clicked.connect(self.logout)
        self.history_btn = QPushButton('History')
        self.history_btn.clicked.connect(self.open_history)
        auth_row.addWidget(self.user_label)
        auth_row.addStretch(1)
        auth_row.addWidget(self.history_btn)
        auth_row.addWidget(self.login_btn)
        auth_row.addWidget(self.logout_btn)
        main_layout.addLayout(auth_row)
        
        # Upload section
        upload_group = QGroupBox('Upload CSV File')
        upload_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #667eea;
                border-radius: 5px;
                margin-top: 10px;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        upload_layout = QHBoxLayout()
        
        self.file_label = QLabel('No file selected')
        self.file_label.setStyleSheet("padding: 5px;")
        
        self.browse_button = QPushButton('Browse')
        self.browse_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #764ba2, stop:1 #667eea);
            }
        """)
        self.browse_button.clicked.connect(self.browse_file)
        
        self.upload_button = QPushButton('Upload and Analyze')
        self.upload_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #764ba2, stop:1 #667eea);
            }
            QPushButton:disabled {
                background: #cccccc;
            }
        """)
        self.upload_button.clicked.connect(self.upload_file)
        self.upload_button.setEnabled(False)
        
        upload_layout.addWidget(self.file_label)
        upload_layout.addWidget(self.browse_button)
        upload_layout.addWidget(self.upload_button)
        upload_group.setLayout(upload_layout)
        main_layout.addWidget(upload_group)
        
        # Summary section
        summary_group = QGroupBox('Summary Statistics')
        summary_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #667eea;
                border-radius: 5px;
                margin-top: 10px;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        summary_layout = QGridLayout()
        
        # Summary labels
        self.total_label = self.create_summary_label('Total Equipment: N/A')
        self.flowrate_label = self.create_summary_label('Avg Flowrate: N/A')
        self.pressure_label = self.create_summary_label('Avg Pressure: N/A')
        self.temperature_label = self.create_summary_label('Avg Temperature: N/A')
        
        summary_layout.addWidget(self.total_label, 0, 0)
        summary_layout.addWidget(self.flowrate_label, 0, 1)
        summary_layout.addWidget(self.pressure_label, 0, 2)
        summary_layout.addWidget(self.temperature_label, 0, 3)
        
        summary_group.setLayout(summary_layout)
        main_layout.addWidget(summary_group)
        
        # Charts and Table Section
        splitter = QSplitter(Qt.Vertical)
        
        # Charts section
        charts_widget = QWidget()
        charts_layout = QHBoxLayout(charts_widget)
        
        # Type Distribution Chart
        self.type_chart_figure = Figure(figsize=(6, 4))
        self.type_chart_canvas = FigureCanvas(self.type_chart_figure)
        charts_layout.addWidget(self.type_chart_canvas)
        
        # Average Values Chart
        self.avg_chart_figure = Figure(figsize=(6, 4))
        self.avg_chart_canvas = FigureCanvas(self.avg_chart_figure)
        charts_layout.addWidget(self.avg_chart_canvas)
        
        splitter.addWidget(charts_widget)
        
        # Data Table
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        table_label = QLabel('Equipment Data Table')
        table_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        table_layout.addWidget(table_label)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(6)
        self.data_table.setHorizontalHeaderLabels(['#', 'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.data_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #ddd;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        table_layout.addWidget(self.data_table)
        
        splitter.addWidget(table_widget)
        splitter.setSizes([400, 300])
        
        main_layout.addWidget(splitter)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)
    
    def _set_authenticated_state(self, authed):
        self.upload_button.setEnabled(authed and hasattr(self, 'selected_file'))
        self.history_btn.setEnabled(authed)
        self.logout_btn.setEnabled(authed)

    def open_auth(self):
        dlg = AuthDialog(self.api_base_url, self.session, self)
        if dlg.exec_() == QDialog.Accepted:
            self.access_token = dlg.access_token
            self.username = dlg.username
            self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})
            self.user_label.setText(f'Logged in: {self.username}')
            self._set_authenticated_state(True)

    def logout(self):
        self.access_token = None
        self.username = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        self.user_label.setText('Not logged in')
        self._set_authenticated_state(False)

    def open_history(self):
        if not self.access_token:
            QMessageBox.information(self, 'Login required', 'Please login first.')
            return
        HistoryDialog(self.api_base_url, self.session, self).exec_()

    def create_summary_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        label.setAlignment(Qt.AlignCenter)
        return label
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Select CSV File', 
            '', 
            'CSV Files (*.csv)'
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f'Selected: {file_path.split("/")[-1]}')
            self._set_authenticated_state(bool(self.access_token))
    
    def upload_file(self):
        if not hasattr(self, 'selected_file'):
            return

        if not self.access_token:
            QMessageBox.information(self, 'Login required', 'Please login first.')
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                response = self.session.post(f'{self.api_base_url}/upload/', files=files, timeout=60)
            
            if response.status_code == 201:
                data = response.json()
                self.current_data = data
                self.update_summary(data['summary'])
                self.update_charts(data['summary'])
                self.update_table(data['equipment_data'])
                QMessageBox.information(self, 'Success', 'File uploaded and processed successfully!')
            elif response.status_code == 401:
                QMessageBox.warning(self, 'Unauthorized', 'Session expired. Please login again.')
                self.logout()
            else:
                error_msg = response.json().get('error', 'Unknown error')
                QMessageBox.warning(self, 'Error', f'Upload failed: {error_msg}')
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Connection Error', 
                               'Cannot connect to the backend server.\nMake sure the Django server is running on http://localhost:8000')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
    
    def update_summary(self, summary):
        total = summary['total_equipment']
        avg_vals = summary['average_values']
        
        self.total_label.setText(f'Total Equipment: {total}')
        self.flowrate_label.setText(f'Avg Flowrate: {avg_vals["flowrate"]}')
        self.pressure_label.setText(f'Avg Pressure: {avg_vals["pressure"]}')
        self.temperature_label.setText(f'Avg Temperature: {avg_vals["temperature"]}')
    
    def update_charts(self, summary):
        # Clear previous charts
        self.type_chart_figure.clear()
        self.avg_chart_figure.clear()
        
        # Equipment Type Distribution Chart
        type_dist = summary['type_distribution']
        ax1 = self.type_chart_figure.add_subplot(111)
        ax1.bar(type_dist.keys(), type_dist.values(), color='#667eea', alpha=0.8)
        ax1.set_title('Equipment Type Distribution', fontweight='bold', fontsize=12)
        ax1.set_xlabel('Equipment Type')
        ax1.set_ylabel('Count')
        ax1.tick_params(axis='x', rotation=45)
        self.type_chart_figure.tight_layout()
        
        # Average Values Chart
        avg_vals = summary['average_values']
        ax2 = self.avg_chart_figure.add_subplot(111)
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        values = [avg_vals['flowrate'], avg_vals['pressure'], avg_vals['temperature']]
        colors = ['#667eea', '#764ba2', '#ed64a6']
        ax2.bar(parameters, values, color=colors, alpha=0.8)
        ax2.set_title('Average Parameter Values', fontweight='bold', fontsize=12)
        ax2.set_ylabel('Value')
        self.avg_chart_figure.tight_layout()
        
        # Refresh canvases
        self.type_chart_canvas.draw()
        self.avg_chart_canvas.draw()
    
    def update_table(self, equipment_data):
        self.data_table.setRowCount(len(equipment_data))
        
        for row, item in enumerate(equipment_data):
            self.data_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.data_table.setItem(row, 1, QTableWidgetItem(str(item['Equipment Name'])))
            self.data_table.setItem(row, 2, QTableWidgetItem(str(item['Type'])))
            self.data_table.setItem(row, 3, QTableWidgetItem(str(item['Flowrate'])))
            self.data_table.setItem(row, 4, QTableWidgetItem(str(item['Pressure'])))
            self.data_table.setItem(row, 5, QTableWidgetItem(str(item['Temperature'])))
        
        self.data_table.resizeColumnsToContents()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ChemicalEquipmentAnalyzer()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()