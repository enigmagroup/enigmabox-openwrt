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
	cp -r ./files/* $(1)
endef

$(eval $(call BuildPackage,teletext))
