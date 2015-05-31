include $(TOPDIR)/rules.mk

PKG_NAME:=dokuwiki
PKG_VERSION:=2015-05-20-ee6d15b6ee72f57c177065e23d15d15570bdb890
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.bz2
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_URL:=https://github.com/claudehohl/dokuwiki-kickstart.git
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=ee6d15b6ee72f57c177065e23d15d15570bdb890
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/dokuwiki
  SECTION:=admin
  CATEGORY:=Enigmabox
  TITLE:=DokuWiki - a document based Wiki
  DEPENDS:=hypesites
  SUBMENU:=Hypesite apps
endef

define Package/dokuwiki/description
 DokuWiki is a simple to use and highly versatile Open Source wiki software that doesn't require a database.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/dokuwiki/install
	$(INSTALL_DIR) $(1)/www/htdocs/dokuwiki
	$(CP) -rv $(PKG_BUILD_DIR)/* $(1)/www/htdocs/dokuwiki/

	# hypesite config
	$(INSTALL_DIR) $(1)/etc/lighttpd/hypesites.d
	$(INSTALL_DATA) ./files/dokuwiki.conf $(1)/etc/lighttpd/hypesites.d/dokuwiki.conf
endef

$(eval $(call BuildPackage,dokuwiki))
