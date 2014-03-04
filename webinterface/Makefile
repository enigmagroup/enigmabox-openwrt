include $(TOPDIR)/rules.mk

PKG_NAME:=enigmabox-webinterface
PKG_VERSION:=20
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/enigmabox-webinterface
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Enigmabox Webinterface
  URL:=http://enigmabox.net/en/
  DEPENDS:=+python-django-1.4 +django-south +python-expat +python-json +python-sqlite3 +python-unidecode +asterisk18 +php5 +php5-mod-mcrypt +php5-mod-sqlite3 +nginx +privoxy +dovecot +exim4
endef

define Package/enigmabox-webinterface/description
	Description.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/enigmabox-webinterface/install
	mkdir $(1)/box
	cp -r ./files/* $(1)
endef

$(eval $(call BuildPackage,enigmabox-webinterface))
