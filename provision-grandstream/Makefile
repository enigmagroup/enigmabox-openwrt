include $(TOPDIR)/rules.mk

PKG_NAME:=provision-grandstream
PKG_VERSION:=0.2.0
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/provision-grandstream
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Provision Grandstream
  URL:=http://enigmabox.net/en/
  DEPENDS:=+lighttpd
endef

define Package/provision-grandstream/description
	Description.
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
