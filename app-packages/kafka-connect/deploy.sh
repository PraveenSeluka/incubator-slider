#! /bin/bash

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
export HADOOP_CONF_DIR=/usr/lib/hadoop2/etc/hadoop/
export PATH=$PATH:~/src/incubator-slider/slider-assembly/target/slider-0.91.0-incubating-SNAPSHOT-all/slider-0.91.0-incubating-SNAPSHOT/bin/

APPNAME=${1:-kc}
rm slider-kafka-connect-package-1.0.0.zip
zip -r slider-kafka-connect-package-1.0.0.zip .
slider install-package --replacepkg --name KC --package slider-kafka-connect-package-1.0.0.zip
slider stop $APPNAME
slider destroy --force $APPNAME
slider create $APPNAME  --template appConfig-default.json --resources resources-default.json
