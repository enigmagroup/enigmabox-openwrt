include $(TOPDIR)/rules.mk

PKG_NAME:=webinterface
PKG_VERSION:=1.7.1
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/webinterface
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Enigmabox web interface
  URL:=http://enigmabox.net/en/
  DEPENDS:=+cjdns-master +cjdns-v6 +cjdns-v16
  DEPENDS+= +curl +syslog-ng +zip +unzip +shadow-usermod +kmod-ipt-nat6 +isc-dhcp-server-ipv4 +radvd +gesftpserver +vnstat +rsync +fdisk +@DROPBEAR_ECC +@BUSYBOX_CUSTOM +@BUSYBOX_CONFIG_DIFF
  DEPENDS+= +python +python-django-1.4 +python-gunicorn +python-six +python-gevent +python-requests +django-south +python-json +python-unidecode +python-beanstalkc +python-imglib
  DEPENDS+= +asterisk11 +asterisk11-sounds +asterisk11-codec-gsm +asterisk11-format-gsm +asterisk11-format-wav +asterisk11-res-srtp +asterisk11-res-musiconhold +asterisk11-app-confbridge +asterisk11-app-read +asterisk11-res-timing-timerfd +asterisk11-voicemail +asterisk11-format-h264 +asterisk11-app-system +svox +libffmpeg-audio-dec +sox
  DEPENDS+= +php5 +php5-cgi +php5-cli +php5-mod-mcrypt +php5-mod-pdo-sqlite +php5-mod-mysql +php5-mod-mysqli +php5-mod-session +php5-mod-iconv +php5-mod-json +php5-mod-ctype +php5-mod-dom +php5-mod-gd +php5-mod-hash +php5-mod-mbstring +php5-mod-simplexml +php5-mod-xml +php5-mod-xmlreader +php5-mod-xmlwriter +php5-mod-zip +php5-mod-curl +php5-mod-pdo-mysql +php5-mod-sqlite3 +php5-mod-fileinfo +php5-mod-exif +php5-mod-ftp +@PHP5_FILTER +@PHP5_LIBXML +@BUILD_NLS
  DEPENDS+= +mysql-server
  DEPENDS+= +lighttpd +lighttpd-mod-auth +lighttpd-mod-access +lighttpd-mod-cgi +lighttpd-mod-fastcgi +lighttpd-mod-proxy +lighttpd-mod-rewrite +lighttpd-mod-setenv
  DEPENDS+= +privoxy
  DEPENDS+= +dovecot +exim4
  DEPENDS+= +cfengine +cfengine-promises
  DEPENDS+= +beanstalkd
  DEPENDS+= +cryptsetup +losetup +kmod-loop +kmod-crypto-xts +kmod-crypto-cbc +kmod-crypto-misc +kmod-crypto-iv +e2fsprogs
  DEPENDS+= +zoneinfo-africa +zoneinfo-asia +zoneinfo-atlantic +zoneinfo-australia-nz +zoneinfo-europe +zoneinfo-india +zoneinfo-northamerica +zoneinfo-pacific +zoneinfo-poles +zoneinfo-simple +zoneinfo-southamerica
  DEPENDS+= +kmod-usb-net +kmod-usb-net-asix +kmod-usb-net-asix-ax88179 +kmod-usb-net-cdc-eem +kmod-usb-net-cdc-ether +kmod-usb-net-cdc-mbim +kmod-usb-net-cdc-ncm +kmod-usb-net-cdc-subset +kmod-usb-net-dm9601-ether +kmod-usb-net-hso +kmod-usb-net-huawei-cdc-ncm +kmod-usb-net-ipheth +kmod-usb-net-kalmia +kmod-usb-net-kaweth +kmod-usb-net-mcs7830 +kmod-usb-net-pegasus +kmod-usb-net-qmi-wwan +kmod-usb-net-rndis +kmod-usb-net-sierrawireless +kmod-usb-net-smsc95xx
  DEPENDS+= +wireless-tools +wpa-supplicant +kmod-ath +kmod-ath9k-htc +kmod-brcmfmac +kmod-carl9170 +kmod-libertas-usb +kmod-p54-usb +kmod-rt2500-usb +kmod-rt2800-usb +kmod-rt73-usb +kmod-rtl8187 +kmod-rtl8192cu +kmod-zd1211rw +kmod-net-rtl8188eu
#  DEPENDS+= +kmod-e1000 +kmod-r8169 +kmod-via-rhine
  DEPENDS+= +kmod-fs-btrfs +kmod-fs-cifs +kmod-fs-cramfs +kmod-fs-ext4 +kmod-fs-hfs +kmod-fs-hfsplus +kmod-fs-isofs +kmod-fs-jfs +kmod-fs-msdos +kmod-fs-nfs +kmod-fs-ntfs +kmod-fs-reiserfs +kmod-fs-udf +kmod-fs-vfat +kmod-fs-xfs +kmod-fuse
  DEPENDS+= +kmod-nls-cp1250 +kmod-nls-cp1251 +kmod-nls-cp437 +kmod-nls-cp775 +kmod-nls-cp850 +kmod-nls-cp852 +kmod-nls-cp862 +kmod-nls-cp864 +kmod-nls-cp866 +kmod-nls-cp932 +kmod-nls-iso8859-1 +kmod-nls-iso8859-13 +kmod-nls-iso8859-15 +kmod-nls-iso8859-2 +kmod-nls-iso8859-6 +kmod-nls-iso8859-8 +kmod-nls-koi8r +kmod-nls-utf8
  DEPENDS+= +hypesites +dokuwiki +owncloud +owncloud-documents +stikked
  DEPENDS+= +@LIBC_USE_UCLIBC #doesn't work, set it manually!
endef

define Package/webinterface/description
 The Enigmabox administration web interface, used for configuring
 the settings of the Enigmabox. It does not depend on any OpenWrt
 interface, in fact, it replaces LuCI.

 It also serves as a metapackage. Select it, and everything else
 required for the Enigmabox will be selected.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/webinterface/install
	$(INSTALL_DIR) $(1)/box
	cp -rv ./files/root/* $(1)

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/webinterface.init $(1)/etc/init.d/webinterface

	$(INSTALL_DIR) $(1)/etc/lighttpd/sites.d
	$(INSTALL_DATA) ./files/lighttpd-site.conf $(1)/etc/lighttpd/sites.d/webinterface.conf

	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) ./files/backup-stuff $(1)/usr/sbin/backup-stuff
	$(INSTALL_BIN) ./files/restore-stuff $(1)/usr/sbin/restore-stuff
	$(INSTALL_BIN) ./files/set-country $(1)/usr/sbin/set-country
	$(INSTALL_BIN) ./files/volumes-mounter $(1)/usr/sbin/volumes-mounter

	$(INSTALL_DIR) $(1)/etc/hotplug.d/usb
	$(INSTALL_BIN) ./files/trigger-volume-mounter $(1)/etc/hotplug.d/usb/trigger-volume-mounter
endef

$(eval $(call BuildPackage,webinterface))
