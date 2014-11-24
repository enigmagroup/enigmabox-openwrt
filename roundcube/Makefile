include $(TOPDIR)/rules.mk

PKG_NAME:=roundcube
PKG_VERSION:=1.0.1
PKG_RELEASE:=6

include $(INCLUDE_DIR)/package.mk

define Package/roundcube
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Enigmabox web mail
endef

define Package/roundcube/description
 Roundcube is a browser-based multilingual IMAP client with an
 application-like user interface. It provides full functionality you expect
 from an email client, including MIME support, address book, folder
 manipulation, message searching and spell checking.

 This version has been modified to integrate with the Enigmabox address book.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/roundcube/install
	cp -rv ./files/root/* $(1)

	$(INSTALL_DIR) $(1)/etc/lighttpd/sites.d
	$(INSTALL_DATA) ./files/lighttpd-site.conf $(1)/etc/lighttpd/sites.d/roundcube.conf
endef

$(eval $(call BuildPackage,roundcube))
