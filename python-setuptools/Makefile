
include $(TOPDIR)/rules.mk

PKG_NAME:=python-setuptools
PKG_VERSION:=5.2
PKG_RELEASE:=1

PKG_SOURCE:=setuptools-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/source/s/setuptools/
PKG_MD5SUM:=ea6ed9ab1a4abe978dade73a592a229c

PKG_BUILD_DIR:=$(BUILD_DIR)/setuptools-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=python

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/python-setuptools
  SECTION:=language-python
  CATEGORY:=Languages
  SUBMENU:=Python
  TITLE:=Python Setuptools
  URL:=https://pypi.python.org/pypi/setuptools/
endef

define Package/python-setuptools/description
 Easily download, build, install, upgrade, and uninstall Python packages.
endef

define Build/Compile
	$(call Build/Compile/PyMod,., \
		install --prefix="/usr" --root="$(PKG_INSTALL_DIR)" \
	)
endef

define Package/python-setuptools/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
		$(1)$(PYTHON_PKG_DIR)/
endef

$(eval $(call BuildPackage,python-setuptools))
