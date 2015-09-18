include $(TOPDIR)/rules.mk

PKG_NAME:=cfengine-promises
PKG_VERSION:=1.5.3
PKG_RELEASE:=5

include $(INCLUDE_DIR)/package.mk

define Package/cfengine-promises
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=CFEngine promises
  DEPENDS:=+cfengine
endef

define Package/cfengine-promises/config
	source "$(SOURCE)/Config.in"
endef

define Package/cfengine-promises/description
 The promises for CFEngine which configure the Enigmabox.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/cfengine-promises/install
	$(INSTALL_DIR) $(1)/opt/cfengine
	$(INSTALL_BIN) ./files/root/bootstrap.cf $(1)/opt/cfengine/bootstrap.cf
	$(INSTALL_BIN) ./files/root/site.cf $(1)/opt/cfengine/site.cf

	$(INSTALL_DIR) $(1)/opt/enigmabox/cfengine-promises
	cp -rv ./files/root/* $(1)/opt/enigmabox/cfengine-promises/

	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) ./files/cfengine-apply $(1)/usr/sbin/cfengine-apply
	$(INSTALL_BIN) ./files/init-mysql $(1)/usr/sbin/init-mysql

	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) ./files/hello $(1)/usr/bin/hello
	$(INSTALL_BIN) ./files/speedtest $(1)/usr/bin/speedtest
	$(INSTALL_BIN) ./files/tts-de $(1)/usr/bin/tts-de
	$(INSTALL_BIN) ./files/tts-en $(1)/usr/bin/tts-en
	$(INSTALL_BIN) ./files/generate-enigmabox-statusmsg $(1)/usr/bin/generate-enigmabox-statusmsg

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/cfengine-promises.init $(1)/etc/init.d/cfengine-promises
	$(INSTALL_BIN) ./files/rebuild-iptables.init $(1)/etc/init.d/rebuild-iptables
	$(INSTALL_BIN) ./files/setup-cjdns-networking.init $(1)/etc/init.d/setup-cjdns-networking

	$(INSTALL_DIR) $(1)/etc
	$(INSTALL_DATA) ./files/resolv.conf $(1)/etc/resolv.conf.enigmabox

	# network profile
	$(INSTALL_DIR) $(1)/etc/enigmabox
	if [ "$(CONFIG_NETWORK_PROFILE_ALIX)" == "y" ]; then echo alix > $(1)/etc/enigmabox/network-profile; fi
	if [ "$(CONFIG_NETWORK_PROFILE_APU)" == "y" ]; then echo apu > $(1)/etc/enigmabox/network-profile; fi
	if [ "$(CONFIG_NETWORK_PROFILE_RASPI)" == "y" ]; then echo raspi > $(1)/etc/enigmabox/network-profile; fi

	# create empty crontab so that the cron service starts
	$(INSTALL_DIR) $(1)/etc/crontabs
	touch $(1)/etc/crontabs/root
endef

$(eval $(call BuildPackage,cfengine-promises))
