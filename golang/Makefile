include $(TOPDIR)/rules.mk

PKG_NAME:=golang
PKG_VERSION:=1.9.2
PKG_RELEASE:=1

PKG_SOURCE:=go1.9.2.linux-amd64.tar.gz
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://storage.googleapis.com/golang
PKG_HASH:=de874549d9a8d8d8062be05808509c09a88a248e77ec14eb77453530829ac02b
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_UNPACK=$(HOST_TAR) -C $(PKG_BUILD_DIR) -xzf $(DL_DIR)/$(PKG_SOURCE)

include $(INCLUDE_DIR)/package.mk

define Package/golang
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Golang
endef

define Package/golang/description
 Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.
endef

define Build/Configure
endef

define Build/Compile
endef

define Build/InstallDev
	$(INSTALL_DIR) $(STAGING_DIR_HOSTPKG)/usr/local
	$(CP) -r $(PKG_BUILD_DIR)/go $(STAGING_DIR_HOSTPKG)/usr/local/
endef

$(eval $(call BuildPackage,golang))
