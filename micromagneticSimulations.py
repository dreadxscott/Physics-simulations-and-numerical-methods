import oommfc as mc
import discretisedfield as df 
import ubermagutil.typesystem as ts
import vtk


# Define the system's geometry and mesh
p1 = (0, 0, 0)
p2 = (100e-9, 100e-9, 10e-9)
n = (10, 10, 1)
mesh = df.Mesh(p1=p1, p2=p2, n=n)

# Define the material parameters
Ms = 8e5  # Saturation magnetization (A/m)
A = 1.3e-11  # Exchange energy constant (J/m)
K = 6e3  # Uniaxial anisotropy constant (J/m^3)
u = (0, 0, 1)  # Uniaxial anisotropy axis

# Define the system
system = mc.System(name="simple_system")
system.hamiltonian = mc.Exchange(A=A) + mc.UniaxialAnisotropy(K=K, u=u) + mc.Demag()
system.m = df.Field(mesh, dim=3, value=(0, 0, 1), norm=Ms)

# Define the dynamics equation (LLG)
system.dynamics = mc.Precession(gamma0=ts.Parameter(2.211e5)) + mc.Damping(alpha=ts.Parameter(0.1))

# Create a simulation object and run the simulation
sim = mc.Simulation(system)
sim.driver.do_precession = True
sim.driver.run_until(1e-9)

# Save the final magnetization configuration
final_m = system.m.copy()
final_m.write("final_magnetization.vtk")
