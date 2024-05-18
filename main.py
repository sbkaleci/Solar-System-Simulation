import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk
from solar_system import SolarSystem
import sys

class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solar System Simulation")

        self.solar_system = SolarSystem()
        self.t_step = 1*24*3600

        self.fig, self.ax = self.setup_plot()

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.X)  

        self.add_widgets()

        self.ani = FuncAnimation(self.fig, self.update, frames=None, init_func=self.init,
                                 fargs=(self.solar_system, self.orbit_lines, self.current_position_markers, self.trajectories),
                                 interval=0.0000005, blit=True)

    def setup_plot(self):
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        initial_zoom_level = 10  
        self.ax.set_xlim([-5e11, 5e11])
        self.ax.set_ylim([-5e11, 5e11])
        self.ax.set_zlim([-5e11, 5e11])

        self.max_xlim = [-5e12, 5e12]
        self.max_ylim = [-5e12, 5e12]
        self.max_zlim = [-5e12, 5e12]

        self.ax.set_xlabel('X (meters)', fontsize=14)
        self.ax.set_ylabel('Y (meters)', fontsize=14)
        self.ax.set_zlabel('Z (meters)', fontsize=14)

        self.ax.ticklabel_format(style='scientific', axis='x', scilimits=(0, 0))
        self.ax.ticklabel_format(style='scientific', axis='y', scilimits=(0, 0))
        self.ax.ticklabel_format(style='scientific', axis='z', scilimits=(0, 0))

        self.ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda val, pos: f'{val:.0e}'))
        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, pos: f'{val:.0e}'))
        self.ax.zaxis.set_major_formatter(plt.FuncFormatter(lambda val, pos: f'{val:.0e}'))

        self.body_names = ["Sun", "Earth", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
        colors = ['yellow', 'blue', 'lightgray', 'darkgray', 'magenta', 'red', 'orange', 'goldenrod', 'cyan', 'purple']

        self.orbit_lines = [self.ax.plot([], [], [], color=colors[i], linewidth=1.5)[0] for i in range(len(self.solar_system.bodies))]
        self.current_position_markers = [self.ax.plot([], [], [], 'o', color=colors[i], markersize=8, label=self.body_names[i])[0] for i in range(len(self.solar_system.bodies))]

        self.trajectories = [[] for _ in range(len(self.solar_system.bodies))]

        self.ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize=16)

        return fig, self.ax

    def add_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14), padding=10)
        style.configure("TLabel", font=("Arial", 14), padding=10)
        style.configure("TScale", font=("Arial", 14))

        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.date_label = ttk.Label(bottom_frame, text=f"Date: {self.solar_system.time.iso}", style="TLabel")
        self.date_label.pack(side=tk.LEFT, padx=10)

        self.slider = ttk.Scale(bottom_frame, from_=0, to=3*24*3600, orient=tk.HORIZONTAL, length=600)
        self.slider.set(self.t_step)
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=10)
        self.slider.bind("<Motion>", self.update_slider)

        self.zoom_slider = ttk.Scale(bottom_frame, from_=1, to=10, orient=tk.HORIZONTAL, command=self.update_zoom, length=600)
        self.zoom_slider.set(10)  
        self.zoom_slider.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=10)

    def init(self):
        for line in self.orbit_lines + self.current_position_markers:
            line.set_data([], [])
            line.set_3d_properties([])
        self.date_label.config(text=f"Date: {self.solar_system.time.iso}")
        return self.orbit_lines + self.current_position_markers

    def update(self, num, solar_system, orbit_lines, current_position_markers, trajectories):
        if self.t_step == 0:
            return self.orbit_lines + self.current_position_markers

        solar_system.update(self.t_step)
        state = solar_system.export_state()
        num_bodies = len(solar_system.bodies)
        positions = state[:3*num_bodies].reshape((num_bodies, 3))

        max_trajectory_length = 1000  # Limit the length of the trajectories

        for i, pos in enumerate(positions):
            trajectories[i].append(pos)
            if len(trajectories[i]) > max_trajectory_length:
                trajectories[i] = trajectories[i][-max_trajectory_length:]  # Keep only the last 1000 points
            data = np.array(trajectories[i])
            orbit_lines[i].set_data(data[:, 0], data[:, 1])
            orbit_lines[i].set_3d_properties(data[:, 2])
            current_position_markers[i].set_data([pos[0]], [pos[1]])
            current_position_markers[i].set_3d_properties([pos[2]])

        self.date_label.config(text=f"Date: {self.solar_system.time.iso}")

        return orbit_lines + current_position_markers

    def update_slider(self, event):
        self.t_step = int(self.slider.get())

    def update_zoom(self, event):
        zoom_level = float(self.zoom_slider.get())
        self.ax.set_xlim([x / zoom_level for x in self.max_xlim])
        self.ax.set_ylim([y / zoom_level for y in self.max_ylim])
        self.ax.set_zlim([z / zoom_level for z in self.max_zlim])
        self.canvas.draw_idle()

    def on_closing(self):
        self.root.quit()
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SolarSystemApp(root)
    root.geometry("1800x1200")
    root.iconbitmap('icon.ico')  
    root.protocol("WM_DELETE_WINDOW", sys.exit())
    root.mainloop()