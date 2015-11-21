import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.4

Dialog {
    id: optionsPage
    height: optionsList.height + Theme.paddingLarge
/*
    BusyIndicator {
        id: loader
        anchors.centerIn: parent
        running: false
    }
*/
    SilicaFlickable {
        width: parent.width
        height: parent.height
        /* https://lists.sailfishos.org/pipermail/devel/2014-May/004136.html */
        contentHeight: optionsList.y + optionsList.height

        // Why is this necessary?
        contentWidth: parent.width

        VerticalScrollDecorator {}

        Column {
            id: optionsList
            width: parent.width

            DialogHeader {
                title: qsTr('Mobile options')
                acceptText: qsTr('Save')
            }

            SectionHeader {
                id: headerVoicemail
                text: qsTr('Voicemail')
                wrapMode: Text.WordWrap
                anchors {
                    left: parent.left
                    right: parent.right
                    leftMargin: Theme.paddingLarge
                    rightMargin: Theme.paddingLarge
                }
            }

            TextSwitch {
                id: voicemailActiveSwitch
                text: qsTr('Voicemail active')
                checked: choozzeMainApp.choozzeData.voicemail_active
                focus: true
                anchors {
                    left: parent.left
                    right: parent.right
                }
            }

            TextField {
                id: voicemailPin
                width: parent.width
                visible: voicemailActiveSwitch.checked
                label: qsTr('Voicemail pincode')
                placeholderText: label
                text: choozzeMainApp.choozzeData.voicemail_pin
                validator: RegExpValidator { regExp: /^[0-9]{4}$/ }
                color: errorHighlight? "red" : Theme.primaryColor
                EnterKey.onClicked: voicemailEmail.focus = true;
                anchors {
                    left: parent.left
                    right: parent.right
                }
            }

            TextField {
                id: voicemailEmail
                width: parent.width
                visible: voicemailActiveSwitch.checked
                label: qsTr('Voicemail email address')
                placeholderText: label
                text: choozzeMainApp.choozzeData.voicemail_email
                /*validator: RegExpValidator { regExp: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/ } */
                color: errorHighlight? "red" : Theme.primaryColor
                anchors {
                    left: parent.left
                    right: parent.right
                }
            }

            SectionHeader {
                id: headerCallForwarding
                text: qsTr('Call forwarding')
                wrapMode: Text.WordWrap
                anchors {
                    left: parent.left
                    right: parent.right
                    leftMargin: Theme.paddingLarge
                    rightMargin: Theme.paddingLarge
                }
            }

            Label {
                id: callForwardingWarning
                text: qsTr('Extra costs will be added when call forwarding is enabled')
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                color: "red"
                visible: callforwardingActive.checked
                anchors {
                    left: parent.left
                    right: parent.right
                    leftMargin: Theme.paddingLarge
                    rightMargin: Theme.paddingLarge
                }
            }

            TextSwitch {
                id: callforwardingActive
                text: qsTr('Call forwarding active')
                checked: choozzeMainApp.choozzeData.callforward_active
                anchors {
                    left: parent.left
                    right: parent.right
                }
            }

            TextField {
                id: callforwardingDirect
                width: parent.width
                visible: callforwardingActive.checked
                label: qsTr('Direct forwarding number')
                placeholderText: label
                text: choozzeMainApp.choozzeData.callforward_direct
                /*validator: RegExpValidator { regExp: /^[0-9]{4}$/ }*/
                color: errorHighlight? "red" : Theme.primaryColor
                EnterKey.onClicked: callforwardingBusy.focus = true;
                anchors {
                    left: parent.left
                    right: parent.right
                }
            }

            TextField {
                id: callforwardingBusy
                width: parent.width
                visible: callforwardingActive.checked
                labelVisible: true
                label: qsTr('Busy forwarding number')
                placeholderText: label
                text: !voicemailActiveSwitch.checked ? choozzeMainApp.choozzeData.callforward_busy : qsTr('Not possible when voicemail enabled')
                readOnly: voicemailActiveSwitch.checked
                /*validator: RegExpValidator { regExp: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/ } */
                color: errorHighlight? "red" : Theme.primaryColor
                anchors {
                    left: parent.left
                    right: parent.right
                }
            }
        }
    }

    onDone: {
        if (result === DialogResult.Accepted) {
            choozzeMainApp.choozzeData.voicemail_active = voicemailActiveSwitch.checked
            choozzeMainApp.choozzeData.voicemail_pin = voicemailPin.text
            choozzeMainApp.choozzeData.voicemail_email = voicemailEmail.text

            choozzeMainApp.choozzeData.callforward_active = callforwardingActive.checked
            if (choozzeMainApp.choozzeData.callforward_active) {
                choozzeMainApp.choozzeData.callforward_direct = callforwardingDirect.text
                choozzeMainApp.choozzeData.callforward_busy = callforwardingBusy.text
            } else {
                choozzeMainApp.choozzeData.callforward_direct = ''
                choozzeMainApp.choozzeData.callforward_busy = ''
            }

            if (choozzeMainApp.choozzeData.voicemail_active) {
                choozzeMainApp.choozzeData.callforward_busy = ''
            }

            choozzeMainApp.saveMobileOptions()
            choozzeMainApp.notificationMessage(qsTr('Mobile options are saved'))
        }
    }
}
