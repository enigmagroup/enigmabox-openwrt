include $(TOPDIR)/rules.mk

PKG_NAME:=qdbm
PKG_VERSION:=1.8.77
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/qdbm-$(PKG_VERSION)
PKG_SOURCE:=qdbm-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=@SF/qdbm
PKG_MD5SUM:=084e07824e231969356ec7cefac97985
PKG_CAT:=zcat

include $(INCLUDE_DIR)/package.mk

define Package/qdbm
  SECTION:=base
  CATEGORY:=Libraries
  TITLE:=QDBM: Quick DataBase Manager
  URL:=http://sourceforge.net/projects/qdbm/
endef

define Package/qdbm/description
QDBM is a library of routines for managing a database. It is developed referring to GDBM for the purpose
of the following three points: higher processing speed, smaller size of a database file, and simpler API.
endef

define Build/Configure
  $(call Build/Configure/Default,--with-linux-headers=$(LINUX_DIR))
endef

define Package/qdbm/install
	$(INSTALL_DIR) $(1)/usr/sbin
endef

$(eval $(call BuildPackage,qdbm))
