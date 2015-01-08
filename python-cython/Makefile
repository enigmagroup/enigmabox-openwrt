#
# Copyright (C) 2009-2010 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-cython
PKG_VERSION:=0.20.2
PKG_RELEASE:=1

PKG_SOURCE:=Cython-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=http://www.cython.org/release/
PKG_BUILD_DIR:=$(BUILD_DIR)/Cython-$(PKG_VERSION)
PKG_MD5SUM:=7fc13e1c665bdf7cea19ad08906af91f

PKG_BUILD_DEPENDS:=python python-cython/host
HOST_BUILD_DEPENDS:=python

HOST_BUILD_DIR:=$(BUILD_DIR_HOST)/Cython-$(PKG_VERSION)

include $(INCLUDE_DIR)/host-build.mk
include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/python-cython
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=python-cython
  URL:=http://www.cython.org
  DEPENDS:=+python
endef

define Package/python-cython/description
  Cython is a language that should make writing C extensions for the Python language easier
endef

define Build/Compile
	echo build-compile
	# <--no-cython-compile> required, otherwise setup.py calls the target-gcc to create so-files which obviously can't be used by <python> on the host system.
	$(call Build/Compile/PyMod,,install --single-version-externally-managed --no-cython-compile --prefix="/usr" --root="$(PKG_INSTALL_DIR)")
endef

#$(call Build/Compile/PyMod,,install --single-version-externally-managed --no-cython-compile --prefix="/usr" --root="$(PKG_INSTALL_DIR)")

define Build/InstallDev
	echo build-installdev
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
	    $(PKG_INSTALL_DIR)/usr/lib/python2.7/site-packages/* \
	    $(1)$(PYTHON_PKG_DIR)
	$(CP) \
	    $(PKG_INSTALL_DIR)/usr/lib/python2.7/site-packages/* \
	    $(STAGING_DIR_HOST)/lib/python2.7/site-packages/
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
	echo host-compile
	$(call Host/Compile/PyMod,,install --single-version-externally-managed --no-cython-compile --prefix="/usr" --root="$(STAGING_DIR_HOST)")
endef

#$(call Host/Compile/PyMod,,install --single-version-externally-managed --no-cython-compile --prefix="/usr" --root="$(STAGING_DIR_HOST)")

define Host/Install
endef

$(eval $(call HostBuild))

$(eval $(call BuildPackage,python-cython))
