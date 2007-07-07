#!/bin/sh

PYVER=2.5

export SRCROOT=${SRCROOT:-$(pwd)}
export BUILD_ROOT=${BUILD_ROOT:-${SRCROOT}/build}
export TARGET_BUILD_DIR=${TARGET_BUILD_DIR:-${BUILD_ROOT}}
export TARGET_TEMP_DIR=${TARGET_TEMP_DIR:-${BUILD_ROOT}}

do_command() {
	local result
	echo "${@}"
	"${@}"
	result=${?}
	if [ "${result}" != "0" ]
	then
		exit "${result}"
	else
		return "${result}"
	fi
}

sdist() {
	echo "*** running sdist ***"
	do_command python${PYVER} setup.py sdist
	echo "*** done with sdist ***"
}

_do_install() {
	local src
	if ${ALIAS}
	then
		for src in "${@}"
		do
			do_command ln -fs "${src}" "${dst}"
		done
	else
		do_command cp -fpr "${@}" "${dst}"
	fi
}

build() {
	clean
	if ! ${ALIAS}
	then
		sdist
	fi
	echo "*** running build ***"
	if ${ALIAS}
	then
		do_command python${PYVER} setup.py py2app --alias
	else
		do_command python${PYVER} setup.py py2app
	fi
	
	SRC_FRAMEWORK_DIR="/Library/Frameworks/Python.framework/Versions/${PYVER}"
	SRC_INCLUDE_DIR="${SRC_FRAMEWORK_DIR}/include/python${PYVER}"
	SRC_LIB_DIR="${SRC_FRAMEWORK_DIR}/lib/python${PYVER}"
	SRC_LIB_DYNLOAD_DIR="${SRC_LIB_DIR}/lib-dynload"
	
	DST_RESOURCES_DIR="${TARGET_BUILD_DIR}/Forgery.app/Contents/Resources"
	DST_INCLUDE_DIR="${DST_RESOURCES_DIR}/include/python${PYVER}"
	DST_LIB_DIR="${DST_RESOURCES_DIR}/lib/python${PYVER}"
	DST_LIB_DYNLOAD_DIR="${DST_LIB_DIR}/lib-dynload"
	DST_FRAMEWORK_DIR="${TARGET_BUILD_DIR}/Forgery.app/Contents/Frameworks/Python.framework/Versions/${PYVER}"
	DST_FRAMEWORK_LIB_DIR="${DST_FRAMEWORK_DIR}/lib/python${PYVER}"
	
	do_command mkdir -p "${DST_INCLUDE_DIR}"
	do_command mkdir -p "${DST_LIB_DYNLOAD_DIR}"
	do_command mkdir -p "${DST_FRAMEWORK_LIB_DIR}"
	
	dst=${DST_RESOURCES_DIR} _do_install "${SRC_LIB_DIR}"/site-packages/{PyOpenGL-3.0.0a6-py${PYVER}.egg,PyOpenGL.pth,setuptools-0.6c5-py${PYVER}.egg,setuptools.pth}
	if ! ${ALIAS}
	then
		dst=${DST_RESOURCES_DIR} _do_install "${SRCROOT}"/dist/*
	fi
	dst=${DST_INCLUDE_DIR} _do_install "${SRC_INCLUDE_DIR}"/pyconfig.h
	dst=${DST_LIB_DIR} _do_install "${SRC_LIB_DIR}"/{ctypes,distutils,logging,new.pyc,sets.pyc}
	dst=${DST_LIB_DYNLOAD_DIR} _do_install "${SRC_LIB_DYNLOAD_DIR}"/{_ctypes.so,gestalt.so}
	dst=${DST_FRAMEWORK_LIB_DIR} _do_install "${SRC_LIB_DIR}"/config
	
	if ! ${ALIAS}
	then
		echo find "${DST_RESOURCES_DIR}" -name .DS_Store -delete
		find "${DST_RESOURCES_DIR}" -name .DS_Store -delete
	fi
}

bdist() {
	local old_pwd
	build
	echo "*** running bdist ***"
	old_pwd=$(pwd)
	do_command cd "${TARGET_BUILD_DIR}"
	do_command mkdir -p "${SRCROOT}/dist"
	do_command /usr/bin/zip -r "${SRCROOT}"/dist/Forgery-0.1.0.zip Forgery.app
	do_command cd "${old_pwd}"
}

clean() {
	echo "*** running clean ***"
	echo /bin/rm -rf "${BUILD_ROOT}"/* "${SRCROOT}"/dist "${SRCROOT}"/Forgery.egg-info "${SRCROOT}"/*.pyc
	/bin/rm -rf "${BUILD_ROOT}"/* "${SRCROOT}"/dist "${SRCROOT}"/Forgery.egg-info "${SRCROOT}"/*.pyc
	true
}

if [ "${BUILD_STYLE}" == "Development" ]
then
	ALIAS=true
else
	ALIAS=false
fi
#ALIAS=false
#for opt in "${@}"
#do
#	if [ "${opt}" == "--alias" ]
#	then
#		ALIAS=true
#	elif [ "${opt}" == "--no-alias" ]
#	then
#		ALIAS=false
#	fi
#done

TARGET=${1}
if [ -z "${TARGET}" ]
then
	if ${ALIAS}
	then
		TARGET=build
	else
		TARGET=bdist
	fi
else
	shift 1
fi

"${TARGET}"
