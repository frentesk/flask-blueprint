from flask import render_template,jsonify
from . import downloadraster

@downloadraster.app_errorhandler(404)
def page_not_found(e):
    return jsonify({'code':404,'msg':'error','succ':False,"data":""})

@downloadraster.app_errorhandler(500)
def internal_server_error(e):
    return  jsonify({'code':500,'msg':'error','succ':False,"data":""})

@downloadraster.app_errorhandler(405)
def method_not_allowed(e):
    return jsonify({'code':405,'msg':'error','succ':False,"data":""})

@downloadraster.app_errorhandler(400)
def method_not_allowed(e):
    return jsonify({'code':405,'msg':e,'succ':False,"data":""})