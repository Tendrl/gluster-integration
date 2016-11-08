Name: tendrl-gluster-bridge
Version: 0.0.1
Release: 1%{?dist}
BuildArch: noarch
Summary: Module for Gluster Bridge
Source0: %{name}-%{version}.tar.gz
License: LGPLv2
URL: https://github.com/Tendrl/gluster_bridge

BuildRequires: systemd
BuildRequires: python2-devel
BuildRequires: pytest

Requires: python-etcd
Requires: python-dateutil >= 2.4
Requires: python-gevent >= 1.0
Requires: python-greenlet >= 0.4
Requires: pytz
Requires: python-taskflow >= 2.6
Requires: tendrl-bridge-common
Requires: systemd

%description
Python module for Tendrl gluster bridge to manage gluster tasks.

%prep
%setup -n %{name}-%{version}

# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%{__python} setup.py build

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -m 755 --directory $RPM_BUILD_ROOT%{_var}/log/tendrl
install -Dm 0644 tendrl-glusterd.service $RPM_BUILD_ROOT%{_unitdir}/tendrl-glusterd.service
install -Dm 755 etc/tendrl/tendrl.conf.sample $RPM_BUILD_ROOT%{_datadir}/tendrl/commons/tendrl.conf
install -Dm 755 etc/tendrl/tendrl.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/tendrl.conf.sample

%post
%systemd_post tendrl-glusterd.service

%preun
%systemd_preun tendrl-glusterd.service

%postun
%systemd_postun_with_restart tendrl-glusterd.service

%check
py.test -v tendrl/gluster_bridge/tests

%files -f INSTALLED_FILES
%dir %{_var}/log/tendrl
%doc README.rst
%license LICENSE
%{_datarootdir}/tendrl/commons/tendrl.conf
%{_sysconfdir}/tendrl.conf.sample
%{_unitdir}/tendrl-glusterd.service

%changelog
* Mon Oct 24 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
