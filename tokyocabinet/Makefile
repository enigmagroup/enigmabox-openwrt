include $(TOPDIR)/rules.mk

PKG_NAME:=libtokyocabinet
PKG_VERSION:=1.4.48
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=http://fallabs.com/tokyocabinet/tokyocabinet-1.4.48.tar.gz
PKG_SOURCE_VERSION:=1.4.48
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/libtokyocabinet
  SECTION:=lib
  CATEGORY:=Libraries
  TITLE:=Tokyocabinet library
  DEPENDS:=+libbz2
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

#define Build/Configure
#endef

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

$(eval $(call BuildPackage,libtokyocabinet))
