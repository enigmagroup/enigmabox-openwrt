include $(TOPDIR)/rules.mk

PKG_NAME:=webinterface
PKG_VERSION:=1.0.3
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/webinterface
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Enigmabox web interface
  URL:=http://enigmabox.net/en/
  DEPENDS:=+cjdns-master
  DEPENDS+= +curl +syslog-ng +zip +unzip +shadow-usermod +kmod-ipt-nat6 +isc-dhcp-server-ipv4 +radvd +gesftpserver
  DEPENDS+= +python +python-django-1.4 +python-gunicorn +python-six +python-gevent +python-openssl +python-requests +django-south +python-expat +python-json +python-sqlite3 +python-unidecode +python-beanstalkc +python-imaging-library +pyyaml
  DEPENDS+= +asterisk11 +asterisk11-sounds +asterisk11-codec-gsm +asterisk11-format-gsm +asterisk11-res-srtp +asterisk11-res-musiconhold
  DEPENDS+= +php5 +php5-fastcgi +php5-mod-mcrypt +php5-mod-pdo-sqlite +php5-mod-mysql +php5-mod-session +php5-mod-iconv +php5-mod-json +@PHP5_FILTER
  DEPENDS+= +mysql-server
  DEPENDS+= +lighttpd +lighttpd-mod-auth +lighttpd-mod-fastcgi +lighttpd-mod-proxy
  DEPENDS+= +privoxy
  DEPENDS+= +dovecot +exim4
  DEPENDS+= +cfengine +cfengine-promises
  DEPENDS+= +beanstalkd
  DEPENDS+= +kmod-usb-net +kmod-usb-net-asix +kmod-usb-net-cdc-eem +kmod-usb-net-cdc-ether +kmod-usb-net-cdc-mbim +kmod-usb-net-cdc-ncm +kmod-usb-net-cdc-subset +kmod-usb-net-dm9601-ether +kmod-usb-net-hso +kmod-usb-net-huawei-cdc-ncm +kmod-usb-net-ipheth +kmod-usb-net-kalmia +kmod-usb-net-kaweth +kmod-usb-net-mcs7830 +kmod-usb-net-pegasus +kmod-usb-net-qmi-wwan +kmod-usb-net-rndis +kmod-usb-net-sierrawireless +kmod-usb-net-smsc95xx
  DEPENDS+= +wireless-tools +wpa-supplicant +kmod-ath +kmod-ath9k-htc +kmod-brcmfmac +kmod-carl9170 +kmod-libertas-sd +kmod-libertas-usb +kmod-net-zd1201 +kmod-p54-usb +kmod-rt2500-usb +kmod-rt2800-usb +kmod-rt73-usb +kmod-rtl8187 +kmod-rtl8192cu +kmod-zd1211rw +kmod-net-rtl8188eu
#  DEPENDS+= +kmod-e1000 +kmod-r8169
endef

define Package/webinterface/description
 The Enigmabox administration web interface, used for configuring
 the settings of the Enigmabox. It does not depend on any OpenWRT
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
	$(INSTALL_DATA) ./files/mysite.conf $(1)/etc/lighttpd/sites.d/mysite.conf
	$(INSTALL_DIR) $(1)/www/htdocs

	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) ./files/backup-stuff $(1)/usr/sbin/backup-stuff
	$(INSTALL_BIN) ./files/restore-stuff $(1)/usr/sbin/restore-stuff
	$(INSTALL_BIN) ./files/set-country $(1)/usr/sbin/set-country
endef

$(eval $(call BuildPackage,webinterface))
