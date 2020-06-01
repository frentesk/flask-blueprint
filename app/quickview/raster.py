import arcpy
import os
import zipfile
import requests
import urllib
from urllib.parse import quote




def getRaster1(url,fileName,imageguids,selection_feature,ds_name,download_path,sde_file):
    print("arcpy is ok")
    #arcpy.env.workspace = download_path
    #arcpy.CreateFolder_management(arcpy.env.workspace, fileName)
    arcpy.CreateFolder_management(download_path, fileName)
    count = 0;
    where = ""
    for imageryguid in imageguids:
        if (count == 0):
            where += "imageryguid='" + imageryguid + "'"
        else:
            where += " or imageryguid='" + imageryguid + "'"
        count += 1
        downloadRasterWhere="imageryguid='" + imageryguid + "'"
        ##不标准代码
        print(downloadRasterWhere)
        print()
        url1=url.replace("https://xingyun.national-space.com/gxyh/rest/","http://xingyunserver.national-space.com:6080/arcgis/rest/")
        print(url1)
        print(ds_name)
        if ds_name=='DS_PSI':
            print("DS_type1")
            arcpy.DownloadRasters_management(url1,download_path+"/"+fileName, downloadRasterWhere,"", "", "", "", "","", "MAINTAIN_FOLDER")
        else:
            print("DS_type2")
            arcpy.ExportMosaicDatasetItems_management(sde_file+"/"+ds_name,download_path+"/"+fileName,"", downloadRasterWhere,"TIFF", "", "NONE","", "")

    arcpy.CreateFileGDB_management(download_path+"/"+fileName, "data", "Current")

    arcpy.ExportMosaicDatasetGeometry_management(sde_file+"/"+ds_name,
                                                 download_path+"/"+fileName+""+"/data.gdb/footprints",
                                                 where, "FOOTPRINT")
    copyQuickview(url,imageguids,fileName,download_path)
    #exportRaster(ds_name,where,fileName,download_path,sde_file)
    ZipRaster(download_path+"/"+fileName,download_path,fileName)
    print(fileName)

def exportRaster(ds_name,where,fileName,download_path,sde_file):
    output_prefix=""
    output_folder=download_path+"/"+fileName
    output_width=512
    output_height=512
    source_mosaic_dataset=sde_file+"/"+ds_name
    md_fields = arcpy.ListFields(source_mosaic_dataset)
    md_fields_set = set([field.baseName.upper() for field in md_fields])

    guid_field = 'IMAGERYGUID'
    if not ('IMAGERYGUID' in md_fields_set):
        guid_field = 'OID@'

    fields = ['OID@', 'SHAPE@', guid_field]

    with arcpy.da.SearchCursor(source_mosaic_dataset, fields, where) as cursor:
        for row in cursor:
            objectid = row[0]
            extent = row[1].extent
            guid = str(row[2])
            where_clause = '"OBJECTID" = %d' % int(objectid)
            process_md_layer = 'process_md_layer_' + guid

            env_overwriteOutput = arcpy.env.overwriteOutput
            arcpy.env.overwriteOutput = True
            if output_prefix == '#' or not output_prefix:
                output_preview_path = os.path.join(output_folder, guid + '.jpg')
            else:
                output_preview_path = os.path.join(output_folder, '%s_%s.jpg' % (output_prefix, guid))

            output_cell_size = max(extent.width / output_width, extent.height / output_height)

            XCenter = (extent.XMax + extent.XMin) / 2.0
            YCenter = (extent.YMax + extent.YMin) / 2.0

            XMin = XCenter - output_width / 2.0 * output_cell_size
            XMax = XMin + output_width * output_cell_size

            YMin = YCenter - output_height / 2.0 * output_cell_size
            YMax = YMin + output_height * output_cell_size

            extent = arcpy.Extent(XMin, YMin, XMax, YMax)

            arcpy.MakeMosaicLayer_management(source_mosaic_dataset,
                                             process_md_layer,
                                             where_clause,
                                             extent,
                                             "1;2;3",
                                             "LOCK_RASTER",
                                             "",
                                             "",
                                             objectid,
                                             "ASCENDING",
                                             "FIRST",
                                             output_cell_size)
            env = {}

            if 'compression' in arcpy.env.keys():
                env['compression'] = arcpy.env.compression

            if 'rasterStatistics' in arcpy.env.keys():
                env['rasterStatistics'] = arcpy.env.rasterStatistics

            if 'pyramid' in arcpy.env.keys():
                env['pyramid'] = arcpy.env.pyramid

            if 'tileSize' in arcpy.env.keys():
                env['tileSize'] = arcpy.env.tileSize

            if 'nodata' in arcpy.env.keys():
                env['nodata'] = arcpy.env.nodata

            if 'extent' in arcpy.env.keys():
                env['extent'] = arcpy.env.extent

            arcpy.env.compression = "'JPEG_YCbCr' 75"
            arcpy.env.tileSize = "128 128"
            arcpy.env.rasterStatistics = "NONE"
            arcpy.env.pyramid = "NONE"
            arcpy.env.nodata = 'NONE'  # 'MAXIMUM' MAP_DOWN
            arcpy.env.extent = extent

            arcpy.CopyRaster_management(process_md_layer,
                                        output_preview_path,
                                        '#',
                                        '255',
                                        '255',
                                        '#',
                                        '#',
                                        '8_BIT_UNSIGNED',
                                        'ScalePixelValue',
                                        '#')

            if 'compression' in env.keys():
                arcpy.env.compression = env['compression']

            if 'rasterStatistics' in env.keys():
                arcpy.env.rasterStatistics = env['rasterStatistics']

            if 'pyramid' in env.keys():
                arcpy.env.pyramid = env['pyramid']

            if 'tileSize' in env.keys():
                arcpy.env.tileSize = env['tileSize']

            if 'nodata' in env.keys():
                arcpy.env.nodata = env['nodata']

            if 'extent' in env.keys():
                arcpy.env.extent = env['extent']

            # restore env variable
        arcpy.env.overwriteOutput = env_overwriteOutput

def ZipRaster(downloadDirectory,ZipDirectory,zipName):
    f = zipfile.ZipFile(ZipDirectory+"/"+zipName+".zip", 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(downloadDirectory):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()


def copyQuickview(url,imageguids,fileName,download_path):
    try:
        url1 = url.replace("ImageServer?", "ImageServer") + "/query"
        for imageguid in imageguids:
            where = "imageryguid='" + imageguid + "'";
            print(where)
            data = {
                "where": where,
                "geometryType": "esriGeometryEnvelope",
                "spatialRel": "esriSpatialRelIntersects",
                "outFields": "updatetaskguid",
                "returnIdsOnly": "false",
                "returnCountOnly": "false",
                "returnDistinctValues": "false",
                "returnTrueCurves": "false",
                "returnGeometry": "false",
                "f": "pjson"
            }
            print(url1)
            res = requests.post(url=url1, data=data)
            out_json = res.json()
            updatetaskguid = out_json['features'][0]['attributes']['updatetaskguid']
            fileName = download_img("http://192.168.128.50:8033/quickview/" + quote(updatetaskguid,'utf-8') + "/" +  quote(imageguid,'utf-8') + ".png", fileName,
                         imageguid, download_path)
            # download_img("https://img.ithome.com/newsuploadfiles/2020/3/20200331_081532_515.jpg",fileName,imageguid,download_path)
            return fileName
    except:
        return "failed"

def download_img(img_url,fileName,imageguid,download_path):
    print(img_url)
    request = urllib.request.Request(img_url)
    try:
        response = urllib.request.urlopen(request)
        img_name = imageguid+".jpg"
        filename = download_path+"/"+ fileName+"/"+img_name
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read()) # 将内容写入图片
            return filename
    except:
        return "failed"

#copyQuickview("","")
#exportRaster("DS_PSI","imageryguid='{721BD180-284D-11EA-B716-F85971C10C15}'","4828c604-dd85-463d-b1b0-ee2d85202b1c","D://datashare/downloadFolder")

