#
# Copyright (C) 2013 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-gevent
PKG_VERSION:=1.0
PKG_RELEASE:=1

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/surfly/gevent.git
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_VERSION:=a5ae94cab7c91f70e74eaba9d343983523d4554f
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION).tar.gz

PKG_BUILD_DEPENDS:=python python-cython

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/python-gevent
  SUBMENU:=Python
  SECTION:=libs
  CATEGORY:=Libraries
  TITLE:=gevent
  URL:=http://www.gevent.org/
  DEPENDS:=+python +python-greenlet
endef

define Package/python-gevent/description
  gevent is a coroutine-based Python networking library.
endef

define Build/Compile
	(cd $(PKG_BUILD_DIR)/libev; \
		$(TARGET_CONFIGURE_OPTS) \
                CFLAGS="$(TARGET_CFLAGS)" \
                CPPFLAGS="-I$(STAGING_DIR)/usr/include -I$(STAGING_DIR)/include" \
                LDFLAGS="-L$(STAGING_DIR)/usr/lib -L$(STAGING_DIR)/lib" \
		$(PKG_BUILD_DIR)/libev/configure \
			--target=$(GNU_TARGET_NAME) \
                        --host=$(GNU_TARGET_NAME) \
                        --build=$(GNU_HOST_NAME) \
                        --prefix=/usr \
                        --without-libiconv-prefix \
                        --without-libintl-prefix \
                        --disable-nls \
	);
	$(call Build/Compile/PyMod,,install --prefix="$(PKG_INSTALL_DIR)/usr", \
		CYTHON="$(STAGING_DIR_HOST)/usr/bin/cython" \
	)
endef

define Package/python-gevent/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
	    $(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
	    $(1)$(PYTHON_PKG_DIR)
endef

$(eval $(call BuildPackage,python-gevent))
