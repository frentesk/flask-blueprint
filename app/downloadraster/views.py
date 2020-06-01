from flask import render_template,redirect,request,url_for,jsonify,current_app,make_response,send_file, send_from_directory,Response
from . import downloadraster
import os
import uuid
import json
import zipstream
import requests

@downloadraster.route('/downloadraster',methods=['get'])
def download_raster():
    return jsonify({'code':200,'msg':'ok','succ':True,"data":"hello world"})

