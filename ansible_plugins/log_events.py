from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    author: Paweł Tomaszek
    callback: log_events
    type: notification
    short_description: save playbook output to rest api
    description:
      - This callback save playbook output to prepared local rest api service
    requirements:
     - Whitelist in configuration is not necessary
     - Run local rest api service 
    options:
      callback_url:
        default: http://localhost:5000/events
        description: Post data to the api where log events will be saved.
'''

import json
import requests
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'log_events'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self, *args, **kwargs):
        super(CallbackModule, self).__init__()
        self.tasks = {}

    def v2_playbook_on_start(self, playbook):
        self.playbook = playbook

    def v2_playbook_on_play_start(self, play):
        self.play = play
        self.callback_url = 'http://localhost:5000/events'
        
    def v2_playbook_on_task_start(self, task, is_conditional):
        self.tasks[task._uuid] = task.name

    def v2_runner_on_ok(self, result):
        if (result._task.action == "command"):
          payload = { "state": "success", "name": result.task_name, "description": json.dumps(result._result) }
          r = requests.post(self.callback_url, json=payload)
          print(r.json())
        pass

    def v2_runner_on_failed(self, result, ignore_errors=False):
        payload = {"state": "failed", "name": result.task_name, "description": result._result['msg'] }
        r = requests.post(self.callback_url, json=payload)
        print(r.json())
        pass

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for host in hosts:
          print(stats.summarize(host))