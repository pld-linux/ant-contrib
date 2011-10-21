# TODO
# - some deps missing:
#build_contrib_jar:
#    [javac] Compiling 88 source files to ant-contrib/build/classes
#    [javac] ant-contrib/src/net/sf/antcontrib/antserver/server/ConnectionHandler.java:22: package org.apache.xml.serialize does not exist

%define		subver b2
%define		rel	0.1
Summary:	Collection of tasks for Ant
Name:		ant-contrib
Version:	1.0
Release:	0.%{subver}.%{rel}
License:	ASL 2.0
Group:		Development/Libraries
URL:		http://ant-contrib.sourceforge.net/
Source0:	http://downloads.sourceforge.net/ant-contrib/%{name}-%{version}%{subver}-src.tar.gz
# Source0-md5:	66511dddcef3dc9798db33dbaca0d3de
Patch0:		build_xml.patch
Patch2:		antservertest.patch
BuildRequires:	ant-junit >= 1.6.2
BuildRequires:	java(jaxp_parser_impl)
BuildRequires:	java-bcel >= 5.0
BuildRequires:	java-junit >= 3.8.0
BuildRequires:	jdk >= 1.4.2
BuildRequires:	jpackage-utils >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	ant >= 1.6.2
Requires:	java(jaxp_parser_impl)
Requires:	java-junit >= 3.8.0
BuildArch:	noarch

%description
The Ant-Contrib project is a collection of tasks (and at one point
maybe types and other tools) for Apache Ant.

%package javadoc
Summary:	Javadoc for Ant contrib tasks
Group:		Documentation

%description javadoc
API documentation for Ant contrib tasks.

%prep
%setup -q  -n %{name}
%patch0
%patch2

%undos manual/tasks/foreach.html manual/tasks/for.html

%{__rm} -r test/src/net/sf/antcontrib/antclipse

install -d test/lib

%build
junit_jar=$(find-jar junit)
ln -s $junit_jar test/lib/junit-$(JUNIT_VER).jar

export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
CLASSPATH=build/lib/ant-contrib-%{version}.jar:$CLASSPATH
echo $ANT_HOME
%ant -Dsource=1.4 -Dversion=%{version} -Dbcel.jar=file://%{_javadir}/bcel.jar all

%install
rm -rf $RPM_BUILD_ROOT

# jars
cp -p build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/ant/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf build/docs/api

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "ant/ant-contrib" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/ant-contrib

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc build/docs/LICENSE.txt
%doc build/docs/tasks/*
%{_sysconfdir}/ant.d/ant-contrib
%{_javadir}/ant/*.jar

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
