include $(TOPDIR)/rules.mk

PKG_NAME:=hypesites
PKG_VERSION:=0.0.3
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/hypesites
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Hypesites - Hyperboria website hosting
endef

define Package/hypesites/description
 Hypesites - host your own websites inside Hyperboria.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/hypesites/install
	$(INSTALL_DIR) $(1)/etc/lighttpd/sites.d
	$(INSTALL_DATA) ./files/hypesites.conf $(1)/etc/lighttpd/sites.d/hypesites.conf

	$(INSTALL_DIR) $(1)/etc/lighttpd/hypesites.d
	$(INSTALL_DATA) ./files/index.conf $(1)/etc/lighttpd/hypesites.d/index.conf

	$(INSTALL_DIR) $(1)/www/htdocs
	$(INSTALL_DATA) ./files/index.html $(1)/www/htdocs/index.html

	$(INSTALL_DATA) ./files/site.conf $(1)/etc/lighttpd/hypesites.d/site.conf
	$(INSTALL_DIR) $(1)/www/htdocs/site
endef

$(eval $(call BuildPackage,hypesites))
