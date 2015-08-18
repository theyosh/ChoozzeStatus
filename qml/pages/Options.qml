import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.4

Dialog {
    id: optionsPage
    height: optionsList.height + Theme.paddingLarge

    BusyIndicator {
        id: loader
        anchors.centerIn: parent
        running: false
    }

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
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        TextSwitch {
            id: voicemailActiveSwitch
            text: qsTr('Voicemail active')
            checked: choozzeMainApp.choozzeData.voicemail_active
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        TextField {
            id: voicemailPin
            width: parent.width
            visible: voicemailActiveSwitch.checked
            label: qsTr('Voicemail pincode')
            placeholderText: qsTr('Enter voicemail pincode')
            text: choozzeMainApp.choozzeData.voicemail_pin
            validator: RegExpValidator { regExp: /^[0-9]{4}$/ }
            color: errorHighlight? "red" : Theme.primaryColor
            EnterKey.onClicked: voicemailEmail.focus = true;
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        TextField {
            id: voicemailEmail
            width: parent.width
            visible: voicemailActiveSwitch.checked
            label: qsTr('Voicemail email address')
            placeholderText: qsTr('Enter voicemail email address')
            text: choozzeMainApp.choozzeData.voicemail_email
            /*validator: RegExpValidator { regExp: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/ } */
            color: errorHighlight? "red" : Theme.primaryColor
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        SectionHeader {
            id: headerCallForwarding
            text: qsTr('Call forwarding')
            wrapMode: Text.WordWrap
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        Label {
            id: callForwardingWarning
            text: qsTr('Extra costs will be added when call forwarding is enabled')
            wrapMode: Text.WordWrap
            color: "red"
            visible: callforwardingActive.checked
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        TextSwitch {
            id: callforwardingActive
            text: qsTr('Call forwarding active')
            checked: choozzeMainApp.choozzeData.callforward_active
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        TextField {
            id: callforwardingDirect
            width: parent.width
            visible: callforwardingActive.checked
            label: qsTr('Direct forwarding number')
            placeholderText: qsTr('Enter direct forwarding number')
            text: choozzeMainApp.choozzeData.callforward_direct
            focus: true
            /*validator: RegExpValidator { regExp: /^[0-9]{4}$/ }*/
            color: errorHighlight? "red" : Theme.primaryColor
            EnterKey.onClicked: voicemailEmail.focus = true;
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        TextField {
            id: callforwardingBusy
            width: parent.width
            visible: callforwardingActive.checked
            label: qsTr('Busy forwarding number')
            placeholderText: qsTr('Enter busy forwarding number')
            text: choozzeMainApp.choozzeData.callforward_busy
            /*validator: RegExpValidator { regExp: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/ } */
            color: errorHighlight? "red" : Theme.primaryColor
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

            choozzeMainApp.saveMobileOptions()
            choozzeMainApp.notificationMessage(qsTr('Mobile options are saved'))
        }

    }
}
