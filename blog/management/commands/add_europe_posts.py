from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from blog.models import Category, Post


class Command(BaseCommand):
    help = "Add Paris, France and England demo posts"

    def handle(self, *args, **options):

        authors = [
            User.objects.get(username="alex.morgan"),
            User.objects.get(username="sophia.lee"),
            User.objects.get(username="daniel.carter"),
        ]

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

        posts = [
            {
                "title": "A Weekend in Paris: A First-Timer's Guide",
                "author": authors[0],
                "days_ago": 3,
                "featured": True,
                "login_require": False,
                "categories": ["City Breaks", "Culture"],
                "tags": ["Paris", "France", "Eiffel Tower", "Louvre", "Travel Tips"],
                "content": """
                    <p>Paris is one of those cities that feels familiar even on your first visit. 
                    From the Eiffel Tower to the quiet streets of Montmartre, there is always another 
                    corner waiting to be discovered.</p>

                    <p>For a first trip, start with the Eiffel Tower and continue along the Seine before 
                    spending an afternoon exploring the Louvre. Leave some time simply to walk, stop at 
                    a small café, and enjoy the rhythm of the city.</p>

                    <p>In the evening, head toward the Latin Quarter or Montmartre for dinner. Paris is 
                    best experienced without rushing from one attraction to another.</p>
                """
            },
            {
                "title": "Walking Through the Streets of Montmartre",
                "author": authors[1],
                "days_ago": 5,
                "featured": False,
                "login_require": False,
                "categories": ["City Breaks", "Culture"],
                "tags": ["Paris", "Montmartre", "France", "Photography"],
                "content": """
                    <p>Montmartre offers a completely different side of Paris. Its narrow streets, old 
                    stairways, small cafés, and artistic history make it one of the most atmospheric 
                    neighborhoods in the city.</p>

                    <p>Start near Sacré-Cœur and slowly walk downhill. Instead of following a strict 
                    itinerary, explore the smaller streets and discover local bakeries and quiet squares.</p>

                    <p>Sunset is an especially beautiful time to visit. From the steps of Sacré-Cœur, 
                    the rooftops of Paris stretch toward the horizon and create one of the city's most 
                    memorable views.</p>
                """
            },
            {
                "title": "Beyond Paris: Exploring the French Countryside",
                "author": authors[2],
                "days_ago": 8,
                "featured": True,
                "login_require": False,
                "categories": ["Nature", "Culture"],
                "tags": ["France", "Countryside", "Provence", "Road Trip"],
                "content": """
                    <p>France has much more to offer beyond its capital. The countryside reveals a slower 
                    side of the country, with historic villages, local markets, vineyards, and long roads 
                    surrounded by beautiful landscapes.</p>

                    <p>Provence is a great choice for travelers looking for warm weather, charming villages, 
                    local food, and scenic drives. The best experiences often come from stopping somewhere 
                    that was never on the original itinerary.</p>

                    <p>If you have extra time after Paris, renting a car and exploring smaller towns can 
                    turn a classic city trip into a much richer French adventure.</p>
                """
            },
            {
                "title": "A Road Trip Through the South of France",
                "author": authors[0],
                "days_ago": 11,
                "featured": False,
                "login_require": False,
                "categories": ["Adventure", "Nature"],
                "tags": ["France", "Nice", "Cannes", "Antibes", "Road Trip"],
                "content": """
                    <p>The South of France is made for road trips. Starting in Nice, travelers can follow 
                    the coast toward Cannes and Antibes before continuing into the countryside.</p>

                    <p>Nice is perfect for a relaxed first few days, with its waterfront promenade, old town, 
                    and colorful streets. From there, short drives lead to coastal towns where the pace feels 
                    completely different.</p>

                    <p>The real reward comes when the road leaves the coast and enters the countryside. 
                    Small villages, scenic viewpoints, and local restaurants make the journey as enjoyable 
                    as the destinations.</p>
                """
            },
            {
                "title": "Three Days in London: What Not to Miss",
                "author": authors[1],
                "days_ago": 14,
                "featured": True,
                "login_require": False,
                "categories": ["City Breaks", "Culture", "Travel Tips"],
                "tags": ["London", "England", "United Kingdom", "City Break"],
                "content": """
                    <p>Three days is enough to experience the highlights of London while still leaving 
                    room to wander. Start with Westminster, Buckingham Palace, and the area around the 
                    River Thames.</p>

                    <p>On the second day, explore Tower Bridge and the historic streets around the City 
                    of London. Museums and galleries are another great option, especially if the weather 
                    turns typically British.</p>

                    <p>Finish the trip with a relaxed walk through Notting Hill, Covent Garden, or one of 
                    London's many parks. The best London memories often come from the moments between the 
                    major attractions.</p>
                """
            },
            {
                "title": "A Quiet Escape to the English Countryside",
                "author": authors[2],
                "days_ago": 17,
                "featured": False,
                "login_require": False,
                "categories": ["Nature", "Culture"],
                "tags": ["England", "Cotswolds", "Countryside", "Nature"],
                "content": """
                    <p>For a completely different experience from London, head into the English countryside. 
                    The Cotswolds are famous for their stone villages, green hills, quiet roads, and traditional 
                    country houses.</p>

                    <p>A countryside trip is less about checking attractions off a list and more about slowing 
                    down. Walk between villages, stop for tea, and spend an afternoon exploring local shops 
                    and small cafés.</p>

                    <p>It is an ideal choice for travelers who want a peaceful few days surrounded by nature 
                    while still staying close enough to England's major cities.</p>
                """
            },
        ]

        created = 0

        for item in posts:
            post, was_created = Post.objects.get_or_create(
                title=item["title"],
                defaults={
                    "content": item["content"].strip(),
                    "image": "blog/default.jpg",
                    "author": item["author"],
                    "status": True,
                    "is_featured": item["featured"],
                    "login_require": item["login_require"],
                    "publish_date": now - timedelta(days=item["days_ago"]),
                }
            )

            if not was_created:
                continue

            post.category.set(
                [categories[name] for name in item["categories"]]
            )
            post.tags.set(item["tags"])
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{created} Paris/France/England demo posts added successfully."
            )
        )
