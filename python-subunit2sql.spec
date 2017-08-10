%global pypi_name subunit2sql
%global with_doc 1

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
subunit2SQL is a tool for storing test results data in a SQL database. \
Like it's name implies it was originally designed around converting \
subunit streams to data in a SQL database and the packaged utilities \
assume a subunit stream as the input format. However, the data model \
used for the DB does not preclude using any test result format.

Name:           python-%{pypi_name}
Version:        1.8.0
Release:        4%{?dist}
Summary:        Tooling for converting subunit streams into a SQL DB

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/subunit2sql
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

# Test Requirements
BuildRequires:  python-fixtures
BuildRequires:  python-mock
BuildRequires:  python-testscenarios
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
BuildRequires:  python-PyMySQL
BuildRequires:  python-psycopg2
BuildRequires:  python-os-testr
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-testresources
BuildRequires:  python-dateutil

Requires:   python-pbr
Requires:   python-alembic
Requires:   python-oslo-config
Requires:   python-oslo-db
Requires:   python-subunit
Requires:   python-six
Requires:   python-SQLAlchemy
Requires:   python-stevedore
Requires:   python-dateutil

%description -n python2-%{pypi_name}
%{common_desc}

%package -n    python2-%{pypi_name}-graph
Summary:    %{name} graph subpackage

Requires:   python2-%{pypi_name} = %{version}-%{release}
Requires:   python-pandas
Requires:   python-matplotlib

%description -n    python2-%{pypi_name}-graph
%{common_desc}

It contains graph plugin for %{name}.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr

# Test Requirements
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools
BuildRequires:  python3-PyMySQL
BuildRequires:  python3-psycopg2
BuildRequires:  python3-os-testr
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-testresources
BuildRequires:  python3-dateutil

Requires:   python3-pbr
Requires:   python3-alembic
Requires:   python3-oslo-config
Requires:   python3-oslo-db
Requires:   python3-subunit
Requires:   python3-six
Requires:   python3-sqlalchemy
Requires:   python3-stevedore
Requires:   python3-dateutil

%description -n python3-%{pypi_name}
%{common_desc}

%package -n    python3-%{pypi_name}-graph
Summary:    %{name} graph subpackage

Requires:   python3-%{pypi_name} = %{version}-%{release}
Requires:   python3-pandas
Requires:   python3-matplotlib

%description -n    python3-%{pypi_name}-graph
%{common_desc}

It contains graph plugin for %{name}.
%endif

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        subunit2sql documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-oslo-db

%description -n python-%{pypi_name}-doc
%{common_desc}

It contains the documentation for subunit2sql.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm -f test-requirements.txt requirements.txt

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%if 0%{?with_python3}
%py3_install
cp %{buildroot}/%{_bindir}/subunit2sql-db-manage %{buildroot}/%{_bindir}/subunit2sql-db-manage-3
ln -sf %{_bindir}/subunit2sql-db-manage-3 %{buildroot}/%{_bindir}/subunit2sql-db-manage-%{python3_version}
cp %{buildroot}/%{_bindir}/subunit2sql %{buildroot}/%{_bindir}/subunit2sql-3
ln -sf %{_bindir}/subunit2sql-3 %{buildroot}/%{_bindir}/subunit2sql-%{python3_version}
cp %{buildroot}/%{_bindir}/sql2subunit %{buildroot}/%{_bindir}/sql2subunit-3
ln -sf %{_bindir}/sql2subunit-3 %{buildroot}/%{_bindir}/sql2subunit-%{python3_version}
cp %{buildroot}/%{_bindir}/subunit2sql-graph %{buildroot}/%{_bindir}/subunit2sql-graph-3
ln -sf %{_bindir}/subunit2sql-graph-3 %{buildroot}/%{_bindir}/subunit2sql-graph-%{python3_version}
%endif

%py2_install
cp %{buildroot}/%{_bindir}/subunit2sql-db-manage %{buildroot}/%{_bindir}/subunit2sql-db-manage-2
ln -sf %{_bindir}/subunit2sql-db-manage-2 %{buildroot}/%{_bindir}/subunit2sql-db-manage-%{python2_version}
cp %{buildroot}/%{_bindir}/subunit2sql %{buildroot}/%{_bindir}/subunit2sql-2
ln -sf %{_bindir}/subunit2sql-2 %{buildroot}/%{_bindir}/subunit2sql-%{python2_version}
cp %{buildroot}/%{_bindir}/sql2subunit %{buildroot}/%{_bindir}/sql2subunit-2
ln -sf %{_bindir}/sql2subunit-2 %{buildroot}/%{_bindir}/sql2subunit-%{python2_version}
cp %{buildroot}/%{_bindir}/subunit2sql-graph %{buildroot}/%{_bindir}/subunit2sql-graph-2
ln -sf %{_bindir}/subunit2sql-graph-2 %{buildroot}/%{_bindir}/subunit2sql-graph-%{python2_version}


%check
%{__python2} setup.py test

%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/subunit2sql-db-manage
%{_bindir}/subunit2sql-db-manage-2
%{_bindir}/subunit2sql-db-manage-%{python2_version}
%{_bindir}/subunit2sql
%{_bindir}/subunit2sql-2
%{_bindir}/subunit2sql-%{python2_version}
%{_bindir}/sql2subunit
%{_bindir}/sql2subunit-2
%{_bindir}/sql2subunit-%{python2_version}
%exclude %{_bindir}/subunit2sql-graph
%exclude %{_bindir}/subunit2sql-graph-2
%exclude %{_bindir}/subunit2sql-graph-%{python2_version}
%{python2_sitelib}/%{pypi_name}
%exclude %{python2_sitelib}/%{pypi_name}/analysis
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python2-%{pypi_name}-graph
%{_bindir}/subunit2sql-graph
%{_bindir}/subunit2sql-graph-2
%{_bindir}/subunit2sql-graph-%{python2_version}
%{python2_sitelib}/%{pypi_name}/analysis

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/subunit2sql-db-manage-3
%{_bindir}/subunit2sql-db-manage-%{python3_version}
%{_bindir}/subunit2sql-3
%{_bindir}/subunit2sql-%{python3_version}
%{_bindir}/sql2subunit-3
%{_bindir}/sql2subunit-%{python3_version}
%exclude %{_bindir}/subunit2sql-graph-3
%exclude %{_bindir}/subunit2sql-graph-%{python3_version}
%{python3_sitelib}/%{pypi_name}
%exclude %{python3_sitelib}/%{pypi_name}/analysis
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python3-%{pypi_name}-graph
%{_bindir}/subunit2sql-graph-3
%{_bindir}/subunit2sql-graph-%{python3_version}
%{python3_sitelib}/%{pypi_name}/analysis
%endif

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Thu Aug 10 2017 Chandan Kumar <chkumar246@gmail.com> - 1.8.0-4
- Fixed package name for sqlalchemy

* Wed Aug 02 2017 Chandan Kumar <chkumar246@gmail.com> - 1.8.0-3
- Enable python3 subpackage
- Shortened summary and description

* Tue Aug 01 2017 Chandan Kumar <chkumar246@gmail.com> - 1.8.0-2
- Moved graph binary to a seperate subpackage

* Mon Jul 31 2017 Chandan Kumar <chkumar246@gmail.com> - 1.8.0-1
- Initial package.
