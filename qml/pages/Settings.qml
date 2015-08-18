import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.4

Dialog {
    id: dialog
    canAccept: false

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
        }

        TextField {
            id: passwordField
            width: parent.width
            inputMethodHints: Qt.ImhNoPredictiveText
            echoMode: TextInput.Password
            label: qsTr('Password')
            placeholderText: qsTr('Enter Choozze.nu password')
            text: choozzeMainApp.choozzeData.password
            EnterKey.onClicked: testConnectionButton.focus = true
        }

        Button {
           id: testConnectionButton
           text: qsTr('Test credentials')
           onClicked: python.checkCredentials()
           anchors {
               left: parent.left
               right: parent.right
               leftMargin: Theme.paddingSmall
               rightMargin: Theme.paddingSmall
           }
        }
    }

    onDone: {
        if (result == DialogResult.Accepted) {
            choozzeMainApp.choozzeData.username = usernameField.text
            choozzeMainApp.choozzeData.password = passwordField.text
            choozzeMainApp.updateMainData()
            choozzeMainApp.notificationMessage(qsTr('Credentials are saved'))
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
                        dialog.canAccept = true
                    } else {
                        choozzeMainApp.notificationMessage(qsTr('Credentials are not correct'))
                    }
                    return result
                });
            }
        }
}
