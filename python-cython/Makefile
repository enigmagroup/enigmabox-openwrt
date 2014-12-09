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
  DEPENDS:=+python-mini
endef

define Package/python-cython/description
  Cython is a language that should make writing C extensions for the Python language easier
endef

define Build/Compile
	echo build-compile
	# <--no-cython-compile> required, otherwise setup.py calls the target-gcc to create so-files which obviously can't be used by <python> on the host system.
	$(call Build/Compile/PyMod,., \
		install --no-cython-compile --prefix="$(PKG_INSTALL_DIR)/usr", \
	)
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
#define Host/Compile/PyMod
#        $(call HostPython, \
#                cd $(HOST_BUILD_DIR)/$(strip $(1)); \
#                CFLAGS="$(HOST_CFLAGS)" \
#                CPPFLAGS="$(HOST_CPPFLAGS)" \
#                LDFLAGS="$(HOST_LDFLAGS)" \
#                $(3) \
#                , \
#                ./setup.py $(2) \
#        )
#endef

# $(1) => build subdir
# $(2) => additional arguments to setup.py
# $(3) => additional variables
define Host/Compile/PyMod
	$(INSTALL_DIR) $(PKG_INSTALL_DIR)/$(PYTHON_PKG_DIR)
	$(call HostPython, \
		cd $(HOST_BUILD_DIR)/$(strip $(1)); \
		CC="$(TARGET_CC)" \
		CCSHARED="$(TARGET_CC) $(FPIC)" \
		LD="$(TARGET_CC)" \
		LDSHARED="$(TARGET_CC) -shared" \
		CFLAGS="$(HOST_CFLAGS)" \
		CPPFLAGS="$(HOST_CPPFLAGS) -I$(PYTHON_INC_DIR)" \
		LDFLAGS="$(HOST_LDFLAGS) -lpython$(PYTHON_VERSION)" \
		_PYTHON_HOST_PLATFORM="linux-$(ARCH)" \
		__PYVENV_LAUNCHER__="/usr/bin/$(PYTHON)" \
		$(3) \
		, \
		./setup.py $(2) \
	)
	find $(PKG_INSTALL_DIR) -name "*\.pyc" -o -name "*\.pyo" | xargs rm -f
endef

define Host/Compile
	echo host-compile
	$(call Host/Compile/PyMod,., \
		install --no-cython-compile --prefix="$(STAGING_DIR_HOST)/usr", \
		PYTHONPATH="/root:$(STAGING_DIR_HOST)/usr/lib/python2.7/site-packages/:/root:$(PYTHON_LIB_DIR):$(STAGING_DIR_ROOT)/$(PYTHON_PKG_DIR)"; \
	)
endef

define Host/Install
endef

$(eval $(call HostBuild))

$(eval $(call BuildPackage,python-cython))
