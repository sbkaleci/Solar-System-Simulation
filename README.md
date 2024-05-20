# Solar System Simulation

This is a Python application that simulates the motion of celestial bodies in our solar system. It uses the Astropy library to fetch the initial coordinates and velocities of the planets, the Sun, and the Moon, and then integrates their equations of motion using the SciPy library, and then shows the motions through matplotlib.


## Features

- 3D visualization of the orbits of the planets, the Sun, and the Moon
- Real-time updates of the celestial bodies' positions
- Date and time display
- Zoom in/out functionality

## Adjustable Simulation Parameters

- **Time Step (t_step)**: Controls how fast the simulation progresses. Larger steps increase speed but reduce accuracy. Adjust using the slider.
- **Zoom Level**: Use the toolbar to zoom in and out, adjusting the view range of the 3D plot.
- **Refresh Rate**: Set the interval (in milliseconds) between frame updates. Higher rates make the simulation smoother but use more resources. Refresh Rate can be adjusted by editing main.py file.
- **Date Display Format**: Customize the date format in the settings menu using standard Python date format strings.

## Requirements
- Python 3.x
- numpy
- matplotlib
- tkinter
- astropy
- scipy

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/solar-system-simulation.git
2. Install the required packages: 
    ```sh
    pip install matplotlib scipy astropy numpy
3. Navigate to the project directory and run the script:
    ```sh
    cd solar-system-simulation
    python main.py

## License
This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.
