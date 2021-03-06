from flask import Flask, config, render_template
from nornir import InitNornir, init_nornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

app = Flask(__name__)


@app.route("/")
def test_homepage():
    return render_template("base.html")

@app.route("/newpage")
def new_page():
    return render_template("newpage.html")

@app.route("/hosts/inventory")
def get_all_inventory():
    nr = InitNornir("config.yaml")
    return render_template("inventory.html", my_list=nr.inventory.hosts.values())

@app.route("/all/running")
def get_running_config():
    nr = InitNornir("config.yaml")
    results = nr.run(task=send_command, command="show run")
    my_list = [v.scrapli_response.result for v in results.values()]
    return render_template("running.html", my_list=my_list)

@app.route("/all/version")
def get_version():
    nr = InitNornir(config_file="config.yaml")
    results = nr.run(task=send_command, command="show version")
    my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template("version.html", my_list=my_list)


@app.route("/hosts/<hostname>/version")
def get_host_version(hostname):
    nr = InitNornir(config_file="config.yaml")
    filtered = nr.filter(F(hostname=hostname))
    results = filtered.run(task=send_command, command="show version")
    my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template("version.html", my_list=my_list)

@app.route("/greetings")
def say_hello():
    return "Hello There"

if __name__ == "__main__":
    app.run(debug=True)