%define realname flex
%define _requires_exceptions libc.so.0

%define basedir %{_prefix}/%{_target_cpu}-linux-uclibc
%define _mandir %{basedir}/usr/share/man
%define _bindir %{basedir}/usr/bin
%define _libdir %{basedir}/usr/lib
%define _libexecdir %{basedir}/usr/lib
%define _docdir %{basedir}/usr/share/doc
%define _includedir %{basedir}/include

Summary:	A tool for creating scanners (text pattern recognizers)
Name:		uClibc-%{realname}
Version:	2.5.4a
Release:	%mkrel 8
License:	GPL
Group:		Development/Other
URL: 		http://www.gnu.org/software/flex/flex.htm
Source:		ftp.gnu.org:/non-gnu/flex/flex-2.5.4a.tar.bz2
Patch0:		flex-2.5.4a-skel.patch
Patch1:         flex-2.5.4-glibc22.patch
Patch2:		flex-2.5.4-c++fixes.patch
Requires:	uClibc
BuildRequires:	byacc autoconf uClibc-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
The flex program generates scanners. Scanners are
programs which can recognize lexical patterns in text.

Flex takes pairs of regular expressions and C code as input and
generates a C source file as output. The output file is compiled and
linked with a library to produce an executable.

The executable searches through its input for occurrences of the
regular expressions. When a match is found, it executes the
corresponding C code.

Flex was designed to work with both Yacc and Bison, and is used by
many programs as part of their build process.

You should install flex if you are going to use your system for
application development.

%prep
%setup -q -n %{realname}-2.5.4
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .c++fixes
# Force regeneration of skel.c with Patch2 changes
rm -f skel.c
# Force regeneration of configure script with --libdir= support
autoconf

%build
uclibc %configure
uclibc %make

%install
rm -rf %{buildroot}
%makeinstall

cd %{buildroot}%{_bindir}
ln -sf flex lex

cd %{buildroot}%{_mandir}/
mkdir man1
mv flex.1 man1
cd man1
ln -s flex.1 lex.1
ln -s flex.1 flex++.1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,755)
%doc COPYING NEWS README
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/libfl.a
%{_includedir}/FlexLexer.h


