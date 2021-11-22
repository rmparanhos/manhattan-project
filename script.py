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


relationship_maker(5)               