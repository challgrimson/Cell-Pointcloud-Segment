from CellPCSegment import CellPointCloud
from CellPCSegment.utils import GSDAsciiReader


path = r'/mnt/c/Users/chris/Documents/MSc/Cell-Pointcloud-Segment/ExampleData/Cav1.ascii'
savepath  = r'/mnt/c/Users/chris/Documents/MSc/Cell-Pointcloud-Segment/ExampleData/Cav1Example10.png'

GSDreader = GSDAsciiReader()
rawCellData = GSDreader.read(path)
print('Data shape: ', rawCellData.shape)
print('Reading')
Cell = CellPointCloud(rawCellData)

print('Saving')
Cell.save_2d_image(savepath, scaleFactor=10, dpi=96, test=False)

