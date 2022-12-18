from objects.RServer import RServer
from objects.RResponse import RResponse
from objects.RTask import RTask

app = RServer.getServer().getFlaskBluePrint()


@app.route("/task/stop/<tid>", methods=["GET"])
def stop_task(tid):
    tid = int(tid)
    print(tid)
    try:
        RTask.exit_task(tid)
    except ValueError as e:
        RResponse.abort(400, f"Task({tid}) not in list")
    return RResponse.ok(f"Task({tid}) has been stopped")