
include $(TOPDIR)/rules.mk

PKG_NAME:=python-unidecode
PKG_VERSION:=0.04.14
PKG_RELEASE:=1

PKG_SOURCE:=Unidecode-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/source/U/Unidecode/
PKG_MD5SUM:=d4106bcfdef39625944f4294ef4666de

PKG_BUILD_DIR:=$(BUILD_DIR)/Unidecode-$(PKG_VERSION)/Unidecode-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=python

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/python-unidecode
  SECTION:=language-python
  CATEGORY:=Languages
  SUBMENU:=Python
  TITLE:=Python Unidecode
  URL:=https://pypi.python.org/pypi/Unidecode
endef

define Package/python-unidecode/description
 TODO
endef

define Build/Compile
	$(call Build/Compile/PyMod,., \
		install --prefix="/usr" --root="$(PKG_INSTALL_DIR)" \
	)
endef

define Package/python-unidecode/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
		$(1)$(PYTHON_PKG_DIR)/
endef

$(eval $(call BuildPackage,python-unidecode))
