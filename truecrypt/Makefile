include $(TOPDIR)/rules.mk

PKG_NAME:=truecrypt
PKG_VERSION:=7.1a
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://enigmabox.net/truecrypt/
PKG_MD5SUM:=102d9652681db11c813610882332ae48
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)-source

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/truecrypt
  SECTION:=admin
  CATEGORY:=Utilities
  SUBMENU:=Filesystem
  TITLE:=TrueCrypt
  DEPENDS:=+fuse-utils
  PKG_BUILD_DEPENDS:=libfuse
endef

define Package/truecrypt/description
 TrueCrypt is a discontinued source-available freeware utility used for on-the-fly encryption (OTFE). It can create a virtual encrypted disk within a file or encrypt a partition or (under Microsoft Windows except Windows 8 with GPT) the entire storage device (pre-boot authentication).
endef

define Build/Compile
	cd $(PKG_BUILD_DIR) && make NOGUI=1 WX_ROOT=$(PKG_BUILD_DIR)/wxWidgets-2.8.12 wxbuild
	cd $(PKG_BUILD_DIR) && make NOGUI=1 WXSTATIC=1 NOASM=1
endef

define Build/Configure
	$(CP) ./files/pkcs11.h $(PKG_BUILD_DIR)
	$(CP) ./files/pkcs11f.h $(PKG_BUILD_DIR)
	$(CP) ./files/pkcs11t.h $(PKG_BUILD_DIR)
	wget http://switch.dl.sourceforge.net/project/wxwindows/2.8.12/wxWidgets-2.8.12.tar.gz
	tar xzvf wxWidgets-2.8.12.tar.gz -C $(PKG_BUILD_DIR)
endef

define Package/truecrypt/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/Main/truecrypt 	$(1)/usr/sbin/truecrypt
endef

$(eval $(call BuildPackage,truecrypt))
