Name:           resultsdb_frontend
Version:        1.2.0
Release:        2%{?dist}
Summary:        Frontend for the ResultsDB

License:        GPLv2+
URL:            https://bitbucket.org/fedoraqa/resultsdb_frontend
Source0:        https://qadevel.cloud.fedoraproject.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       python-flask
Requires:       python2-iso8601
Requires:       python-resultsdb_api
Requires:       python-six
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%description
ResultsDB fronted is a simple application that
allows browsing the data stored inside ResultsDB.

%prep
%setup -q

%check
# for some reason, this is the only place where the files get deleted, better ideas?
rm -f %{buildroot}%{_sysconfdir}/resultsdb_frontend/*.py{c,o}

%build
%py2_build

%install
%py2_install

# apache and wsgi settings
mkdir -p %{buildroot}%{_datadir}/resultsdb_frontend/conf
install -p -m 0644 conf/resultsdb_frontend.conf %{buildroot}%{_datadir}/resultsdb_frontend/conf/resultsdb_frontend.conf
install -p -m 0644 conf/resultsdb_frontend.wsgi %{buildroot}%{_datadir}/resultsdb_frontend/resultsdb_frontend.wsgi

mkdir -p %{buildroot}%{_sysconfdir}/resultsdb_frontend
install -p -m 0644 conf/settings.py.example %{buildroot}%{_sysconfdir}/resultsdb_frontend/settings.py

%files
%doc README.md
%license LICENSE
%{python2_sitelib}/resultsdb_frontend
%{python2_sitelib}/*.egg-info

%dir %{_sysconfdir}/resultsdb_frontend
%config(noreplace) %{_sysconfdir}/resultsdb_frontend/settings.py

%dir %{_datadir}/resultsdb_frontend
%{_datadir}/resultsdb_frontend/*

%changelog
* Thu Nov 10 2016 Martin Krizek <mkrizek@fedoraproject.org> - 1.2.0-2
- do not replace config file

* Thu Nov 3 2016 Tim FLink <tflink@fedoraproject.org> - 1.2.0-1
- add support for resultsdb v2.0

* Mon Sep 26 2016 Martin Krizek <mkrizek@redhat.com> - 1.1.9-4
- preserve timestamps on installed files

* Wed Sep 21 2016 Martin Krizek <mkrizek@redhat.com> - 1.1.9-3
- use python macros for building and installing
- use python2-* where possible

* Mon Jun 13 2016 Martin Krizek <mkrizek@redhat.com> - 1.1.9-2
- add license
- remove not needed custom macros

* Thu Dec 17 2015 Martin Krizek <mkrizek@redhat.com> - 1.1.9-1
- cleaner search with no item specified (D566)
- change mock root to f22

* Tue Aug 18 2015 Tim Flink <tflink@fedoraproject.org> - 1.1.8-1
- add fedmenu support (D363)

* Wed Jul 22 2015 Martin Krizek <mkrizek@redhat.com> - 1.1.7-1
- provide better description of the job info link

* Tue Jul 21 2015 Martin Krizek <mkrizek@redhat.com> - 1.1.6-1
- firefox search fix
- search by outcome

* Wed Jul 8 2015 Martin Krizek <mkrizek@redhat.com> - 1.1.5-1
- Search improvements
- Updated conf to be compatible with Apache 2.4
- Show version in footer

* Wed Apr 1 2015 Tim Flink <tflink@fedoraproject.org> - 1.1.4-1
- better handling of 404 errors (T410)
- fixing search button to redirect to proper URL (T402)

* Wed Oct 29 2014 Tim Flink <tflink@fedoraproject.org> - 1.1.3-1
- adding search button to frontpage (T347)

* Fri Jun 27 2014 Tim Flink <tflink@fedoraproject.org> - 1.1.1-1
- Adding link to logs from result detail

* Fri May 16 2014 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Releasing resultsdb_frontend 1.1.0

* Fri Apr 25 2014 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- updating to new upstream, fixing some variable name errors

* Fri Apr 25 2014 Tim Flink <tflink@fedoraproject.org> - 1.0.1-2
- updating to new upstream, fixing resultsdb_api dep, removing resultsdb_frontend binary

* Thu Feb 6 2014 Jan Sedlak <jsedlak@redhat.com> - 1.0.0-1
- initial packaging
