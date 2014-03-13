include $(TOPDIR)/rules.mk

PKG_NAME:=teletext
PKG_VERSION:=1
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/teletext
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Teletext
endef

define Package/teletext/description
	Description.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/teletext/install
	cp -r ./files/root/* $(1)

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/teletext.init $(1)/etc/init.d/teletext

	$(INSTALL_DIR) $(1)/etc/nginx/sites
	$(INSTALL_DATA) ./files/nginx-site.conf $(1)/etc/nginx/sites/teletext.conf
endef

$(eval $(call BuildPackage,teletext))
