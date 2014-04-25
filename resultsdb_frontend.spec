%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           resultsdb_frontend
Version:        1.0.2
Release:        1%{?dist}
Summary:        Frontend for the ResultsDB

License:        GPLv2+
URL:            https://bitbucket.org/fedoraqa/resultsdb_frontend
Source0:        https://qadevel.cloud.fedoraproject.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       python-flask
Requires:       python-flask-wtf
Requires:       python-flask-restful
Requires:       python-six
Requires:       python-iso8601
Requires:       resultsdb_api
BuildRequires:  python2-devel python-setuptools

%description
ResultsDB fronted is a simple application that
allows browsing the data stored inside ResultsDB.

%prep
%setup -q

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# apache and wsgi settings
mkdir -p %{buildroot}%{_datadir}/resultsdb_frontend/conf
cp conf/resultsdb_frontend.conf %{buildroot}%{_datadir}/resultsdb_frontend/conf/.
cp conf/resultsdb_frontend.wsgi %{buildroot}%{_datadir}/resultsdb_frontend/.

mkdir -p %{buildroot}%{_sysconfdir}/resultsdb_frontend
install conf/settings.py.example %{buildroot}%{_sysconfdir}/resultsdb_frontend/settings.py.example

%files
%doc README.md conf/*
%{python_sitelib}/resultsdb_frontend
%{python_sitelib}/*.egg-info

%dir %{_sysconfdir}/resultsdb_frontend
%{_sysconfdir}/resultsdb_frontend/*
%dir %{_datadir}/resultsdb_frontend
%{_datadir}/resultsdb_frontend/*

%changelog
* Fri Apr 25 2014 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- updating to new upstream, fixing some variable name errors

* Fri Apr 25 2014 Tim Flink <tflink@fedoraproject.org> - 1.0.1-2
- updating to new upstream, fixing resultsdb_api dep, removing resultsdb_frontend binary

* Thu Feb 6 2014 Jan Sedlak <jsedlak@redhat.com> - 1.0.0-1
- initial packaging
