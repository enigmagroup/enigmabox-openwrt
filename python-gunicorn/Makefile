
include $(TOPDIR)/rules.mk

PKG_NAME:=python-gunicorn
PKG_VERSION:=18.0
PKG_RELEASE:=1

PKG_SOURCE:=gunicorn-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/source/g/gunicorn/
PKG_MD5SUM:=c7138b9ac7515a42066922d2b6120fbe

PKG_BUILD_DIR:=$(BUILD_DIR)/gunicorn-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=python python-setuptools

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/python-gunicorn
  SECTION:=language-python
  CATEGORY:=Languages
  SUBMENU:=Python
  TITLE:=Python Gunicorn
  URL:=https://pypi.python.org/pypi/gunicorn/
  DEPENDS:=+python-setuptools
endef

define Package/python-gunicorn/description
 TODO
endef

define Build/Compile
	$(call Build/Compile/PyMod,., \
		install --prefix="/usr" --root="$(PKG_INSTALL_DIR)", \
		PYTHONPATH="$(PYTHON_LIB_DIR):$(STAGING_DIR_ROOT)/$(PYTHON_PKG_DIR)"; \
	)
endef

define Package/python-gunicorn/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
		$(1)$(PYTHON_PKG_DIR)/

	$(INSTALL_DIR) $(1)/usr/bin
	$(CP) \
		$(PKG_INSTALL_DIR)/usr/bin/gunicorn \
		$(1)/usr/bin/
	sed 's/#!.*/#!\/usr\/bin\/python/' -i $(1)/usr/bin/gunicorn
endef

$(eval $(call BuildPackage,python-gunicorn))
