from .day import Day
from fractions import Fraction
import numpy as np
from scipy.optimize import least_squares


class Entry:
    def __init__(self, line: str):
        vals = line.split()
        self.px = int(vals.pop(0).rstrip(','))
        self.py = int(vals.pop(0).rstrip(','))
        self.pz = int(vals.pop(0).rstrip(','))
        _ = vals.pop(0)
        self.vx = int(vals.pop(0).rstrip(','))
        self.vy = int(vals.pop(0).rstrip(','))
        self.vz = int(vals.pop(0).rstrip(','))

    def intersect_2d(self, other) -> type[tuple[int, int], None]:
        # find (x, y) coordinate where self intersects with other
        m_self, b_self = self.m_and_b_2d()
        m_other, b_other = other.m_and_b_2d()
        if m_self is None or b_self is None or m_self == m_other:
            return None

        # where do two lines intersect, based on formula?
        # y = m1x+b1
        # y = m2x+b2
        # y - m1x - b1 = 0
        # y - m2x - b2 = 0
        # 0 - m1x + m2x - b1 + b2 = 0
        # (m2-m1)x = b1-b2
        # x = (b1-b2)/(m2-m1)
        ix = (b_self-b_other)/(m_other-m_self)
        iy = ix * m_self + b_self

        # make sure intersection is in the future
        if ix >= self.px and self.vx < 0:
            return None
        if ix <= self.px and self.vx > 0:
            return None
        if iy >= self.py and self.vy < 0:
            return None
        if iy <= self.py and self.vy > 0:
            return None
        if ix >= other.px and other.vx < 0:
            return None
        if ix <= other.px and other.vx > 0:
            return None
        if iy >= other.py and other.vy < 0:
            return None
        if iy <= other.py and other.vy > 0:
            return None

        return ix, iy

    def m_and_b_2d(self) -> type[tuple[Fraction, int], tuple[None, None]]:
        # y = mx + b
        # y = (vy/vx)x + b
        # b = y - (vy/vx)x
        if self.vx == 0:
            return None, None
        m = Fraction(self.vy, self.vx)
        b = self.py - m * self.px
        return m, b

    def __str__(self) -> str:
        return f"Entry(pos=({self.px}, {self.py}, {self.pz}) vel=({self.vx}, {self.vy}, {self.vz})"


class Day24(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        entries = self.entries()
        i_count_test = 0
        i_count_real = 0
        for i in range(len(entries)):
            for j in range(i+1, len(entries)):
                intersect = entries[i].intersect_2d(entries[j])
                print(f"{entries[i]} intersect {entries[j]} at {intersect}")
                if intersect is not None and 7 <= intersect[0] <= 27 and 7 <= intersect[1] <= 27:
                    i_count_test += 1
                if intersect is not None and 200000000000000 <= intersect[0] <= 400000000000000 and 200000000000000 <= intersect[1] <= 400000000000000:
                    i_count_real += 1
        print(f"test={i_count_test}")
        return str(i_count_real)

    def part2(self) -> str:
        # This solution was provided by the o1-mini GPT model. Too much hard math!!
        # Load the data
        positions = []
        velocities = []
        for entry in self.entries():
            positions.append([entry.px, entry.py, entry.pz])
            velocities.append([entry.vx, entry.vy, entry.vz])
        positions = np.array(positions)
        velocities = np.array(velocities)

        # Verify the number of objects
        num_objects = len(positions)
        print(f"Number of objects parsed: {num_objects}")

        # Step 2: Define the Residuals Function
        def residuals(params, positions, velocities):
            x_s, y_s, z_s, v_sx, v_sy, v_sz = params
            res = []
            for i in range(len(positions)):
                x_i, y_i, z_i = positions[i]
                v_ix, v_iy, v_iz = velocities[i]

                # First Equation: (x_s -x_i)*(v_iy - v_sy) - (y_s - y_i)*(v_ix - v_sx) = 0
                res1 = (x_s - x_i) * (v_iy - v_sy) - (y_s - y_i) * (v_ix - v_sx)

                # Second Equation: (x_s -x_i)*(v_iz - v_sz) - (z_s - z_i)*(v_ix - v_sx) = 0
                res2 = (x_s - x_i) * (v_iz - v_sz) - (z_s - z_i) * (v_ix - v_sx)

                res.extend([res1, res2])
            return res

        # Step 3: Initial Guess
        # A reasonable initial guess is the average position and average velocity
        initial_guess = [
            np.mean(positions[:,0]),  # x_s
            np.mean(positions[:,1]),  # y_s
            np.mean(positions[:,2]),  # z_s
            np.mean(velocities[:,0]), # v_sx
            np.mean(velocities[:,1]), # v_sy
            np.mean(velocities[:,2])  # v_sz
        ]

        print("Initial guess for parameters:")
        print(f"x_s: {initial_guess[0]}, y_s: {initial_guess[1]}, z_s: {initial_guess[2]}")
        print(f"v_sx: {initial_guess[3]}, v_sy: {initial_guess[4]}, v_sz: {initial_guess[5]}")

        # Step 4: Solve the System Using Nonlinear Solver
        result = least_squares(
            residuals,
            initial_guess,
            args=(positions, velocities),
            method='lm',  # Levenberg-Marquardt algorithm
            ftol=1e-12,   # Tolerance for termination by the change of the cost function
            xtol=1e-12,   # Tolerance for termination by the change of the solution
            gtol=1e-12    # Tolerance for termination by the norm of the gradient
        )

        # Step 5: Extract and Display the Solution
        if result.success:
            x_s, y_s, z_s, v_sx, v_sy, v_sz = result.x
            print("\nSolution Found:")
            print("Starting position of the solution object:")
            print(f"x_s = {x_s}")
            print(f"y_s = {y_s}")
            print(f"z_s = {z_s}")

            print("\nVelocity of the solution object:")
            print(f"v_sx = {v_sx}")
            print(f"v_sy = {v_sy}")
            print(f"v_sz = {v_sz}")

            # Optional: Verify Residuals
            final_residuals = residuals(result.x, positions, velocities)
            max_residual = np.max(np.abs(final_residuals))
            print(f"\nMaximum residual after optimization: {max_residual}")
            if np.allclose(final_residuals, 0, atol=1e-6):
                print("All residuals are effectively zero. Exact solution achieved.")
            else:
                print("Residuals are not all zero. Check the data or optimization parameters.")
        else:
            print("Optimization failed. Try adjusting the initial guess or solver parameters.")

        return f"{int(x_s+y_s+z_s)}"

    def entries(self) -> tuple[Entry, ...]:
        return tuple([Entry(line) for line in self.data_lines()])



