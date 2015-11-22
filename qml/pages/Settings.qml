import QtQuick 2.0
import Sailfish.Silica 1.0

Dialog {
    id: dialog
    canAccept: usernameField.text !== '' && passwordField.text !== ''

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
            EnterKey.onClicked: passwordField.focus = true
            validator: RegExpValidator { regExp: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/ }
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

        Label {
            text: "\n"
            width: parent.width
        }

        Button {
            id: resetSettingsButton
            text: qsTr('Reset settings')
            width: parent.width
            onClicked: resetSettings()
        }
    }

    function resetSettings() {
        usernameField.text = ''
        passwordField.text = ''
        updateTimeout.text = 4
        choozzeMainApp.resetSettings()
    }

    onDone: {
        if (result === DialogResult.Accepted) {
            choozzeMainApp.saveSettings(usernameField.text,passwordField.text,updateTimeout.text);
        }
    }
}
