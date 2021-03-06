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
import io.thp.pyotherside 1.4
import 'pages'
import 'cover'

ApplicationWindow
{
    property variant choozzeData: QtObject {
        id: choozzeDataObject

        property string username
        property string password

        property int data_update_timeout: 4

        property string mobilenumber
        property string mobileplan
        property string mobileextracosts

        property variant last_update: new Date()

        property variant call_usage: QtObject {
            property int total: 0
            property int used: 0
            property int free: 0
            property int percentage: 0
        }

        property variant sms_usage: QtObject {
            property int total: 0
            property int used: 0
            property int free: 0
            property int percentage: 0
        }

        property variant data_usage: QtObject {
            property int total: 0
            property int used: 0
            property int free: 0
            property int percentage: 0
        }

        property variant days_usage: QtObject {
            property int total: 0
            property int used: 0
            property int free: 0
            property int percentage: 0
        }

        property bool voicemail_active
        property string voicemail_pin
        property string voicemail_email

        property bool callforward_active
        property string callforward_direct
        property string callforward_busy

        property string history: 'Loading...'
    }

    property bool dataLoading: false
    property bool __debug: false
    property string version: '0.6.2'

    id: choozzeMainApp
    initialPage: Component { Home {} }
    cover: Component { Cover {} }

    function debug(message) {
        if (choozzeMainApp.__debug){
          console.log('debug: ' + message);
        }
    }

    // Function for showing a nice notification on top of the screen. Animation is about 6 seconds
    function notificationMessage(message) {
        if (choozzeMainApp.__debug){
          console.log('notificationMessage: ' + message);
        }
        notificationText.text = message
        notificationAnimation.running = true
    }

    // Start loading animation
    function startLoader() {
        choozzeMainApp.dataLoading = true
    }

    // Stop loading animation
    function stopLoader() {
        choozzeMainApp.dataLoading = false
    }

    // Function for updating the data from other pages

    function updateMainData(force_update) {
        force_update = force_update ? force_update : false;
        python.updateData(force_update)
    }

    function saveMobileOptions() {
        python.saveOptions()
    }

    // Check if the needed credentials are availabe. If not, go to the settings screen
    function force_settings_page() {
        if (choozzeMainApp.pageStack.busy) {
            choozzeMainApp.pageStack.completeAnimation();
        }
        choozzeMainApp.pageStack.push(Qt.resolvedUrl('pages/Settings.qml'));
    }

    function saveSettings(username,password,data_update_timeout) {
        return python.saveSettings(username,password,data_update_timeout);
    }

    function resetSettings() {
        return python.resetSettings();
    }

    // Function for human readable bite sizes
    function byteSize(bytes) {
        var untis = ['b','Kb','Mb','Gb']
        var indicator = ''
        var counter = 0
        if (bytes < 0) {
            indicator = '-'
            bytes *= -1
        }
        while (bytes / 1000 > 1) {
            counter++
            bytes = bytes / 1000
        }
        return indicator + bytes + '' + untis[counter]
    }

    Item {
        id: notificationPlaceHolder
        width: Screen.width
        height: 45
        opacity: 0
        anchors {
            top: Screen.top
            left: Screen.left
        }

        Rectangle {
            width: parent.width
            height: parent.height
            color: Theme.highlightColor
            opacity: 0.4
            anchors {
                top: parent.top
                left: parent.left
            }
        }
        Label {
            id: notificationText
            text: ''
            wrapMode: Text.WordWrap
            font.pixelSize: Theme.fontSizeSmall
            horizontalAlignment: Text.AlignHCenter
            width: parent.width
            height: parent.height
            anchors {
                top: parent.top
                left: parent.left
                leftMargin: Theme.paddingSmall
                rightMargin: Theme.paddingSmall
            }
        }

        // this is a standalone animation, it's not running by default
        SequentialAnimation {
            id: notificationAnimation
            running: false
            PropertyAnimation { id: animationIn;   target: notificationPlaceHolder; property: 'opacity'; to: 1; duration: 2000 }
            PropertyAnimation { id: animationStay; target: notificationPlaceHolder; property: 'opacity'; to: 1; duration: 2000 }
            PropertyAnimation { id: animationOut;  target: notificationPlaceHolder; property: 'opacity'; to: 0; duration: 2000 }
        }
    }

    Python {
        id: python

        Component.onCompleted: {

            setHandler('update-data', function(message) {
                debug('Got a data update from Python module: ' + message)
                updateData()
            });

            setHandler('notification', function(message) {
                debug('Got a notification from Python module: ' + message)
                notificationMessage(message)
            });

            addImportPath(Qt.resolvedUrl('python'));

            /* Module should auto start scraper daemon, and that should sent a signal*/
            debug('Start deamon!');

            importModule('ChoozzeScraper', function() {
                startLoader();
                debug('Get credentials!');

                // Here we use synchronized calls, so that we are sure to get all the data at the right time
                var username = call_sync('ChoozzeScraper.choozzescraper.get_username',[]);
                if (username !== undefined && username !== '') {
                    debug('Got username: ' + username);
                    choozzeDataObject.username = username;
                }

                var password = call_sync('ChoozzeScraper.choozzescraper.get_password',[]);
                if (password !== undefined && password !== '') {
                    debug('Got password: ' + password);
                    choozzeDataObject.password = password;
                }

                if (choozzeDataObject.username !== '' && choozzeDataObject.password != '') {
                    debug('Check if logged in already?');
                    if (python.isLoggedIn()) {
                        debug('Yup, and now update data');
                        updateData(true);
                    } else {
                        // Invalid credentials
                        notificationMessage(qsTr('The loaded credentials are invalid'))
                        force_settings_page();
                    }
                } else {
                    debug('Force settings window');
                    notificationMessage(qsTr('No credentials available'))
                    force_settings_page()
                }
            });

        }

        // Function to check if we are loggedin at the Mobile provider
        function isLoggedIn() {
            return call_sync('ChoozzeScraper.choozzescraper.isLoggedIn', []);
        }

        function checkCredentials(username,password) {
            return call_sync('ChoozzeScraper.choozzescraper.set_credentials', [username,password]);
        }

        // Get the latest data from your Mobile operator
        function updateData(force_update) {
            startLoader();
            force_update = force_update ? force_update : false;

            call('ChoozzeScraper.choozzescraper.get_all_data', [force_update],function(result){
                debug('Got account data: (' +  choozzeMainApp.dataLoading + ')');

                choozzeDataObject.mobilenumber = result['mobile_number'];
                choozzeDataObject.mobileplan = result['mobile_plan'];
                choozzeDataObject.mobileextracosts = result['extra_costs'];

                choozzeDataObject.call_usage.total = result['call_usage']['total'];
                choozzeDataObject.call_usage.used = result['call_usage']['used'];
                choozzeDataObject.call_usage.free = result['call_usage']['free'];
                choozzeDataObject.call_usage.percentage = (choozzeDataObject.call_usage.used / choozzeDataObject.call_usage.total ) * 100;

                choozzeDataObject.sms_usage.total = result['sms_usage']['total']
                choozzeDataObject.sms_usage.used = result['sms_usage']['used']
                choozzeDataObject.sms_usage.free = result['sms_usage']['free']
                choozzeDataObject.sms_usage.percentage = (choozzeDataObject.sms_usage.used / choozzeDataObject.sms_usage.total ) * 100;

                choozzeDataObject.data_usage.total = result['data_usage']['total']
                choozzeDataObject.data_usage.used = result['data_usage']['used']
                choozzeDataObject.data_usage.free = result['data_usage']['free']
                choozzeDataObject.data_usage.percentage = (choozzeDataObject.data_usage.used / choozzeDataObject.data_usage.total ) * 100;

                choozzeDataObject.days_usage.total = result['days_usage']['total']
                choozzeDataObject.days_usage.used = result['days_usage']['used']
                choozzeDataObject.days_usage.free = result['days_usage']['free']
                choozzeDataObject.days_usage.percentage = (choozzeDataObject.days_usage.used / choozzeDataObject.days_usage.total ) * 100;

                choozzeDataObject.voicemail_active = result['voicemail_active']
                choozzeDataObject.voicemail_pin    = result['voicemail_pin']
                choozzeDataObject.voicemail_email  = result['voicemail_email']

                choozzeDataObject.callforward_active = result['callforward_active']
                choozzeDataObject.callforward_direct = result['callforward_direct']
                choozzeDataObject.callforward_busy   = result['callforward_busy']

                choozzeDataObject.data_update_timeout = result['data_update_timeout'] / 3600

                choozzeDataObject.last_update = new Date(result['last_update'] * 1000)

                getHistory()

                notificationMessage(qsTr('Update account data'))

                stopLoader();
            });
        }

        function saveOptions() {
            call('ChoozzeScraper.choozzescraper.set_voicemail_settings', [choozzeDataObject.voicemail_active,choozzeDataObject.voicemail_pin,choozzeDataObject.voicemail_email],function(result){
                debug('Saved voicemail settings: ' + result);
                notificationMessage(qsTr('Updated voicemail settings'))
            });

            call('ChoozzeScraper.choozzescraper.set_callforward_settings', [choozzeDataObject.callforward_direct,choozzeDataObject.callforward_busy],function(result){
                debug('Saved callforward settings: ' + result);
                notificationMessage(qsTr('Updated call forwarding settings'))
            });
        }

        function saveSettings(username,password,data_update_timeout) {
            debug('Start saving settings');
            startLoader();

            var login = true;
            if (username !== choozzeDataObject.username || password !== choozzeDataObject.password) {
                debug('Check new credentials...');
                if (checkCredentials(username,password)) {
                    choozzeDataObject.username = username;
                    choozzeDataObject.password = password;
                    stopLoader();
                    notificationMessage(qsTr('The new credentials are saved'))
                    updateData(true);
                } else {
                    login = false;
                    stopLoader();
                    notificationMessage(qsTr('The new credentials are not valid'))
                }
            }

            if (data_update_timeout !== choozzeDataObject.data_update_timeout) {
                call('ChoozzeScraper.choozzescraper.set_data_update_timeout', [data_update_timeout],function(result){
                    stopLoader();
                    if (result) {
                        choozzeDataObject.data_update_timeout = data_update_timeout
                        notificationMessage(qsTr('Timeout set to %L1 hours').arg(choozzeDataObject.data_update_timeout))
                    } else {
                        notificationMessage(qsTr('Error updating timeout'))
                    }

                });
            }
            return login;
        }

        function getHistory() {
            call('ChoozzeScraper.choozzescraper.get_history', [],function(result){
                var history = qsTr('Date      ///    Call left, SMS left, Data left') + '\n' + '================================' + '\n'
                for (var key in result) {
                    history = history + Qt.formatDate(new Date(result[key].last_update * 1000),'dd MMM yyyy')  + '       ///        ' + result[key].call_usage.free + ', ' + result[key].sms_usage.free + ', ' + byteSize(result[key].data_usage.free) + '\n'
                }
                choozzeDataObject.history = history
            });
        }

        function resetSettings() {
            call('ChoozzeScraper.choozzescraper.reset_settings', [],function(result){
                debug('Reset settings: ' + result);
                if (result === true) {
                    choozzeDataObject.username = ''
                    choozzeDataObject.password = ''

                    choozzeDataObject.mobilenumber = ''
                    choozzeDataObject.mobileplan = ''
                    choozzeDataObject.mobileextracosts = ''

                    choozzeDataObject.call_usage.total = 0
                    choozzeDataObject.call_usage.used = 0
                    choozzeDataObject.call_usage.free = 0
                    choozzeDataObject.call_usage.percentage = 0

                    choozzeDataObject.sms_usage.total = 0
                    choozzeDataObject.sms_usage.used = 0
                    choozzeDataObject.sms_usage.free = 0
                    choozzeDataObject.sms_usage.percentage = 0

                    choozzeDataObject.data_usage.total = 0
                    choozzeDataObject.data_usage.used = 0
                    choozzeDataObject.data_usage.free = 0
                    choozzeDataObject.data_usage.percentage = 0

                    choozzeDataObject.days_usage.total = 0
                    choozzeDataObject.days_usage.used = 0
                    choozzeDataObject.days_usage.free = 0
                    choozzeDataObject.days_usage.percentage = 0

                    choozzeDataObject.voicemail_active = ''
                    choozzeDataObject.voicemail_pin    = ''
                    choozzeDataObject.voicemail_email  = ''

                    choozzeDataObject.callforward_active = ''
                    choozzeDataObject.callforward_direct = ''
                    choozzeDataObject.callforward_busy   = ''

                    choozzeDataObject.data_update_timeout = 4

                    choozzeDataObject.history = 'loading...'

                    choozzeDataObject.last_update = new Date()
                 }
            });
        }
    }
}
