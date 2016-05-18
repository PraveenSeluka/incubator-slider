# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys
import os
import inspect
import pprint
import util
from resource_management import *

logger = logging.getLogger()

class Kafka(Script):
  def install(self, env):
    self.install_packages(env)

  def configure(self, env):
    import params
    env.set_params(params)

  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)
    import subprocess
    subprocess.call('rm /tmp/connect.properties',shell=True)
    cmd = "sed 's/xxxx/" + str(params.port) + "/' /Users/ps/src/kafka/config/connect-distributed.properties > /tmp/connect.properties"
    subprocess.call(cmd,shell=True)
    process_cmd=format('/Users/ps/src/kafka/bin/connect-distributed.sh /tmp/connect.properties >/tmp/connect.log')
    Execute(process_cmd,
        user=params.app_user,
        logoutput=True,
        wait_for_finish=False,
        pid_file=params.pid_file
    )

  def stop(self, env):
    import params
    env.set_params(params)
    pid = format("`cat {pid_file}` >/dev/null 2>&1")
    #ex = "ps -ef | grep `cat {pid_file}` | grep Connect | awk '{print $2}' >/dev/null 2>&1"
    #connect_pid = Execute(format(ex),user=params.app_user)
    Execute(format("pkill -TERM -P {pid}"),
      user=params.app_user
    )
    Execute(format("pkill -kill -P {pid}"),
      ignore_failures=True,
      user=params.app_user
    )
    Execute(format("rm -f {pid_file}"),
      user=params.app_user)

  def status(self, env):
    import status_params
    env.set_params(status_params)
##    jps_cmd = format("{java64_home}/bin/jps")
##    no_op_test = format("ls {pid_file} >/dev/null 2>&1 && ps `cat {pid_file}` >/dev/null 2>&1")
##    cmd = format("echo `{jps_cmd} | grep Kafka | cut -d' ' -f1` > {pid_file}")
##    Execute(cmd, not_if=no_op_test)
    check_process_status(status_params.pid_file)

if __name__ == "__main__":
  Kafka().execute()
