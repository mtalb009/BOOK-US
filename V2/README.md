# SAY WHO — Book Us · V2

Ouvrir `public/index.html` (redirige vers `saywho-book-us.html`). Page autonome : HTML + CSS + JS dans un seul fichier, images dans `public/assets/`.

## Changements par rapport à la version Microburo

1. **Photo hero remplacée** — `assets/hero.jpg` (même nom de fichier, 2576 × 1719).
2. **Nouvel agenda « discovery call » (étape 4)** — l'iframe Google Appointment est remplacée par un module de réservation minimaliste, inspiré de Cal.com, dans la charte :
   - en-tête : initiales + nom de l'interlocuteur, « Discovery call », 15 min · Google Meet · Europe/Paris ;
   - calendrier mensuel (jours disponibles sur fond gris, jour choisi en noir, point sous aujourd'hui) ;
   - colonne d'horaires (bascule 12h/24h) ; un clic sur un horaire affiche « horaire | Confirmer » ;
   - responsive via container query : sous 520 px, horaires sous le calendrier en grille de 3.
3. **Écran de fin** après confirmation : date et heure du RDV, brief du projet, bouton « Copier mon brief ».
4. **Correctif** : dans le brief, « Country » affiche « Not provided » au lieu de « Select a country » quand aucun pays n'est choisi.
5. **Traductions** FR / IT ajoutées pour tous les nouveaux textes (`SW_TRANSLATIONS`).

## Agenda branché sur Google Calendar (option A)

Arborescence (projet Cloudflare Pages) :

```
V2/
  public/                     ← fichiers servis (index.html, saywho-book-us.html, assets/)
  functions/api/[[route]].js  ← API Google Calendar (Pages Function)
  wrangler.toml               ← config non secrète (agendas, horaires)
  .dev.vars.example           ← modèle des secrets
```

- `GET /api/availability?who=paris&month=2026-11` → `freeBusy` sur l'agenda de l'interlocuteur, renvoie les créneaux libres de 15 min (pas de 30 min) dans les plages d'ouverture, heure de Paris.
- `POST /api/book` → revérifie le créneau, puis `events.insert` avec lien Google Meet automatique, client en invité (`sendUpdates=all` : il reçoit l'invitation par email), brief en description. Créneau pris entre-temps → 409, le front recharge les disponibilités.
- Côté page : `calAvail()` lit les créneaux chargés par mois et par interlocuteur, `confirmMockCall()` fait le POST. Si l'API ne répond pas (ex. fichier ouvert en local), l'agenda affiche un lien vers la page Google Appointment de l'interlocuteur (`BOOKING_LINKS`).

Routage inchangé : `getRouting()` → `paris` (Anne-Laure, + toute demande « Creative Campaign »), `usa` (Chloé Cvoric), `italy` (Ludovica Arcero).

### Mise en service

1. **Google Cloud** : créer un projet, activer *Google Calendar API*.
2. **Accès aux agendas** — au choix :
   - **Compte de service (recommandé si Google Workspace)** : créer un compte de service + une clé JSON. Dans la console admin Workspace › Sécurité › Contrôle des API › Délégation au niveau du domaine, ajouter l'ID client du compte de service avec les scopes
     `https://www.googleapis.com/auth/calendar.events,https://www.googleapis.com/auth/calendar.freebusy`.
     Secrets : `GOOGLE_SA_EMAIL`, `GOOGLE_SA_PRIVATE_KEY` (champ `private_key` du JSON).
   - **OAuth** (sans admin Workspace) : client OAuth « application Web », chaque interlocuteur autorise une fois (ex. via OAuth Playground, scopes ci-dessus, accès hors ligne). Secrets : `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN_PARIS|USA|ITALY`.
3. **Cloudflare Pages** : renseigner `CALENDAR_PARIS|USA|ITALY` (adresse email Google de chacun) dans `wrangler.toml`, puis :
   ```
   cd V2
   npx wrangler pages secret put GOOGLE_SA_EMAIL
   npx wrangler pages secret put GOOGLE_SA_PRIVATE_KEY
   npx wrangler pages deploy
   ```
   Test local : copier `.dev.vars.example` en `.dev.vars`, puis `npx wrangler pages dev`.
4. **Horaires** : par défaut lun–ven, 9h–13h et 14h–18h (heure de Paris), préavis 12 h, 6 mois max. Réglable par interlocuteur, ex. `WORK_HOURS_USA = "15:00-23:00"` pour Chloé.

À savoir : l'API est publique (comme tout formulaire de réservation). Pour limiter les abus, ajouter Cloudflare Turnstile ou une règle de rate limiting sur `/api/book`.

L'ancien bloc Google (`BOOKING_EMBEDS`, iframe `#bookingEmbed`) est toujours dans le code mais masqué et non chargé ; `BOOKING_LINKS` sert de secours si l'API est indisponible.

## Toujours en mode démo (inchangé)

- « Envoyer ma demande » (proposition par email) : simulé — l'endpoint prévu `EMAIL_ENDPOINT = /api/send-booking-request.php` n'existe pas encore.
- Formulaire newsletter et « Cookie settings » du footer : à relier aux outils existants du site.
- Mention « Simulation… » sur l'écran de confirmation de la proposition par email : à retirer une fois l'envoi d'email branché.
