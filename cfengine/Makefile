include $(TOPDIR)/rules.mk

PKG_NAME:=cfengine
PKG_VERSION:=3.5.3
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/cfengine/core.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=3.5.3
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/cfengine
  SECTION:=admin
  CATEGORY:=Administration
  TITLE:=cfengine3
  DEPENDS:=+libpcre +libopenssl +USE_UCLIBC
endef

define Package/cfengine/description
	Desc.
endef

	#cd $(PKG_BUILD_DIR) && ./autogen.sh \
	#--prefix=/usr \
	#--srcdir=$(PKG_BUILD_DIR) \
	#--with-sysroot=$(PKG_BUILD_DIR) \
	#--with-workdir=$(PKG_BUILD_DIR) \
	#--enable-fhs \
	#--disable-maintainer-mode \
	#--without-libvirt

	#$(call Build/Configure/Default,--with-linux-headers=$(LINUX_DIR))

define Build/Configure
	cd $(PKG_BUILD_DIR) && CFLAGS="$(TARGET_CFLAGS)" ./autogen.sh --host=i486 --without-tokyocabinet $(TARGET_CONFIGURE_OPTS)
endef

#define Build/Compile
#	CFLAGS="$(TARGET_CFLAGS) $(EXTRA_CPPFLAGS) " \
#	LDFLAGS="$(EXTRA_LDFLAGS) " \
#	cd $(PKG_BUILD_DIR)
#	$(MAKE) -C $(PKG_BUILD_DIR) \
#		$(TARGET_CONFIGURE_OPTS) \
#		CROSS="$(TARGET_CROSS)" \
#		CXXFLAGS="$(TARGET_CFLAGS) $(EXTRA_CPPFLAGS) " \
#		ARCH="$(ARCH)";
#endef

define Package/cfengine/install
	$(INSTALL_DIR) $(1)/var/cfengine/bin
	$(INSTALL_DIR) $(1)/var/cfengine/lib

	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-agent/cf-agent   $(1)/var/cfengine/bin/cf-agent
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-execd/cf-execd   $(1)/var/cfengine/bin/cf-execd
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-key/cf-key   $(1)/var/cfengine/bin/cf-key
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-monitord/cf-monitord   $(1)/var/cfengine/bin/cf-monitord
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-promises/cf-promises   $(1)/var/cfengine/bin/cf-promises
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-runagent/cf-runagent   $(1)/var/cfengine/bin/cf-runagent
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cf-serverd/cf-serverd   $(1)/var/cfengine/bin/cf-serverd
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/ext/rpmvercmp   $(1)/var/cfengine/bin/cf-rpmvercmp
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/libpromises/libpromises.la   $(1)/var/cfengine/lib/cf-libpromises.la
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/libpromises/libpromises.la   $(1)/var/cfengine/lib/libpromises.so.1.0.0
endef

$(eval $(call BuildPackage,cfengine,+libc))
