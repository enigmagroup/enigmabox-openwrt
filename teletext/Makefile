include $(TOPDIR)/rules.mk

PKG_NAME:=teletext
PKG_VERSION:=0.9.1
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/enigmagroup/teletext.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=39976b0a7dc3d6c768049664b7fbcda471dcfc22
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk

define Package/teletext
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Teletext - a distributed Twitter clone
  URL:=https://enigmabox.net/en/blog/2014/02/teletext-mass-communication-coordinating-a-revolution-below-the-radar/
endef

define Package/teletext/description
 Teletext - a distributed Twitter clone.

 (TS//SI//REL) Teletext provides distributed mass protest coordination
 below the radar by implementing a Twitter like messaging system
 using cjdns addresses.
 
 (TS//SI//REL) This technique supports users on writing telegrams
 and spreading out important information quickly to reach critical mass.
 
 (TS//SI//REL) Through its distributed nature, Telegrams published
 on the Teletext system can not be censored, nor controlled.
 It is all end-to-end encrypted.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/teletext/install
	$(INSTALL_DIR) $(1)/opt/enigmabox/teletext
	cp -rv $(PKG_BUILD_DIR)/arrow $(1)/opt/enigmabox/teletext/
	cp -rv $(PKG_BUILD_DIR)/dateutil $(1)/opt/enigmabox/teletext/
	cp -rv $(PKG_BUILD_DIR)/public $(1)/opt/enigmabox/teletext/
	cp -rv $(PKG_BUILD_DIR)/views $(1)/opt/enigmabox/teletext/
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/api.py $(1)/opt/enigmabox/teletext/api.py
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/beanstalkc.py $(1)/opt/enigmabox/teletext/beanstalkc.py
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/bottle.py $(1)/opt/enigmabox/teletext/bottle.py
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/data.py $(1)/opt/enigmabox/teletext/data.py
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/queue.py $(1)/opt/enigmabox/teletext/queue.py
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/routes.py $(1)/opt/enigmabox/teletext/routes.py
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/teletext.py $(1)/opt/enigmabox/teletext/teletext.py
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/utils.py $(1)/opt/enigmabox/teletext/utils.py
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/workers.py $(1)/opt/enigmabox/teletext/workers.py

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/teletext.init $(1)/etc/init.d/teletext

	$(INSTALL_DIR) $(1)/etc/lighttpd/sites.d
	$(INSTALL_DATA) ./files/lighttpd-site.conf $(1)/etc/lighttpd/sites.d/teletext.conf
endef

$(eval $(call BuildPackage,teletext))
