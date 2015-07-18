include $(TOPDIR)/rules.mk

PKG_NAME:=owncloud-documents
PKG_VERSION:=8.1.0
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
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
	$(CP) -rv $(PKG_BUILD_DIR)/appinfo $(1)/srv/www/owncloud/apps/documents/appinfo
	$(CP) -rv $(PKG_BUILD_DIR)/assets $(1)/srv/www/owncloud/apps/documents/assets
	$(CP) -rv $(PKG_BUILD_DIR)/controller $(1)/srv/www/owncloud/apps/documents/controller
	$(CP) -rv $(PKG_BUILD_DIR)/css $(1)/srv/www/owncloud/apps/documents/css
	$(CP) -rv $(PKG_BUILD_DIR)/img $(1)/srv/www/owncloud/apps/documents/img
	$(CP) -rv $(PKG_BUILD_DIR)/js $(1)/srv/www/owncloud/apps/documents/js
	$(CP) -rv $(PKG_BUILD_DIR)/l10n $(1)/srv/www/owncloud/apps/documents/l10n
	$(CP) -rv $(PKG_BUILD_DIR)/lib $(1)/srv/www/owncloud/apps/documents/lib
	$(CP) -rv $(PKG_BUILD_DIR)/src $(1)/srv/www/owncloud/apps/documents/src
	$(CP) -rv $(PKG_BUILD_DIR)/templates $(1)/srv/www/owncloud/apps/documents/templates
	$(CP) -rv $(PKG_BUILD_DIR)/tests $(1)/srv/www/owncloud/apps/documents/tests
	$(CP) -rv $(PKG_BUILD_DIR)/admin.php $(1)/srv/www/owncloud/apps/documents/admin.php
	$(CP) -rv $(PKG_BUILD_DIR)/index.php $(1)/srv/www/owncloud/apps/documents/index.php
	$(CP) -rv $(PKG_BUILD_DIR)/personal.php $(1)/srv/www/owncloud/apps/documents/personal.php
	$(CP) -rv $(PKG_BUILD_DIR)/public.php $(1)/srv/www/owncloud/apps/documents/public.php
	$(CP) -rv $(PKG_BUILD_DIR)/settings.php $(1)/srv/www/owncloud/apps/documents/settings.php
endef

$(eval $(call BuildPackage,owncloud-documents))
