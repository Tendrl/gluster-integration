NAME=gstatus
VERSION=0.64
RELEASE=3

clean:
	rm -fr gstatus* *.log

dist:
	wget https://github.com/gluster/gstatus/archive/v$(VERSION)-$(RELEASE).tar.gz
	tar -zxvf v$(VERSION)-$(RELEASE).tar.gz
	mv $(NAME)-$(VERSION)-$(RELEASE) $(NAME)
	cp $(NAME)/$(NAME).spec .
	tar -pczf $(NAME)-$(VERSION).tar.gz $(NAME)
	rm -fr v$(VERSION)* $(NAME)

srpm:
	fedpkg --dist epel7 srpm

rpm:
	mock -r epel-7-x86_64 rebuild $(NAME)*src.rpm --resultdir=. --define "dist .el7"

