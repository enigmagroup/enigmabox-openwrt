#
# Copyright (C) 2006 OpenWrt.org
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
PKG_BUILD_DIR:=$(BUILD_DIR)/Cython-$(PKG_VERSION)/
PKG_MD5SUM:=7fc13e1c665bdf7cea19ad08906af91f

PKG_BUILD_DEPENDS:=python-setuptools

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/python-cython
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=The Cython compiler for writing C extensions for the Python language.
  URL:=http://www.cython.org
  DEPENDS:=+python
endef

define Package/python-cython/description
 The Cython language makes writing C extensions for the Python language as
 easy as Python itself.  Cython is a source code translator based on the
 well-known Pyrex but supports more cutting edge functionality and
 optimizations.
 The Cython language is very close to the Python language and most Python
 code is also valid Cython code but Cython additionally supports calling C
 functions and declaring C types on variables and class attributes. This
 allows the compiler to generate very efficient C code from Cython code.
 This makes Cython the ideal language for writing glue code for external C
 libraries and for fast C modules that speed up the execution of Python
endef

define Build/Compile
	# <--no-cython-compile> required, otherwise setup.py calls the target-gcc to create so-files which obviously can't be used by <python> on the host system.
	$(call Build/Compile/PyMod,., \
		install --no-cython-compile --prefix="/usr" --root="$(PKG_INSTALL_DIR)" \
	)
endef

define Build/InstallDev
	$(INSTALL_DIR) $(STAGING_DIR)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
		$(STAGING_DIR)$(PYTHON_PKG_DIR)/
	[ ! -e $(PKG_INSTALL_DIR)/usr/include ] || $(CP) \
		$(PKG_INSTALL_DIR)/usr/include/* \
		$(STAGING_DIR)/usr/include/
endef

define Package/python-cython/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
		$(1)$(PYTHON_PKG_DIR)
	$(INSTALL_DIR) $(1)/usr/bin
	$(CP) \
		$(PKG_INSTALL_DIR)/usr/bin/cython \
		$(1)/usr/bin/cython
	$(SED) \
		's,^#!.*,#!/usr/bin/env python$(PYTHON_BINABI),g' \
		$(1)/usr/bin/cython
endef

define Host/Compile
	$(call Host/Compile/PyMod,., \
		install --no-cython-compile --prefix="/usr" --root="$(STAGING_DIR_HOST)" \
	)
endef

define Host/Install
endef

$(eval $(call HostBuild))

$(eval $(call BuildPackage,python-cython))
