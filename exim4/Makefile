include $(TOPDIR)/rules.mk

PKG_NAME:=exim4
PKG_VERSION:=4.82
PKG_RELEASE:=1

PKG_SOURCE:=exim-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=http://mirror.switch.ch/ftp/mirror/exim/exim/exim4/
PKG_MD5SUM:=7f7b50394f8f3d4141e7dca9392f62f0

PKG_BUILD_DIR:=$(BUILD_DIR)/exim-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk

define Package/exim4
  SECTION:=mail
  CATEGORY:=Mail
  TITLE:=Exim Internet Mailer Version 4
  URL:=http://www.exim.org/
endef

define Package/exim4/description
	Description.
endef

#define Build/Configure
#	cp ./files/Makefile $(PKG_BUILD_DIR)/Local/Makefile
#endef

#define Build/Compile
#endef

#define Package/exim4/install
#endef

$(eval $(call BuildPackage,exim4))
