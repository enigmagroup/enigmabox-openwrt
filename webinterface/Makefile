include $(TOPDIR)/rules.mk

PKG_NAME:=webinterface
PKG_VERSION:=0.17.0
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/webinterface
  SECTION:=administration
  CATEGORY:=Enigmabox
  TITLE:=Enigmabox Webinterface
  URL:=http://enigmabox.net/en/
  DEPENDS:=+cjdns-master +python-django-1.4 +curl +python-gunicorn +python-six +python-gevent +python-openssl +python-requests +django-south +python-expat +python-json +python-sqlite3 +python-unidecode +asterisk18 +php5 +php5-fastcgi +php5-mod-mcrypt +php5-mod-pdo-sqlite +php5-mod-session +php5-mod-iconv +php5-mod-json +@PHP5_FILTER +nginx +privoxy +dovecot +exim4 +cfengine +cfengine-policies +beanstalkd +python-beanstalkc +pyyaml +syslog-ng +zip +unzip +shadow-usermod +kmod-ipt-nat6
endef

define Package/webinterface/description
	Description.
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/webinterface/install
	$(INSTALL_DIR) $(1)/box
	cp -r ./files/root/* $(1)

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/webinterface.init $(1)/etc/init.d/webinterface

	$(INSTALL_DIR) $(1)/etc/nginx/sites
	$(INSTALL_DATA) ./files/nginx-site.conf $(1)/etc/nginx/sites/webinterface.conf

	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) ./files/backup-stuff $(1)/usr/sbin/backup-stuff
	$(INSTALL_BIN) ./files/restore-stuff $(1)/usr/sbin/restore-stuff
endef

$(eval $(call BuildPackage,webinterface))
