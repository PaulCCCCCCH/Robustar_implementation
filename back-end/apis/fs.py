from flask import request
from objects.RServer import RServer
from objects.RResponse import RResponse
from objects.RTask import RTask
import os
import os.path as osp
import shutil

server = RServer.getServer()
dataManager = server.getDataManager()
bp = server.getFlaskBluePrint()
app = server.getFlaskApp()

baseDir = server.baseDir
datasetDir = server.datasetDir
ckptDir = server.ckptDir


def fileOpWrapper(fileOp):
    try:
        return RResponse.ok(fileOp())
    except Exception as e:
        return RResponse.fail(e)


@bp.route("/fs/ls/<path>", methods=["GET"])
def ls(path):
    return fileOpWrapper(lambda: os.listdir(osp.join(baseDir, path)))

@bp.route("/fs/dirlen/<path>", methods=["GET"])
def dirlen(path):
    return fileOpWrapper(lambda: os.listdir(osp.join(baseDir, path)))

@bp.route("/fs/exist/<path>", methods=["GET"])
def exist(path):
    return fileOpWrapper(lambda: osp.exists(osp.join(baseDir, path)))
    
@bp.route("/fs/rm/<path>", methods=["GET"])
def rm(path):
    target = osp.join(baseDir, path)
    def fileOp():
        if osp.isdir(target):
            return os.removedirs(target)
        return os.remove(target)
    return fileOpWrapper(fileOp)

@bp.route("/fs/mkdir/<path>", methods=["GET"])
def mkdir(path):
    return fileOpWrapper(lambda: os.mkdir(osp.join(baseDir, path)))


@bp.route("/fs/mkdirs/<path>", methods=["GET"])
def mkdirs(path):
    return fileOpWrapper(lambda: os.makedirs(osp.join(baseDir, path), exist_ok=True))


@bp.route("/fs/cp", methods=["POST"])
def cp():
    json_data = request.get_json()
    def fileOp():
        src_path = osp.join(json_data['from'])
        dst_path = osp.join(json_data['to'])
        return shutil.copyfile(src_path, dst_path)

    return fileOpWrapper(fileOp)


@bp.route("/fs/read/<path>/<length>", methods=["GET"])
def read(path, length):
    target = osp.join(baseDir, path)
    def fileOp():
        with open(target, 'wb') as f:
            data = f.read() if length == 0 else f.read(length)
        return data

    return fileOpWrapper(fileOp)

@bp.route("/fs/write/<path>", methods=["POST"])
def write(path):
    target = osp.join(baseDir, path)
    json_data = request.get_json()
    data = json_data['data']
    append = 'append' in json_data
    def fileOp():
        mode = 'ab' if append else 'wb'
        with open(target, mode) as f:
            return f.write(data)
        
    return fileOpWrapper(fileOp)


# TODO: Registering this function somehow closes DB immediatly after server startup.
# @app.teardown_appcontext
def close_connection(exception):
    conn = dataManager.get_db_conn()
    if conn is not None:
        conn.close()