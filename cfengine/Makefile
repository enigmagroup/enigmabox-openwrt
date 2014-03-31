include $(TOPDIR)/rules.mk

PKG_NAME:=cfengine
PKG_VERSION:=3.6.0eb2-build2
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
  DEPENDS:=+libpcre +libopenssl +libxml2 +tokyocabinet +libpam
endef

define Package/cfengine/description
	Desc.
endef

define Build/Configure
	cd $(PKG_BUILD_DIR) && CFLAGS="$(TARGET_CFLAGS)" ./autogen.sh --host=$(ARCH) --target=$(GNU_TARGET_NAME) --with-tokyocabinet --without-libxml2 --without-postgresql $(TARGET_CONFIGURE_OPTS)
endef

define Package/cfengine/install
	$(INSTALL_DIR) $(1)/opt/cfengine/bin
	$(INSTALL_DIR) $(1)/opt/cfengine/lib

	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-agent/cf-agent $(1)/opt/cfengine/bin/cf-agent
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-execd/cf-execd $(1)/opt/cfengine/bin/cf-execd
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-key/cf-key $(1)/opt/cfengine/bin/cf-key
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-monitord/cf-monitord $(1)/opt/cfengine/bin/cf-monitord
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-promises/cf-promises $(1)/opt/cfengine/bin/cf-promises
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-runagent/cf-runagent $(1)/opt/cfengine/bin/cf-runagent
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-serverd/cf-serverd $(1)/opt/cfengine/bin/cf-serverd
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/ext/rpmvercmp $(1)/opt/cfengine/bin/cf-rpmvercmp
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/libpromises/libpromises.la $(1)/opt/cfengine/lib/cf-libpromises.la
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/libpromises/libpromises.la $(1)/opt/cfengine/lib/libpromises.so.1.0.0

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/cfengine.init $(1)/etc/init.d/cfengine

	# we will never use those keys for server communication, so this is just for speedup at boot
	$(INSTALL_DIR) $(1)/opt/cfengine/ppkeys
	$(INSTALL_DATA) ./files/localhost.priv $(1)/opt/cfengine/ppkeys/localhost.priv
	$(INSTALL_DATA) ./files/localhost.pub $(1)/opt/cfengine/ppkeys/localhost.pub
endef

$(eval $(call BuildPackage,cfengine))
