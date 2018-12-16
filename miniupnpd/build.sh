#!/bin/sh

yum -y install iptables-devel openssl-devel which iproute

cd miniupnp
MY_VERSION=`cat miniupnpd/VERSION`
MY_DATE=`git log -1 --date=raw miniupnpd | grep Date | awk '{print $2}'`
MY_DATE=`TZ="UTC" date --date="@${MY_DATE}" +%Y%m%d%H%M%S`
cd ${WORKSPACE}

mkdir -p ${WORKSPACE}/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
echo -e "%_topdir\t$WORKSPACE/rpmbuild" > ${HOME}/.rpmmacros

curl -O https://raw.githubusercontent.com/adamrushad/RPMSpecs/master/miniupnpd/miniupnpd.spec
sed -i -e "s/__VERSION__/${MY_VERSION}_${MY_DATE}/" miniupnpd.spec
mv miniupnpd.spec ${WORKSPACE}/rpmbuild/SPECS/

cd ${WORKSPACE}/rpmbuild/SOURCES/
curl -O https://raw.githubusercontent.com/adamrushad/RPMSpecs/master/miniupnpd/miniupnpd
curl -O https://raw.githubusercontent.com/adamrushad/RPMSpecs/master/miniupnpd/miniupnpd.service
cd ${WORKSPACE}

cp -r miniupnp/miniupnpd miniupnpd-${MY_VERSION}_${MY_DATE}
tar czf miniupnpd-${MY_VERSION}_${MY_DATE}.tar.gz miniupnpd-${MY_VERSION}_${MY_DATE}/
mv miniupnpd-${MY_VERSION}_${MY_DATE}.tar.gz ${WORKSPACE}/rpmbuild/SOURCES/
rm -rf miniupnpd-${MY_VERSION}_${MY_DATE}/

rpmbuild -ba ${WORKSPACE}/rpmbuild/SPECS/miniupnpd.spec
find ${WORKSPACE}/rpmbuild/
