%define	lib_major 1
%define lib_name %mklibname xml %{lib_major}

Summary:	The libXML library
Name:		libxml
Version:	1.8.17
Release:	%mkrel 18
License:	LGPL
Group:		System/Libraries
URL:		http://www.xmlsoft.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# (gb) 1.8.17-2mdk add missing include
Patch0:		libxml-1.8.17-includes.patch
# (fc) 1.8.17-3mdk remove -L/usr/lib from xml-config --libs
Patch1:		libxml-1.8.17-libdir.patch
Patch2:		libxml-1.8.17-open.patch
Patch3:		libxml-1.8.17-fix-str-fmt.patch
Patch4:		libxml-1.8.17-CVE-2009-2414,2416.diff
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This library allows you to manipulate XML files.

%package -n	%{lib_name}
Summary:	%{summary}
Group:		%{group}
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n	%{lib_name}
This library allows you to manipulate XML files.

%package -n	%{lib_name}-devel
Summary:	Libraries, includes and other files to develop libxml applications
Group:		Development/C
# (gb) As of 1.8.17 version, I can't see any changes that would
# require a specific dependency on release, thus permitting
# rpmlintfixes
Requires:	%{lib_name} = %{version}
Requires:	zlib-devel
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{lib_name}-devel
This packages contains the libraries, include and other files 
you can use to develop libxml applications.

%prep

%setup -q
%patch0 -p1 -b .includes
%patch1 -p1 -b .libdir
%patch2 -p1
%patch3 -p0 -b .str
%patch4 -p0 -b .CVE-2009-2414,2416

%build
autoreconf -fi
%configure2_5x
%make

%check
# all tests must pass
make check

%install
rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{lib_name}
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{lib_name}
%endif

%clean
rm -rf %{buildroot}

%files -n %{lib_name}
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING COPYING.LIB TODO
%{_libdir}/lib*.so.*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%{_bindir}/xml-config
%{_libdir}/lib*.so
%{_libdir}/*a
%{_libdir}/*.sh
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gnome-xml
