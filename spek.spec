Name:           spek
Version:        0.7
Release:        3%{?dist}
Summary:        Free acoustic spectrum analyzer
Group:          Applications/Multimedia
License:        GPLv3
URL:            http://www.spek-project.org/
Source0:        http://spek.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel ffmpeg-devel vala-devel
BuildRequires:  intltool gettext
BuildRequires:  desktop-file-utils
Requires:       gtk2 >= 2.18
Requires:       ffmpeg

%description
Spek helps to analyze your audio files by showing their spectrogram.
Spectrograms are used to analyze the quality of audio files, you can easily
detect lossy re-encodes, web-rips and other badness by just looking at the
spectrogram. Spek uses ffmpeg to read audio files which means it supports
most file formats you can think of.

%prep
%setup -q

# Fix missing semicolons in the desktop file
# http://code.google.com/p/spek/issues/detail?id=49
sed -i "s|Categories=AudioVideo;Audio|Categories=AudioVideo;Audio;|" data/spek.desktop.in.in
sed -i "s|application/x-dts|application/x-dts;|" data/spek.desktop.in.in

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

# Remove Vala-generated C files
pushd src && for i in *.vala; do rm `basename $i .vala`.c; done && popd

make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" install

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS NEWS README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/*/*/apps/%{name}.*
%{_datadir}/man/man1/%{name}.1.*

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%changelog
* Tue May 10 2011 Thibault North <tnorth@fedoraproject.org> - 0.7-3
- Fix buildroot

* Tue May 10 2011 Thibault North <tnorth@fedoraproject.org> - 0.7-2
- Fix desktop file

* Sun Apr 24 2011 Thibault North <tnorth@fedoraproject.org> - 0.7-1
- New upstream release
- Drop gstreamer dependency for ffmpeg

* Tue Jun 01 2010 glang <glang@lavabit.com> - 0.4-2
- Added gstreamer-plugins-base and good runtime dependency

* Sun May 30 2010 Christophe Donatsch <cdonatsch@lavabit.com> - 0.4-1
- Initial packaging
