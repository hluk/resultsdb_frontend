%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global pkgname resultsdb_frontend
%global tarball_name resultsdb_frontend
%global commitname 1de5b340e4c6
%global bitbucket_username rajcze

Name:           resultsdb_frontend
Version:        1.0.0
Release:        1%{?dist}
Summary:        Frontend for the ResultsDB

License:        GPLv2+
URL:            https://bitbucket.org/rajcze/resultsdb_frontend
Source0:        https://bitbucket.org/rajcze/%{pkgname}/get/v1.0.tar.gz

BuildArch:      noarch

Requires:       python-flask
Requires:       python-flask-wtf
Requires:       python-flask-restful
Requires:       python-six
Requires:       python-iso8601
Requires:       python-resultsdb_api
BuildRequires:  python2-devel python-setuptools

%description
ResultsDB fronted is a simple application that
allows browsing the data stored inside ResultsDB.

%prep
%setup -qn %{bitbucket_username}-%{pkgname}-%{commitname}

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

%attr(755,root,root) %{_bindir}/resultsdb_frontend
%dir %{_sysconfdir}/resultsdb_frontend
%{_sysconfdir}/resultsdb_frontend/*
%dir %{_datadir}/resultsdb_frontend
%{_datadir}/resultsdb_frontend/*

%changelog
* Thu Feb 6 2014 Jan Sedlak <jsedlak@redhat.com> - 1.0.0-1
- initial packaging
