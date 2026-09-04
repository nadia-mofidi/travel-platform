from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta

from accounts.models import Profile
from blog.models import Category, Post, Comment
from website.models import Newsletter


class Command(BaseCommand):
    help = "Create demo data for the Travel Platform"

    def handle(self, *args, **options):
        authors_group, _ = Group.objects.get_or_create(name="Authors")

        users_data = [
            ("alex.morgan", "Alex", "Morgan", "alex.morgan@example.com", True),
            ("sophia.lee", "Sophia", "Lee", "sophia.lee@example.com", True),
            ("daniel.carter", "Daniel", "Carter", "daniel.carter@example.com", True),
            ("emma.johnson", "Emma", "Johnson", "emma.johnson@example.com", False),
            ("mike.wilson", "Mike", "Wilson", "mike.wilson@example.com", False),
        ]

        users = {}

        for username, first_name, last_name, email, is_author in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                },
            )

            if created:
                user.set_password("DemoPass123!")
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email

            user.save()

            if is_author:
                user.groups.add(authors_group)
            else:
                user.groups.remove(authors_group)

            users[username] = user

        profiles = {
            "alex.morgan": {
                "job_title": "Travel Writer",
                "bio": "I love discovering quiet places, local food, and stories worth sharing.",
                "avatar_preset": "avatar1.png",
                "facebook": "https://facebook.com/alex.morgan",
                "twitter": "https://twitter.com/alexmorgan",
                "instagram": "https://instagram.com/alexmorgan",
                "behance": "https://behance.net/alexmorgan",
            },
            "sophia.lee": {
                "job_title": "Travel Photographer",
                "bio": "I document landscapes, city streets, and the small moments that make a journey memorable.",
                "avatar_preset": "avatar2.png",
                "facebook": "https://facebook.com/sophia.lee",
                "twitter": "https://twitter.com/sophialee",
                "instagram": "https://instagram.com/sophialee",
                "behance": "https://behance.net/sophialee",
            },
            "daniel.carter": {
                "job_title": "Adventure Blogger",
                "bio": "I write about road trips, mountain trails, coastal escapes, and practical travel experiences.",
                "avatar_preset": "avatar3.png",
                "facebook": "https://facebook.com/daniel.carter",
                "twitter": "https://twitter.com/danielcarter",
                "instagram": "https://instagram.com/danielcarter",
                "behance": "https://behance.net/danielcarter",
            },
        }

        for username, profile_data in profiles.items():
            profile = users[username].profile
            for field, value in profile_data.items():
                setattr(profile, field, value)
            profile.avatar = None
            profile.save()

        category_names = [
            "Adventure",
            "Beach",
            "City Breaks",
            "Culture",
            "Nature",
            "Travel Tips",
        ]

        categories = {}
        for name in category_names:
            category, _ = Category.objects.get_or_create(name=name)
            categories[name] = category

        now = timezone.now()

        posts_data = [
            {
                "title": "Hidden Beaches of Kerala",
                "author": "alex.morgan",
                "days_ago": 7,
                "featured": True,
                "login_require": False,
                "categories": ["Beach", "Nature"],
                "tags": ["Kerala", "India", "Coast", "Beach"],
            },
            {
                "title": "A Weekend in Cappadocia",
                "author": "sophia.lee",
                "days_ago": 9,
                "featured": True,
                "login_require": False,
                "categories": ["Adventure", "Culture"],
                "tags": ["Turkey", "Adventure", "Balloons", "Weekend"],
            },
            {
                "title": "Walking Through Old Lisbon",
                "author": "daniel.carter",
                "days_ago": 12,
                "featured": False,
                "login_require": False,
                "categories": ["City Breaks", "Culture"],
                "tags": ["Portugal", "Lisbon", "Culture", "Europe"],
            },
            {
                "title": "The Best Sunset Spots in Santorini",
                "author": "alex.morgan",
                "days_ago": 15,
                "featured": False,
                "login_require": False,
                "categories": ["Beach", "Nature"],
                "tags": ["Greece", "Sunset", "Photography"],
            },
            {
                "title": "A Beginner Guide to Kerala Backwaters",
                "author": "sophia.lee",
                "days_ago": 17,
                "featured": False,
                "login_require": True,
                "categories": ["Nature", "Travel Tips"],
                "tags": ["Kerala", "Backwaters", "Nature", "Travel Tips"],
            },
            {
                "title": "Seven Days in the Swiss Alps",
                "author": "daniel.carter",
                "days_ago": 20,
                "featured": True,
                "login_require": False,
                "categories": ["Adventure", "Nature"],
                "tags": ["Switzerland", "Mountains", "Adventure"],
            },
            {
                "title": "How to Pack Light for a Long Trip",
                "author": "alex.morgan",
                "days_ago": 23,
                "featured": False,
                "login_require": False,
                "categories": ["Travel Tips"],
                "tags": ["Travel Tips", "Packing", "Adventure"],
            },
            {
                "title": "Our Next Destination: Japan",
                "author": "sophia.lee",
                "days_ago": None,
                "featured": False,
                "login_require": False,
                "status": False,
                "categories": ["Culture", "Travel Tips"],
                "tags": ["Japan", "Asia", "Planning"],
            },
            {
                "title": "Planning a Road Trip Across Oman",
                "author": "daniel.carter",
                "days_ago": None,
                "featured": False,
                "login_require": False,
                "status": False,
                "categories": ["Adventure", "Travel Tips"],
                "tags": ["Oman", "Road Trip", "Adventure"],
            },
            {
                "title": "A Private Travel Journal",
                "author": "alex.morgan",
                "days_ago": 25,
                "featured": False,
                "login_require": True,
                "categories": ["Travel Tips"],
                "tags": ["Travel", "Journal", "Members"],
            },
        ]

        created_posts = {}

        for item in posts_data:
            status = item.get("status", True)
            publish_date = (
                now - timedelta(days=item["days_ago"])
                if item["days_ago"] is not None
                else None
            )

            content = (
                f"<h3>{item['title']}</h3>"
                "<p>This is a demo travel story created for the Travel Platform portfolio. "
                "It shares practical ideas, memorable places, and inspiration for the next journey.</p>"
                "<p>Use this sample post to explore search, filters, author pages, comments, "
                "login-required posts, and previous/next navigation.</p>"
            )

            post, _ = Post.objects.get_or_create(
                title=item["title"],
                defaults={
                    "content": content,
                    "image": "blog/default.jpg",
                    "author": users[item["author"]],
                    "status": status,
                    "is_featured": item["featured"],
                    "login_require": item["login_require"],
                    "publish_date": publish_date,
                },
            )

            post.content = content
            post.image = "blog/default.jpg"
            post.author = users[item["author"]]
            post.status = status
            post.is_featured = item["featured"]
            post.login_require = item["login_require"]
            post.publish_date = publish_date
            post.save()

            post.category.set([categories[name] for name in item["categories"]])
            post.tags.set(item["tags"])
            created_posts[item["title"]] = post

        comments_data = [
            ("Hidden Beaches of Kerala", "Emma Johnson", "emma.johnson@example.com", "Beautiful place!", "The beach looks amazing. Adding this to my list.", True),
            ("A Weekend in Cappadocia", "Mike Wilson", "mike.wilson@example.com", "Great guide", "The travel ideas were really useful.", True),
            ("Walking Through Old Lisbon", "Emma Johnson", "emma.johnson@example.com", "Love Lisbon", "The walking route sounds perfect.", True),
            ("The Best Sunset Spots in Santorini", "Mike Wilson", "mike.wilson@example.com", "Wonderful views", "That sunset section is my favorite.", False),
            ("A Beginner Guide to Kerala Backwaters", "Emma Johnson", "emma.johnson@example.com", "Helpful tips", "Thanks for sharing these practical ideas.", True),
        ]

        for title, name, email, subject, message, approved in comments_data:
            Comment.objects.get_or_create(
                post=created_posts[title],
                email=email,
                subject=subject,
                defaults={
                    "name": name,
                    "message": message,
                    "approved": approved,
                },
            )

        for email in [
            "emma.johnson@example.com",
            "mike.wilson@example.com",
            "hello@example.com",
        ]:
            Newsletter.objects.get_or_create(email=email)

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
        self.stdout.write("Demo password for all users: DemoPass123!")
