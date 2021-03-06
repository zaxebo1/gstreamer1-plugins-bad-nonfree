# which plugins to actually build and install
%global extdirs ext/faac

Summary:        GStreamer 1.0 streaming media framework "bad" non-free plug-ins
Name:           gstreamer1-plugins-bad-nonfree
Version:        1.10.0
Release:        1%{?dist}
License:        LGPLv2+
Group:          Applications/Multimedia
URL:            http://gstreamer.freedesktop.org/
Source0:        http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz
BuildRequires:  gstreamer1-devel >= 1.4.0
BuildRequires:  gstreamer1-plugins-base-devel >= 1.4.0
BuildRequires:  check
BuildRequires:  gettext-devel
BuildRequires:  libXt-devel
BuildRequires:  gtk-doc
BuildRequires:  orc-devel
BuildRequires:  libdca-devel
BuildRequires:  faac-devel

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins that depend on libraries which use a non-free
license.


%prep
%setup -q -n gst-plugins-bad-%{version}
# Build against 1.9.2 as 1.10.0 is not yet in the stable Fedora repo
sed -i 's/1.10.0/1.9.2/' configure


%build
# Note we don't bother with disabling everything which is in Fedora, that
# is unmaintainable, instead we selectively run make in subdirs
%configure \
    --with-package-name="gst-plugins-bad 1.0 nonfree rpmfusion rpm" \
    --with-package-origin="http://rpmfusion.org/" \
    --enable-debug --disable-static --enable-experimental
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
for i in %{extdirs}; do
    pushd $i
    make %{?_smp_mflags} V=2
    popd
done


%install
for i in %{extdirs}; do
    pushd $i
    make install V=2 DESTDIR=$RPM_BUILD_ROOT
    popd
done
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/*.la


%files
%doc AUTHORS NEWS README RELEASE
%license COPYING.LIB
# Plugins with external dependencies
%{_libdir}/gstreamer-1.0/libgstfaac.so


%changelog
* Fri Nov 11 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.10.0-1
- Update to 1.10.0

* Sat Jul  9 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.8.2-1
- Update to 1.8.2

* Sat Jul  9 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.4-1
- Update to 1.6.4

* Sat Aug 22 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.5-1
- Initial gstreamer1-plugins-bad-nonfree rpmfusion package
