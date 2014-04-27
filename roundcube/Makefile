include $(TOPDIR)/rules.mk

PKG_NAME:=roundcube
PKG_VERSION:=0.9.5
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/roundcube
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Enigmabox Webmail
endef

define Package/roundcube/description
	Description.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/roundcube/install
	cp -r ./files/root/* $(1)

	$(INSTALL_DIR) $(1)/etc/nginx/sites
	$(INSTALL_DATA) ./files/nginx-site.conf $(1)/etc/nginx/sites/roundcube.conf
endef

$(eval $(call BuildPackage,roundcube))
