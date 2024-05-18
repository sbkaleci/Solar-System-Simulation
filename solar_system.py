from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation, get_body_barycentric_posvel
from astropy import units
import numpy as np
from scipy.integrate import solve_ivp
from scipy.constants import gravitational_constant as G
from datetime import datetime

class CelestialObject:
    def __init__(self, position, velocity, mass):
        self.position = position
        self.velocity = velocity
        self.mass = mass

class SolarSystem:
    def __init__(self):
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M")
        self.time = Time(now)
        self.loc = EarthLocation.of_site('greenwich')

        with solar_system_ephemeris.set('builtin'):
            self.earth = self._create_body('earth', 5.972e24)
            self.sun = self._create_body('sun', 1.9885e30)
            self.moon = self._create_body('moon', 7.342e22)
            self.mercury = self._create_body('mercury', 3.3011e23)
            self.venus = self._create_body('venus', 4.8675e24)
            self.mars = self._create_body('mars', 6.4171e23)
            self.jupiter = self._create_body('jupiter', 1.8982e27)
            self.saturn = self._create_body('saturn', 5.6834e26)
            self.uranus = self._create_body('uranus', 8.6810e25)
            self.neptune = self._create_body('neptune', 1.02413e26)

        self.bodies = [self.earth, self.sun, self.moon, self.mercury, self.venus,
                       self.mars, self.jupiter, self.saturn, self.uranus, self.neptune]

    def export_state(self):
        positions = np.array([body.position.value for body in self.bodies]).flatten()
        velocities = np.array([body.velocity.value for body in self.bodies]).flatten()
        conditions = np.concatenate([positions, velocities])
        return conditions

    def _create_body(self, name, mass):
        pos, vel = get_body_barycentric_posvel(name, self.time)
        return CelestialObject(pos.xyz.to(units.m), vel.xyz.to(units.m/units.s), mass * units.kg)

    def equations_of_motion(self, t, y):
        num_bodies = len(self.bodies)
        positions = y[:3*num_bodies].reshape((num_bodies, 3))
        velocities = y[3*num_bodies:].reshape((num_bodies, 3))
        accelerations = np.zeros_like(positions)

        for i in range(num_bodies):
            for j in range(num_bodies):
                if i != j:
                    r_vector = positions[j] - positions[i]
                    r = np.linalg.norm(r_vector)
                    accelerations[i] += G * self.bodies[j].mass.value * r_vector / r**3

        derivatives = np.concatenate([velocities, accelerations]).flatten()
        return derivatives

    def update_state(self, new_positions_and_velocities):
        num_bodies = len(self.bodies)
        positions = new_positions_and_velocities[:3*num_bodies].reshape((num_bodies, 3))
        velocities = new_positions_and_velocities[3*num_bodies:].reshape((num_bodies, 3))

        for i, body in enumerate(self.bodies):
            body.position = positions[i] * units.m
            body.velocity = velocities[i] * (units.m / units.s)

    def integrate(self, t_span, initial_conditions):
        solution = solve_ivp(self.equations_of_motion, t_span, initial_conditions, method='DOP853')
        final_positions = solution.y[:3*len(self.bodies)].reshape((len(self.bodies), 3, -1))[:, :, -1]
        final_velocities = solution.y[3*len(self.bodies):].reshape((len(self.bodies), 3, -1))[:, :, -1]
        final_conditions = np.concatenate([final_positions.flatten(), final_velocities.flatten()])
        return final_conditions

    def update(self, t_step):
        initial_conditions = self.export_state()
        t_span = (0, t_step)
        final_conditions = self.integrate(t_span, initial_conditions)
        self.update_state(final_conditions)
        self.time += t_step * units.s