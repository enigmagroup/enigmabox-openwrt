include $(TOPDIR)/rules.mk

PKG_NAME:=cjdns-master
PKG_VERSION:=0.7.0
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/cjdelisle/cjdns.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=8f49d618f97a59a0f61b7409bb263c497b416709
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=libssp

include $(INCLUDE_DIR)/package.mk

define Package/cjdns-master
  SECTION:=net
  CATEGORY:=Network
  SUBMENU:=Routing and Redirection
  TITLE:=Experimental self configuring routing protocol.
  DEPENDS:=+kmod-tun +kmod-ipv6 +libnl +libpthread +librt +@SSP_SUPPORT +libssp
endef

define Build/Configure
endef

define Build/Compile
	CROSS="true" \
	CFLAGS="$(TARGET_CFLAGS)" \
	NO_PIE="true" \
	CC="$(TARGET_CC)" \
	ARCH="$(ARCH)" \
	LDFLAGS="$(TARGET_LDFLAGS) -lssp" \
	$(PKG_BUILD_DIR)/do
endef


define Package/cjdns-master/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cjdroute 	$(1)/usr/sbin/cjdroute
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/dnsserv 	$(1)/usr/sbin/dnsserv
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/privatetopublic $(1)/usr/sbin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/publictoip6 	$(1)/usr/sbin/

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/cjdns.init $(1)/etc/init.d/cjdns
endef

$(eval $(call BuildPackage,cjdns-master))
