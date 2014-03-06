include $(TOPDIR)/rules.mk

PKG_NAME:=cfengine-policies
PKG_VERSION:=1
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_VERSION:=$(PKG_VERSION)
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

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

define Package/cfengine-policies/install
	$(INSTALL_DIR) $(1)/opt/enigmabox/cfengine-policies
	$(INSTALL_BIN) ./files/bootstrap.cf $(1)/opt/enigmabox/cfengine-policies/bootstrap.cf
endef

$(eval $(call BuildPackage,cfengine-policies))
