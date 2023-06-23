#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess

SCRIPT_DIR = '$HOME/scripts/'

def run(command):
  call = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
  stdout = call.communicate()[0]
  return stdout.strip().decode('utf-8'), call.returncode

def run_script(command):
  return run(SCRIPT_DIR + command)

def i3_msg(type):
  ''' Executes i3-msg -t <type> and returns the parsed JSON output.  '''
  return json.loads(run(f'i3-msg -t {type}')[0])

def get_workspace():
  ''' Returns the node of the currently focused workspace. '''
  workspaces = i3_msg('get_workspaces')
  tree = i3_msg('get_tree')

  focused_num = next(
      (workspace['num'] for workspace in workspaces if workspace['focused']),
      None,
  )
  return next(
      (node for node in tree['nodes'][1]['nodes'][1]['nodes']
       if node['num'] == focused_num),
      None,
  )

# TODO remove a flag which one is the active window
def get_window_titles():
  ''' Returns an array of window titles of the current workspace.  '''

  expression = parse("$..window_properties.title")
  return [match.value for match in expression.find(get_workspace())]
