include $(TOPDIR)/rules.mk

PKG_NAME:=cfengine
PKG_VERSION:=3.6.0b1-build4
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/cfengine/core.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=$(PKG_VERSION)
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/cfengine
  SECTION:=admin
  CATEGORY:=Administration
  TITLE:=cfengine3
  DEPENDS:=+libpcre +libopenssl +tokyocabinet +libxml2 +qdbm
endef

define Package/cfengine/description
	Desc.
endef

define Build/Configure
	cd $(PKG_BUILD_DIR) && CFLAGS="$(TARGET_CFLAGS)" ./autogen.sh --host=i486 --target=i386-pc-linux-gnu $(TARGET_CONFIGURE_OPTS)
endef

define Package/cfengine/install
	$(INSTALL_DIR) $(1)/opt/cfengine/bin
	$(INSTALL_DIR) $(1)/opt/cfengine/lib

	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-agent/cf-agent   $(1)/opt/cfengine/bin/cf-agent
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-execd/cf-execd   $(1)/opt/cfengine/bin/cf-execd
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-key/cf-key   $(1)/opt/cfengine/bin/cf-key
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-monitord/cf-monitord   $(1)/opt/cfengine/bin/cf-monitord
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-promises/cf-promises   $(1)/opt/cfengine/bin/cf-promises
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-runagent/cf-runagent   $(1)/opt/cfengine/bin/cf-runagent
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-serverd/cf-serverd   $(1)/opt/cfengine/bin/cf-serverd
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/ext/rpmvercmp   $(1)/opt/cfengine/bin/cf-rpmvercmp
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/libpromises/libpromises.la   $(1)/opt/cfengine/lib/cf-libpromises.la
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/libpromises/libpromises.la   $(1)/opt/cfengine/lib/libpromises.so.1.0.0
endef

$(eval $(call BuildPackage,cfengine))
