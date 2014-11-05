include $(TOPDIR)/rules.mk

PKG_NAME:=provision-grandstream
PKG_VERSION:=1.0.0
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/provision-grandstream
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Auto-configuration for the Grandstream phone
  DEPENDS:=+lighttpd
endef

define Package/provision-grandstream/description
 Installs a website which serves a cfg.xml for the Grandstream phone.
 It will be read at boot time and sets the server and account details.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/provision-grandstream/install
	$(INSTALL_DIR) $(1)/etc/lighttpd/sites.d
	$(INSTALL_DATA) ./files/lighttpd-site.conf $(1)/etc/lighttpd/sites.d/provision-grandstream.conf

	$(INSTALL_DIR) $(1)/opt/enigmabox/provision-grandstream
	$(INSTALL_DATA) ./files/cfg.xml $(1)/opt/enigmabox/provision-grandstream/cfg.xml
endef

$(eval $(call BuildPackage,provision-grandstream))
