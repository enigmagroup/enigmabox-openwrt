enigmabox-openwrt
=================

OpenWRT package feed for the Enigmabox software suite.

Description in our wiki: http://wiki.enigmabox.net/roadmap/openwrt

How to build that stuff:

    $ git clone git://git.openwrt.org/openwrt.git
    $ cd openwrt

    $ cp feeds.conf.default feeds.conf
    $ vi feeds.conf

Your feeds.conf should look like this:

    src-git packages https://github.com/openwrt/packages.git
    src-git oldpackages http://git.openwrt.org/packages.git
    src-git routing https://github.com/openwrt-routing/packages.git
    src-git telephony http://git.openwrt.org/feed/telephony.git

    src-git enigmabox https://github.com/enigmagroup/enigmabox-openwrt.git

Next use that package system to incorporate the enigmabox software suite:

    $ ./scripts/feeds update -a
    $ ./scripts/feeds install -a
    $ make defconfig
    $ make prereq

Then configure for your system:

    $ make menuconfig

Select "Target System": x86 Generic

Configure "Target Images" as you please. Example:
* Root filesystem archives: none
* Root filesystem images: jffs2
* Pad images to filesystem size: yes
* GZip images: no
* Root filesystem partition size: 900 (set that a little bit lower than the size of your CFCard)

Select everything under "Enigmabox"

Quit and save your .config

Then:

    $ make

After about 30mins (depending on your machine), your image is ready:

    bin/x86/openwrt-x86-generic-combined-jffs2-128k.img

