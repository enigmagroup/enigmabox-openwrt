include $(TOPDIR)/rules.mk

PKG_NAME:=roundcube
PKG_VERSION:=1
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
	cp -r ./files/* $(1)
endef

$(eval $(call BuildPackage,roundcube))
