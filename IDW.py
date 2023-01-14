import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
import arcpy 

arcpy.AddMessage('##############################################')

arcpy.AddMessage('Tools made for Mapi - israel center of mapping')

arcpy.AddMessage('### If any bugs found, contact medad hoze ###')

arcpy.AddMessage('### medadhoze@hotmail.com  ###')

arcpy.AddMessage('### plz Send: 1) Picture of the error, 2) layers, 3) Arcmap version (10.1/10.3/10.5/10.6/10.8/arcpro)  ###')

arcpy.AddMessage('##############################################')

def create_IDW(data,Ras_path,type_idw,Num_row,num_columns):

    x = np.array([i[0] for i in data])
    y = np.array([i[1] for i in data])
    z = np.array([i[2] for i in data])

    st_X  = x.max() - x.min()
    st_Y  = y.max() - y.min()

    nx, ny =  int(Num_row),  int(num_columns)

    X_col = st_X / nx
    Y_col = st_Y / ny

    xi = np.linspace(x.min(), x.max(), nx)
    yi = np.linspace(y.min(), y.max(), ny)
    xi, yi = np.meshgrid(xi, yi)
    xi, yi = xi.flatten(), yi.flatten()

    if type_idw == 'simple_idw':
        grid1 = simple_idw(x,y,z,xi,yi)
        grid1 = grid1.reshape((ny, nx))

    if type_idw == 'scipy_idw':
        grid1 = scipy_idw(x,y,z,xi,yi)
        grid1 = grid1.reshape((ny, nx))

    if type_idw == 'linear_rbf':
        grid1 = linear_rbf(x,y,z,xi,yi)
        grid1 = grid1.reshape((ny, nx))

    myRasterBlock = arcpy.NumPyArrayToRaster(grid1, arcpy.Point(x.min(), y.min()),
                                                 X_col,
                                                 Y_col)
    myRasterBlock.save(Ras_path)


def simple_idw(x, y, z, xi, yi):
    dist = distance_matrix(x,y, xi,yi)
    weights = 1.0 / dist
    weights /= weights.sum(axis=0)
    zi = np.dot(weights.T, z)
    return zi

def linear_rbf(x, y, z, xi, yi):
    dist = distance_matrix(x,y, xi,yi)
    internal_dist = distance_matrix(x,y, x,y)
    weights = np.linalg.solve(internal_dist, z)
    zi =  np.dot(dist.T, weights)
    return zi


def scipy_idw(x, y, z, xi, yi):
    interp = Rbf(x, y, z, function='linear')
    return interp(xi, yi)

def distance_matrix(x0, y0, x1, y1):
    obs    = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T
    d0 = np.subtract.outer(obs[:,0], interp[:,0])
    d1 = np.subtract.outer(obs[:,1], interp[:,1])

    return np.hypot(d0, d1)


path        = arcpy.GetParameterAsText(0) # feature class points
field       = arcpy.GetParameterAsText(1) # Z- field
type_idw    = arcpy.GetParameterAsText(2) #'simple_idw','scipy_idw','linear_rbf'
Ras_path    = arcpy.GetParameterAsText(3) # raster
Num_row     = arcpy.GetParameterAsText(4) # int
num_columns = arcpy.GetParameterAsText(5) # int

data  = [[pt.X,pt.Y,row[1]] for row in arcpy.da.SearchCursor(path,['SHAPE@',field]) for pt in row[0] if row[1]]

if len(data) > 0:
    create_IDW(data,Ras_path,type_idw,Num_row,num_columns)
else:
    arcpy.AddMessage('No data Found in Point Layer')
