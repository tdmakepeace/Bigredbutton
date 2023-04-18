#!/bin/bash

#starts a new tmux session and start the inner_run_script
tmux new -d -s ELK './inner_run.sh'

#comment out if you want to run in the back ground.
tmux att -t ELK

# cntl+b then d to jump out the window but leave it running.


