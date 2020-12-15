CURDIR := $(shell pwd)
MUNKIPKG := /usr/local/bin/munkipkg
PKG_ROOT := $(CURDIR)/pkg/plistyamlplist/payload
PKG_BUILD := $(CURDIR)/pkg/plistyamlplist/build
PKG_VERSION := $(shell defaults read $(CURDIR)/pkg/plistyamlplist/build-info.plist version)

objects = $(PKG_ROOT)/usr/local/bin/plistyamlplist \
	$(PKG_ROOT)/usr/local/bin/plistyamlplist_lib


default : $(PKG_BUILD)/plistyamlplist-$(PKG_VERSION).pkg
	@echo "Building plistyamlplist pkg"


$(PKG_BUILD)/plistyamlplist-$(PKG_VERSION).pkg: $(objects)
	cd $(CURDIR)/pkg && $(MUNKIPKG) plistyamlplist
	open $(CURDIR)/pkg/plistyamlplist/build


$(PKG_ROOT)/usr/local/bin/plistyamlplist:
	@echo "Copying plistyamlplist into /usr/local/bin"
	mkdir -p "$(PKG_ROOT)/usr/local/bin"
	cp "$(CURDIR)/plistyamlplist.py" "$(PKG_ROOT)/usr/local/bin/plistyamlplist"
	chmod 755 "$(PKG_ROOT)/usr/local/bin/plistyamlplist"


$(PKG_ROOT)/usr/local/bin/plistyamlplist_lib:
	@echo "Copying plistyamlplist_lib into /usr/local/bin"
	cp -Rf "$(CURDIR)/plistyamlplist_lib" "$(PKG_ROOT)/usr/local/bin/plistyamlplist_lib"

.PHONY : clean
clean :
	@echo "Cleaning up package root"
	rm "$(PKG_ROOT)/usr/local/bin/plistyamlplist" ||:
	rm -rf "$(PKG_ROOT)/usr/local/bin/plistyamlplist_lib" ||:
	rm $(CURDIR)/pkg/plistyamlplist/build/*.pkg ||:
