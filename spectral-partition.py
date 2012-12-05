import numpy as np
from scipy.sparse import coo_matrix
import scipy.sparse.linalg as sla
import matplotlib.pyplot as pt

from mesh import make_mesh
mesh = make_mesh()

points = np.array(mesh.points)
elements = np.array(mesh.elements)

if 1:
    pt.triplot(points[:, 0], points[:, 1], elements, color="black")
    pt.show()

    import sys
    sys.exit()

# {{{ find connectivity

neighbors = {}
for a, b, c in mesh.elements:
    for v1, v2 in [(a,b), (b,c), (c,a)]:
        for x, y in [(v1, v2), (v2, v1)]:
            neighbors.setdefault(v1, set()).add(v2)

# }}}

# {{{ make graph laplacian

row  = []
col  = []
data = []
for vnr, nb_nrs in neighbors.iteritems():
    row.append(vnr)
    col.append(vnr)
    data.append(len(nb_nrs))

    for nb in nb_nrs:
        row.append(vnr)
        col.append(nb)
        data.append(-1)

lap = coo_matrix((data, (row,col)), dtype=np.float64).tocsr()

# }}}

eigval, eigvec = sla.eigs(lap, 6, which="SM")
print eigval

for vec in eigvec.T[1:]:
    vec = vec.real
    pt.triplot(points[:, 0], points[:, 1], elements, color="black", lw=0.1)
    pt.tripcolor(points[:, 0], points[:, 1], elements, vec)
    pt.colorbar()
    pt.tricontour(points[:, 0], points[:, 1], elements, vec, colors="black", levels=[0])
    pt.show()

# vim: foldmethod=marker
