include $(TOPDIR)/rules.mk

PKG_NAME:=owncloud
PKG_VERSION:=v8.0.0
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/owncloud/core.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=$(PKG_VERSION)
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/owncloud
  SECTION:=admin
  CATEGORY:=Enigmabox
  TITLE:=ownCloud - self hosted cloud
endef

define Package/owncloud/description
 Access your data from all your devices, on an open platform you can extend and modify.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/owncloud/install
	$(INSTALL_DIR) $(1)/www/htdocs/owncloud
	$(CP) -rv $(PKG_BUILD_DIR)/* $(1)/www/htdocs/owncloud/

	# hypesite config
	$(INSTALL_DIR) $(1)/etc/lighttpd/hypesites.d
	$(INSTALL_DATA) ./files/owncloud.conf $(1)/etc/lighttpd/hypesites.d/owncloud.conf
endef

$(eval $(call BuildPackage,owncloud))
