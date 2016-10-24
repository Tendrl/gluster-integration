%define pkg_name tendrl-gluster-bridge
%define pkg_version 0.0.1
%define pkg_release 1

Name: %{pkg_name}
Version: %{pkg_version}
Release: %{pkg_release}%{?dist}
BuildArch: noarch
Summary: Common Module for All Bridges
Source0: %{pkg_name}-%{pkg_version}.tar.gz
Group:   Applications/System
License: GPLv2+
Url: https://github.com/Tendrl/gluster_bridge

#Requires: python-etcd
Requires: python-dateutil >= 2.2
Requires: python-gevent >= 1.0
Requires: python-greenlet >= 0.3.2
Requires: pytz

%description
Python module for Tendrl gluster bridge to manage gluster tasks.

%prep
%setup -n %{pkg_name}-%{pkg_version}

# Remove bundled egg-info
rm -rf %{pkg_name}.egg-info

%build
%{__python} setup.py build

# generate html docs
%if 0%{?rhel}==6
sphinx-1.0-build doc/source html
%else
sphinx-build doc/source html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -Dm 0644 tendrl-glusterd.service $RPM_BUILD_ROOT/usr/lib/systemd/system/tendrl-glusterd.service

%post
cat <<EOF >> /etc/tendrl/tendrl.conf

[gluster_bridge]
# Path to log file
log_path = /var/log/tendrl/gluster_bridge.log
log_level = DEBUG
EOF

/bin/systemctl enable tendrl-glusterd.service >/dev/null 2>&1 || :
/bin/systemctl restart tendrl-glusterd.service >/dev/null 2>&1 || :

%clean
rm -rf $RPM_BUILD_ROOT

%if 0%{?do_test}
%check
%{__python} setup.py test
%endif

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc html README.rst LICENSE
%{_usr}/lib/systemd/system/tendrl-glusterd.service


%changelog
* Mon Oct 24 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
