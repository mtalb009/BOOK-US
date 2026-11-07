"""One-shot patch: detail panels ("i") and the project placeholder translated in FR / IT.

openDetail() runs every string through swT(); translations appended to SW_TRANSLATIONS.
Usage: python3 tools/patch-details-i18n.py
"""
import json
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "html" / "saywho-book-us.html"
html = path.read_text(encoding="utf-8")


def sub(old, new):
    global html
    if old not in html:
        raise SystemExit(f"not found: {old[:80]}")
    html = html.replace(old, new, 1)


sub("document.getElementById('swDetailTitle').textContent=d.title;",
    "document.getElementById('swDetailTitle').textContent=swT(d.title);")
sub("document.getElementById('swDetailText').textContent=d.text;",
    "document.getElementById('swDetailText').textContent=swT(d.text);")
sub("h.textContent=d.heading;", "h.textContent=swT(d.heading);")
sub("sp.textContent=t;", "sp.textContent=swT(t);")
sub("n.textContent=d.note;", "n.textContent=swT(d.note);")

# EN -> (FR, IT)
T = {
    "e.g. Brand launch in New York": ("ex. Lancement de marque à New York", "es. Lancio di un brand a New York"),
    "What’s included": ("Ce qui est inclus", "Cosa è incluso"),
    "How it works": ("Comment ça marche", "Come funziona"),
    # Photo coverage
    "Photo coverage": ("Couverture photo", "Servizio fotografico"),
    "Event photography and portraits by SAY WHO photographers — for your guests, your brand and our editorial pages.":
        ("Photos d’événement et portraits par les photographes SAY WHO — pour vos invités, votre marque et nos pages éditoriales.",
         "Foto dell’evento e ritratti a cura dei fotografi SAY WHO — per i tuoi ospiti, il tuo brand e le nostre pagine editoriali."),
    "A SAY WHO photographer on site, for the time slot you choose":
        ("Un photographe SAY WHO sur place, sur le créneau de votre choix",
         "Un fotografo SAY WHO sul posto, nella fascia oraria che scegli"),
    "Guest portraits, atmosphere and key moments":
        ("Portraits des invités, ambiance et temps forts", "Ritratti degli ospiti, atmosfera e momenti chiave"),
    "An edited selection of images, cleared for your communication":
        ("Une sélection d’images retouchées, libres pour votre communication",
         "Una selezione di immagini editate, utilizzabili per la tua comunicazione"),
    "Possible publication on SAY WHO, at editorial discretion":
        ("Publication possible sur SAY WHO, à la discrétion de la rédaction",
         "Possibile pubblicazione su SAY WHO, a discrezione della redazione"),
    "Pricing depends on duration and location — confirmed in your proposal.":
        ("Le tarif dépend de la durée et du lieu — confirmé dans votre proposition.",
         "Il prezzo dipende da durata e luogo — confermato nella tua proposta."),
    # Video coverage
    "Video coverage": ("Couverture vidéo", "Copertura video"),
    "Event films, highlights and short-form reels by SAY WHO videographers — for your guests, your brand and our editorial pages.":
        ("Films d’événement, highlights et reels courts par les vidéastes SAY WHO — pour vos invités, votre marque et nos pages éditoriales.",
         "Film dell’evento, highlights e reel brevi a cura dei videomaker SAY WHO — per i tuoi ospiti, il tuo brand e le nostre pagine editoriali."),
    "A SAY WHO videographer on site, for the time slot you choose":
        ("Un vidéaste SAY WHO sur place, sur le créneau de votre choix",
         "Un videomaker SAY WHO sul posto, nella fascia oraria che scegli"),
    "A highlights film and reels ready for social channels":
        ("Un film highlights et des reels prêts pour les réseaux sociaux",
         "Un film highlights e reel pronti per i social"),
    "Edited footage, cleared for your communication":
        ("Des images montées, libres pour votre communication", "Riprese montate, utilizzabili per la tua comunicazione"),
    "Pricing depends on duration, format and location — confirmed in your proposal.":
        ("Le tarif dépend de la durée, du format et du lieu — confirmé dans votre proposition.",
         "Il prezzo dipende da durata, formato e luogo — confermato nella tua proposta."),
    # Article
    "Article on SAY WHO": ("Article sur SAY WHO", "Articolo su SAY WHO"),
    "An editorial piece in the Diary, What or Interviews sections of SAY WHO, written and published by our editorial team.":
        ("Un contenu éditorial dans les rubriques Diary, What ou Interviews de SAY WHO, rédigé et publié par notre rédaction.",
         "Un contenuto editoriale nelle sezioni Diary, What o Interviews di SAY WHO, scritto e pubblicato dalla nostra redazione."),
    "A format chosen with the editors: Diary report, What feature or interview":
        ("Un format choisi avec la rédaction : reportage Diary, sujet What ou interview",
         "Un formato scelto con la redazione: reportage Diary, articolo What o intervista"),
    "Writing and images produced by SAY WHO":
        ("Textes et images produits par SAY WHO", "Testi e immagini prodotti da SAY WHO"),
    "Publication on saywhomedia.com": ("Publication sur saywhomedia.com", "Pubblicazione su saywhomedia.com"),
    "Publication remains at SAY WHO’s editorial discretion.":
        ("La publication reste à la discrétion de la rédaction SAY WHO.",
         "La pubblicazione resta a discrezione della redazione SAY WHO."),
    # Creative Campaign
    "Creative Campaign": ("Campagne créative", "Campagna creativa"),
    "Concept, art direction and production by SAY WHO STUDIO — a campaign built around your brand, from the first idea to delivery.":
        ("Concept, direction artistique et production par SAY WHO STUDIO — une campagne construite autour de votre marque, de la première idée à la livraison.",
         "Concept, direzione artistica e produzione a cura di SAY WHO STUDIO — una campagna costruita attorno al tuo brand, dalla prima idea alla consegna."),
    "Concept and art direction led by SAY WHO STUDIO":
        ("Concept et direction artistique menés par SAY WHO STUDIO",
         "Concept e direzione artistica guidati da SAY WHO STUDIO"),
    "Production of photo and video assets":
        ("Production des contenus photo et vidéo", "Produzione dei contenuti foto e video"),
    "Handled by the Studio lead, whatever the event country":
        ("Suivi par le responsable du Studio, quel que soit le pays de l’événement",
         "Seguito dal responsabile dello Studio, qualunque sia il paese dell’evento"),
    "Scope and pricing are defined with the Studio after a first call.":
        ("Le périmètre et le tarif sont définis avec le Studio après un premier échange.",
         "Perimetro e prezzo vengono definiti con lo Studio dopo una prima call."),
    # Social takeover
    "Social takeover": ("Social takeover", "Social takeover"),
    "A planned takeover of SAY WHO social channels, on Instagram and TikTok, around your event.":
        ("Une prise de parole planifiée sur les réseaux SAY WHO, Instagram et TikTok, autour de votre événement.",
         "Un takeover pianificato dei canali social SAY WHO, su Instagram e TikTok, attorno al tuo evento."),
    "Content planned with the SAY WHO social team":
        ("Contenus planifiés avec l’équipe social de SAY WHO", "Contenuti pianificati con il team social di SAY WHO"),
    "Coverage published on Instagram and TikTok as agreed":
        ("Publication sur Instagram et TikTok selon le plan convenu",
         "Pubblicazione su Instagram e TikTok come concordato"),
    "Timing and format agreed before the event":
        ("Calendrier et format validés avant l’événement", "Tempistiche e formato concordati prima dell’evento"),
    "Availability and format are confirmed in your proposal.":
        ("Disponibilité et format confirmés dans votre proposition.",
         "Disponibilità e formato confermati nella tua proposta."),
    # Corporate coverage
    "Corporate coverage": ("Couverture corporate", "Copertura corporate"),
    "Photo and video coverage delivered privately to your team — no publication on SAY WHO is requested.":
        ("Couverture photo et vidéo livrée en privé à votre équipe — sans publication sur SAY WHO.",
         "Copertura foto e video consegnata privatamente al tuo team — senza pubblicazione su SAY WHO."),
    "Private delivery of the final images and films":
        ("Livraison privée des images et films finaux", "Consegna privata di immagini e video finali"),
    "No publication on SAY WHO": ("Aucune publication sur SAY WHO", "Nessuna pubblicazione su SAY WHO"),
    "Usage rights agreed in your proposal":
        ("Droits d’usage définis dans votre proposition", "Diritti d’uso definiti nella tua proposta"),
    # Videographer
    "A videographer": ("Un vidéaste", "Un videomaker"),
    "A videographer joins your photo team to capture the event in motion.":
        ("Un vidéaste rejoint votre équipe photo pour capter l’événement en mouvement.",
         "Un videomaker si unisce al team foto per riprendere l’evento in movimento."),
    "One videographer alongside your photographers":
        ("Un vidéaste aux côtés de vos photographes", "Un videomaker al fianco dei tuoi fotografi"),
    "Footage for highlights or social content":
        ("Des images pour un film highlights ou des contenus social", "Riprese per highlights o contenuti social"),
    "Coordinated with the photo team on site":
        ("Coordonné avec l’équipe photo sur place", "Coordinato con il team foto sul posto"),
    "Added to your coverage — confirmed in your proposal.":
        ("Ajouté à votre couverture — confirmé dans votre proposition.",
         "Aggiunto alla tua copertura — confermato nella tua proposta."),
    # Additional crew
    "Additional crew": ("Équipe renforcée", "Team aggiuntivo"),
    "Two or more photographers and/or videographers, to cover several areas or moments at once.":
        ("Deux photographes et/ou vidéastes ou plus, pour couvrir plusieurs espaces ou moments à la fois.",
         "Due o più fotografi e/o videomaker, per coprire più spazi o momenti contemporaneamente."),
    "Simultaneous coverage of several spaces":
        ("Couverture simultanée de plusieurs espaces", "Copertura simultanea di più spazi"),
    "Extra coverage on the key moments":
        ("Couverture renforcée sur les temps forts", "Copertura rafforzata nei momenti chiave"),
    "One point of coordination at SAY WHO":
        ("Un seul interlocuteur chez SAY WHO", "Un unico referente in SAY WHO"),
    "Team size is confirmed with your contact.":
        ("La taille de l’équipe est confirmée avec votre contact.",
         "La dimensione del team viene confermata con il tuo referente."),
    # On-site editor
    "On-site editor": ("Éditeur sur place", "Editor sul posto"),
    "An editor works during your event to select and retouch images as they come in.":
        ("Un éditeur travaille pendant l’événement pour sélectionner et retoucher les images au fil de l’eau.",
         "Un editor lavora durante l’evento per selezionare e ritoccare le immagini man mano che arrivano."),
    "A live selection of the best images":
        ("Une sélection en direct des meilleures images", "Una selezione in diretta delle immagini migliori"),
    "Light retouching on site": ("Retouche légère sur place", "Ritocco leggero sul posto"),
    "A faster turnaround after the event":
        ("Une livraison plus rapide après l’événement", "Tempi di consegna più rapidi dopo l’evento"),
    # Image live delivery
    "Image live delivery": ("Livraison des images en direct", "Consegna foto in tempo reale"),
    "Selected images delivered to you during the event, so you can communicate the same day.":
        ("Une sélection d’images livrée pendant l’événement, pour communiquer le jour même.",
         "Una selezione di immagini consegnata durante l’evento, per comunicare in giornata."),
    "A first selection sent while the event is running":
        ("Une première sélection envoyée pendant l’événement", "Una prima selezione inviata durante l’evento"),
    "Delivery through a shared link or the channel you prefer":
        ("Livraison par lien partagé ou par le canal de votre choix",
         "Consegna tramite link condiviso o il canale che preferisci"),
    "Works best together with an on-site editor":
        ("Idéal avec un éditeur sur place", "Ideale insieme a un editor sul posto"),
    "Delivery times depend on connectivity at the venue.":
        ("Les délais dépendent de la connexion sur le lieu.", "I tempi dipendono dalla connessione sul posto."),
    # Amplification card
    "Amplification": ("Amplification", "Amplificazione"),
    "Bring your event to a wider, relevant audience through SAY WHO, using one or more of the options in this card.":
        ("Faites rayonner votre événement auprès d’une audience plus large et qualifiée grâce à SAY WHO, avec une ou plusieurs options de cette carte.",
         "Porta il tuo evento a un pubblico più ampio e mirato con SAY WHO, scegliendo una o più opzioni di questa scheda."),
    "Social media amplification: your event relayed through SAY WHO accounts":
        ("Amplification sur les réseaux sociaux : votre événement relayé par les comptes SAY WHO",
         "Amplificazione sui social media: il tuo evento rilanciato dagli account SAY WHO"),
    "Weekly digest inclusion: a feature slot in the SAY WHO newsletter":
        ("Intégration dans la newsletter hebdomadaire : un emplacement dédié dans la newsletter SAY WHO",
         "Inserimento nella newsletter settimanale: uno spazio dedicato nella newsletter SAY WHO"),
    "Press push: a short press note sent to relevant journalists and editors":
        ("Relais presse : une courte note envoyée aux journalistes et rédactions concernés",
         "Diffusione stampa: una breve nota inviata a giornalisti e redazioni pertinenti"),
    "Dark posts with paid reach: paid social posts aimed at your audience, kept off the SAY WHO feed":
        ("Dark posts avec amplification payante : posts sponsorisés ciblant votre audience, hors du fil SAY WHO",
         "Dark post con promozione a pagamento: post sponsorizzati rivolti al tuo pubblico, fuori dal feed SAY WHO"),
    "Format, calendar and media budget are agreed in your proposal. Press pick-up cannot be guaranteed.":
        ("Format, calendrier et budget média sont définis dans votre proposition. Les reprises presse ne peuvent être garanties.",
         "Formato, calendario e budget media sono definiti nella tua proposta. Le uscite stampa non possono essere garantite."),
    # Media partners card
    "Media partners": ("Partenaires médias", "Media partner"),
    "A bespoke amplification proposal with media partners that fit your event. Tick the option to choose the titles you are interested in.":
        ("Une proposition d’amplification sur mesure avec des médias partenaires adaptés à votre événement. Cochez l’option pour choisir les titres qui vous intéressent.",
         "Una proposta di amplificazione su misura con media partner adatti al tuo evento. Seleziona l’opzione per scegliere le testate che ti interessano."),
    "Titles chosen from the SAY WHO partner network":
        ("Des titres choisis dans le réseau de partenaires SAY WHO",
         "Testate scelte dalla rete di partner SAY WHO"),
    "A proposal tailored to your event":
        ("Une proposition adaptée à votre événement", "Una proposta su misura per il tuo evento"),
    "Handled by your SAY WHO contact": ("Suivi par votre contact SAY WHO", "Seguito dal tuo referente SAY WHO"),
    "Placements are subject to availability, editorial approval and a separate agreement.":
        ("Les parutions sont soumises à disponibilité, validation éditoriale et accord séparé.",
         "Le uscite sono soggette a disponibilità, approvazione editoriale e accordo separato."),
    # Step 4 modes
    "Discovery call": ("Échange découverte", "Call conoscitiva"),
    "A 15-minute video call with the SAY WHO contact responsible for your project, to talk through your event and your needs.":
        ("Un appel vidéo de 15 minutes avec le contact SAY WHO en charge de votre projet, pour parler de votre événement et de vos besoins.",
         "Una videochiamata di 15 minuti con il referente SAY WHO del tuo progetto, per parlare del tuo evento e delle tue esigenze."),
    "Pick a date and a time in the calendar":
        ("Choisissez une date et un horaire dans le calendrier", "Scegli una data e un orario nel calendario"),
    "The call takes place on Google Meet":
        ("L’appel a lieu sur Google Meet", "La call si svolge su Google Meet"),
    "Your contact depends on your country and services":
        ("Votre contact dépend de votre pays et des services choisis",
         "Il tuo referente dipende dal paese e dai servizi scelti"),
    "Times are shown in Paris time.":
        ("Les horaires sont affichés en heure de Paris.", "Gli orari sono indicati nel fuso di Parigi."),
    "Proposal by email": ("Proposition par email", "Proposta via email"),
    "Prefer to skip the call? Send your request and receive a written proposal by email.":
        ("Vous préférez éviter l’appel ? Envoyez votre demande et recevez une proposition écrite par email.",
         "Preferisci evitare la call? Invia la richiesta e ricevi una proposta scritta via email."),
    "Review your summary and send it":
        ("Relisez votre récapitulatif et envoyez-le", "Controlla il riepilogo e invialo"),
    "A SAY WHO contact replies with a proposal":
        ("Un contact SAY WHO vous répond avec une proposition", "Un referente SAY WHO ti risponde con una proposta"),
    "Ideal if you already know what you need":
        ("Idéal si vous savez déjà ce dont vous avez besoin", "Ideale se sai già di cosa hai bisogno"),
    "Pricing is detailed in the proposal.":
        ("Le tarif est détaillé dans la proposition.", "Il prezzo è dettagliato nella proposta."),
}

fr = json.dumps({k: v[0] for k, v in T.items()}, ensure_ascii=False)
it = json.dumps({k: v[1] for k, v in T.items()}, ensure_ascii=False)
block = ("// ----- Detail panels + placeholder (FR / IT) -----\n"
         f"Object.assign(SW_TRANSLATIONS.fr,{fr});\n"
         f"Object.assign(SW_TRANSLATIONS.it,{it});\n")
sub("swTranslateUI();swUpdateDynamic();\n\n</script></body></html>",
    block + "swTranslateUI();swUpdateDynamic();\n\n</script></body></html>")
path.write_text(html, encoding="utf-8")
print("patched", path, len(T), "keys")
