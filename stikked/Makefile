include $(TOPDIR)/rules.mk

PKG_NAME:=stikked
PKG_VERSION:=0.10.0
PKG_RELEASE:=2

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
	$(INSTALL_DIR) $(1)/srv/www/pastebin
	$(CP) -v $(PKG_BUILD_DIR)/htdocs/* $(1)/srv/www/pastebin/

	# stikked config
	$(INSTALL_DATA) ./files/stikked.php $(1)/srv/www/pastebin/application/config/stikked.php
endef

$(eval $(call BuildPackage,stikked))
