
include $(TOPDIR)/rules.mk

PKG_NAME:=python-six
PKG_VERSION:=1.7.2
PKG_RELEASE:=1

PKG_SOURCE:=six-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/source/s/six/
PKG_MD5SUM:=4c26276583b01dfc73474cb32327af91

PKG_BUILD_DIR:=$(BUILD_DIR)/six-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=python

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/python-six
  SECTION:=language-python
  CATEGORY:=Languages
  SUBMENU:=Python
  TITLE:=Python Six
  URL:=https://pypi.python.org/pypi/six
endef

define Package/python-six/description
 Python 2 and 3 compatibility utilities.
endef

define Build/Compile
	$(call Build/Compile/PyMod,., \
		install --prefix="/usr" --root="$(PKG_INSTALL_DIR)" \
	)
endef

define Package/python-six/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
		$(1)$(PYTHON_PKG_DIR)/
endef

$(eval $(call BuildPackage,python-six))
