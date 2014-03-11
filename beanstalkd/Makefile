include $(TOPDIR)/rules.mk

PKG_NAME:=beanstalkd
PKG_VERSION:=v1.9
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/kr/beanstalkd.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=$(PKG_VERSION)
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/beanstalkd
  SECTION:=net
  CATEGORY:=Network
  TITLE:=Beanstalk
endef

define Package/beanstalkd/description
	Desc.
endef

define Build/Configure
endef

define Build/Compile
	cd $(PKG_BUILD_DIR) && make CC="$(TARGET_CC)" CFLAGS="$(TARGET_CFLAGS)"
endef

define Package/beanstalkd/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/beanstalkd $(1)/usr/bin/beanstalkd
endef

$(eval $(call BuildPackage,beanstalkd))
