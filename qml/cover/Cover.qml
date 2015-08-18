/*
  Copyright (C) 2013 Jolla Ltd.
  Contact: Thomas Perl <thomas.perl@jollamobile.com>
  All rights reserved.

  You may use this file under the terms of BSD license as follows:

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Jolla Ltd nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR
  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

import QtQuick 2.0
import Sailfish.Silica 1.0

CoverBackground {
    id: cover
    CoverPlaceholder {
        anchors.fill: parent
        icon.source: Qt.resolvedUrl('../images/butterfly-couple.png')
    }

    function force_update_account_data() {
        choozzeMainApp.updateMainData(true)
    }

    CoverActionList {
        id: coverAction
        iconBackground: false
        CoverAction {
            iconSource: Qt.resolvedUrl('../images/butterfly-sm.png')
            onTriggered: force_update_account_data()
        }
    }

    BusyIndicator {
        id: loader
        anchors.centerIn: parent
        running: choozzeMainApp.dataLoading
    }

    Column {
        id: column
        width: parent.width
        height: parent.height

        PageHeader {
            title: qsTr('Choozze.nu')
        }

        ProgressBar {
            id: callusageBar
            minimumValue: 0
            maximumValue: 100
            value: (choozzeMainApp.choozzeData.call_usage.used / choozzeMainApp.choozzeData.call_usage.total ) * 100;
            label: qsTr('Call: %L1 out of %L2').arg(choozzeMainApp.choozzeData.call_usage.used).arg(choozzeMainApp.choozzeData.call_usage.total)
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        ProgressBar {
            id: smsusageBar
            minimumValue: 0
            maximumValue: 100

            value: (choozzeMainApp.choozzeData.sms_usage.used / choozzeMainApp.choozzeData.sms_usage.total ) * 100;
            label: qsTr('SMS: %L1 out of %L2').arg(choozzeMainApp.choozzeData.sms_usage.used).arg(choozzeMainApp.choozzeData.sms_usage.total)

            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        ProgressBar {
            id: datausageBar
            minimumValue: 0
            maximumValue: 100

            value: (choozzeMainApp.choozzeData.data_usage.used / choozzeMainApp.choozzeData.data_usage.total ) * 100;
            label: qsTr('Inet: %1 out of %2').arg(choozzeMainApp.byteSize(choozzeMainApp.choozzeData.data_usage.used)).arg(choozzeMainApp.byteSize(choozzeMainApp.choozzeData.data_usage.total))

            anchors {
                left: parent.left
                right: parent.right
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }
    }
}
