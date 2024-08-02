#Demo

'''
usage: Image_resizing_tiling.py [-h] [--warp] [--angle_range ANGLE_RANGE] [--tile] [--tile_size TILE_SIZE]
                                input_folder output_folder factors [factors ...]

Resize and optionally warp images by specified factors.

positional arguments:
  input_folder          Path to the folder containing input images
  output_folder         Path to the folder to store resized images
  factors               Resize factors (e.g. 2 4 6)

optional arguments:
  -h, --help            show this help message and exit
  --warp                If given, images will be warped to mimic human capture orientations
  --angle_range ANGLE_RANGE
                        Range of angles for random warping (default: 30 degrees)
  --tile                If given, warped images will be tiled
  --tile_size TILE_SIZE
                        Size of each tile (default: 256)
'''
