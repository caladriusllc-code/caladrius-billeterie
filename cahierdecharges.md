Voici un cahier des charges complet pour ton application de billetterie de formation en présentielle.---

## Cahier des charges — Application de billetterie de formation

### 1. Contexte & objectifs

L'application permet à des participants de s'inscrire et de payer leur place pour une formation en présentielle, et à l'organisateur de gérer les sessions, les réservations et les participants.

---

### 2. Stack technique

**Frontend** — Nuxt.js 3 (Vue 3, TypeScript, Composition API, Pinia, Tailwind CSS, `useFetch` / `$fetch`)

**Backend** — Django 5 + Django REST Framework, SimpleJWT pour l'authentification, Celery + Redis pour les tâches asynchrones (envoi d'emails, génération de QR codes)

**Base de données** — PostgreSQL

**Paiement** — Stripe (international) ou PayDunya (Côte d'Ivoire / UEMOA)

**Emails transactionnels** — SendGrid ou Mailgun

**Déploiement** — Backend sur Railway/Render, Frontend sur Vercel, ou Docker Compose sur un VPS

---

### 3. Fonctionnalités

#### 3.1 Côté participant (public)
- Consulter la page de présentation de la formation (programme, dates, lieu, prix, places restantes)
- S'inscrire (créer un compte ou continuer en tant qu'invité)
- Sélectionner le nombre de places et procéder au paiement
- Recevoir un email de confirmation avec le ticket (PDF + QR code)
- Accéder à son espace pour retrouver ses tickets

#### 3.2 Côté organisateur (admin)
- Créer/modifier une ou plusieurs sessions de formation
- Définir le quota de places, le prix, les dates
- Suivre les inscriptions en temps réel (tableau de bord)
- Exporter la liste des participants (CSV)
- Scanner les QR codes à l'entrée (interface de validation)
- Envoyer des rappels par email à tous les inscrits

---

### 4. Modèles de données Django

```python
# formations/models.py
class Formation(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    location    = models.CharField(max_length=300)
    starts_at   = models.DateTimeField()
    ends_at     = models.DateTimeField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    capacity    = models.PositiveIntegerField()
    is_active   = models.BooleanField(default=True)

    @property
    def available_seats(self):
        return self.capacity - self.tickets.filter(status='confirmed').count()

class Ticket(models.Model):
    STATUS_CHOICES = [('pending', 'En attente'), ('confirmed', 'Confirmé'), ('cancelled', 'Annulé')]
    formation   = models.ForeignKey(Formation, related_name='tickets', on_delete=models.PROTECT)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField(default=1)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    qr_code     = models.ImageField(upload_to='qrcodes/', blank=True)
    checked_in  = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    ticket         = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    provider       = models.CharField(max_length=50)  # 'stripe' ou 'paydunya'
    provider_id    = models.CharField(max_length=200, unique=True)
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    currency       = models.CharField(max_length=3, default='XOF')
    status         = models.CharField(max_length=20, default='pending')
    paid_at        = models.DateTimeField(null=True, blank=True)
```

---

### 5. Endpoints API (DRF)

```
GET    /api/formations/                   → liste des formations actives
GET    /api/formations/{id}/              → détail + places restantes
POST   /api/tickets/                      → créer une réservation (auth requis)
GET    /api/tickets/mine/                 → billets de l'utilisateur connecté
POST   /api/payments/checkout/            → initier le paiement (retourne checkout_url)
POST   /api/payments/webhook/stripe/      → webhook Stripe (signature vérifiée)
POST   /api/tickets/{uuid}/check-in/      → valider le QR code à l'entrée (admin)
GET    /api/admin/formations/{id}/participants/ → export participants (admin)
```

---

### 6. Structure Nuxt.js

```
pages/
  index.vue              ← présentation de la formation
  formations/[id].vue    ← détail + bouton "Réserver"
  checkout.vue           ← récap + paiement
  success.vue            ← confirmation post-paiement
  mon-espace/
    index.vue            ← liste de mes tickets
    ticket-[uuid].vue    ← ticket individuel + QR
  admin/
    dashboard.vue
    participants.vue
    scan.vue             ← scanner QR à l'entrée

composables/
  useAuth.ts
  useTickets.ts
  useFormation.ts

stores/
  auth.ts
  cart.ts
```

---

### 7. Bonnes pratiques à respecter

**Sécurité**
- Authentification JWT avec refresh token httpOnly cookie
- Rate limiting sur les endpoints sensibles (inscription, paiement)
- Validation des webhooks Stripe par signature HMAC
- Variables sensibles exclusivement dans `.env` (jamais dans le code)
- CORS configuré strictement (whitelist du domaine Nuxt uniquement)

**Backend Django**
- Découper en apps Django indépendantes (`accounts`, `formations`, `tickets`, `payments`)
- Utiliser `select_related` / `prefetch_related` pour éviter les requêtes N+1
- Wraper la création ticket + initiation paiement dans une transaction atomique (`@transaction.atomic`)
- Tâches asynchrones avec Celery : envoi d'emails, génération PDF/QR code
- Tests unitaires avec `pytest-django` pour les modèles et les endpoints critiques

**Frontend Nuxt**
- SSR pour la page de présentation (SEO), CSR pour l'espace personnel
- Middleware Nuxt pour protéger les routes `/admin/*` et `/mon-espace/*`
- Gestion des erreurs API centralisée avec un plugin `$fetch` interceptor
- Optimistic UI sur le panier, avec rollback en cas d'erreur serveur

**Déploiement**
- CI/CD avec GitHub Actions (lint → tests → build → deploy)
- Variables d'environnement séparées par environnement (`dev`, `staging`, `prod`)
- Migrations Django versionées et appliquées avant le redémarrage du serveur
- Logs centralisés (Sentry pour le monitoring d'erreurs)

---

### 8. Phases de développement suggérées

**Phase 1 — Socle (2 semaines)** : Setup Django + DRF + JWT, modèles de base, endpoints formations/tickets, setup Nuxt avec authentification, page de présentation.

**Phase 2 — Paiement (1 semaine)** : Intégration Stripe ou PayDunya, webhook + confirmation automatique du ticket, génération QR code.

**Phase 3 — Notifications & UX (1 semaine)** : Emails transactionnels (confirmation, rappel), espace personnel, page ticket avec QR, export CSV admin.

**Phase 4 — Mise en production (3 jours)** : Docker Compose ou déploiement PaaS, CI/CD, Sentry, tests de charge basiques.

---

Veux-tu que je t'aide à démarrer une partie en particulier — par exemple le setup initial du projet Django, les serializers DRF, ou la structure Nuxt avec Pinia ?