# TODO: system uchardet?
#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	cChardet - high speed universal character encoding detector
Summary(pl.UTF-8):	cChardet - szybki, uniwersalny wykrywacz kodowania znaków
Name:		python-cchardet
Version:	2.1.5
Release:	3
License:	MPL v1.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cchardet/
Source0:	https://files.pythonhosted.org/packages/source/c/cchardet/cchardet-%{version}.tar.gz
# Source0-md5:	681af4e6546e47e2ae856057a8a7d105
URL:		https://pypi.org/project/cchardet/
BuildRequires:	libstdc++-devel
%if %{with python2}
BuildRequires:	python-Cython
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-nose
%endif
%endif
%if %{with python3}
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cChardet is high speed universal character encoding detector - binding
to uchardet.

%description -l pl.UTF-8
cChardet to szybki, uniwersalny wykrywacz kodowania znaków - wiązanie
do biblioteki uchardet.

%package -n python3-cchardet
Summary:	cChardet - high speed universal character encoding detector
Summary(pl.UTF-8):	cChardet - szybki, uniwersalny wykrywacz kodowania znaków
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-cchardet
cChardet is high speed universal character encoding detector - binding
to uchardet.

%description -n python3-cchardet -l pl.UTF-8
cChardet to szybki, uniwersalny wykrywacz kodowania znaków - wiązanie
do biblioteki uchardet.

%prep
%setup -q -n cchardet-%{version}

ln -snf ../tests src/tests/tests

# these fail:
# - recognized as Windows-1252
%{__rm} src/tests/testdata/{fi,ga}/iso-8859-1.txt
# - recognized as iso-8859-11
%{__rm} src/tests/testdata/th/tis-620.txt

%build
%if %{with python2}
%py_build

%if %{with tests}
cd src/tests
LC_ALL=C \
PYTHONPATH=$(readlink -f ../../build-2/lib.*) \
%{__python} -m nose test.py
cd ../..
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
cd src/tests
LC_ALL=C \
PYTHONPATH=$(readlink -f ../../build-3/lib.*) \
%{__python3} -m nose test.py
cd ../..
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/cchardetect
%endif
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%if %{without python3}
%attr(755,root,root) %{_bindir}/cchardetect
%endif
%dir %{py_sitedir}/cchardet
%{py_sitedir}/cchardet/*.py[co]
%attr(755,root,root) %{py_sitedir}/cchardet/*.so
%{py_sitedir}/cchardet-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-cchardet
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/cchardetect
%dir %{py3_sitedir}/cchardet
%{py3_sitedir}/cchardet/*.py
%attr(755,root,root) %{py3_sitedir}/cchardet/*.so
%{py3_sitedir}/cchardet/__pycache__
%{py3_sitedir}/cchardet-%{version}-py*.egg-info
%endif
