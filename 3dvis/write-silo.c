#include <silo.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
  // {{{ create the silo file

  DBfile *dbfile = NULL;
  dbfile = DBCreate("example.silo", DB_CLOBBER, DB_LOCAL,
      "Comment about the data", DB_HDF5);
  if(dbfile == NULL)
  {
    fprintf(stderr, "Could not create Silo file!\n");
    abort();
  }

  // }}}

  // {{{ write a curvilinear mesh

#define NX 4
#define NY 3
#define NZ 2
  {
    float x[NZ][NY][NX] = {
      {{0.,1.,2.,3.},{0.,1.,2.,3.}, {0.,1.,2.,3.}},
      {{0.,1.,2.,3.},{0.,1.,2.,3.}, {0.,1.,2.,3.}}
    };
    float y[NZ][NY][NX] = {
      {{0.5,0.,0.,0.5},{1.,1.,1.,1.}, {1.5,2.,2.,1.5}},
      {{0.5,0.,0.,0.5},{1.,1.,1.,1.}, {1.5,2.,2.,1.5}}
    };
    float z[NZ][NY][NX] = {
      {{0.,0.,0.,0.},{0.,0.,0.,0.},{0.,0.,0.,0.}},
      {{1.,1.,1.,1.},{1.,1.,1.,1.},{1.,1.,1.,1.}}
    };
    int dims[] = {NX, NY, NZ};
    int ndims = 3;
    float *coords[] = {(float*)x, (float*)y, (float*)z};
    DBPutQuadmesh(dbfile, "quadmesh", NULL, coords, dims, ndims,
        DB_FLOAT, DB_NONCOLLINEAR, NULL);
  }

  // }}}

  // {{{ write data on curvilinear mesh

  {
    int i, dims[3], ndims = 3;
    int nnodes = NX*NY*NZ;
    float *data = (float *)malloc(sizeof(float)*nnodes);
    for(i = 0; i < nnodes; ++i)
      data[i] = (float)i;
    dims[0] = NX; dims[1] = NY; dims[2] = NZ;
    DBPutQuadvar1(dbfile, "nodal", "quadmesh", data, dims,
        ndims, NULL, 0, DB_FLOAT, DB_NODECENT, NULL);
    free(data);
  }

  // }}}

  // {{{ close the silo file
  DBClose(dbfile);
  // }}}

  return 0;
}

// vim: fdm=marker
