from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_ticket_email(order):
    """
    Prépare et envoie l'e-mail contenant les tickets à l'acheteur (connecté ou invité)
    """
    # 1. Déterminer l'adresse de destination et le nom
    to_email = order.user.email if order.user else order.guest_email
    buyer_name = order.user.username if order.user else order.guest_name
    
    if not to_email:
        return False # Pas d'email disponible
        
    subject = f"🎟️ Vos billets pour : {order.event.title} (Commande N° {order.order_number})"
    
    # 2. Contexte pour le template HTML
    context = {
        'buyer_name': buyer_name,
        'order': order,
        # On passe la liste complète des lignes et des tickets associés
        'items': order.items.prefetch_related('tickets', 'ticket_type')
    }
    
    # 3. Génération du contenu HTML et texte brut (fallback pour les vieilles boîtes mail)
    html_content = render_to_string('orders/emails/ticket_email.html', context)
    text_content = strip_tags(html_content) # Supprime les balises HTML
    
    # 4. Création de l'e-mail
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email]
    )
    email.attach_alternative(html_content, "text/html")
    
    # 5. Envoi effectif
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {str(e)}")
        return False