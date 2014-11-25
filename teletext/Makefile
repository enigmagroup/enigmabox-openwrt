include $(TOPDIR)/rules.mk

PKG_NAME:=teletext
PKG_VERSION:=0.1.7
PKG_RELEASE:=2

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
	cp -rv ./files/root/* $(1)

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/teletext.init $(1)/etc/init.d/teletext

	$(INSTALL_DIR) $(1)/etc/lighttpd/sites.d
	$(INSTALL_DATA) ./files/lighttpd-site.conf $(1)/etc/lighttpd/sites.d/teletext.conf
endef

$(eval $(call BuildPackage,teletext))
