Name: tendrl-gluster-bridge
Version: 0.0.1
Release: 1%{?dist}
BuildArch: noarch
Summary: Module for Gluster Bridge
Source0: %{name}-%{version}.tar.gz
License: LGPLv2+
URL: https://github.com/Tendrl/gluster_bridge

BuildRequires: systemd
BuildRequires: python2-devel
BuildRequires: pytest
BuildRequires: python-mock
BuildRequires: python-dateutil
BuildRequires: python-gevent
BuildRequires: python-greenlet

Requires: python-etcd
Requires: python-dateutil
Requires: python-gevent
Requires: python-greenlet
Requires: pytz
Requires: tendrl-bridge-common
Requires: systemd

%description
Python module for Tendrl gluster bridge to manage gluster tasks.

%prep
%setup

# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%{__python} setup.py build

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -m 755 --directory $RPM_BUILD_ROOT%{_var}/log/tendrl/gluster_bridge
install -Dm 0644 tendrl-glusterd.service $RPM_BUILD_ROOT%{_unitdir}/tendrl-glusterd.service
install -Dm 755 etc/tendrl/tendrl.conf.sample $RPM_BUILD_ROOT%{_datadir}/tendrl/gluster_bridge/tendrl.conf.sample

%post
%systemd_post tendrl-glusterd.service

%preun
%systemd_preun tendrl-glusterd.service

%postun
%systemd_postun_with_restart tendrl-glusterd.service

%check
# the following test will be enabled once the test issues fixed
#py.test -v tendrl/gluster_bridge/tests

%files -f INSTALLED_FILES
%dir %{_var}/log/tendrl/gluster_bridge
%doc README.rst
%license LICENSE
%{_datarootdir}/tendrl/gluster_bridge/tendrl.conf.sample
%{_unitdir}/tendrl-glusterd.service

%changelog
* Mon Oct 24 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
