# i3-wm / Virtual Machine Integration
This project offers a seamless isolate tasks with the use of Virtual Machines
without giving up your window managers abilities.

## Overview
If you run i3-wm and you like the idea of working from a VM for isolation or
portability reasons, this is worth a look.

To get started, Run the vm_target_server.py somewhere. I sugguest running it on
startup.

Then, you can use the client tool to change targets, and execute tasks over
SSH with XFowarding.

```
# Run URXVT from the current target.
./vm_target_slave -r urxvt
```

## Integration
Add these directives into your i3 configuration file. Feel free to change the
keybindings to suite your taste.

```
## Change VM Targets
bindsym $mod+n exec ~/.scripts/vm_target_client.py -n
bindsym $mod+b exec ~/.scripts/vm_target_client.py -p

## Open Terminal on target VM
bindsym $mod+Return exec ~/.scripts/vm_target_client.py -r "urxvt"

## Open Dmenu on target VM
bindsym $mod+p exec "~/.scripts/vm_target_client.py -r dmenu_run"

## Start the VM Manager on startup
exec --no-startup-id "~/.scripts/vm_target_server.py"
```

## More Options
I have also created a module for py3status that will show the current VM in
your i3 status bar. You can find that module here.

https://github.com/en0/py3status/blob/master/py3status/modules/vm_target.py

More detail on py3status can be found at the project root.
