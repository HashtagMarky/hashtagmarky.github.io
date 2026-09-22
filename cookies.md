---
layout: default
title: Cookie Policy
description: "Cookie policy for HashtagMarky. Details on Google Analytics usage and how to manage your preferences."
---

<section id="one" markdown="1">
<header class="major">
<h1>Cookie Policy</h1>
</header>

This site uses **Google Analytics** to understand how visitors find and use the site, things like which pages are popular and how people arrive here. This helps improve the content over time.

### What Google Analytics collects

- Pages visited and time spent on them
- General location (country/region, not precise)
- Browser and device type
- How you arrived (search engine, direct, referral)

No personally identifiable information is collected. Data is processed by Google under their [privacy policy](https://policies.google.com/privacy).

### Your preference

<div id="cookie-status" style="margin: 1.5em 0 0.5em;"></div>

<div style="display: flex; gap: 1em; flex-wrap: wrap; margin-top: 1em;">
    <button class="button primary" id="cookies-accept">Accept Analytics</button>
    <button class="button" id="cookies-decline">Decline</button>
</div>

<script>
(function () {
    var status = document.getElementById('cookie-status');
    var consent = localStorage.getItem('ga_consent');

    function setStatus(text) {
        status.innerHTML = '<p>' + text + '</p>';
    }

    if (consent === 'granted') {
        setStatus('You have <strong>accepted</strong> analytics cookies.');
    } else if (consent === 'denied') {
        setStatus('You have <strong>declined</strong> analytics cookies.');
    } else {
        setStatus('You have not yet set a preference.');
    }

    document.getElementById('cookies-accept').addEventListener('click', function () {
        localStorage.setItem('ga_consent', 'granted');
        gtag('consent', 'update', { analytics_storage: 'granted' });
        setStatus('You have <strong>accepted</strong> analytics cookies.');
    });

    document.getElementById('cookies-decline').addEventListener('click', function () {
        localStorage.setItem('ga_consent', 'denied');
        gtag('consent', 'update', { analytics_storage: 'denied' });
        setStatus('You have <strong>declined</strong> analytics cookies.');
    });
})();
</script>

</section>
