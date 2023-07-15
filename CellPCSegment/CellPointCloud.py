import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class CellPointCloud:
    def __init__(self, pointcloud):
        self.pointcloud = np.array(pointcloud)

        #ensure Nx3 or Nx2
        if not self.pointcloud.shape[1] in [2,3]:
            self.pointcloud = self.pointcloud.T

        self.max = np.max(self.pointcloud, axis=0)
        self.min = np.min(self.pointcloud, axis=0)

        
    def save_2d_image(self, path, scaleFactor=10, dpi=96):
        w, h = np.abs(self.max - self.min)
        iw, ih = w/scaleFactor, h/scaleFactor
        print(f'Pointcloud width: {w}, height {h}')
        print(f'With scaleFactor {scaleFactor}, Image width: {iw}, height {ih}')
        iw, ih = iw/dpi, ih/dpi

        fig = plt.figure(frameon=False)
        fig.set_size_inches(iw,ih)
        ax = plt.Axes(fig, [0., 0., 1., 1.], )
        ax.set_axis_off()
        fig.add_axes(ax)

        scatter = plt.plot(self.pointcloud[:,0], self.pointcloud[:,1], '.')

        #ax = fig.axes[0]
        #ax.


        fig.savefig(path, format='png', dpi=dpi,  bbox_inches='tight')
        plt.close(fig)

