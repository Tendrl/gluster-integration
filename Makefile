<<<<<<< HEAD
NAME=tendrl-gluster-integration
=======
NAME=tendrl-gluster-bridge
>>>>>>> 0dc82528d2391bd647f9e2c51617fc405c5069bc
VERSION=0.0.1

all: srpm

clean:
	rm -rf dist/
	rm -rf $(NAME)-$(VERSION).tar.gz
	rm -rf $(NAME)-$(VERSION)-1.el7.src.rpm

dist:
	python setup.py sdist \
	  && mv dist/$(NAME)-$(VERSION).tar.gz .

srpm: dist
	fedpkg --dist epel7 srpm

rpm: dist
	mock -r epel-7-x86_64 rebuild $(NAME)-$(VERSION)-1.el7.src.rpm

.PHONY: dist rpm srpm
