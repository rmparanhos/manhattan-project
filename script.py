import shapefile
import json
from shapely.geometry import mapping, shape

def relationship_maker(row):
    with shapefile.Reader("nyc_mappluto_20v8_arc_shp/MapPLUTO.shp") as shp_2020:
        #print(shp_2020.fields)
        #print(shp.records()[0])
        #print(shp.record(0)['PolicePrct'])
        info = shp_2020.record(row)
        #print(info['Borough'])
        #print(info['Block'])
        #print(info['Address'])
        #print(info['BBL'])
        
        forma_pyshp = shp_2020.shape(row)
        #print(forma_pyshp.__geo_interface__)

        forma_shapely = shape(forma_pyshp.__geo_interface__)
        #print(forma_shapely)
        #print(forma_shapely.intersects(forma_shapely))
        block = info['Block']
        borough = info['Borough']
        print("2020{},{},{},{},2020".format(info['BBL'],info['Borough'],info['Block'],info['Address']))
        with shapefile.Reader("nyc_mappluto_21v3_shp/MapPLUTO.shp") as shp_2021:
#            print('')
            #print(shp_2021.fields)
            #print(shp.records()[0])
            #print(shp.record(0)['PolicePrct'])
            count = 0
            for item in shp_2021.records():
                if item['Block'] == block and item['Borough'] == borough:
#                    print(item['Borough'])
#                    print(item['Block'])
#                    print(item['Address'])
#                    print(item['BBL'])
#                    print("2021{},{},{},{},2021".format(item['BBL'],item['Borough'],item['Block'],item['Address']))
                    
                    forma_pyshp_aux = shp_2021.shape(count)
                    #print(forma_pyshp_aux.__geo_interface__)

                    forma_shapely_aux = shape(forma_pyshp_aux.__geo_interface__)
                    #print(forma_shapely_aux)
                    #print(forma_shapely.intersects(forma_shapely_aux))
                    if(forma_shapely.intersects(forma_shapely_aux)):
                        print("2020{},2021{}".format(info['BBL'],item['BBL']))
                count += 1    

def relationship_maker_by_block(block_number, borough_name):
    with shapefile.Reader("nyc_mappluto_20v8_arc_shp/MapPLUTO.shp") as shp_2020, shapefile.Reader("nyc_mappluto_21v3_shp/MapPLUTO.shp") as shp_2021, open('nodes.csv', 'a') as nodes_csv, open('edges.csv','a') as edges_csv:
        index = 0
        nodes_list = []
        for record_row in shp_2020.records():
            if record_row['Block'] == block_number and record_row['Borough'] == borough_name:
                forma_shapely = shape(shp_2020.shape(index).__geo_interface__)
                if "2020{}".format(record_row['BBL']) not in nodes_list:
                    nodes_list.append("2020{}".format(record_row['BBL']))
                    nodes_csv.write("2020{},{},{},{},2020\n".format(record_row['BBL'],record_row['Borough'],record_row['Block'],record_row['Address']))
                    print("2020{},{},{},{},2020".format(record_row['BBL'],record_row['Borough'],record_row['Block'],record_row['Address']))
                index_aux = 0
                for record_row_aux in shp_2021.records():
                    if record_row_aux['Block'] == block_number and record_row_aux['Borough'] == borough_name:
                        if "2021{}".format(record_row_aux['BBL']) not in nodes_list:
                            nodes_list.append("2021{}".format(record_row_aux['BBL']))
                            nodes_csv.write("2021{},{},{},{},2021\n".format(record_row_aux['BBL'],record_row_aux['Borough'],record_row_aux['Block'],record_row_aux['Address']))
                            print("2021{},{},{},{},2021".format(record_row_aux['BBL'],record_row_aux['Borough'],record_row_aux['Block'],record_row_aux['Address']))
                        forma_shapely_aux = shape(shp_2021.shape(index_aux).__geo_interface__)
                        if(forma_shapely.intersects(forma_shapely_aux)):
                            intersect_area = forma_shapely.intersection(forma_shapely_aux).area
                            if intersect_area > 0:
                                #registrando apenas intersecao com area maior q zero (estranho, mas o intersects ta dando true para intersecao com area zero)
                                edges_csv.write("2020{},2021{},{},{},{}\n".format(record_row['BBL'],record_row_aux['BBL'],intersect_area,forma_shapely.area/intersect_area, forma_shapely_aux.area/intersect_area))
                                print("2020{},2021{},{},{},{}".format(record_row['BBL'],record_row_aux['BBL'],intersect_area,forma_shapely.area/intersect_area, forma_shapely_aux.area/intersect_area))
                    index_aux += 1
            index += 1        
        

#relationship_maker(5)
#relationship_maker_by_block(16, 'MN')    
#rlationship_maker_by_block(17, 'MN')           
#relationship_maker_by_block(18, 'MN')
#relationship_maker_by_block(19, 'MN')
relationship_maker_by_block(22, 'MN')