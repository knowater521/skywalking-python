#
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
#
import inspect
import time
import unittest
from os.path import dirname

import requests
from testcontainers.compose import DockerCompose

from tests.plugin import BasePluginTest


class TestPlugin(BasePluginTest):
    @classmethod
    def setUpClass(cls):
        cls.compose = DockerCompose(filepath=dirname(inspect.getfile(cls)))
        cls.compose.start()
        cls.compose.wait_for(cls.url(('consumer', '9090'), 'users?test=test1&test=test2&test2=test2'))

    def test_plugin(self):
        time.sleep(3)

        self.validate()
        response = requests.get(TestPlugin.url(('consumer', '9090'), 'users'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["correlation"], "correlation")


if __name__ == '__main__':
    unittest.main()
