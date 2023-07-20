import numpy as np

from PIL import Image
from PIL.PngImagePlugin import PngInfo

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

    #lower dpi will improve the accuracy of the translation, but make it harder to annotate. Currently the inaccuracy is ~0.1%     
    def save_2d_image(self, path, scaleFactor=10, dpi=72, test=False):
        w, h = np.abs(self.max - self.min)
        iw, ih = w/scaleFactor, h/scaleFactor
        xlim = [self.min[0], self.max[0]]
        ylim = [self.min[1], self.max[1]]
        print(f'Pointcloud width: {w}, height {h}')
        iw, ih = (w/dpi)/scaleFactor, (h/dpi)/scaleFactor #reduce inaccuracy, divide by the larger number first
        
        print(f'With scaleFactor {scaleFactor}, Image width: ~{np.floor(iw*dpi)}, height ~{np.floor(ih*dpi)}')
        print(f'With limits of x: {xlim}, y: {ylim}')

        fig = plt.figure()
        fig.set_size_inches(iw,ih) #need for the required resolution size
        ax = plt.Axes(fig, [0., 0., 1., 1.], ) #need next 3 to remove white border
        ax.set_axis_off()
        fig.add_axes(ax)



        scatter = plt.plot(self.pointcloud[:,0], self.pointcloud[:,1], '.', markersize=1, antialiased=True)

        #place a test cloud ta a specific location to test accuracy of localization in image
        if test:
            testcloud = []
            testrange = [10000, 10050]
            for x in range(testrange[0], testrange[1]):
                for y in range(testrange[0], testrange[1]):
                    testcloud.append([x,y])
            testcloud = np.array(testcloud)

            print(f'a red test cloud should be found within x range of {(testrange[0] - xlim[0])/scaleFactor} -> {(testrange[1] - xlim[0])/scaleFactor} and y range of {(testrange[0] - ylim[0])/scaleFactor} -> {(testrange[1] - ylim[0])/scaleFactor}')
            plt.plot(testcloud[:,0], testcloud[:,1], '.', markersize=1, antialiased=True, markerfacecolor='r')

        #also need the next 2 for removing border
        plt.xlim(xlim)
        plt.ylim(ylim)


        fig.savefig(path, format='png', dpi=dpi, pad_inches=0.0, facecolor='black')#,  bbox_inches='tight')#, pad_inches=0.0)
        
        #add metadata, doing so with matplotlib is annoying to read
        metadata = PngInfo()
        metadata.add_text("scalefactor", str(scaleFactor))

        targetImage = Image.open(path)
        targetImage.save(path, pnginfo=metadata)
        
        plt.close(fig)

    
    def convert_points_img_to_pc(self, dim1, dim2, scalefactor):
        minD1, minD2 = self.min
        dim1 = dim1*scalefactor + minD1
        dim2 = dim2*scalefactor + minD2
        return int(dim1), int(dim2)

    def convert_points_pc_to_img(self, dim1, dim2, scalefactor):
        minD1, minD2 = self.min
        dim1 = (dim1 - minD1)/scalefactor
        dim2 = (dim2 - minD2)/scalefactor
        return int(dim1), int(dim2)

    def split_into_bf(self, seg_mask, scalefactor):
        #seg_mask = np.flip(seg_mask, axis=0)

        new_pointcloud = []
        for point in self.pointcloud[:,:2]:
            dim1, dim2 = point

            dim1, dim2 = self.convert_points_pc_to_img(dim1, dim2, scalefactor)
            if seg_mask[dim2-1, dim1-1] > 0:
                new_pointcloud.append(point)

        return np.array(new_pointcloud)

        


