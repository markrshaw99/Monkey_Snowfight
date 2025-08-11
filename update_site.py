#!/usr/bin/env python
"""
Quick script to update Django site domain to fix [example.com] in emails
Run this on Heroku: python update_site.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monkey_snowfight.settings')
django.setup()

from django.contrib.sites.models import Site

try:
    site = Site.objects.get(pk=1)
    site.domain = 'monkey-snowfight-game-and-chat.herokuapp.com'
    site.name = 'Monkey Snowfight'
    site.save()
    print(f"✅ Site updated: {site.name} - {site.domain}")
except Exception as e:
    print(f"❌ Error updating site: {e}")
