#
# Copyright (C) 2013 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-gevent
PKG_VERSION:=2014-12-14-72119c8c3e704b75a2d91d8555ca8673928ebabb
PKG_RELEASE:=1

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/surfly/gevent.git
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_VERSION:=72119c8c3e704b75a2d91d8555ca8673928ebabb
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz

PKG_BUILD_DEPENDS:=python python-cython
PKG_USE_MIPS16:=0

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

# This is required in addition to PKG_USE_MIPS16:=0 because otherwise MIPS16
# flags are inherited from the Python base package (via sysconfig module)
ifdef CONFIG_USE_MIPS16
TARGET_CFLAGS += -mno-mips16 -mno-interlink-mips16
endif

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
	$(call Build/Compile/PyMod,., \
		install --prefix="/usr" --root="$(PKG_INSTALL_DIR)", \
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
