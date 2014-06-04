include $(TOPDIR)/rules.mk

PKG_NAME:=nacl4raspi
PKG_VERSION:=1.0.0
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/srneb/nacl4raspi.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=c68637a609c7d2c0b59534de30aab3f3d1cf0623
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk

define Package/nacl4raspi
  SECTION:=lib
  CATEGORY:=Libraries
  TITLE:=NaCl for Raspberry Pi
  DEPENDS:=+@SSP_SUPPORT +libssp
endef

define Build/Configure
endef

define Build/Compile
endef


define Package/nacl4raspi/install
	$(INSTALL_DIR) $(1)/usr/include/nacl
	$(CP) $(PKG_BUILD_DIR)/include/* 	$(1)/usr/include/nacl/

	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_BUILD_DIR)/libnacl.a 	$(1)/usr/lib/
endef

$(eval $(call BuildPackage,nacl4raspi))
