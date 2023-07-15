from CellPCSegment import CellPointCloud
from CellPCSegment.utils import GSDAsciiReader


path = r'/mnt/c/Users/chris/Documents/MSc/Cell-Pointcloud-Segment/ExampleData/Cav1.ascii'
savepath  = r'/mnt/c/Users/chris/Documents/MSc/Cell-Pointcloud-Segment/ExampleData/Cav1ExampleSave.png'

GSDreader = GSDAsciiReader()
rawCellData = GSDreader.read(path)

print('Reading')
Cell = CellPointCloud(rawCellData)

print('Saving')
Cell.save_2d_image(savepath)