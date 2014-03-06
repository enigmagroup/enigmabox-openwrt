include $(TOPDIR)/rules.mk

PKG_NAME:=cfengine-policies
PKG_VERSION:=1
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/cfengine-policies
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=cfengine policies
  DEPENDS:=+cfengine
endef

define Package/cfengine-policies/description
	Desc.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/cfengine-policies/install
	$(INSTALL_BIN) ./files/bootstrap.cf $(1)/opt/cfengine/bootstrap.cf

	$(INSTALL_DIR) $(1)/opt/enigmabox/cfengine-policies
endef

$(eval $(call BuildPackage,cfengine-policies))
