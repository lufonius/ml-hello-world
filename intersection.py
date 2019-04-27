from package.linear_algebra.line import Line
from package.linear_algebra.vector import Vector
from package.linear_algebra.point import Point

line1 = Line(Vector([1, 5]), 6)
line2 = Line(Vector([2, 6]), 9)

line1.normal_vector = Vector([2, 5])

intersection = line1.get_intersection_with(line2)

print(intersection)

line1 = Line(Vector([1, 5]), 6)
line2 = Line(Vector([1, 5]), 6)

is_same = line1.is_same_line(line2)

print(is_same)

line1 = Line(Vector([1, 5]), 6)
line2 = Line(Vector([2, 10]), 6)

is_parallel = line1.is_parallel_with(line2)

print(is_parallel)
