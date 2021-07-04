<h1 align="center">MUDA</h1>
<p align="center">
<a href="./LICENSE.md"><img src="https://img.shields.io/badge/License-GPL%20v2-blue.svg"></a>
<img src="https://img.shields.io/badge/Made%20With-Python3-green.svg"></a>

<h2>Configuring The Environment</h2>
<p>In your <code>.env</code> file add the following lines:</p>
<pre>VIRUS_TOTAL_KEY=your-api-key
IPSTACK_KEY=your-api-key</pre>

<h2>Module Information</h2>
<p>Below I have tried to briefly explain what each module does:</p>
<ul>
  <li>main.py - The <code>main</code> function to call other functions(Duh)</li>
  <li>modules.py - Miscellaneous functions to help with various stuff</li>
  <li>check_uri.py - Defines a <code>URI</code> Class which contains various information about the URI provided</li>
  <li>virustotal.py - Defines a class <code>VIRUS_TOTAL</code> to store the results of <a href='https://www.virustotal.com/gui/'>Virus Total</a> Analysis</li>
  <li>whoisinfo.py - Defines a class <code>WHOIS</code> to store whois directory lookup</li>
  <li>phishtank.py - Defines a class <code>PHISHTANK</code> to store the results of <a href='http://phishtank.org/'>PhishTank</a> Analysis</li>
  <li>sslcheck.py - Defines a class <code>SSL_INSPECTION</code> to contain information about the target website's SSL Certificate(when ever valid)</li>
  <li>geotag.py - Defines a class <code>GEO_IP</code> to store location information by leveraging <a href="https://ipstack.com/">IPStack API</a></li>
</ul>
  