
include $(TOPDIR)/rules.mk

PKG_NAME:=django-south
PKG_VERSION:=0.8.3
PKG_RELEASE:=1

PKG_SOURCE:=south-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=http://www.aeracode.org/releases/south/
PKG_MD5SUM:=672e6399d7acee82987dac7551ed812d

PKG_BUILD_DIR:=$(BUILD_DIR)/south-$(PKG_VERSION)/South-$(PKG_VERSION)
PKG_BUILD_DEPENDS:=python

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python-package.mk)

define Package/django-south
  SECTION:=language-python
  CATEGORY:=Languages
  SUBMENU:=Python
  TITLE:=Django south 0.8.3
  URL:=http://south.aeracode.org/
  DEPENDS:=+python-django-1.4
endef

define Package/django-south/description
 TODO
endef

define Build/Compile
	$(call Build/Compile/PyMod,., \
		install --prefix="/usr" --root="$(PKG_INSTALL_DIR)" \
	)
endef

define Package/django-south/install
	$(INSTALL_DIR) $(1)$(PYTHON_PKG_DIR)
	$(CP) \
		$(PKG_INSTALL_DIR)$(PYTHON_PKG_DIR)/* \
		$(1)$(PYTHON_PKG_DIR)/
endef

$(eval $(call BuildPackage,django-south))
