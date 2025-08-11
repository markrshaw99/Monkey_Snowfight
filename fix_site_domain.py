#!/usr/bin/env python
"""
Simple script to update Django site domain on Heroku
Run with: heroku run python fix_site_domain.py --app your-app-name
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monkey_snowfight.settings')
django.setup()

from django.contrib.sites.models import Site

try:
    site = Site.objects.get(pk=1)
    old_domain = site.domain
    old_name = site.name
    
    # Update to your actual Heroku domain
    site.domain = 'monkey-snowfight-game-and-chat-ce8d3c703935.herokuapp.com'
    site.name = 'Monkey Snowfight'
    site.save()
    
    print(f"✅ SITE UPDATED SUCCESSFULLY!")
    print(f"Old domain: {old_domain}")
    print(f"New domain: {site.domain}")
    print(f"Old name: {old_name}")
    print(f"New name: {site.name}")
    print("Emails should now show correct domain instead of [example.com]")
    
except Site.DoesNotExist:
    print("❌ Site with ID 1 does not exist")
except Exception as e:
    print(f"❌ Error: {e}")
