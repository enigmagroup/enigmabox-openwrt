include $(TOPDIR)/rules.mk

PKG_NAME:=owncloud-documents
PKG_VERSION:=8.1.0
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_URL:=https://github.com/owncloud/documents.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=v8.1.0
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/owncloud-documents
  SECTION:=admin
  CATEGORY:=Enigmabox
  TITLE:=ownCloud Documents
  DEPENDS:=hypesites
  SUBMENU:=Hypesite apps
endef

define Package/owncloud-documents/description
 ownCloud Documents is collaborative editing of rich-text documents.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/owncloud-documents/install
	$(INSTALL_DIR) $(1)/srv/www/owncloud/apps/documents
	$(CP) -rv $(BUILD_DIR)/* $(1)/srv/www/owncloud/apps/documents/
endef

$(eval $(call BuildPackage,owncloud-documents))
