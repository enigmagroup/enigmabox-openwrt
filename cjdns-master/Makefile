include $(TOPDIR)/rules.mk

PKG_NAME:=cjdns-master
PKG_VERSION:=master
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/cjdelisle/cjdns.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=$(PKG_VERSION)
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk

define Package/cjdns-master
  SECTION:=net
  CATEGORY:=Network
  SUBMENU:=Routing and Redirection
  TITLE:=Experimental self configuring routing protocol.
  DEPENDS:=+kmod-tun +kmod-ipv6 +libnl +nacl +libpthread
endef

TARGET_CFLAGS += -I$(STAGING_DIR)/usr/include

define Package/cjdns-master/description
	Description.
endef

define Build/Compile
	cd $(PKG_BUILD_DIR) && CC=$(TARGET_CC) CFLAGS=$(TARGET_CFLAGS) ./do
endef

define Package/cjdns-master/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cjdroute   $(1)/usr/sbin/cjdroute
endef

$(eval $(call BuildPackage,cjdns-master))
