import numpy as np
import matplotlib.pyplot as pt

from mesh import make_mesh
mesh = make_mesh()

# {{{ find connectivity

adjacency = {}
for a, b, c in mesh.elements:
    for v1, v2 in [(a,b), (b,c), (c,a)]:
        for x, y in [(v1, v2), (v2, v1)]:
            adjacency.setdefault(v1, set()).add(v2)

# }}}

from pymetis import part_graph

points = np.array(mesh.points)
elements = np.array(mesh.elements)

vweights = points[:,0]**2

cuts, part_vert = part_graph(2, adjacency,
        #vweights=[int(20*x) for x in vweights]
        )

pt.triplot(points[:, 0], points[:, 1], elements, color="black", lw=0.1)
pt.tripcolor(points[:, 0], points[:, 1], elements, part_vert)
pt.tricontour(points[:, 0], points[:, 1], elements, part_vert, colors="black", levels=[0])
pt.show()
