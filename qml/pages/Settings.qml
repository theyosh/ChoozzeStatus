import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.4

Dialog {
    id: dialog

    BusyIndicator {
        id: loader
        anchors.centerIn: parent
        running: false
    }

    Column {
        width: parent.width

        DialogHeader {
            title: qsTr('Choozze.nu settings')
            acceptText: qsTr('Save')
        }

        TextField {
            id: usernameField
            width: parent.width
            label: qsTr('Username')
            placeholderText: qsTr('Enter Choozze.nu username')
            text: choozzeMainApp.choozzeData.username
            focus: true
            EnterKey.onClicked: passwordField.focus = true;
            anchors {
                left: parent.left
                right: parent.right
            }
        }

        TextField {
            id: passwordField
            width: parent.width
            inputMethodHints: Qt.ImhNoPredictiveText
            echoMode: TextInput.Password
            label: qsTr('Password')
            placeholderText: qsTr('Enter Choozze.nu password')
            text: choozzeMainApp.choozzeData.password
            EnterKey.onClicked: updateTimeout.focus = true
            anchors {
                left: parent.left
                right: parent.right
            }
        }

        TextField {
            id: updateTimeout
            width: parent.width
            inputMethodHints: Qt.ImhNoPredictiveText
            label: qsTr('Update timeout')
            placeholderText: qsTr('Enter the timeout in hours for updating')
            text: choozzeMainApp.choozzeData.data_update_timeout
            validator: IntValidator { bottom: 2; top: 24 }
            anchors {
                left: parent.left
                right: parent.right
            }
        }
    }

    onDone: {
        if (result === DialogResult.Accepted) {
            var update = (choozzeMainApp.choozzeData.username !== usernameField.text || choozzeMainApp.choozzeData.password !== passwordField.text)

            choozzeMainApp.choozzeData.username = usernameField.text
            choozzeMainApp.choozzeData.password = passwordField.text
            choozzeMainApp.choozzeData.data_update_timeout = updateTimeout.text

            python.setDataTimeout()

            if ( update === true) {
                if (choozzeMainApp.__debug){
                  console.log('New credentials entered... check them');
                }
                python.checkCredentials()
            }
        }
    }

    Python {
        id: python

        function checkCredentials() {
            loader.running = true
            call('ChoozzeScraper.choozzescraper.set_credentials', [usernameField.text,passwordField.text],function(result){
                if (choozzeMainApp.__debug){
                  console.log('login result: ' + result);
                }
                loader.running = false

                if (result) {
                    choozzeMainApp.notificationMessage(qsTr('Credentials are correct'))
                    choozzeMainApp.updateMainData()
                } else {
                    choozzeMainApp.notificationMessage(qsTr('Credentials are not correct'))
                }

                return result
            });
        }

        function setDataTimeout() {
            call('ChoozzeScraper.choozzescraper.set_data_update_timeout', [updateTimeout.text],function(result){

            });
        }
    }
}
