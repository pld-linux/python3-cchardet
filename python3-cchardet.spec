# TODO: system uchardet?
#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	cChardet - high speed universal character encoding detector
Summary(pl.UTF-8):	cChardet - szybki, uniwersalny wykrywacz kodowania znaków
Name:		python3-cchardet
Version:	2.1.7
Release:	1
License:	MPL v1.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cchardet/
Source0:	https://files.pythonhosted.org/packages/source/c/cchardet/cchardet-%{version}.tar.gz
# Source0-md5:	8a76472ad09c68c12069203ea9348ee3
URL:		https://pypi.org/project/cchardet/
BuildRequires:	libstdc++-devel
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cChardet is high speed universal character encoding detector - binding
to uchardet.

%description -l pl.UTF-8
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
%py3_build

%if %{with tests}
cd src/tests
LC_ALL=C \
PYTHONPATH=$(readlink -f ../../build-3/lib.*) \
%{__python3} -m nose test.py
cd ../..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/cchardetect
%dir %{py3_sitedir}/cchardet
%{py3_sitedir}/cchardet/*.py
%attr(755,root,root) %{py3_sitedir}/cchardet/*.so
%{py3_sitedir}/cchardet/__pycache__
%{py3_sitedir}/cchardet-%{version}-py*.egg-info
