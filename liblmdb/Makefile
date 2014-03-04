include $(TOPDIR)/rules.mk

PKG_NAME:=liblmdb
PKG_VERSION:=LMDB_0.9.10
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://git.gitorious.org/mdb/mdb.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=$(PKG_VERSION)
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)/libraries/liblmdb

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/liblmdb
  SECTION:=base
  CATEGORY:=Libraries
  TITLE:=liblmdb
endef

define Package/liblmdb/description
	Desc.
endef

#define Build/Configure
#	cd $(PKG_BUILD_DIR) && CFLAGS="$(TARGET_CFLAGS)" ./autogen.sh --host=i486 --target=i386-pc-linux-gnu $(TARGET_CONFIGURE_OPTS)
#endef

define Package/liblmdb/install
	$(INSTALL_DIR) $(1)/usr
endef

$(eval $(call BuildPackage,liblmdb))
