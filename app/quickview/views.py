from flask import render_template,redirect,request,url_for,jsonify,current_app,make_response,send_file, send_from_directory,Response
from . import quickview
import os
import uuid
import json
# import zipstream
import requests

@quickview.route('/downloadraster',methods=['POST'])
def download_raster():
    img_url=request.json['img_url']
    img_imageryguids=request.json['img_guids']
    ds_name=request.json['ds_name']

    print(img_url)
    print((img_imageryguids))
    print(ds_name)

    count=0;
    sWhere=""
    for imageryguid in img_imageryguids:
        if(count==0):
            sWhere+="imageryguid='"+imageryguid+"'"
        else:
            sWhere +=" or imageryguid='"+imageryguid+"'"
        count+=1
    print(sWhere)
    radom=str(uuid.uuid4())
    print(current_app.config.get('DOWNLOAD_PATH'))
    download_path=current_app.config.get('DOWNLOAD_PATH')
    sde_file = current_app.config.get('SDE_FILE')
	
    from . import raster
    raster.getRaster1(img_url, radom,
                    img_imageryguids, "312",ds_name,download_path,sde_file)
    pp=0
    data1=download_path+"\\"+radom
    data2=u"http://"+current_app.config.get('SERVERNAME')+":"+str(current_app.config.get('PORT'))+"/downloadraster/"+radom+".zip"
    return jsonify({'code':200,'msg':'ok','succ':True,"data":[data1,data2]})

@downloadraster.route('/downloadraster/<filename>',methods=['get'])
def get_raster(filename):
    directory = os.getcwd()  # 假设在当前目录
    print(directory)
    directory=current_app.config.get('DOWNLOAD_PATH')
    print(directory)
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@downloadraster.route('/quickview/<taskguid>/<imageguid>',methods=['get'])
def get_pic(taskguid,imageguid):
    directory = os.getcwd()  # 假设在当前目录
    print(directory)
    quickviewDirectory = current_app.config.get('QUICKVIEWPATH')
    directory=quickviewDirectory+"\\"+taskguid
    filename=imageguid;
    print(directory)
    imagePath=directory+"\\"+imageguid;
    response = make_response(send_from_directory(directory, filename, as_attachment=False))
    response.headers['Content-Type'] = 'image/png'
    #response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@downloadraster.route('/quickview_8/<taskguid>/<imageguid>', methods=['get'])
def get_pic2(taskguid,imageguid):
    quickviewDirectory = current_app.config.get('QUICKVIEWPATH')
    directory=quickviewDirectory+"\\"+taskguid
    filename=imageguid[0:-4]
    print("filename:"+filename)
    print(directory)
    imagePath=directory+"\\"+filename+"_8.png"
    if(not (os.path.isfile(imagePath))):
        from . import png
        png.ToPng8(directory,filename)
    filename1 = filename + "_8.png"
    response = make_response(send_from_directory(directory, filename1, as_attachment=False))
    response.headers['Content-Type'] = 'image/png'
    return response


# @downloadraster.route('/downloadraster/package.zip',methods=['get'])
# def downlaod_zip():
#     z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
#     z.write(r'D:\1workstation\成都环保\最终文档\5、项目文档\4、部署方案\成都市环境保护信息中心环境GIS数据加工服务采购项目 系统部署记录.docx')
#     z.write(r'\\10.10.10.182\datastore\测试数据\GF-1\GF1_WFV3_E101.0_N28.9_20190330_L1A0003914059\GF1_WFV3_E101.0_N28.9_20190330_L1A0003914059.tiff')
#
#     response = Response(z, mimetype='application/zip')
#     response.headers['Content-Disposition'] = 'attachment; filename={}'.format('files.zip')
#     return response
