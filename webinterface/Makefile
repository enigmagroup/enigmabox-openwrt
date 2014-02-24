include $(TOPDIR)/rules.mk

PKG_NAME:=enigmabox-webinterface
PKG_VERSION:=20
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/enigmabox-webinterface
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Enigmabox Webinterface
  DEFAULT:=y
endef

define Package/enigmabox-webinterface/description
	Description.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/enigmabox-webinterface/install
	cp -r ./files/* $(1)
endef

$(eval $(call BuildPackage,enigmabox-webinterface))
