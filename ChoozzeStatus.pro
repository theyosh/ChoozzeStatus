# NOTICE:
#
# Application name defined in TARGET has a corresponding QML filename.
# If name defined in TARGET is changed, the following needs to be done
# to match new name:
#   - corresponding QML filename must be changed
#   - desktop icon filename must be changed
#   - desktop filename must be changed
#   - icon definition filename in desktop file must be changed
#   - translation filenames have to be changed

# The name of your application
TARGET = ChoozzeStatus

CONFIG += sailfishapp

SOURCES += src/ChoozzeStatus.cpp

OTHER_FILES += qml/ChoozzeStatus.qml \
    rpm/ChoozzeStatus.changes.in \
    rpm/ChoozzeStatus.spec \
    rpm/ChoozzeStatus.yaml \
    translations/*.ts \
    ChoozzeStatus.desktop \
    qml/pages/Home.qml \
    qml/pages/About.qml \
    qml/cover/Cover.qml \
    qml/pages/Settings.qml \
    qml/python/ChoozzeScraper.py \
    qml/pages/Options.qml \
    qml/python/Encryption.py \
    qml/python/MockData.py \
    qml/images/butterfly-couple.png \
    qml/images/butterfly-sm.png

# to disable building translations every time, comment out the
# following CONFIG line
CONFIG += sailfishapp_i18n

# German translation is enabled as an example. If you aren't
# planning to localize your app, remember to comment out the
# following TRANSLATIONS line. And also do not forget to
# modify the localized app name in the the .desktop file.
TRANSLATIONS += translations/ChoozzeStatus-nl.ts

