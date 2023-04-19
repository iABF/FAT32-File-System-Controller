# FAT32-File-System-Controller
**Target:** Control FAT32 File System as a shell.

**Language:** Python 3.7.5

**Allowed Commands:**
* ls
* ls -l
* pwd
* cd \<DIR\>
* mkdir \<DIRNAME\>
* file \<FILENAME\>
* tree

## Example
```
D:\Program\Python\FAT32\venv\Scripts\python.exe D:/Program/Python/FAT32/main.py
{'sizeofSector': 512, 'SectorPerCluster': 1, 'NumberOfReservedSector': 32, 'NumberOfSector': 204800, 'SectorPerFAT': 1576, 'ClusterNumberOfRootDir': 2}
{'FAT1Offset': 16384, 'FAT2Offset': 823296, 'RootDirOffset': 1630208, 'sizeofDir': 32, 'sizeofCluster': 512, 'NumberOfDirInCluster': 16, 'AvailableClusterNumberInFAT': 201726}
**************************** Welcome to FAT32 ****************************
[iABF@FAT32] » ls
init.d
[iABF@FAT32] » cd init.d
[iABF@FAT32] » ls
.	..	acpid	alsa-utils	anacron	apparmor	apport	avahi-daemon	bluetooth	console-setup.sh
cron	cups	cups-browsed	dbus	dns-clean	gdm3	grub-common	hwclock.sh	irqbalance	kerneloops
keyboard-setup.sh	kmod	network-manager	networking	plymouth	plymouth-log	pppd-dns	procps	rsync	rsyslog
saned	speech-dispatcher	spice-vdagent	udev	ufw	unattended-upgrades	uuidd	whoopsie	x11-common	iABF
test
[iABF@FAT32] » mkdir test2
[iABF@FAT32] » ls
.	..	acpid	alsa-utils	anacron	apparmor	apport	avahi-daemon	bluetooth	console-setup.sh
cron	cups	cups-browsed	dbus	dns-clean	gdm3	grub-common	hwclock.sh	irqbalance	kerneloops
keyboard-setup.sh	kmod	network-manager	networking	plymouth	plymouth-log	pppd-dns	procps	rsync	rsyslog
saned	speech-dispatcher	spice-vdagent	udev	ufw	unattended-upgrades	uuidd	whoopsie	x11-common	iABF
test	test2
[iABF@FAT32] » cd test2
[iABF@FAT32] » ls
.	..
[iABF@FAT32] » mkdir 1712874
[iABF@FAT32] » ls
.	..	1712874
[iABF@FAT32] » cd 1712874
[iABF@FAT32] » mkdir CHANGKUO
[iABF@FAT32] » ls
.	..	CHANGKUO
[iABF@FAT32] » cd ..
[iABF@FAT32] » ls
.	..	1712874
[iABF@FAT32] » cd .
[iABF@FAT32] » ls
.	..	1712874
[iABF@FAT32] » cd ..
[iABF@FAT32] » ls
.	..	acpid	alsa-utils	anacron	apparmor	apport	avahi-daemon	bluetooth	console-setup.sh
cron	cups	cups-browsed	dbus	dns-clean	gdm3	grub-common	hwclock.sh	irqbalance	kerneloops
keyboard-setup.sh	kmod	network-manager	networking	plymouth	plymouth-log	pppd-dns	procps	rsync	rsyslog
saned	speech-dispatcher	spice-vdagent	udev	ufw	unattended-upgrades	uuidd	whoopsie	x11-common	iABF
test	test2
[iABF@FAT32] » file console-setup.sh
#!/bin/sh
### BEGIN INIT INFO
# Provides:          console-setup.sh
# Required-Start:    $remote_fs
# Required-Stop:
# Should-Start:      console-screen kbd
# Default-Start:     2 3 4 5
# Default-Stop:
# X-Interactive:     true
# Short-Description: Set console font and keymap
### END INIT INFO

if [ -f /bin/setupcon ]; then
    case "$1" in
        stop|status)
        # console-setup isn't a daemon
        ;;
        start|force-reload|restart|reload)
            if [ -f /lib/lsb/init-functions ]; then
                . /lib/lsb/init-functions
            else
                log_action_begin_msg () {
	            echo -n "$@... "
                }

                log_action_end_msg () {
	            if [ "$1" -eq 0 ]; then
	                echo done.
	            else
	                echo failed.
	            fi
                }
            fi
            log_action_begin_msg "Setting up console font and keymap"
            if /lib/console-setup/console-setup.sh; then
	        log_action_end_msg 0
	    else
	        log_action_end_msg $?
	    fi
	    ;;
        *)
            echo 'Usage: /etc/init.d/console-setup {start|reload|restart|force-reload|stop|status}'
            exit 3
            ;;
    esac
fi
                                                                                                                                                                                                                                                                                                                
[iABF@FAT32] » pwd
/init.d
[iABF@FAT32] » cd test2
[iABF@FAT32] » pwd
/init.d/test2
[iABF@FAT32] » cd ..
[iABF@FAT32] » cd ..
[iABF@FAT32] » ls
init.d
[iABF@FAT32] » pwd
/
[iABF@FAT32] » cd init.d
[iABF@FAT32] » ls -l
00010000 13:13:16    DEC  25  2019          0  .
00010000 13:13:16    DEC  25  2019          0  ..
00100000 13:13:16    DEC  25  2019       2269  acpid
00100000 13:13:16    DEC  25  2019       5336  alsa-utils
00100000 13:13:16    DEC  25  2019       2014  anacron
00100000 13:13:16    DEC  25  2019       4335  apparmor
00100000 13:13:16    DEC  25  2019       2802  apport
00100000 13:13:16    DEC  25  2019       2401  avahi-daemon
00100000 13:13:16    DEC  25  2019       2968  bluetooth
00100000 13:13:16    DEC  25  2019       1232  console-setup.sh
00100000 13:13:16    DEC  25  2019       3049  cron
00100000 13:13:16    DEC  25  2019       2804  cups
00100000 13:13:16    DEC  25  2019       1961  cups-browsed
00100000 13:13:16    DEC  25  2019       2813  dbus
00100000 13:13:16    DEC  25  2019       1172  dns-clean
00100000 13:13:16    DEC  25  2019       3033  gdm3
00100000 13:13:16    DEC  25  2019        985  grub-common
00100000 13:13:16    DEC  25  2019       3809  hwclock.sh
00100000 13:13:16    DEC  25  2019       2444  irqbalance
00100000 13:13:16    DEC  25  2019       3131  kerneloops
00100000 13:13:16    DEC  25  2019       1479  keyboard-setup.sh
00100000 13:13:16    DEC  25  2019       2044  kmod
00100000 13:13:16    DEC  25  2019       1942  network-manager
00100000 13:13:16    DEC  25  2019       4597  networking
00100000 13:13:16    DEC  25  2019       1366  plymouth
00100000 13:13:16    DEC  25  2019        752  plymouth-log
00100000 13:13:16    DEC  25  2019        612  pppd-dns
00100000 13:13:16    DEC  25  2019       1191  procps
00100000 13:13:16    DEC  25  2019       4355  rsync
00100000 13:13:16    DEC  25  2019       2864  rsyslog
00100000 13:13:16    DEC  25  2019       2333  saned
00100000 13:13:16    DEC  25  2019       2117  speech-dispatcher
00100000 13:13:16    DEC  25  2019       2484  spice-vdagent
00100000 13:13:16    DEC  25  2019       5974  udev
00100000 13:13:16    DEC  25  2019       2083  ufw
00100000 13:13:16    DEC  25  2019       1391  unattended-upgrades
00100000 13:13:16    DEC  25  2019       1306  uuidd
00100000 13:13:16    DEC  25  2019        485  whoopsie
00100000 13:13:16    DEC  25  2019       2757  x11-common
00010000 19:39:40    DEC  28  2019          0  iABF
00010000 21:17:28    DEC  28  2019          0  test
00010000 21:18:20    DEC  28  2019          0  test2
[iABF@FAT32] » cd ..
[iABF@FAT32] » tree
* init.d
|-* acpid
|-* alsa-utils
|-* anacron
|-* apparmor
|-* apport
|-* avahi-daemon
|-* bluetooth
|-* console-setup.sh
|-* cron
|-* cups
|-* cups-browsed
|-* dbus
|-* dns-clean
|-* gdm3
|-* grub-common
|-* hwclock.sh
|-* irqbalance
|-* kerneloops
|-* keyboard-setup.sh
|-* kmod
|-* network-manager
|-* networking
|-* plymouth
|-* plymouth-log
|-* pppd-dns
|-* procps
|-* rsync
|-* rsyslog
|-* saned
|-* speech-dispatcher
|-* spice-vdagent
|-* udev
|-* ufw
|-* unattended-upgrades
|-* uuidd
|-* whoopsie
|-* x11-common
|-* iABF
  |-* third
    |-* fourth
|-* test
|-* test2
  |-* 1712874
    |-* CHANGKUO
[iABF@FAT32] » exit

Process finished with exit code 0
```
