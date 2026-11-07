import re, pathlib

ROOT = pathlib.Path('/Users/superbien/Claude Projects/projects/saywho/html')
BUILD = pathlib.Path(__file__).resolve().parent
src = (ROOT / 'src' / 'v20.stripped.html').read_text(encoding='utf-8')
css_own = (BUILD / 'style.css').read_text(encoding='utf-8')
extra_js = (BUILD / 'extra.js').read_text(encoding='utf-8')


def once(text, old, new):
    n = text.count(old)
    assert n == 1, (n, old[:80])
    return text.replace(old, new)


def ico(name, cls=''):
    return f'<svg class="i{(" " + cls) if cls else ""}" aria-hidden="true"><use href="#i-{name}"/></svg>'


# ---------- blocks extracted verbatim from v20 ----------
title = re.search(r'<title>.*?</title>', src, re.S).group(0)
header = src[src.index('<header class="sw-header">'):src.index('</header>') + len('</header>')]
header = once(header, 'src="DATAURI"', 'src="assets/v20-asset-1.svg"')
header = once(header, '>⌕</a>', '>' + ico('search') + '</a>')

footer = src[src.index('<footer class="sw-site-footer">'):src.index('</footer>') + len('</footer>')]
footer = once(footer, 'src="DATAURI"', 'src="assets/v20-asset-2.svg"')

select = src[src.index('<select id="eventCountry"'):src.index('</select>') + len('</select>')]
assert 'KEY MARKETS' in select

lines = src.split('\n')
footer_css = '\n'.join(lines[77:80])
assert footer_css.startswith('.sw-site-footer{') and '.sw-copyright{' in footer_css
footer_css = footer_css.replace('accent-color:#f16c65', 'accent-color:#fff')

script = src[src.index('<script>\n') + len('<script>\n'):src.index('</script>')]

# ---------- script patches ----------
script = once(script, 'link.href=url;', 'if(link)link.href=url;')
script = once(script, "btn.disabled=true;btn.textContent='SENDING…';", "btn.disabled=true;setBtnLabel(btn,swT('Sending…'));")
script = once(script, "btn.disabled=false;btn.textContent='SEND MY REQUEST →';", "btn.disabled=false;setBtnLabel(btn,swT('Send my request'));")
script = once(script, "['','YOUR REQUEST','YOUR PRODUCTION','MAXIMISE YOUR IMPACT','LET’S CONNECT'][n]+' — STEP '+n+' OF 4'",
              "['','Your request','Your production','Maximise your impact','Let’s connect'][n]+' — step '+n+' of 4'")
script = once(script, "'<strong>YOUR SELECTION</strong><br>'", "'<strong>Your selection</strong><br>'")
script = once(script, "labels={en:['','YOUR REQUEST','YOUR PRODUCTION','MAXIMISE YOUR IMPACT','LET’S CONNECT'],fr:['','VOTRE DEMANDE','VOTRE PRODUCTION','MAXIMISEZ VOTRE IMPACT','ÉCHANGEONS'],it:['','LA TUA RICHIESTA','LA TUA PRODUZIONE','MASSIMIZZA L’IMPATTO','PARLIAMONE']}",
              "labels={en:['','Your request','Your production','Maximise your impact','Let’s connect'],fr:['','Votre demande','Votre production','Maximisez votre impact','Échangeons'],it:['','La tua richiesta','La tua produzione','Massimizza l’impatto','Parliamone']}")
script = once(script, "(swLanguage==='fr'?'ÉTAPE':swLanguage==='it'?'FASE':'STEP')", "(swLanguage==='fr'?'étape':swLanguage==='it'?'fase':'step')")
script = once(script, "(swLanguage==='fr'?'SUR':swLanguage==='it'?'DI':'OF')", "(swLanguage==='fr'?'sur':swLanguage==='it'?'di':'of')")
script = once(script, "swT('YOUR SELECTION')", "swT('Your selection')")
script = once(script, ".sw-copyright'))continue;", ".sw-copyright,.sw-detail-overlay'))continue;")

# ---------- markup ----------
def choice(cid, name, value, ttl, meta, checked=False):
    return (f'<div class="choice-row"><input type="checkbox" id="{cid}" name="{name}" value="{value}"{" checked" if checked else ""}>'
            f'<label class="choice-main" for="{cid}"><span class="cb">{ico("check")}</span>'
            f'<span class="choice-text"><strong>{ttl}</strong><small>{meta}</small></span></label>'
            f'<button type="button" class="info-btn" data-detail="{value}" aria-label="More about {ttl}">{ico("info")}</button></div>')


def check_line(name, value, label, extra_attrs=''):
    return (f'<label class="check-line"><input type="checkbox" name="{name}" value="{value}"{extra_attrs}>'
            f'<span class="cb">{ico("check")}</span><span>{label}</span></label>')


def btn(label, onclick, kind='', icon='', extra=''):
    k = ' secondary' if kind == 'secondary' else ''
    return f'<button type="button" class="btn{k}" onclick="{onclick}"{extra}><span class="btn-label">{label}</span>{ico(icon) if icon else ""}</button>'


step1 = ('<div id="step1"><h2>What can we do for you?</h2>'
         '<p class="lead">Select one or more services. We’ll tailor our team to your project.</p><div class="choice-list">'
         + choice('req1', 'request', 'Photo coverage', 'Photo coverage', 'Event photography and portraits', True)
         + choice('req2', 'request', 'Video coverage', 'Video coverage', 'Films, highlights and reels')
         + choice('req3', 'request', 'Article on SAY WHO / Interview', 'Article on SAY WHO', 'Editorial article (Diary, What or interview)')
         + choice('req4', 'request', 'Creative Campaign', 'Creative Campaign', 'Concept, art direction &amp; production by SAY WHO STUDIO')
         + choice('req5', 'request', 'Social takeover', 'Social takeover', 'Instagram / TikTok')
         + choice('req6', 'request', 'Corporate coverage', 'Corporate coverage', 'Private delivery, no publication requested')
         + '</div><div class="actions">' + btn('Continue', 'go(2)', icon='arrow-right') + '</div></div>')

step2 = ('<div id="step2" class="hidden"><h2>Let\'s plan your production.</h2><div class="fields">'
         '<label class="field full">Project / event name<input id="projectName" placeholder="e.g. Brand launch in New York"></label>'
         '<label class="field full">Country' + select + '</label>'
         '<label class="field">Event date<span class="date-wrap"><input id="eventDate" type="date">' + ico('calendar', 'date-ico') + '</span></label>'
         '<label class="field">City<input id="eventCity" placeholder="Paris, London, New York, Milan..." list="saywho-cities" autocomplete="address-level2"><datalist id="saywho-cities"></datalist></label>'
         '<p class="hint" id="countryHint">The event country determines your SAY WHO contact. Creative Campaign requests go to SAY WHO STUDIO.</p>'
         '<label class="field full">Tell us about your project<textarea id="projectDescription" rows="1" placeholder="A few words about your event, goals and requirements"></textarea></label></div>'
         '<h3 class="section-title">Do you need extra production support?</h3>'
         '<p class="lead">Optional — choose anything that would help your event run smoothly.</p><div class="choice-list">'
         + choice('prod1', 'production', 'Videographer', 'A videographer', 'Alongside your photo team')
         + choice('prod2', 'production', 'Multiple crew members', 'Additional crew', '2+ photographers / videographers')
         + choice('prod3', 'production', 'On-site editor', 'On-site editor', 'Editing during your event')
         + choice('prod4', 'production', 'Image live delivery', 'Image live delivery', 'Selected images delivered during the event')
         + '</div><h3 class="section-title">Any special requirements?</h3>'
         '<textarea id="specialRequirements" class="control" rows="3" placeholder="Timing, turnaround, deliverables, specific requests..."></textarea>'
         '<div class="actions">' + btn('Back', 'go(1)', 'secondary') + btn('Continue', 'go(3)', icon='arrow-right') + '</div></div>')

partners = ['Madame Figaro', 'Numéro', 'Vanity Fair', 'Vogue', 'AD', 'GQ', 'Gala', 'Beauxarts.com', 'Fashion Network', 'Point de Vue']
partner_grid = ''.join(check_line('mediaPartner', p, p) for p in partners)


def card_head(tag, key, label):
    return (f'<div class="upsell-head"><span class="tag">{tag}</span>'
            f'<button type="button" class="info-btn" data-detail="{key}" aria-label="More about {label}">{ico("info")}</button></div>')


step3 = ('<div id="step3" class="hidden"><h2>Maximise the impact of your event.</h2>'
         '<p class="lead">Go beyond event coverage. Extend your story through SAY WHO channels and our media partner network.</p><div class="cards">'
         '<div class="upsell">' + card_head('Extend your reach', 'card:amplification', 'Amplification') +
         '<h3>Amplification</h3><p>Bring your event to a wider, relevant audience through SAY WHO.</p><div class="check-list">'
         + check_line('impact', 'Social media amplification', 'Social media amplification')
         + check_line('impact', 'Weekly digest', 'Weekly digest inclusion')
         + check_line('impact', 'Press push', 'Press push')
         + check_line('impact', 'Dark posts with reach', 'Dark posts with paid reach')
         + '</div></div>'
         '<div class="upsell">' + card_head('Go even further', 'card:media', 'Media partners') +
         '<h3>Media partners</h3><p>Explore a bespoke amplification proposal with relevant media partners.</p><div class="check-list">'
         '<label class="check-line"><input type="checkbox" id="mediaPartnerToggle" name="impact" value="Media partner amplification" onchange="toggleMediaPartners()">'
         f'<span class="cb">{ico("check")}</span><span>I\'m interested in media partner amplification</span></label></div>'
         '<div id="mediaPartnerChoices" class="media-partner-choices hidden"><div class="tiny">SELECT YOUR MEDIA PARTNERS — MULTIPLE CHOICES POSSIBLE</div>'
         '<div class="media-partner-grid">' + partner_grid + '</div></div>'
         '<p class="softnote">Media partner placements are subject to availability, editorial approval and separate agreement.</p></div></div>'
         '<div class="actions">' + btn('Back', 'go(2)', 'secondary') + btn('Continue', 'go(4)', icon='arrow-right')
         + '<button type="button" class="skip" onclick="go(4)">Skip this step</button></div></div>')

scheduler = (
    '<div class="sw-scheduler" aria-label="SAY WHO appointment calendar">'
    '<div class="sw-scheduler-head"><div><span class="tiny">DISCOVERY CALL</span><h4>SELECT YOUR DATE &amp; TIME</h4></div>'
    '<span class="sw-duration">' + ico('clock') + '15 MIN</span></div>'
    '<div class="sw-scheduler-meta"><span>' + ico('clock') + '15-minute Google Meet</span><span>' + ico('map-pin') + 'Europe/Paris (CET / CEST)</span></div>'
    '<div class="sw-scheduler-body"><div class="sw-calendar-column"><div class="sw-month-head">'
    '<button type="button" class="sw-icon-button" onclick="changeMockMonth(-1)" aria-label="Previous month">' + ico('chevron-left') + '</button>'
    '<strong id="swMonthTitle"></strong>'
    '<button type="button" class="sw-icon-button" onclick="changeMockMonth(1)" aria-label="Next month">' + ico('chevron-right') + '</button></div>'
    '<div class="sw-weekdays"><span>MON</span><span>TUE</span><span>WED</span><span>THU</span><span>FRI</span><span>SAT</span><span>SUN</span></div>'
    '<div id="swCalendarDays" class="sw-calendar-days"></div>'
    '<p class="sw-small-note">Dates and time slots are illustrative in this design preview.</p></div>'
    '<div class="sw-times-column"><div class="sw-time-heading"><span class="tiny">AVAILABLE TIMES</span><strong id="swSelectedDateLabel">Select a date</strong></div>'
    '<div id="swTimeSlots" class="sw-time-slots"></div>'
    '<p class="sw-small-note">Times shown in Paris time. Live availability requires a Google Calendar API connection.</p></div></div>'
    '<div class="sw-scheduler-footer"><div id="swChosenSlot" class="sw-chosen">Select a date and a time to continue.</div>'
    '<button type="button" class="btn" id="swConfirmMock" onclick="confirmMockCall()" disabled><span class="btn-label">Confirm my call</span>' + ico('arrow-right') + '</button></div></div>')

step4 = ('<div id="step4" class="hidden"><h2>Let\'s connect.</h2><div class="fields">'
         '<label class="field">Your name<input id="contactName" placeholder="Full name"></label>'
         '<label class="field">Company<input id="contactCompany" placeholder="Company / Brand"></label>'
         '<label class="field full">Work email<input id="contactEmail" type="email" placeholder="you@company.com"></label></div>'
         '<div class="selection-box">' + ico('check') + '<div class="summary" id="summary"></div></div>'
         '<h3 class="section-title">How would you like to proceed?</h3>'
         '<div class="option selected" data-mode="call" onclick="pick(this)" tabindex="0">' + ico('clock') +
         '<div class="option-text"><strong>Schedule a 15-minute discovery call</strong><div class="muted">Choose a time with the SAY WHO team responsible for your project.</div></div>'
         '<button type="button" class="info-btn" data-detail="mode:call" aria-label="More about the discovery call">' + ico('info') + '</button></div>'
         '<div class="option" data-mode="proposal" onclick="pick(this)" tabindex="0">' + ico('mail') +
         '<div class="option-text"><strong>Receive a proposal by email</strong><div class="muted">For clients who already know what they need.</div></div>'
         '<button type="button" class="info-btn" data-detail="mode:proposal" aria-label="More about the proposal by email">' + ico('info') + '</button></div>'
         '<div id="bookingArea" class="booking-area" aria-live="polite">'
         '<h3 id="bookingTitle">YOUR SAY WHO CONTACT</h3><p id="bookingExplanation" class="muted"></p>'
         '<div class="booking-actions"><a id="bookingLink" class="btn" href="#" target="_blank" rel="noopener"><span class="btn-label">View available times</span>' + ico('arrow-up-right') + '</a>'
         '<button type="button" class="btn secondary" onclick="copyBrief()"><span class="btn-label">Copy my brief</span>' + ico('arrow-up-right') + '</button></div>'
         '<p id="bookingTimezone" class="softnote"></p>'
         '<p class="softnote">Pick a slot, then confirm it with your contact details on the Google page. Nothing entered here is sent automatically.</p>'
         '<p class="muted lead-in">Choose a date and time in the SAY WHO calendar below.</p>'
         + scheduler +
         '<div class="brief-preview"><strong>PROJECT BRIEF — FOR YOUR CONSULTANT</strong><pre id="briefPreview"></pre></div></div>'
         '<div id="proposalArea" class="booking-area hidden"><h3>Review and send your request</h3>'
         '<p class="muted">Your request will be sent to <strong>booking@saywhomedia.com</strong> once the SAY WHO email endpoint is connected.</p>'
         '<div class="brief-preview" id="proposalRecap" aria-live="polite"><strong id="proposalRecapHeading">YOUR REQUEST — SUMMARY</strong><div id="proposalPreview" class="sw-recap-content"></div></div>'
         '<div class="booking-actions"><button class="btn" type="button" id="sendRequestBtn" onclick="sendProposal()"><span class="btn-label">Send my request</span>' + ico('arrow-right') + '</button></div>'
         '<p id="proposalStatus" class="softnote" role="status" aria-live="polite"></p>'
         '<p class="softnote">DEMO MODE: Clicking SEND MY REQUEST simulates successful delivery. No email is actually sent in this preview.</p></div>'
         '<div id="completionArea" class="hidden" role="status" aria-live="polite"><div class="success-mark" aria-hidden="true">' + ico('check') + '</div>'
         '<div class="tiny">THANK YOU · SAY WHO</div><h3 id="completionTitle"></h3><p id="completionText" class="muted"></p><div id="completionExtra"></div>'
         '<p class="softnote">You can now close this window.</p>'
         '<button class="btn secondary" type="button" onclick="startNewRequest()"><span class="btn-label">Start a new request</span>' + ico('arrow-up-right') + '</button></div>'
         '<div class="actions" id="step4Back">' + btn('Back', 'go(3)', 'secondary') + '</div>'
         '<p class="softnote" id="step4Legal">All editorial publication requests are subject to SAY WHO editorial discretion. Booking slots and confirmation screens are simulated in this preview; no real call or email is created.</p></div>')

sprite = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
          '<symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></symbol>'
          '<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></symbol>'
          '<symbol id="i-calendar" viewBox="0 0 24 24"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></symbol>'
          '<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></symbol>'
          '<symbol id="i-mail" viewBox="0 0 24 24"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></symbol>'
          '<symbol id="i-arrow-right" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></symbol>'
          '<symbol id="i-arrow-up-right" viewBox="0 0 24 24"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></symbol>'
          '<symbol id="i-chevron-left" viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"/></symbol>'
          '<symbol id="i-chevron-right" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></symbol>'
          '<symbol id="i-x" viewBox="0 0 24 24"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></symbol>'
          '<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></symbol>'
          '<symbol id="i-map-pin" viewBox="0 0 24 24"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></symbol>'
          '</defs></svg>')

overlay = ('<div class="sw-detail-overlay hidden" id="swDetailOverlay"><div class="sw-detail-panel" role="dialog" aria-modal="true" aria-labelledby="swDetailTitle" tabindex="-1">'
           '<button type="button" class="sw-detail-close" id="swDetailClose" aria-label="Close">' + ico('x') + '</button>'
           '<h3 class="sw-detail-title" id="swDetailTitle"></h3><p class="sw-detail-text" id="swDetailText"></p><div id="swDetailBody"></div></div></div>')

body = (sprite + header +
        '<div class="layout"><div class="hero"><img src="assets/hero.jpg" alt="SAY WHO event portrait"></div>'
        '<main class="column"><div class="column-inner">'
        '<div class="intro"><h1>LET\'S MAKE<br>IT HAPPEN.</h1><p>Tell us what you\'re planning. We\'ll bring the right people, creative expertise and media reach.</p></div>'
        '<section class="panel"><div class="step-label" id="stepLabel">Your request — step 1 of 4</div>'
        '<div class="stepbar"><span class="active"></span><span></span><span></span><span></span></div>\n'
        + step1 + '\n' + step2 + '\n' + step3 + '\n' + step4 +
        '</section></div></main></div>' + footer + overlay)

css = css_own.replace('/*FOOTER_CSS*/', footer_css)
css += '\n.booking-area>h3:first-child{margin-top:0}\n'

out = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       + title + '\n<style>\n' + css + '\n</style></head>\n<body>' + body + '\n<script>\n' + script + '\n' + extra_js + '\n</script></body></html>\n')

dest = ROOT / 'saywho-book-us.html'
dest.write_text(out, encoding='utf-8')
(BUILD / 'out-script.js').write_text(script + '\n' + extra_js, encoding='utf-8')
print('written', dest, len(out))
