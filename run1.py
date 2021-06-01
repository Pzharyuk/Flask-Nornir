from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir("config.yaml")

# for data in nr.inventory.hosts.values():
#     print(data.hostname)

results = nr.run(task=send_command, command="show version")
my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
print(my_list)