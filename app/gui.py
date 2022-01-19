import csv

import numpy as np
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
from matplotlib.figure import Figure
from PyQt6 import QtWidgets
from scipy import interpolate

from . import main


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, *args, **kwargs):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.plot_data = {}

        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.left_panel = QtWidgets.QWidget(self.central_widget)
        self.right_panel = QtWidgets.QWidget(self.central_widget)

        layout = QtWidgets.QHBoxLayout(self.central_widget)
        layout.addWidget(self.left_panel)
        layout.addWidget(self.right_panel)

        self.left_layout = QtWidgets.QVBoxLayout(self.left_panel)
        self.right_layout = QtWidgets.QVBoxLayout(self.right_panel)

        self.input_params = QtWidgets.QGroupBox("Входные параметры:", self.left_panel)
        self.q_param = QtWidgets.QDoubleSpinBox(self.input_params)
        self.q_param.setValue(1.2)
        self.lam_param = QtWidgets.QDoubleSpinBox(self.input_params)
        self.lam_param.setValue(2.0)
        self.T_param = QtWidgets.QDoubleSpinBox(self.input_params)
        self.T_param.setValue(5.0)
        self.f_param = QtWidgets.QLineEdit(self.input_params)
        self.f_param.setText("np.sin(t)")

        input_params_layout = QtWidgets.QGridLayout(self.input_params)
        input_params_layout.addWidget(QtWidgets.QLabel("q = ", self.input_params), 0, 0)
        input_params_layout.addWidget(self.q_param, 0, 1)
        input_params_layout.addWidget(QtWidgets.QLabel("λ = ", self.input_params), 1, 0)
        input_params_layout.addWidget(self.lam_param, 1, 1)
        input_params_layout.addWidget(QtWidgets.QLabel("T = ", self.input_params), 2, 0)
        input_params_layout.addWidget(self.T_param, 2, 1)
        input_params_layout.addWidget(QtWidgets.QLabel("f = ", self.input_params), 3, 0)
        input_params_layout.addWidget(self.f_param, 3, 1)
        self.input_params.setLayout(input_params_layout)
        self.left_layout.addWidget(self.input_params)

        self.internal_params = QtWidgets.QGroupBox("Параметры:", self.left_panel)
        self.step_param = QtWidgets.QDoubleSpinBox(self.input_params)
        self.step_param.setValue(0.1)
        internal_params_layout = QtWidgets.QGridLayout(self.internal_params)
        internal_params_layout.addWidget(
            QtWidgets.QLabel("Шаг = ", self.internal_params),
            0,
            0,
        )
        internal_params_layout.addWidget(self.step_param, 0, 1)
        self.internal_params.setLayout(internal_params_layout)
        self.left_layout.addWidget(self.internal_params)

        self.input_f_gb = QtWidgets.QGroupBox("Функция f:", self.left_panel)
        self.is_use_table_f = QtWidgets.QCheckBox(
            "Задать функцию f таблично?",
            self.input_f_gb,
        )
        self.is_use_table_f.stateChanged.connect(self.is_use_table_f_changed)
        self.f_table = QtWidgets.QTableWidget(self.input_f_gb)
        self.f_table.setColumnCount(2)
        self.f_table.setHorizontalHeaderLabels(["t", "f(t)"])
        example_row_count = 5
        t_linspace = np.linspace(0, 1, example_row_count)
        x = np.sin(t_linspace)
        for i in range(example_row_count):
            self.f_table.insertRow(i)
            self.f_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(t_linspace[i])))
            self.f_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(f"{x[i]:.2f}")))
        header = self.f_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.add_row_btn = QtWidgets.QPushButton("Добавить точку")
        self.rm_row_btn = QtWidgets.QPushButton("Удалить точку")
        self.add_row_btn.clicked.connect(self.add_row_btn_clicked)
        self.rm_row_btn.clicked.connect(self.rm_row_btn_clicked)

        input_f_gb_layout = QtWidgets.QVBoxLayout(self.input_f_gb)
        input_f_gb_layout.addWidget(self.is_use_table_f)
        input_f_gb_layout.addWidget(self.f_table)
        input_f_gb_layout.addWidget(self.add_row_btn)
        input_f_gb_layout.addWidget(self.rm_row_btn)
        self.input_f_gb.setLayout(input_f_gb_layout)
        self.left_layout.addWidget(self.input_f_gb)

        self.left_layout.addStretch()

        self.go_btn = QtWidgets.QPushButton("Построить график")
        self.go_btn.clicked.connect(self.go_btn_clicked)
        self.left_layout.addWidget(self.go_btn)

        self.canvas = MplCanvas(self.right_panel)
        self.toolbar = NavigationToolbar2QT(self.canvas, self.right_panel)
        self.toolbar.setStyleSheet("QToolBar { border: 0px }")

        self.right_layout.addWidget(self.toolbar)
        self.right_layout.addWidget(self.canvas)

        self.save_plot_data_btn = QtWidgets.QPushButton("Сохранить данные")
        self.save_plot_data_btn.clicked.connect(self.save_plot_data_btn_clicked)
        self.right_layout.addWidget(self.save_plot_data_btn)

        self.is_use_table_f_changed(...)

    def add_row_btn_clicked(self):
        row_count = self.f_table.rowCount()
        self.f_table.insertRow(row_count)
        self.f_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem("0"))
        self.f_table.setItem(row_count, 1, QtWidgets.QTableWidgetItem("0"))

    def rm_row_btn_clicked(self):
        row_count = self.f_table.rowCount()
        self.f_table.removeRow(row_count - 1)

    def is_use_table_f_changed(self, _):
        if self.is_use_table_f.isChecked():
            self.f_table.setEnabled(True)
            self.add_row_btn.setEnabled(True)
            self.rm_row_btn.setEnabled(True)

            self.T_param.setEnabled(False)
            self.f_param.setEnabled(False)
            self.step_param.setEnabled(False)
        else:
            self.f_table.setEnabled(False)
            self.add_row_btn.setEnabled(False)
            self.rm_row_btn.setEnabled(False)

            self.T_param.setEnabled(True)
            self.f_param.setEnabled(True)
            self.step_param.setEnabled(True)

    def go_btn_clicked(self):

        if self.is_use_table_f.isChecked():
            table_data = {}
            for i in range(self.f_table.rowCount()):
                t = float(self.f_table.item(i, 0).text())
                x = float(self.f_table.item(i, 1).text())
                table_data[t] = x

            t_values = list(table_data.keys())
            x_values = list(table_data.values())

            T = max(t_values)
            t_range = t_values

            f = interpolate.interp1d(t_values, x_values)

        else:
            T = self.T_param.value()

            def f(t):
                return eval(self.f_param.text())

            step = self.step_param.value()
            t_range = np.arange(0, T + step, step, dtype=np.float64)

        params = {
            "q": self.q_param.value(),
            "lam": self.lam_param.value(),
            "T": T,
            "f": f,
        }

        x_t = []
        for t in t_range:
            x_t.append(main.function(t, **params)[0])

        self.plot_data["t"] = t_range
        self.plot_data["x"] = x_t

        self.canvas.axes.cla()
        self.canvas.axes.plot(t_range, x_t)
        self.canvas.draw()

    def save_plot_data_btn_clicked(self):
        if not self.plot_data:
            return

        dialog = QtWidgets.QFileDialog()
        dialog.setNameFilter("CSV (*csv)")
        filename = dialog.getSaveFileName(self, "Сохранить как...", "plot_data.csv")[0]
        if not filename:
            return

        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["t", "x(t)"])
            for t, x in zip(self.plot_data["t"], self.plot_data["x"]):
                writer.writerow([t, x])
