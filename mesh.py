import meshpy.triangle as triangle
import sys
import numpy as np


class Refiners:
    @staticmethod
    def needs_refinement_uni(vertices, area):
        return area > 1e-3

    @staticmethod
    def needs_refinement_us(vertices, area):
        vert_origin, vert_destination, vert_apex = vertices
        bary_x = (vert_origin.x + vert_destination.x + vert_apex.x) / 3
        bary_y = (vert_origin.y + vert_destination.y + vert_apex.y) / 3

        dist_center = np.sqrt((bary_x-600)**2 + (750-bary_y)**2 )
        max_area = 1 + 0.8*dist_center
        return bool(area > max_area)

def make_mesh():
    outline = np.loadtxt(sys.argv[1])


    def round_trip_connect(start, end):
        result = []
        for i in range(start, end):
            result.append((i, i+1))
        result.append((end, start))
        return result


    info = triangle.MeshInfo()
    info.set_points(outline)
    info.set_facets(round_trip_connect(0, len(outline)-1))

    return triangle.build(info,
            refinement_func=getattr(Refiners, "needs_refinement_%s" % sys.argv[2]))
