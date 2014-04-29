include $(TOPDIR)/rules.mk

PKG_NAME:=exim4
PKG_VERSION:=4.82
PKG_RELEASE:=1

PKG_SOURCE:=exim-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=http://mirror.switch.ch/ftp/mirror/exim/exim/exim4/
PKG_MD5SUM:=7f7b50394f8f3d4141e7dca9392f62f0

PKG_BUILD_DIR:=$(BUILD_DIR)/exim-$(PKG_VERSION)

CC="$(TARGET_CC)"

include $(INCLUDE_DIR)/package.mk

define Package/exim4
  SECTION:=mail
  CATEGORY:=Mail
  TITLE:=Exim Internet Mailer Version 4
  DEPENDS:=+libdb47 +libiconv +libpcre +@CCACHE
  URL:=http://www.exim.org/
endef

define Package/exim4/description
	Description.
endef

define Build/Configure
	cp ./files/Makefile $(PKG_BUILD_DIR)/Local/Makefile
endef

define Build/Compile
	cd $(PKG_BUILD_DIR) && EXIM_ARCHTYPE=i386 make
endef

define Package/exim4/install
	$(INSTALL_DIR) $(1)/usr/exim/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exim $(1)/usr/exim/bin/exim
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exim_dumpdb $(1)/usr/exim/bin/exim_dumpdb
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exim_fixdb $(1)/usr/exim/bin/exim_fixdb
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exim_tidydb $(1)/usr/exim/bin/exim_tidydb
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exinext $(1)/usr/exim/bin/exinext
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exiwhat $(1)/usr/exim/bin/exiwhat
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exim_dbmbuild $(1)/usr/exim/bin/exim_dbmbuild
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exicyclog $(1)/usr/exim/bin/exicyclog
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exigrep $(1)/usr/exim/bin/exigrep
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/eximstats $(1)/usr/exim/bin/eximstats
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exipick $(1)/usr/exim/bin/exipick
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exiqgrep $(1)/usr/exim/bin/exiqgrep
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exiqsumm $(1)/usr/exim/bin/exiqsumm
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exim_lock $(1)/usr/exim/bin/exim_lock
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exim_checkaccess $(1)/usr/exim/bin/exim_checkaccess

	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/build-Linux-i386/exim $(1)/usr/sbin/exim4

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/exim.init $(1)/etc/init.d/exim
endef

$(eval $(call BuildPackage,exim4))
