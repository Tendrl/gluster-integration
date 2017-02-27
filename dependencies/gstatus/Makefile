NAME=gstatus
VERSION=0.64

clean:
	rm -fr gstatus*

dist:
	git clone https://github.com/gluster/gstatus > /dev/null || : \
	&& cd gstatus \
	&& python setup.py sdist \
	  && mv dist/$(NAME)-$(VERSION).tar.gz ../. \
	&& cp gstatus.spec ../.

srpm:
	fedpkg --dist epel7 srpm

rpm:
	mock -r epel-7-x86_64 rebuild $(NAME)*src.rpm --resultdir=. --define "dist .el7"

