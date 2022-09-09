import io
import os
from pathlib import Path

METATILE = 8

XYs = []
for i in range(0,METATILE):
    for j in range(0,METATILE):
        XYs.append([i, j])

def list_existing_tiles_in_meta(directory='/var/lib/mod_tile/', map='default'):
    """
    List tiles using x,yz scheme from meta file directory
    """
    # List available meta tiles and write the stdout to "file"
    p = Path(os.path.join(directory, map))
    metas = [str(meta.relative_to(p)).replace('.meta', '') for meta in p.rglob('*.meta')]
    with io.open('/tmp/list_tiles.txt', 'wb') as outfile:
        for meta in metas:
            outfile.write('\n'.join(meta_to_xyz_all(*meta_to_xyz(meta))) + '\n')

def meta_to_xyz(pattern_meta_with_zoom='6/0/0/0/50/136'):
    """
    Convert meta tiles to z x y scheme for mod_tile
    Author: Thomas Gratier based on Frederik Ramm C code from meta2tile.c from mod_tile
    License: GPL
    """
    x, y = 0, 0
    path_elements = [int(i) for i in pattern_meta_with_zoom.split('/')]
    z = path_elements.pop(0)
    for i in path_elements:
        x <<= 4
        y <<= 4
        x |= (i & 0xf0) >> 4
        y |= (i & 0x0f)
    return z, x, y

def meta_to_xyz_all(z, x, y):
    tiles_xyz = ['/'.join([str(z), str(x + mx), str(y + my)]) for (mx, my) in XYs]
    return tiles_xyz

# Test this script
print(meta_to_xyz('14/0/18/85/254/136'))
