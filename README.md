enigmabox-openwrt
=================

OpenWRT package feed for the Enigmabox software suite.

Description in our wiki: http://wiki.enigmabox.net/roadmap/openwrt

How to build that stuff:

    $ git clone git://git.openwrt.org/openwrt.git
    $ cd openwrt

    $ cp feeds.conf.default feeds.conf
    $ vi feeds.conf

And add the following line to the file:

    src-git enigmabox https://github.com/enigmagroup/enigmabox-openwrt.git

Next use that package system to incorporate the enigmabox software suite:

    $ ./scripts/feeds update -a
    $ ./scripts/feeds install enigmabox

Then configure for your system:

    # make menuconfig

Select everything under "Enigmabox".

