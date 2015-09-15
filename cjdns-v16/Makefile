include $(TOPDIR)/rules.mk

PKG_NAME:=cjdns-v16
PKG_VERSION:=2015-09-15-00a90f0997e2863dd218d04f95e24401f2037a4c
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/cjdelisle/cjdns.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=00a90f0997e2863dd218d04f95e24401f2037a4c
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk

define Package/cjdns-v16
  SECTION:=net
  CATEGORY:=Network
  SUBMENU:=Routing and Redirection
  TITLE:=Experimental self configuring routing protocol.
  DEPENDS:=+kmod-tun +kmod-ipv6 +libnl +libpthread +librt
endef

define Package/cjdns-v16/description
 Cjdns is a networking protocol, a system of digital rules for
 message exchange between computers. The philosophy behind cjdns
 is that networks should be easy to set up, protocols should
 scale up smoothly and security should be ubiquitous.
endef

define Build/Configure
endef

## NEON
#define Build/Compile
#	CROSS="true" \
#	CFLAGS="-O2 -march=armv7-a -mtune=cortex-a8 -mfpu=neon -ftree-vectorize -ffast-math -mfloat-abi=hard -marm -Wno-error=maybe-uninitialized" \
#	NO_PIE="true" \
#	Seccomp_NO="true" \
#	CC="$(TARGET_CC)" \
#	ARCH="$(ARCH)" \
#	LDFLAGS="$(CFLAGS)" \
#	$(PKG_BUILD_DIR)/do
#endef

# regular
define Build/Compile
	CROSS="true" \
	CFLAGS="$(TARGET_CFLAGS)" \
	NO_PIE="true" \
	SSP_SUPPORT="n" \
	Seccomp_NO="true" \
	CC="$(TARGET_CC)" \
	ARCH="$(ARCH)" \
	LDFLAGS="$(TARGET_LDFLAGS)" \
	$(PKG_BUILD_DIR)/do
endef

define Package/cjdns-v16/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cjdroute 	$(1)/usr/sbin/cjdroute.v16
endef

$(eval $(call BuildPackage,cjdns-v16))
