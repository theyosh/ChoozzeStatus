#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from random import randint

def random(max):
  return int((randint(1, 200) / 100) * max)

def getpage(page):
  # Fake HTTP traffic duration for testing animation
  time.sleep(randint(1, 3))
  if 'account' == page or 'login' == page:
    return data_account
  if 'voicemail' == page:
    return data_voicemail
  if 'callforward' == page:
    return data_callforward

# Mock Data
data_account = """<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<meta name="description" content="">
<meta name="author" content="">
<link rel="icon" href="favicon.ico">
<link rel="apple-touch-icon" href="apple-touch-icon.png"/>
<link rel="apple-touch-icon-precomposed" href="apple-touch-icon.png"/>
<link rel="icon" href="apple-touch-icon.png" type="image/png"/>

<title>Choozze Me</title>

<!-- Bootstrap core CSS -->
<link href="css/bootstrap.min.css" rel="stylesheet">

<!-- Custom styles for this template -->
<link href="css/navbar-static-top.css" rel="stylesheet">

<!-- Custom styles for this template -->
<link href="css/signin.css" rel="stylesheet">
<link href="css/style.css" rel="stylesheet">

<!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
<script src="js/ie10-viewport-bug-workaround.js"></script>

<!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
<![endif]-->
</head>

<body>

<div>&nbsp;</div>

<div class="container">

  <!-- Main component for a primary marketing message or call to action -->
  <div class="jumbotron">
    <h1>Welkom Choozzer!</h1>
    <p>Jouw Choozze nummer: +31600000009        </p>
    <p>
<p>Jij hebt gekozen voor Choozze Zero</p><b>Happiness verbruiksmeter</b><br/><div class="row"><div class="col-xs-12 col-md-8">100 SMSjes voor nop (13% gebruikt)</div><div class="col-xs-6 col-md-4"></div></div><div class="row"><div class="col-xs-12 col-md-8">100 belminuten voor nop (5% gebruikt)</div><div class="col-xs-6 col-md-4"></div></div><div class="row"><div class="col-xs-12 col-md-8">100MB mobiel internet NL (3% gebruikt)</div><div class="col-xs-6 col-md-4"><a class="btn btn-aanpassen btn-xs" href="https://choozze.me/changedata.php?addon=500MB">Bundel wijzigen</a></div></div><div class="row"><div class="col-xs-12 col-md-8">Geen Onderling bundel</div><div class="col-xs-6 col-md-4"><a class="btn btn-aanpassen btn-xs" href="https://choozze.me/changevoice.php?addon=geen">Bundel wijzigen</a></div></div><br/><div class="row"><div class="col-xs-12 col-md-8"><b>Europa</b><br/><i>Met de Europa bundel kan je kiezen uit 100MB, 200M of 400MB</i></div><div class="col-xs-6 col-md-4"><a class="btn btn-reserveren btn-sm" href="https://choozze.me/changeroaming.php?addon=roam100">Reserveer hier je Europa bundel</a></div></div></p><p>Buitenbundelkosten: &euro;0,00</p>
Buitenbundelkosten kunnen onder andere bevatten: Overschrijdingen van de aanwezige bundels,
kosten voor bellen naar servicenummers, kosten voor bellen naar het buitenland of roaming kosten
(indien geen Europa bundel actief is, of er buiten de EU is gereisd).
<br/><br/>
Let op: Verbruiksgegevens worden met enige vertraging weergegeven en dienen ter indicatie.
  </div>

</div> <!-- /container -->


    <!-- Static navbar -->
  <div class="navbar navbar-default navbar-fixed-bottom" role="navigation">
    <div class="container">
      <div class="navbar-header">
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="https://choozze.me/"><img src="https://choozze.me/img/choozze-logobutton-sm.png" alt="Mijn Choozze"></a>
      </div>
      <div class="navbar-collapse collapse">
        <ul class="nav navbar-nav">
          <li><a href="https://choozze.me/voicemail.php">Voicemail</a></li>
          <li><a href="https://choozze.me/forward.php">Doorschakelen</a></li>
          <li><a href="https://choozze.me/apn.php">Internet</a></li>
          <li><a href="https://choozze.me/simcard.php">Simkaart</a></li>
          <li><a href="https://choozze.me/invoices.php">Facturen</a></li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
          <li><a href="https://choozze.me/contact.php">Contact</a></li>
          <li class="active"><form id="logout" name="logout" method="post" action="https://choozze.me/login.php"><input type="hidden" name="action" value="logout" /></form><a href="#" onClick="document.getElementById('logout').submit()">Logout</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div><!--/.container-fluid -->
  </div>
<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script type="text/javascript">
    $(document).ready(function(){
        if (typeof state !== 'undefined') {
            hideInvoices();

            $('#invoices-toggle').click(function (e) {
                e.preventDefault();
                toggleInvoiceView();
            });

        }
    });
</script>
</body>
</html>
"""

data_voicemail = """<!DOCTYPE html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="apple-touch-icon.png"/>
    <link rel="apple-touch-icon-precomposed" href="apple-touch-icon.png"/>
    <link rel="icon" href="apple-touch-icon.png" type="image/png"/>

    <title>Choozze Me</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/navbar-static-top.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/signin.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="js/ie10-viewport-bug-workaround.js"></script>

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div>&nbsp;</div>

    <div class="container">
      <!-- Main component for a primary marketing message or call to action -->
      <div class="jumbotron">
        <h1>Voicemail</h1>
        <p>Jouw Choozze nummer: +31600000005</p>
        <p>

        <p>Jouw voicemail is actief.</p>

<form class="form-inline" role="form" name="vmsettings" method="post" action="https://choozze.me/voicemail.php">
  <input type="hidden" name="action" value="vmsettings" />

  <div class="row"><div class="col-xs-6 col-md-4">
    Voicemail activeren
  </div><div class="col-xs-12 col-md-8">
    <label><input type="checkbox" name="vmactive" ></label>
  </div></div>

  <div class="row"><div class="col-xs-6 col-md-4">
    Voicemail PIN-code (4 cijfers)
    <label class="sr-only" for="InputPIN">PIN-code</label>
  </div><div class="col-xs-12 col-md-8">
    <input type="text" class="form-control" name="vmpin" id="vmpin" placeholder="Pincode" value="9999">
  </div></div>

  <div class="row"><div class="col-xs-6 col-md-4">
    Voicemails naar email versturen
    <label class="sr-only" for="InputEmail">Email address</label>
  </div><div class="col-xs-12 col-md-8">
    <input type="email" class="form-control" name="vmemail" id="vmemail" placeholder="Voicemail per email sturen aan" >
  </div></div>
  <button type="submit" class="btn btn-success">Instellen</button>
</form>

      </div>

    </div> <!-- /container -->


        <!-- Static navbar -->
      <div class="navbar navbar-default navbar-fixed-bottom" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="https://choozze.me/"><img src="https://choozze.me/img/choozze-logobutton-sm.png" alt="Mijn Choozze"></a>
          </div>
          <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
              <li><a href="https://choozze.me/voicemail.php">Voicemail</a></li>
              <li><a href="https://choozze.me/forward.php">Doorschakelen</a></li>
              <li><a href="https://choozze.me/apn.php">Internet</a></li>
              <li><a href="https://choozze.me/simcard.php">Simkaart</a></li>
              <li><a href="https://choozze.me/invoices.php">Facturen</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
              <li><a href="https://choozze.me/contact.php">Contact</a></li>
              <li class="active"><form id="logout" name="logout" method="post" action="https://choozze.me/login.php"><input type="hidden" name="action" value="logout" /></form><a href="#" onClick="document.getElementById('logout').submit()">Logout</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </div>
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            if (typeof state !== 'undefined') {
                hideInvoices();

                $('#invoices-toggle').click(function (e) {
                    e.preventDefault();
                    toggleInvoiceView();
                });

            }
        });
    </script>
  </body>
</html>"""

data_callforward = """<!DOCTYPE html>
<html lang="nl">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">
    <link rel="apple-touch-icon" href="apple-touch-icon.png"/>
    <link rel="apple-touch-icon-precomposed" href="apple-touch-icon.png"/>
    <link rel="icon" href="apple-touch-icon.png" type="image/png"/>

    <title>Choozze Me</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/navbar-static-top.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/signin.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="js/ie10-viewport-bug-workaround.js"></script>

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div>&nbsp;</div>

    <div class="container">
      <!-- Main component for a primary marketing message or call to action -->
      <div class="jumbotron">
        <h1>Doorschakelen</h1>
        <p>Jouw Choozze nummer: +31600000004</p>
        <p>

<p>Om doorschakelingen in te stellen, voer het bestemmingsnummer in en klik op 'Instellen'. Om ze te deactiveren, wis het nummer uit het gewenste veld en klik op 'Instellen'<br/></p>

<form class="form-inline" role="form" name="cfsettings" method="post" action="https://choozze.me/forward.php">
  <input type="hidden" name="action" value="cfsettings" />

  <div class="row"><div class="col-xs-6 col-md-4">
    Onmiddelijk doorschakelen (*21)
    <label class="sr-only" for="InputCFIM">Onmiddelijk doorschakelen</label>
  </div><div class="col-xs-12 col-md-8">
    <input type="text" class="form-control" name="cfim" id="cfim" placeholder="Doorschakelen naar" value="234353453">
  </div></div>

  <div class="row"><div class="col-xs-6 col-md-4">
    Doorschakelen bij bezet/geen antwoord (*61)
    <label class="sr-only" for="InputCFIM">Vertraagd doorschakelen</label>
  </div><div class="col-xs-12 col-md-8">
<input type='text' class='form-control' name='cfbs' id='cfbs' placeholder='Doorschakelen naar' value='85632432'>  </div></div>

  <button type="submit" class="btn btn-success">Instellen</button>

<p><br/>Let op: de kosten gemaakt bij het doorschakelen vallen buiten de bundel en zullen in rekening worden gebracht.</p>
</form>

      </div>

    </div> <!-- /container -->


        <!-- Static navbar -->
      <div class="navbar navbar-default navbar-fixed-bottom" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="https://choozze.me/"><img src="https://choozze.me/img/choozze-logobutton-sm.png" alt="Mijn Choozze"></a>
          </div>
          <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
              <li><a href="https://choozze.me/voicemail.php">Voicemail</a></li>
              <li><a href="https://choozze.me/forward.php">Doorschakelen</a></li>
              <li><a href="https://choozze.me/apn.php">Internet</a></li>
              <li><a href="https://choozze.me/simcard.php">Simkaart</a></li>
              <li><a href="https://choozze.me/invoices.php">Facturen</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
              <li><a href="https://choozze.me/contact.php">Contact</a></li>
              <li class="active"><form id="logout" name="logout" method="post" action="https://choozze.me/login.php"><input type="hidden" name="action" value="logout" /></form><a href="#" onClick="document.getElementById('logout').submit()">Logout</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </div>
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            if (typeof state !== 'undefined') {
                hideInvoices();

                $('#invoices-toggle').click(function (e) {
                    e.preventDefault();
                    toggleInvoiceView();
                });

            }
        });
    </script>
  </body>
</html>"""
