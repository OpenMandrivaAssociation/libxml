%define url_ver %(echo %{version}|cut -d. -f1,2)

%define	major 1
%define libname %mklibname xml %{major}
%define devname %mklibname xml %{major} -d

Summary:	The libXML library
Name:		libxml
Version:	1.8.17
Release:	22
License:	LGPLv2
Group:		System/Libraries
Url:		http://www.xmlsoft.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/libxml/%{url_ver}/%{name}-%{version}.tar.bz2
# (gb) 1.8.17-2mdk add missing include
Patch0:		libxml-1.8.17-includes.patch
# (fc) 1.8.17-3mdk remove -L/usr/lib from xml-config --libs
Patch1:		libxml-1.8.17-libdir.patch
Patch2:		libxml-1.8.17-open.patch
Patch3:		libxml-1.8.17-fix-str-fmt.patch
Patch4:		libxml-1.8.17-CVE-2009-2414,2416.diff
Patch5:		libxml-1.8.17-CVE-2011-1944.diff
Patch6:		libxml-automake-1.13.patch
BuildRequires:	pkgconfig(zlib)

%description
This library allows you to manipulate XML files.

%package -n	%{libname}
Summary:	%{summary}
Group:		%{group}
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This library allows you to manipulate XML files.

%package -n	%{devname}
Summary:	Libraries, includes and other files to develop libxml applications
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This packages contains the libraries, include and other files 
you can use to develop libxml applications.

%prep
%setup -q
%patch0 -p1 -b .includes
%patch1 -p1 -b .libdir
%patch2 -p1
%patch3 -p0 -b .str
%patch4 -p0 -b .CVE-2009-2414,2416
%patch5 -p0 -b .CVE-2011-1944
%patch6 -p1 -b .am113~
autoreconf -fi

%build
%configure2_5x --disable-static
%make

%check
# all tests must pass
make check

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/libxml.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog NEWS README COPYING COPYING.LIB TODO
%{_bindir}/xml-config
%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gnome-xml

