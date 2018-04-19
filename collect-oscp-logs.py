#!/usr/bin/env python

import sys
import time
import subprocess

log_location = "/var/log/oscp-logs"

def main():

  try:
    old_user = subprocess.check_output([
      "oc",
      "whoami"
    ]).strip()
    print("was logged in as {0}, logging in as system:admin".format(old_user))
    subprocess.check_output([
      "oc",
      "login",
      "-u",
      "system:admin"
    ])
    oc_output = subprocess.check_output([
      "oc",
      "get",
      "pods",
      "--all-namespaces"
    ])
  except subprocess.CalledProcessError:
    print("failed to get pods")
    sys.exit(0)

  pods = oc_output.split("\n")[1:]

  for pod in pods:
    if pod:
      pod = " ".join(pod.split())
      row = pod.split(" ")
      namespace = row[0]
      pod = row[1]

      cmd = [
        "oc",
        "logs",
        pod,
        "--namespace={0}".format(namespace)
      ]
      filename = time.strftime(
        '{0}/%Y-%m-%d-%H-%M-%S_{1}_{2}'.format(
          log_location,namespace, pod
      ))

      print("processing pod {0} in namespace {1}".format(
        pod,
        namespace
      ))

      try:
        log_out = subprocess.check_output(cmd)
        with open(filename, 'w') as logfile:
          logfile.write(log_out)
      except subprocess.CalledProcessError:
        print("failed to get logs")

  try:
    print("logging back in as {0}".format(old_user))
    subprocess.check_output([
      "oc",
      "login",
      "-u",
      old_user
    ])
  except subprocess.CalledProcessError:
    print("failed to login as old user")

  sys.exit(0)


if __name__ == '__main__':
  main()
