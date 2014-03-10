#
# Copyright (C) 2009-2010 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=cython
PKG_VERSION:=0.19
PKG_RELEASE:=1

PKG_SOURCE:=Cython-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=http://www.cython.org/release/
PKG_BUILD_DIR:=$(BUILD_DIR)/Cython-$(PKG_VERSION)
PKG_MD5SUM:=76989337dee4cf7afdcb5cde514423f8

PKG_BUILD_DEPENDS:=python cython/host
HOST_BUILD_DEPENDS:=python

HOST_BUILD_DIR:=$(BUILD_DIR_HOST)/Cython-$(PKG_VERSION)

include $(INCLUDE_DIR)/host-build.mk
include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/cython
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=cython
  URL:=http://www.cython.org
  DEPENDS:=+python-mini
endef

define Package/cython/description
  Cython is a language that should make writing C extensions for the Python language easier
endef

define Build/Compile
	# <--no-cython-compile> required, otherwise setup.py calls the target-gcc to create so-files which obviously can't be used by <python> on the host system.
	$(call Build/Compile/PyMod,,install --no-cython-compile --prefix="$(PKG_INSTALL_DIR)/usr")
endef

define Build/InstallDev
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
	    $(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
	    $(1)$(PYTHON_PKG_DIR)
endef

# TODO: this should be moved to python package
# $(1) => build subdir
# $(2) => additional arguments to setup.py
# $(3) => additional variables
define Host/Compile/PyMod
        $(call HostPython, \
                cd $(HOST_BUILD_DIR)/$(strip $(1)); \
                CFLAGS="$(HOST_CFLAGS)" \
                CPPFLAGS="$(HOST_CPPFLAGS)" \
                LDFLAGS="$(HOST_LDFLAGS)" \
                $(3) \
                , \
                ./setup.py $(2) \
        )
endef

define Host/Compile
	$(call Host/Compile/PyMod,,install --no-cython-compile --prefix="$(STAGING_DIR_HOST)/usr")
endef

define Host/Install
endef

$(eval $(call HostBuild))

$(eval $(call BuildPackage,cython))
