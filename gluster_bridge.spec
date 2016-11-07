%define pkg_name tendrl-gluster-bridge
%define pkg_version 0.0.1
%define pkg_release 1

Name: %{pkg_name}
Version: %{pkg_version}
Release: %{pkg_release}%{?dist}
BuildArch: noarch
Summary: Module for Gluster Bridge
Source0: %{pkg_name}-%{pkg_version}.tar.gz
Group:   Applications/System
License: LGPL2.1
Url: https://github.com/Tendrl/gluster_bridge

Requires: python-etcd
Requires: python-dateutil >= 2.4
Requires: python-gevent >= 1.0
Requires: python-greenlet >= 0.4
Requires: pytz
Requires: python-taskflow >= 2.6
Requires: tendrl-bridge-common

%description
Python module for Tendrl gluster bridge to manage gluster tasks.

%prep
%setup -n %{pkg_name}-%{pkg_version}

# Remove bundled egg-info
rm -rf %{pkg_name}.egg-info

%build
%{__python} setup.py build

# generate html docs
%if 0%{?rhel}==7
sphinx-1.0-build doc/source html
%else
sphinx-build doc/source html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -Dm 0644 tendrl-glusterd.service $RPM_BUILD_ROOT/usr/lib/systemd/system/tendrl-glusterd.service
install -Dm 755 etc/tendrl/tendrl.conf.sample $RPM_BUILD_ROOT/usr/share/tendrl/commons/tendrl.conf
install -Dm 755 etc/tendrl/tendrl.conf.sample $RPM_BUILD_ROOT/etc/tendrl.conf.sample

%post
mkdir /var/log/tendrl >/dev/null 2>&1 || :
%systemd_post tendrl-glusterd.service

%preun
%systemd_preun tendrl-glusterd.service

%postun
%systemd_postun_with_restart tendrl-glusterd.service

%files -f INSTALLED_FILES
%doc html README.rst
%license LICENSE
%{_datarootdir}/tendrl/commons/tendrl.conf
%{_sysconfdir}/tendrl.conf.sample
%{_usr}/lib/systemd/system/tendrl-glusterd.service

%changelog
* Mon Oct 24 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
