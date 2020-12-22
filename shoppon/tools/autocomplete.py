import sys
import json
import argparse

from fuzzywuzzy import process

parser = argparse.ArgumentParser(description="Set clipboard")
parser.add_argument("-k", "--key", help="keywords")
args = parser.parse_args()


EXEC_CMD = "kubectl exec -it $(kubectl get po -n openstack|grep %s|head -n 1|awk '{print $1}'|xargs -L 1) -n openstack -- bash"
LOG_CMD = "kubectl logs $(kubectl get po -n openstack|grep %s|head -n 1|awk '{print $1}'|xargs -L 1) -n openstack|tail -n 20"
GET_PO_CMD = "kubectl get po -n openstack|grep %s"
DESCRIBE_CMD = "kubectl describe po -n openstack $(kubectl get po -n openstack|grep %s|head -n 1|awk '{print $1}'|xargs -L 1)"

SOURCES = {
    'cd_user': 'admin@example.org',
    'cd_pwd': 'Admin@ES20!8',
    'mail_pwd': 'xp@es223',
}

for po in ('busybox', 'fluentd', 'volume', 'compute'):
    SOURCES['k8s_get_' + po] = GET_PO_CMD % po
    SOURCES['k8s_exec_' + po] = EXEC_CMD % po
    SOURCES['k8s_log_' + po] = LOG_CMD % po
    SOURCES['k8s_describe_' + po] = DESCRIBE_CMD % po


def main():
    matches = process.extractBests(args.key, SOURCES.keys())

    sys.stdout.write(json.dumps({
        "items": [{
            "uid": m[1],
            "type": "file",
            "title": m[0],
            "arg": SOURCES[m[0]],
            "subtitle": SOURCES[m[0]]
        } for m in matches]
    }))


if __name__ == '__main__':
    main()
