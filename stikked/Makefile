include $(TOPDIR)/rules.mk

PKG_NAME:=stikked
PKG_VERSION:=0.9.0
PKG_RELEASE:=3

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/claudehohl/stikked.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=$(PKG_VERSION)
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/stikked
  SECTION:=admin
  CATEGORY:=Enigmabox
  TITLE:=Stikked - open source encrypted pastebin
  DEPENDS:=hypesites
  SUBMENU:=Hypesite apps
endef

define Package/stikked/description
 An advanced and beautiful pastebin written in PHP.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/stikked/install
	$(INSTALL_DIR) $(1)/www/htdocs/stikked
	$(CP) -v $(PKG_BUILD_DIR)/htdocs/* $(1)/www/htdocs/stikked/

	# stikked config
	$(INSTALL_DATA) ./files/stikked.php $(1)/www/htdocs/stikked/application/config/stikked.php

	# hypesite config
	$(INSTALL_DIR) $(1)/etc/lighttpd/hypesites.d
	$(INSTALL_DATA) ./files/stikked.conf $(1)/etc/lighttpd/hypesites.d/stikked.conf
endef

$(eval $(call BuildPackage,stikked))
