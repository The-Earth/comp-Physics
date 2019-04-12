from collections import OrderedDict

area_list = list(open("ELIST.lis", 'r'))
areas = OrderedDict()

for i in range(len(area_list)):
    line_list = area_list[i].split()
    try:
        temp = int(line_list[0])
    except (ValueError, IndexError):
        continue

    index = line_list[0]
    point_1 = line_list[6]
    point_2 = line_list[7]
    point_3 = line_list[8]

    areas[int(index)] = (point_1, point_2, point_3)

position_list = list(open("NLIST.lis", 'r'))
positions = OrderedDict()

for j in range(len(position_list)):
    line_list = position_list[j].split()
    try:
        temp = int(line_list[0])
    except (ValueError, IndexError):
        continue

    index = line_list[0]
    x = line_list[1]
    y = line_list[2]
    z = line_list[3]

    positions[int(index)] = (x, y, z)

with open("MESH.DAT", "w") as dat:
    dat.write('TITLE = "Example: Variable and Connectivity List Sharing"\n')
    dat.write('VARIABLES = "X", "Y", "Z"\n')
    dat.write(f'ZONE, DATAPACKING=POINT, NODES={len(positions)}, ELEMENTS={len(areas)}, ZONETYPE=FETRIANGLE\n')
    for index in positions.keys():
        dat.write(f'{positions[index][0]} {positions[index][1]} {positions[index][2]}\n')
    dat.write('\n')
    for index in areas.keys():
        dat.write(f'{areas[index][0]} {areas[index][1]} {areas[index][2]}\n')
