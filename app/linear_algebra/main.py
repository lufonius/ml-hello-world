# main module (the one which is to run) always have to use absolute paths
from app.linear_algebra.vector import Vector

# adding and substracting
print(Vector([8.218, -9.341]) + Vector([-1.129, 2.111]))
print(Vector([7.119, 8.215]) - Vector([-8.223, 0.878]))
print(Vector([1.671, -1.012, -0.318]) * 7.41)

# magnitude and direction
print(Vector([-0.221, 7.437]).magnitude())
print(Vector([8.813, -1.331, -6.247]).magnitude())
print(Vector([5.581, -2.136]).normalize())
print(Vector([1.996, 3.108, -4.554]).normalize())

# dot product and angle
print(Vector([7.887, 4.138]).dot_with(Vector([-8.802, 6.776])))
print(Vector([-5.955, -4.904, -1.874]).dot_with(Vector([-4.496, -8.755, 7.103])))
print(Vector([3.183, -7.627]).dot_with(Vector([-2.668, 5.319])))
print(Vector([7.35, 0.221, 5.188]).dot_with(Vector([2.751, 8.259, 3.985])))

# component and projection
v1 = Vector([3.039, 1.879])
v2 = Vector([0.825, 2.036])
print(v1.project_onto(v2))
print('---')

v1 = Vector([-9.88, -3.264, -8.159])
v2 = Vector([-2.155, -9.353, -9.473])
print(v1.component_to(v2))
print('---')

v1 = Vector([3.009, -6.172, 3.692, -2.51])
v2 = Vector([6.404, -9.144, 2.759, 8.718])
print(v1.project_onto(v2))
print(v1.component_to(v2))
print('---')

# cross product
v1 = Vector([8.462, 7.893, -8.187])
v2 = Vector([6.984, -5.975, 4.778])
print(v1.cross_with(v2))

v1 = Vector([-8.987, -9.838, 5.031])
v2 = Vector([-4.268, -1.861, -8.866])
print(v1.area_parallelogram_with(v2))

v1 = Vector([1.5, 9.547, 3.691])
v2 = Vector([-6.007, 0.124, 5.772])
print(v1.area_triangle_with(v2))
